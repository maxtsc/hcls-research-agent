# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Search agent for retrieving and summarizing articles from pubmed."""

from google.adk import Agent
from Bio import Entrez, Medline
from io import StringIO
import time

from . import prompt

def search_pubmed(
    search_string: str,
    email: str,
    limit: int,
) -> list:
    """
    Fetches articles with abstracts for a search_string from pubmed.

    Args:
        search_string: The string for the search (e.g., "Treatment for KRAS G13D Breast Cancer")
        email: The email to be given to the Entrez API (e.g., "admin@website.com")
        limit: The maximum number of articles to fetch

    Returns:
        On success: A list of dictionaries with the PMID id as key and a dictionary of
        the Medline content as value.
        On error: A list containing the error of the search, either "Error connecting to Pubmed" 
        or "Could not find any articles"
    """
    print(
        f"--- Tool called: Fetching {limit} articles for {search_string} via Pubmed API ---"
    )
    # Always provide an email to identify yourself to the API.
    # This is a requirement from NCBI.
    Entrez.email = email

    # Use Entrez.esearch to perform the search
    try:
        handle = Entrez.esearch(db="pubmed", term=search_string, retmax=limit)
        id_list = Entrez.read(handle)["IdList"]
        handle.close()
    except ConnectionError as e:
        return [f"Error connecting to Pubmed: {e}"]
    
    
    records = []

    # If id_list is empty
    if not id_list:
        return ["Could not find any articles"]


    # Use Entrez.efetch to retrieve the full details of the articles
    # Convert from 
    for id in id_list:
        try:
            handle = Entrez.efetch(db="pubmed", id=id, rettype="medline", retmode="text")
            data = handle.read()
            handle.close()
            record = list(Medline.parse(StringIO(data)))
            records.append(
                {
                    "pmid":id,
                    "article":record,
                }
            )
        except ConnectionError as e:
            return [f"Error connecting to Pubmed: {e}"]
    

        time.sleep(1)

    return records

search_agent = Agent(
    model='gemini-2.5-flash',
    name='search_agent',
    instruction=prompt.SEARCH_PROMPT,
    tools=[search_pubmed],
    output_key="pubmed_results"
)
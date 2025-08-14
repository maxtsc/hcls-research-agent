# HCLS Research Agent

Today, HCLS researchers need to process many documents from databases like pubmed to identify potential research hypotheses around their research question. This agent intends to automate this process.

This project implements a multi-agent system for conducting Health and Life Sciences (HCLS) research using the Google Agent Development Kit (ADK).

## Example Usage
This section illustrates how a domain expert can use the HCLS Research Agent to accelerate their research workflow.

### User Persona: The Clinical Researcher 👩🏽‍⚕️
Our target user is a professional with deep domain expertise in health and life sciences, such as a clinical researcher, a medical science liaison, or a pharmacologist in an R&D department.

Let's consider Dr. Anya Sharma, a clinical researcher specializing in oncology. Dr. Sharma is tasked with identifying potential new therapeutic areas for an existing antibody-drug conjugate. Her goal is to move beyond the drug's approved indications and find novel, "tumor-agnostic" applications based on molecular markers.

Traditionally, this would involve days or weeks of manually searching PubMed, sifting through hundreds of papers, and synthesizing the findings. Dr. Sharma uses the HCLS Research Agent to automate this initial discovery phase.

### Sample Interaction
Here is a sample interaction showing how Dr. Sharma uses the agent to explore new indications for the drug "trastuzumab deruxtecan".
|Actor|Message|
|---|---|
|👩🏽‍⚕️ `user`| Are there underexplored disease entities from trastuzumab deruxtectan where it's currently not an approved therapy?|
|🤖 `research_question_agent`| This is an excellent research question! Would you like to conduct a PubMed search now?|
|👩🏽‍⚕️ `user`| Yes |
|🤖 `search_agent`| Okay, I can help you with that. Here is a proposed search string for PubMed: `("trastuzumab deruxtecan" OR "T-DXd") AND ("new indications" OR "potential indications" OR "other cancers" OR "unmet need")` This string aims to find articles discussing trastuzumab deruxtecan in contexts outside its currently approved indications (breast, gastric, and lung cancer), focusing on underexplored or novel disease entities. Are you agreeable to this search string, or would you like to refine it further?|
|👩🏽‍⚕️ `user`| I'm fine with this|
|🤖 `search_agent`| Great. Before I proceed with the search, I need your email address. This is required to access the Entrez API for logging purposes.|
|👩🏽‍⚕️ `user`| test@gmail.com|
|🤖 `search_agent`| I have successfully completed my search.<br> Search Summary for `("trastuzumab deruxtecan" OR "T-DXd") AND ("new indications" OR "potential indications" OR "other cancers" OR "unmet need")`<br>Number of articles reviewed: 6<br>Based on a review of the abstracts from the top 6 articles found on PubMed, here is a summary of the key findings regarding underexplored disease entities for trastuzumab deruxtecan (T-DXd) where it is not currently an approved therapy:<br>* Potential in Salivary Duct Carcinoma (SDC): A case report suggests that trastuzumab deruxtecan may offer interesting disease control in patients with HER2-positive salivary duct carcinoma... [PMID 40470107]<br>* Efficacy in Desmoplastic Small Round Cell Tumors (DSRCTs): Two studies indicate that T-DXd shows significant activity in desmoplastic small round cell tumors (DSRCTs)... [PMID 39921935, PMID 39120576]<br>* General Context for New Indications: ...the emergence of case reports and preclinical data in other rare cancers suggests a broader potential beyond current approvals... [PMID 39689708]<br>* Overall Conclusion: The literature review indicates that while trastuzumab deruxtecan is well-established in certain HER2-expressing cancers, there is emerging evidence supporting its potential in underexplored, aggressive rare cancers such as Salivary Duct Carcinoma and Desmoplastic Small Round Cell Tumors...<br>Would you like to generate hypotheses based on these results now?|
|👩🏽‍⚕️ `user`| Yes|
|🤖 `hypothesis_agent`| Based on the provided research summary, the following new hypotheses are proposed to address the research question:<br>* Hypothesis 1: Trastuzumab deruxtecan (T-DXd) will demonstrate a clinically meaningful objective response rate and durable disease control in a prospective clinical trial for patients with HER2-positive salivary duct carcinoma. (PMID: 40470107)<br>* Hypothesis 2: Trastuzumab deruxtecan (T-DXd) will exhibit significant anti-tumor activity, leading to improved progression-free survival, in patients with HER2-expressing desmoplastic small round cell tumors who have progressed on standard chemotherapy. (PMID: 39921935, PMID: 39120576)<br>* Hypothesis 3: Broad molecular profiling for HER2 expression across diverse rare and aggressive tumor types with unmet medical needs will identify additional novel indications where trastuzumab deruxtecan (T-DXd) can provide therapeutic benefit, even at lower HER2 expression levels. (PMID: 39689708, PMID: 40470107, PMID: 39921935, PMID: 39120576)|

### Workflow Breakdown
This interaction demonstrates the agent's core capabilities:
* Understand Intent: The agent correctly interprets the user's complex initial query. Although the `research_question_agent` is available, it recognizes that the user has already provided a well-formed question.
* Collaborative Search: The `search_agent` proposes a transparent, editable search query, allowing the expert user to approve or refine it. It intelligently adapts when the initial search yields no results.
* Automated Synthesis: The agent retrieves and synthesizes information from multiple papers, presenting a concise summary with citations.
* Hypothesis Generation: Finally, the `hypothesis_agent` uses the synthesized research to propose concrete, testable hypotheses, directly addressing the user's initial goal and providing a clear starting point for further investigation.

## Agent Architecture

The system consists of a root agent that delegates tasks to the following specialized sub-agents:

*   **research_question_agent**: Responsible for taking a topic and formulating a clear, answerable research question.
*   **search_agent**: Performs searches to find relevant information and academic papers related to the research question. It utilizes the NCBI Entrez API to query the PubMed database.
*   **hypothesis_agent**: Generates a hypothesis based on the gathered research.

## Setup and Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Install Poetry:**
    ```bash
    pip install poetry
    ```

2.  **Install Project Dependencies:**
    ```bash
    poetry install
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file by copying the template:
    ```bash
    cp .env.copy .env
    ```
    Then, fill in the required values in the new `.env` file.

4.  **Authenticate with Google Cloud:**
    Run the following command to authenticate your local environment.
    ```bash
    poetry run gcloud auth application-default login
    ```

## Running the Agent

You can interact with the agent using the ADK web UI or the command-line runner.

### Web UI

To start the interactive web interface, run:

```bash
poetry run adk web
```

Then, open your browser to `http://localhost:8000`.

### Command-Line Runner

To interact with the agent directly from your terminal, run:

```bash
poetry run adk run hcls_research_agent
```

## Testing the Agent

To run the test suite, use the following command:

```bash
poetry run pytest tests
```

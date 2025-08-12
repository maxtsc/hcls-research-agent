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

"""HCLS Research Agent for supporting researchers with pubmed access."""

from google.adk.agents import LlmAgent

from .sub_agents.research_question_agent import research_question_agent
from .sub_agents.hypothesis_agent import hypothesis_agent
from .sub_agents.search_agent import search_agent


hcls_researcher = LlmAgent(
    name='hcls_research_agent',
    model='gemini-2.5-flash',
    description=(
        'Creates research hypotheses for research questions'
        ' based on pubmed search results.'
    ),
    instruction=('Route user requests: You first route to the research_question_agent to define the research question.'
    'Once a research question is defined, you route to the search_agent to conduct a pubmed search.'
    'Once pubmed_results are available, you route to the hypothesis_agent to generate hypotheses.'),
    sub_agents=[research_question_agent, search_agent, hypothesis_agent],
)

root_agent = hcls_researcher

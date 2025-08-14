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

"""Unit tests for the hypothesis agent."""

from unittest.mock import patch

from google.adk.models import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from agents.hcls_research_agent.sub_agents.hypothesis_agent.agent import (
    hypothesis_agent,
)
import pytest


@pytest.mark.asyncio
async def test_successful_hypothesis_generation():
    """Tests that the agent can successfully generate a hypothesis."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=hypothesis_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    research_question = "What is the role of the gut microbiome in the development of Alzheimer's disease?"
    pubmed_results = """
Finding A: Studies show a correlation between a decrease in beneficial bacteria, such as Bifidobacterium, and the presence of amyloid-beta plaques in the brains of mice. (PMID: 12345678)
Finding B: Short-chain fatty acids (SCFAs) produced by gut bacteria are known to cross the blood-brain barrier and have anti-inflammatory effects. However, a specific link between SCFA levels and Alzheimer's progression in humans has not been definitively established. (PMID: 87654321)
Finding C: Probiotic supplementation with Lactobacillus species has been shown to reduce cognitive decline in some human subjects with mild cognitive impairment, but the mechanism is not fully understood. (PMID: 11223344)
"""
    expected_response = "Based on the provided research summary, the following new hypotheses are proposed to address the research question"
    mock_output = {
        "research_question": "Are there underexplored disease entities from trastuzumab deruxtectan where it's currently not an approved therapy?",
        "pubmed_results": "The literature review indicates that while trastuzumab deruxtecan is well-established in certain HER2-expressing cancers, there is emerging evidence supporting its potential in underexplored, aggressive rare cancers such as Salivary Duct Carcinoma and Desmoplastic Small Round Cell Tumors."
    }
    # Mock the LLM response
    async def mock_generate_content_async(*args, **kwargs):
        yield LlmResponse(content=Content(parts=[Part(text=expected_response)]))

    with patch(
        "google.adk.models.Gemini.generate_content_async",
        new=mock_generate_content_async,
    ):
        # Run the agent
        final_response = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=Content(
                parts=[
                    Part(
                        text=f"Research Question: {research_question}\nPubmed Results: {pubmed_results}"
                    )
                ]
            ),
            state_delta=mock_output
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break

        # Assert the response
        assert expected_response in final_response

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

"""Unit tests for the search agent."""

from unittest.mock import patch

from google.adk.models import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from hcls_research_agent.sub_agents.search_agent.agent import \
    search_agent

import pytest


@pytest.mark.asyncio
async def test_successful_search():
    """Tests that the agent can successfully search and summarize articles."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=search_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = "Treatment for KRAS G13D Breast Cancer"
    email = "test@example.com"
    limit = 5
    expected_response = "I have successfully completed my search."
    mock_output = {
        "research_question": "Precision therapy for HER2-low breast cancer"
    }

    # Mock the search_pubmed tool
    async def mock_search_pubmed(*args, **kwargs):
        return [
            {
                "pmid": "12345",
                "article": [{"TI": "Article 1 Title", "AB": "Article 1 Abstract"}],
            }
        ]

    with patch(
        "hcls_research_agent.sub_agents.search_agent.agent.search_pubmed",
        new=mock_search_pubmed,
    ):
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
                new_message=Content(parts=[Part(text=f'{question}\n{email}\n{limit}')]),
                state_delta=mock_output,
            ):
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    break

            # Assert the response
            assert expected_response in final_response


@pytest.mark.asyncio
async def test_no_articles_found():
    """Tests that the agent handles the case where no articles are found."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=search_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = "asdfasdfasdf"
    email = "test@example.com"
    limit = 5
    expected_response = "Could not find any articles"
    mock_output = {
        "research_question": "Precision therapy for HER2-low breast cancer"
    }
    # Mock the search_pubmed tool
    async def mock_search_pubmed(*args, **kwargs):
        return ["Could not find any articles"]

    with patch(
        "hcls_research_agent.sub_agents.search_agent.agent.search_pubmed",
        new=mock_search_pubmed,
    ):
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
                new_message=Content(parts=[Part(text=f'{question}\n{email}\n{limit}')]),
                state_delta=mock_output,
            ):
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    break

            # Assert the response
            assert expected_response in final_response


@pytest.mark.asyncio
async def test_connection_error():
    """Tests that the agent handles a connection error."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=search_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = "Treatment for KRAS G13D Breast Cancer"
    email = "test@example.com"
    limit = 5
    expected_response = "Error connecting to Pubmed"
    mock_output = {
        "research_question": "Precision therapy for HER2-low breast cancer"
    }
    # Mock the search_pubmed tool
    async def mock_search_pubmed(*args, **kwargs):
        return ["Error connecting to Pubmed"]

    with patch(
        "hcls_research_agent.sub_agents.search_agent.agent.search_pubmed",
        new=mock_search_pubmed,
    ):
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
                new_message=Content(parts=[Part(text=f'{question}\n{email}\n{limit}')]),
                state_delta=mock_output,
            ):
                if event.is_final_response():
                    final_response = event.content.parts[0].text
                    break

            # Assert the response
            assert expected_response in final_response

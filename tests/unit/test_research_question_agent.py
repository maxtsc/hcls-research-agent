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

"""Unit tests for the research question agent."""

from unittest.mock import patch

import pytest
from google.adk.models import LlmResponse
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part

from agents.hcls_research_agent.sub_agents.research_question_agent.agent import (
    research_question_agent,
)


@pytest.mark.asyncio
async def test_good_research_question():
    """Tests that the agent commends a good research question."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=research_question_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = (
        "How does prolonged exposure to air pollution in urban areas impact"
        " the respiratory health of adults aged 50 and above over a"
        " five-year period?"
    )
    expected_response = "This is an excellent research question!"

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
            new_message=Content(parts=[Part(text=question)]),
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break

        # Assert the response
        assert expected_response in final_response


@pytest.mark.asyncio
async def test_vague_research_question():
    """Tests that the agent refines a vague research question."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=research_question_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = "How does the environment affect people?"
    expected_refined_question = (
        "How does prolonged exposure to air pollution in urban areas impact"
        " the respiratory health of adults aged 50 and above over a"
        " five-year period?"
    )

    # Mock the LLM response
    async def mock_generate_content_async(*args, **kwargs):
        yield LlmResponse(content=Content(parts=[Part(text=expected_refined_question)]))

    with patch(
        "google.adk.models.Gemini.generate_content_async",
        new=mock_generate_content_async,
    ):
        # Run the agent
        final_response = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=Content(parts=[Part(text=question)]),
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break

        # Assert the response
        assert expected_refined_question in final_response


@pytest.mark.asyncio
async def test_simple_research_question():
    """Tests that the agent refines a simple research question."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=research_question_agent,
        app_name="test_app",
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name="test_app", user_id="test_user"
    )
    question = "Does smoking cause cancer?"
    expected_refined_question = (
        "What is the causal relationship between smoking and the development"
        " of lung cancer, and what are the underlying biological mechanisms?"
    )

    # Mock the LLM response
    async def mock_generate_content_async(*args, **kwargs):
        yield LlmResponse(content=Content(parts=[Part(text=expected_refined_question)]))

    with patch(
        "google.adk.models.Gemini.generate_content_async",
        new=mock_generate_content_async,
    ):
        # Run the agent
        final_response = ""
        async for event in runner.run_async(
            session_id=session.id,
            user_id=session.user_id,
            new_message=Content(parts=[Part(text=question)]),
        ):
            if event.is_final_response():
                final_response = event.content.parts[0].text
                break

        # Assert the response
        assert expected_refined_question in final_response

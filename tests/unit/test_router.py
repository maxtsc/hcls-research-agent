"""Unit tests for routing agent."""

import pytest
import dotenv

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from hcls_research_agent.agent import root_agent

pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()

@pytest.mark.asyncio
async def test_route_research_question():
    """Test that the router to the research question works."""
    user_input = ("Precision therapy for HER2-low breast cancer").strip()

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
    ):
        if event.content.parts and event.content.parts[0].function_call:
            routed_agent = event.content.parts[0].function_call.args['agent_name']

    # The input should route to the research_question_agent.
    assert "research_question_agent" in routed_agent.lower(), "Expected routing to research_question_agent."

@pytest.mark.asyncio
async def test_route_search_agent():
    """Test that the router to the pubmed search works."""
    user_input = ("""Search pubmed for "BRCA HER2-low""").strip()

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    mock_output = {
        "research_question": "Precision therapy for HER2-low breast cancer"
    }
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
        state_delta=mock_output,
    ):
        if event.content.parts and event.content.parts[0].function_call:
            routed_agent = event.content.parts[0].function_call.args['agent_name']

    # The input should route to the search_agent.
    assert "search_agent" in routed_agent.lower(), "Expected routing to search_agent."


@pytest.mark.asyncio
async def test_route_hypothesis_agent():
    """Test that the router to the hypothesis agent works."""
    user_input = ("""Create a research hypothesis""").strip()

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    content = UserContent(parts=[Part(text=user_input)])
    mock_output = {
        "research_question": "Precision therapy for HER2-low breast cancer",
        "pubmed_results": "There have been no studies in breast cancer carriers under 50 years of age."
    }
    async for event in runner.run_async(
        user_id=session.user_id,
        session_id=session.id,
        new_message=content,
        state_delta=mock_output,
    ):
        if event.content.parts and event.content.parts[0].function_call:
            routed_agent = event.content.parts[0].function_call.args['agent_name']

    # The input should route to the search_agent.
    assert "hypothesis_agent" in routed_agent.lower(), "Expected routing to hypothesis_agent."
"""Unit tests for search agent."""

import pytest
import dotenv

from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from hcls_research_agent.sub_agents.search_agent import search_agent


pytest_plugins = ("pytest_asyncio",)

@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()

@pytest.mark.asyncio
async def test_search_string_generation():
    """Test the search functionality."""
    user_input = ("Conduct pubmed search for research question: Therapy for breast cancer").strip()

    runner = InMemoryRunner(agent=search_agent)
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
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # The input should route to the research_question_agent.
    assert "string" in response.lower(), "Expected revised search string."


@pytest.mark.asyncio
async def test_ask_for_email():
    """Test the search functionality."""
    user_input = ("""Conduct pubmed search for search string: 
                  Precision therapy for HER2-low breast cancer.
                  I confirm this search string.""").strip()

    runner = InMemoryRunner(agent=search_agent)
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
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # The input should route to the research_question_agent.
    assert "email" in response.lower(), "Expected agent to ask for email."


@pytest.mark.asyncio
async def test_pubmed_search():
    """Test the search functionality."""
    user_input = ("""Conduct pubmed search for search string: 
                  Precision therapy for HER2-low breast cancer.
                  I confirm this search string.
                  My email is test@gmail.com""").strip()

    runner = InMemoryRunner(agent=search_agent)
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
        if event.content.parts and event.content.parts[0].text:
            response = event.content.parts[0].text

    # The input should route to the research_question_agent.
    assert "trastuzumab" in response.lower(), "Expected pubmed results to contain trastuzumab."
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

"""Unit tests for routing agent."""

import logging

import dotenv
import pytest
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

from agents.hcls_research_agent.agent import root_agent

pytest_plugins = ("pytest_asyncio",)
logger = logging.Logger("test_loggger")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_route_research_question():
    """Test that the router to the research question works."""
    user_input = [
        "My research question is: How much water should I drink per day?",
        "Please refine it further",
    ]

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    for message in user_input:
        content = UserContent(parts=[Part(text=message)])
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if event.content.parts and event.content.parts[0].function_call:
                routed_agent = event.content.parts[0].function_call.args

    # The input should route to the research_question_agent.
    assert "research_question_agent" in str(routed_agent).lower(), (
        "Expected routing to research_question_agent, got {routed_agent}"
    )


@pytest.mark.asyncio
async def test_route_search_agent():
    """Test that the router to the pubmed search works."""
    user_input = [
        "What is the mechanistic basis for exploring novel disease indications for trastuzumab deruxtecan beyond its currently approved uses, focusing on areas with limited clinical investigation?",
        "Yes, please start pubmed search",
        "Yes, please start pubmed search",
    ]

    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    mock_output = {"research_question": "Precision therapy for HER2-low breast cancer"}

    for message in user_input:
        content = UserContent(parts=[Part(text=message)])
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
            state_delta=mock_output,
        ):
            if event.content.parts and event.content.parts[0].function_call:
                routed_agent = event.content.parts[0].function_call.args

    # The input should route to the search_agent.
    assert "search_agent" in str(routed_agent).lower(), (
        f"Expected routing to search_agent, got {routed_agent}"
    )


@pytest.mark.asyncio
async def test_route_hypothesis_agent():
    """Test that the router to the hypothesis agent works."""
    start = "My very good research question is: What is the impact of T-DXd on progression-free survival on HER2-low breast cancer?"
    research_question_input = "Yes, please use this research question."
    pubmed_search_input = """Please start pubmed search with ("trastuzumab deruxtecan" OR "T-DXd") AND ("new indications" OR "potential indications" OR "other cancers" OR "unmet need") my email address is test@gmail.com """
    iterations = 5
    runner = InMemoryRunner(agent=root_agent)
    session = await runner.session_service.create_session(
        app_name=runner.app_name, user_id="test_user"
    )
    mock_output = {
        "research_question": "Are there underexplored disease entities from trastuzumab deruxtectan where it's currently not an approved therapy?",
        "pubmed_results": "The literature review indicates that while trastuzumab deruxtecan is well-established in certain HER2-expressing cancers, there is emerging evidence supporting its potential in underexplored, aggressive rare cancers such as Salivary Duct Carcinoma and Desmoplastic Small Round Cell Tumors.",
    }
    content = UserContent(parts=[Part(text=start)])
    prev_agent = "start"

    while iterations > 0:
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
            state_delta=mock_output,
        ):
            logger.warning(event.content.parts[0])
            if event.content.parts and event.content.parts[0].function_call:
                if "research_question_agent" in str(
                    event.content.parts[0].function_call.args
                ):
                    if prev_agent in ("start"):
                        content = UserContent(
                            parts=[Part(text=research_question_input)]
                        )
                        prev_agent = "research_question_agent"

                elif "search_agent" in str(event.content.parts[0].function_call.args):
                    if prev_agent in ("research_question_agent", "start"):
                        prev_agent = "search_agent"
                        content = UserContent(parts=[Part(text=pubmed_search_input)])

                elif "hypothesis_agent" in str(
                    event.content.parts[0].function_call.args
                ):
                    routed_agent = event.content.parts[0].function_call.args
                    break

                else:
                    content = UserContent(parts=[Part(text="Yes.")])
        iterations -= 1
        if iterations == 0:
            routed_agent = event.content.parts[0].function_call.args

    # The input should route to the search_agent.
    assert "hypothesis_agent" in str(routed_agent).lower(), (
        f"Expected routing to hypothesis_agent, got {routed_agent}."
    )

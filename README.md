# HCLS Research Agent

Today, HCLS researchers need to process many documents from databases like pubmed to identify potential research hypotheses around their research question. This agent intends to automate this process.

This project implements a multi-agent system for conducting Health and Life Sciences (HCLS) research using the Google Agent Development Kit (ADK).

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

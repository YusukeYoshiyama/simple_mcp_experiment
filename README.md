# mcp_simple_experiment

## Overview

This is a simple experiment project using Python. It's managed by `uv` for package and environment management.

## Environment Variables

An `OPENAI_API_KEY` is required for this project to run. Other variables for external services are optional.

These variables can be configured in two ways:
1.  **`.env` file:** Create a `.env` file by copying the example (`cp .env.example .env`) and add your credentials.
2.  **From the UI:** The application will prompt you for any required API keys if they are not already set.

### Required
- `OPENAI_API_KEY`: Your API key for OpenAI.

### Optional
- `BRAVE_API_KEY`: Your API key for Brave Search.
- `GITHUB_PERSONAL_ACCESS_TOKEN`: Your personal access token for GitHub.
- `GOOGLE_MAPS_API_KEY`: Your API key for Google Maps.
- `MAX_ENVS`: Maximum number of environments (defaults to 10).

## Quick Start

Follow these steps to get the project up and running.

### Prerequisites

- [uv](https://github.com/astral-sh/uv)
- git
- Python 3.12+

### Installation & Execution

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YusukeYoshiyama/simple_mcp_experiment
    cd mcp_simple_experiment
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    uv sync
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Run the application:**
    ```bash
    uv run python main.py
    ```

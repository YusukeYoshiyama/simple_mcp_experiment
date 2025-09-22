# MCP Practice Own

This is a web-based tool for experimenting with and testing LangChain ReAct agents that use the Model Context Protocol (MCP). It allows you to dynamically load tools from different MCP servers (like GitHub, Google Maps, and Playwright) and interact with the agent through a Gradio-based web interface.

## Features

- **Web UI for Agent Interaction**: An easy-to-use interface built with Gradio to send prompts to your agent.
- **Dynamic Tool Loading**: Dynamically select and load tools from different MCP servers.
- **Pre-configured MCPs**: Comes pre-configured for GitHub, Google Maps, and Playwright MCPs.
- **Flexible Configuration**: Allows setting system prompts, user prompts, and required environment variables directly from the UI.
- **Detailed Logging**: Displays the agent's final response, detailed execution logs, and token usage information for cost tracking.

## Requirements

- Python >= 3.12
- [uv](https://github.com/astral-sh/uv) (for Python package management)
- Node.js and `npx` (for running MCP servers)

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YusukeYoshiyama/mcp_simple_experiment
    cd mcp-practice-own
    ```

2.  **Install Python dependencies:**
    Make sure you have `uv` installed.
    ```bash
    uv pip install .
    ```

3.  **Set up Environment Variables:**
    Create a `.env` file by copying the example file.
    ```bash
    cp .env.example .env
    ```
    Then, open the `.env` file and fill in the necessary API keys and tokens:
    - `OPENAI_API_KEY`: Your API key for OpenAI.
    - `GITHUB_PERSONAL_ACCESS_TOKEN`: Your GitHub Personal Access Token for using the GitHub MCP.
    - `GOOGLE_MAPS_API_KEY`: Your Google Maps API key for using the Google Maps MCP.

## Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Open the web interface:**
    The application will start a local web server. Open the URL displayed in your terminal (e.g., `http://127.0.0.1:7860`) in your browser.

3.  **Use the application:**
    - **MCP設定 (MCP Settings) Tab**:
        - **MCPを選択 (Select MCP)**: Choose the MCP server you want the agent to use (e.g., `GitHub MCP`). The necessary `npx` command argument will be filled in automatically.
        - **Environment Variables**: If the selected MCP requires specific environment variables (like API keys), they will appear. You can add or modify them as needed.
    - **メッセージ送信 (Send Message) Tab**:
        - **System Prompt**: Modify the system prompt for the agent if needed.
        - **User Prompt**: Enter the task or question you want the agent to perform.
        - **Send Prompt**: Click the button to run the agent.
    - **Results**: The agent's final answer, token usage, and detailed execution logs will be displayed in the respective text areas.

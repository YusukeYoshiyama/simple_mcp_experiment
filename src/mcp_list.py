import os

mcp_list = {
    "Other MCP": {
        "command": "",
        "args": "",
        "env": []
    },
    "Filesystem MCP": {
        "command": "npx",
        "args": "@modelcontextprotocol/server-filesystem [full_path_of_your_permissions_folder]",
        "env": []
    },
    "GitHub MCP": {
        "command": "npx",
        "args": "@modelcontextprotocol/server-github",
        "env": [{"GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN","")}]
    },
    "GoogleMap MCP": {
        "command": "npx",
        "args": "@modelcontextprotocol/server-google-maps",
        "env": [{"GOOGLE_MAPS_API_KEY": os.getenv("GOOGLE_MAPS_API_KEY","")}]
    },
    "Playwright MCP": {
        "command": "npx",
        "args": "@playwright/mcp@latest",
        "env": []
    }
}
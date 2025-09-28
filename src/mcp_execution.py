import os
import asyncio
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain.schema import AIMessage

async def run_agent(system_prompt, user_prompt, command, args, *envs):
    env_vars = {envs[i]: envs[i+1] for i in range(0, len(envs), 2) if envs[i]}
    mcp_settings = {
        "mcp": {
            "command": command,
            "args": args.split(" "),
            "env": env_vars,
            "transport": "stdio",
        }
    }
    client = MultiServerMCPClient(mcp_settings)
    async with client.session("mcp") as session:
        model = ChatOpenAI(model="gpt-5-mini")
        tools = await load_mcp_tools(session)
        agent = create_react_agent(model, tools, prompt=system_prompt)
        response = await agent.ainvoke(
            {"messages": [{"role": "user", "content": user_prompt}]}
        )
    tokens_str, logs_str = format_logs(response)
    return response, tokens_str, logs_str, tools

def format_logs(result):
    token_info = {
        "input_token": 0,
        "output_token": 0,
        "total_token": 0
    }
    logs_str = ""
    for message in result["messages"]:
        logs_str += f"<{message.__class__.__name__}>" + "\n"
        if isinstance(message, AIMessage):
            token_info["input_token"] += message.usage_metadata["input_tokens"]
            token_info["output_token"] += message.usage_metadata["output_tokens"]
            token_info["total_token"] += message.usage_metadata["total_tokens"]
            if "tool_calls" in message.additional_kwargs:
                logs_str += "---Tool Calls---" + "\n"
                logs_str += str(message.additional_kwargs["tool_calls"][0]["function"]) + "\n"
            else:
                logs_str += message.content + "\n"
        else:    
            logs_str += message.content + "\n"
        logs_str += "###################################################################" + "\n\n"
    tokens_str = ""
    tokens_str += f"input token: {token_info["input_token"]}\n"
    tokens_str += f"output token: {token_info["output_token"]}\n"
    tokens_str += f"total token: {token_info["total_token"]}\n\n"

    tokens_str += f"input price: {0.25*token_info["input_token"]/1000000}$\n"
    tokens_str += f"output price: {2*token_info["output_token"]/1000000}$"
    return tokens_str, logs_str
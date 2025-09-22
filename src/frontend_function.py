import gradio as gr
import os

from src.mcp_list import mcp_list

max_envs = int(os.getenv("MAX_ENVS","10"))

def update_ui_from_selection(selection):
    if not selection:
        args_update = gr.Textbox(value="")
        env_updates = [item for _ in range(max_envs) for item in [gr.Textbox(value="", visible=False), gr.Textbox(value="", visible=False)]]
        return [args_update] + env_updates

    selected_data = mcp_list[selection]
    command_value = selected_data["command"]
    args_value = selected_data["args"]
    env_list = selected_data["env"]

    updates = [gr.Textbox(value=command_value),gr.Textbox(value=args_value)]

    for i in range(max_envs):
        if i < len(env_list):
            env_item = env_list[i]
            key = list(env_item.keys())[0]
            value = env_item[key]
            updates.extend([
                gr.Textbox(value=key, visible=True),
                gr.Textbox(value=value, visible=True)
            ])
        else:
            updates.extend([
                gr.Textbox(value="", visible=False),
                gr.Textbox(value="", visible=False)
            ])
            
    return updates

def add_env_row(*all_kvs):
    updates = []
    first_empty_index = -1
    for i in range(0, len(all_kvs), 2):
        key = all_kvs[i]
        value = all_kvs[i+1]
        if not key and not value:
            first_empty_index = i // 2
            break
            
    if first_empty_index == -1:
        first_empty_index = max_envs

    for i in range(max_envs):
        if i <= first_empty_index:
            updates.extend([gr.Textbox(visible=True), gr.Textbox(visible=True)])
        else:
            updates.extend([gr.Textbox(visible=False), gr.Textbox(visible=False)])
            
    return updates
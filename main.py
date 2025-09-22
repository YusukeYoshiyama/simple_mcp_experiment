from dotenv import load_dotenv
load_dotenv(verbose=True)

import gradio as gr
import json
import os

from src.mcp_execution import run_agent
from src.frontend_function import update_ui_from_selection, add_env_row
from src.mcp_list import mcp_list
from src.system_prompt_template import system_prompt

def main():
    max_envs = int(os.getenv("MAX_ENVS","10"))
    with gr.Blocks(theme=gr.themes.Soft(font=gr.themes.GoogleFont("Inter"))) as app:
        with gr.Tab("MCP設定"):
            gr.Markdown("## MCP設定")
            with gr.Row():
                mcp_set = gr.Dropdown(
                    choices=list(mcp_list.keys()),
                    label="MCPを選択",
                    interactive=True
                )
        
            command_textbox = gr.Textbox(label="command", lines=1,max_lines=1)
            args_textbox = gr.Textbox(label="args", lines=1,max_lines=1)

            gr.Markdown("---")
            gr.Markdown("### Environment Variables")
        
            env_textboxes = []
            with gr.Column() as env_area:
                for i in range(max_envs):
                    with gr.Row():
                        key = gr.Textbox(label=f"Key {i+1}", scale=1, visible=False)
                        value = gr.Textbox(label=f"Value {i+1}", scale=2, visible=False)
                        env_textboxes.extend([key, value])
        
            add_button = gr.Button("Add another env", variant="secondary")
            
            mcp_set.change(
                fn=update_ui_from_selection,
                inputs=mcp_set,
                outputs=[command_textbox, args_textbox] + env_textboxes
            )
            
            add_button.click(
                fn=add_env_row,
                inputs=env_textboxes,
                outputs=env_textboxes
            )
        with gr.Tab("メッセージ送信"):
            gr.Markdown("## メッセージ送信")
            with gr.Column():
                with gr.Row():
                    system_prompt_textbox = gr.Textbox(value=system_prompt, label="System Prompt", scale=1, lines=4, max_lines=4)
                    user_prompt_textbox = gr.Textbox(label="User Prompt", scale=1, lines=4, max_lines=4)
            send_button = gr.Button("Send Prompt")
            with gr.Column():
                with gr.Row():
                    result_area = gr.TextArea(label="Result", scale=2, lines=6, max_lines=6)
                    token_area = gr.TextArea(label="Tokens", scale=1, lines=6, max_lines=6)
            logs_area = gr.TextArea(label="Logs", lines=10, max_lines=10)
            send_button.click(
                fn=run_agent, 
                inputs=[system_prompt_textbox,user_prompt_textbox,command_textbox,args_textbox] + env_textboxes,
                outputs=[result_area, token_area, logs_area]
            )
        
    app.launch()


if __name__ == "__main__":
    main()
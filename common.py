#!/usr/bin/env python3
"""
Common utilities for SnapTask - shared between OCR and Vision modes
"""

import subprocess
import os
import json
from datetime import datetime


# Default prompts
DEFAULT_OCR_PROMPT = """Below is text extracted from a user's screenshot. Your tasks:

1. Analyze the content and provide:
   - **Current Focus**: What is the user currently working on?
   - **Context/Application**: What application or context is this?
   - **Action Items**: What are potential next steps or tasks?
   - **Insights**: Any patterns, blockers, or noteworthy observations?

2. Update files using the tools provided:
   - **todo.md**: Add unique action items (check existing todos first to avoid duplicates). Format as markdown checklist: "- [ ] Task description"
   - **focused.md**: Update with current focus (include timestamp). Check if it's different from the last entry to avoid duplicates.

Be concise but insightful. Use the read_file tool first to check existing content, then use write_file to update.

---
EXTRACTED TEXT:
{text}
---"""

DEFAULT_VISION_PROMPT = """Analyze this screenshot. Your tasks:

1. Provide analysis:
   - **Current Focus**: What is the user currently working on?
   - **Context/Application**: What application or context is visible?
   - **Action Items**: What are potential next steps or tasks?
   - **Insights**: Any patterns or insights about the work being done?

2. Update files using the tools provided:
   - **todo.md**: Add unique action items (check existing todos first to avoid duplicates). Format as markdown checklist: "- [ ] Task description"
   - **focused.md**: Update with current focus (include timestamp). Check if it's different from the last entry to avoid duplicates.

Be concise but insightful. Use the read_file tool first to check existing content, then use write_file to update."""


def capture_screenshot(output_path):
    """Capture screenshot using macOS screencapture command"""
    try:
        # -i: interactive selection (drag to select area, spacebar for window)
        # -x: no sound, -t png: format
        subprocess.run(['screencapture', '-i', '-x', '-t', 'png', output_path], check=True)
        print(f"Screenshot saved to: {output_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error capturing screenshot: {e}")
        return False


def load_prompt(prompt_name, default_prompt):
    """Load prompt from config file or use default"""
    prompts_dir = os.path.expanduser('~/.snap/prompts')
    prompt_file = os.path.join(prompts_dir, prompt_name)

    if os.path.exists(prompt_file):
        with open(prompt_file, 'r') as f:
            return f.read().strip()
    return default_prompt


def get_tool_definitions():
    """Return OpenAI function calling tool definitions"""
    return [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read the contents of a file. Use this to check existing todos or focus entries before updating them.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The file path relative to ~/.snap/ (e.g., 'todo.md' or 'focused.md')"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Write or append content to a file. Use this to update todo.md with action items and focused.md with current focus. Be smart about deduplication.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "The file path relative to ~/.snap/ (e.g., 'todo.md' or 'focused.md')"
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file"
                        },
                        "mode": {
                            "type": "string",
                            "enum": ["append", "overwrite"],
                            "description": "Whether to append to existing content or overwrite the file"
                        }
                    },
                    "required": ["file_path", "content", "mode"]
                }
            }
        }
    ]


def execute_tool(tool_name, arguments, snap_dir):
    """
    Execute a tool function and return the result

    Args:
        tool_name: Name of the tool to execute
        arguments: Dict of arguments for the tool
        snap_dir: Base directory for file operations (usually ~/.snap)

    Returns:
        String result of the tool execution
    """
    try:
        if tool_name == "read_file":
            file_path = os.path.join(snap_dir, arguments['file_path'])
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return f.read()
            else:
                return f"File {arguments['file_path']} does not exist yet."

        elif tool_name == "write_file":
            file_path = os.path.join(snap_dir, arguments['file_path'])
            mode = arguments['mode']
            content = arguments['content']

            if mode == "append":
                with open(file_path, 'a') as f:
                    f.write(content)
            else:  # overwrite
                with open(file_path, 'w') as f:
                    f.write(content)

            print(f"   ✓ LLM updated {arguments['file_path']}")
            return f"Successfully wrote to {arguments['file_path']}"

        else:
            return f"Unknown tool: {tool_name}"

    except Exception as e:
        return f"Error: {str(e)}"


def run_agent_loop(client, model, messages, snap_dir, max_iterations=10):
    """
    Run the agent loop: let LLM use tools iteratively

    Args:
        client: OpenAI client instance
        model: Model name (e.g., 'gpt-4o-mini' or 'gpt-4o')
        messages: Initial message list
        snap_dir: Base directory for file operations
        max_iterations: Maximum number of iterations to prevent infinite loops

    Returns:
        String containing the analysis output
    """
    tools = get_tool_definitions()
    analysis_output = []

    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            max_tokens=1500,
            temperature=0.7
        )

        message = response.choices[0].message
        messages.append(message)

        # If no tool calls, we're done
        if not message.tool_calls:
            if message.content:
                analysis_output.append(message.content)
            break

        # Execute tool calls
        for tool_call in message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            result = execute_tool(function_name, arguments, snap_dir)

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return '\n'.join(analysis_output) if analysis_output else "Analysis completed."


def create_prompt_file(prompt_file, default_content):
    """Create a prompt file if it doesn't exist"""
    if not os.path.exists(prompt_file):
        os.makedirs(os.path.dirname(prompt_file), exist_ok=True)
        with open(prompt_file, 'w') as f:
            f.write(default_content)


def get_system_message():
    """Return the standard system message for the agent"""
    return "You are an AI assistant that analyzes screen content and maintains the user's todo.md and focused.md files. Use the provided tools to read existing files and update them intelligently."


def save_analysis(screenshot_path, analysis):
    """Save analysis to a text file"""
    analysis_path = screenshot_path.replace('.png', '_analysis.txt')
    with open(analysis_path, 'w') as f:
        f.write(analysis)
    return analysis_path


def generate_screenshot_path():
    """Generate timestamped screenshot path"""
    screenshots_dir = os.path.expanduser('~/.snap')
    os.makedirs(screenshots_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')

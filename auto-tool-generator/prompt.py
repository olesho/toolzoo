def get_tool_example() -> str:
    with open('temp/tool_example.py', 'r') as file:
        tool_example = file.read()
    return tool_example

def get_html_api_ref() -> str:
    with open('temp/api_ref.html', 'r') as file:
        api_ref = file.read()
    return api_ref

def get_generation_prompt(api_ref: str, tool_example: str) -> str:
    # read prompt.txt to variable
    # replace in this variable "[api_ref.html]" by api_ref param and "[tool_example.py]" by tool_example
    # return this variable
    with open('prompt.txt', 'r') as file:
        prompt = file.read()

    prompt = prompt.replace("[api_ref.html]", api_ref)
    prompt = prompt.replace("[tool_example.py]", tool_example)

    return prompt
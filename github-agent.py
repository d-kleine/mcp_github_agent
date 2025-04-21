import os

from dotenv import load_dotenv
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.utils import Secret
from haystack_integrations.tools.mcp import MCPTool, StdioServerInfo

load_dotenv()

github_mcp_server = StdioServerInfo(
    command="docker",
    args=[
        "run", "-i", "--rm",
        "-e", "GITHUB_PERSONAL_ACCESS_TOKEN",
        "ghcr.io/github/github-mcp-server"
    ],
    env={
        "GITHUB_PERSONAL_ACCESS_TOKEN": os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    }
)

print("MCP server is created")

tool_1 = MCPTool(
    name="get_file_contents",
    server_info=github_mcp_server
)

tool_2 = MCPTool(
    name="create_issue",
    server_info=github_mcp_server,
)

tools = [tool_1, tool_2]

print("MCP tools are created")

agent = Agent(
    chat_generator=OpenAIChatGenerator(
        model="gpt-4o", api_key=Secret.from_env_var("OPENAI_API_KEY")),
    system_prompt="""
    You are a GitHub typo detection specialist. Follow this workflow:
    1. Use the "get_file_content" tool to retrieve the raw text from the README content in the specified repository.
    2. Analyze the extracted text for common typos using patterns:
       - Common misspellings (recieve -> receive)
       - Homophone errors (their vs there)
       - Capitalization inconsistencies
    Verify technical terms before flagging as typos.
    4. For confirmed typos, create an issue in the same repository with the "create_issue" tool with:
       - The provided title
       - A description with location and suggestion how to fix the typo
    """,
    tools=tools
)

print("Agent created")

owner = "d-kleine"
repo = "spring-into-haystack"
path = "README.md"

user_input = f"Can you find the typos in the {path} file of {owner}/{repo}? If there is not yet an existing issue with the given title, create an issue about how to fix the typos."

response = agent.run(messages=[ChatMessage.from_user(text=user_input)],
                     owner=owner,
                     repo=repo,
                     path=path,
                     title="doc: MCP README typo",
                     )

# print(response)
print(response["messages"][-1].text)
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.dataclasses import ChatMessage
from haystack.components.agents import Agent
from haystack_integrations.tools.mcp import MCPTool, StdioServerInfo


github_mcp_server = StdioServerInfo(
        ## TODO: Add correct params for the Github MCP Server (official or legacy)
        env={
            "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR GITHUB TOKEN>" # DO NOT ADD IT TO YOUR COMMIT
        }
    )

print("MCP server is created")

## TODO: Create your tools here:
tool_1 = MCPTool(...

tools = [## TODO: Add tools tool_1, tool_2, tool_3,..]

print("MCP tools are created")

## TODO: Create your Agent here:
agent = Agent(
...
)

print("Agent created")

## Example query to test your agent
user_input = "Can you find the typo in the README of <owner/repo> and open an issue about how to fix it?"

## (OPTIONAL) Feel free to add other example queries that can be resolved with this Agent

response = agent.run(messages=[ChatMessage.from_user(text=user_input)])

## Print the agent thinking process
print(response)
## Print the final response
print(response["messages"][-1].text)
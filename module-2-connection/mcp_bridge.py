import asyncio
# We use the stdio_client to communicate with our local MCP servers.
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def run_mcp_bridge():
    # We define parameters to launch the prebuilt Notion server.
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-notion"],
        # We pass the token securely as an environment variable.
        env={"NOTION_SDK_TOKEN": "your_token_here"}
    )

    # We open the communication tunnel to the server.
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # We initialize the session to make sure the server is ready.
            await session.initialize()
            
            # We ask the server for a list of all available Notion actions.
            available_tools = await session.list_tools()
            
            print("The agent is now hooked into Notion with these capabilities:")
            for tool in available_tools.tools:
                print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(run_mcp_bridge())

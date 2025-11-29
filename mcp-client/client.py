import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:

    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.anthropic = Anthropic()

    async def connect_to_server(self, server_script_path: str):

        # Connecting with MCP Server
        server_params = StdioServerParameters(
            command="python",
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])


    async def process_query(self, query: str) -> str:
        messages = [
            {"role": "user", "content": query}
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "name": tool.name,
            "description": tool.description,
            "input_schema": tool.inputSchema
        } for tool in response.tools]

        ai_response = self.anthropic.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            messages=messages,
            tools=available_tools
        )

        final_output = []

        while True:
            tool_call_found = False

            for content in ai_response.content:

                if content.type == "text":
                    final_output.append(content.text)

                elif content.type == "tool_use":
                    tool_call_found = True
                    tool_name = content.name
                    tool_args = content.input

                    tool_result = await self.session.call_tool(tool_name, tool_args)

                    messages.append({
                        "role": "assistant",
                        "content": [content]
                    })

                    messages.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": content.id,
                            "content": tool_result.content
                        }]
                    })

                    ai_response = self.anthropic.messages.create(
                        model="claude-sonnet-4-20250514",
                        max_tokens=2000,
                        messages=messages,
                        tools=available_tools
                    )

                    break 

            if not tool_call_found:
                break

        return "\n".join(final_output)



    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())

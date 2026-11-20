import asyncio
import time
from fastmcp import Client
from app.mcp.server import mcp


async def main():

    print("1. Connecting to MCP server...")

    async with Client(mcp) as client:

        print("2. MCP connection successful!")

        # Discover tools
        tools = await client.list_tools()

        print("\n3. Available MCP Tools:")

        for tool in tools:
            print("-", tool.name)

        print("\n4. Calling employee leave balance tool...")

        start = time.perf_counter()

        result = await client.call_tool(
            "get_employee_leave_balance",
            {"employee_id": "E102"}
        )

        elapsed = time.perf_counter() - start

        print(f"\nMCP tool call completed in {elapsed:.2f} seconds")
        print(result.structured_content)

        print("\n5. Tool execution completed!")

        print("\n6. Raw tool result:")
        print(result)

        print("\n7. Result content:")

        for item in result.content:
            if hasattr(item, "text"):
                print(item.text)
            else:
                print(item)

        print("\n8. Structured content:")
        print(getattr(result, "structured_content", None))


if __name__ == "__main__":
    asyncio.run(main())
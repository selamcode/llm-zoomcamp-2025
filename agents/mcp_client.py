import asyncio
from fastmcp import Client
import weather_server  # Your weather_server.py file with the MCP instance

async def main():
    async with Client(weather_server.mcp) as mcp_client:
        # Get list of tools
        tools = await mcp_client.list_tools()
        print("Available tools:", tools)

        # Call 'get_weather_tool' with city='berlin'
        weather_berlin = await mcp_client.call_tool(
            name="get_weather_tool",
            arguments={"city": "berlin"}
        )
        print("Weather in Berlin:", weather_berlin)

        # Set weather for Paris to 25.5
        set_response = await mcp_client.call_tool(
            name="set_weather_tool",
            arguments={"city": "paris", "temp": 25.5}
        )
        print("Set weather response:", set_response)

        # Get weather for Paris after setting
        weather_paris = await mcp_client.call_tool(
            name="get_weather_tool",
            arguments={"city": "paris"}
        )
        print("Weather in Paris:", weather_paris)

if __name__ == "__main__":
    asyncio.run(main())

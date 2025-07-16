import random
from fastmcp import FastMCP
import asyncio
from typing import Dict

# In-memory weather data store
known_weather_data: Dict[str, float] = {
    "berlin": 20.0  # default seed data
}

# Weather getter
def get_weather(city: str) -> float:
    """
    Retrieves the temperature for a specified city.

    Parameters:
        city (str): The name of the city for which to retrieve weather data.

    Returns:
        float: The temperature associated with the city.
    """
    city = city.strip().lower()
    return known_weather_data.get(city, round(random.uniform(-5, 35), 1))

# Weather setter
def set_weather(city: str, temp: float) -> str:
    """
    Sets the temperature for a specified city.

    Parameters:
        city (str): The name of the city for which to set the weather data.
        temp (float): The temperature to associate with the city.

    Returns:
        str: A confirmation string 'OK' indicating successful update.
    """
    city = city.strip().lower()
    known_weather_data[city] = temp
    return 'OK'

# Setup MCP server
mcp = FastMCP("Demo 🚀")

# Expose tools
@mcp.tool
def get_weather_tool(city: str) -> float:
    return get_weather(city)

@mcp.tool
def set_weather_tool(city: str, temp: float) -> str:
    return set_weather(city, temp)

# Async entry point
async def main():
    await mcp.run_async(transport="http", host="127.0.0.1", port=8000)

# Run server
if __name__ == "__main__":
    asyncio.run(main())

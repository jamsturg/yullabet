"""TAB API MCP Server for sports and racing information."""

import json
import argparse
import uvicorn
from mcp.server.fastmcp import FastMCP
from .common import (
    DEFAULT_JURISDICTION,
    make_tab_api_request,
    prompt_for_credentials,
    prompt_for_jurisdiction,
    create_starlette_app,
)

# Initialize FastMCP server for TAB API tools (SSE)
mcp = FastMCP("tab-api")


@mcp.tool()
async def get_sports(jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get a list of available sports.
    
    Args:
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = "/v1/tab-info-service/sports/"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching sports: {str(e)}"


@mcp.tool()
async def get_sport_competitions(sport_name: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get competitions for a specific sport.
    
    Args:
        sport_name: The name of the sport (e.g., Rugby League, Soccer)
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/sports/{sport_name}/competitions"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching competitions for {sport_name}: {str(e)}"


@mcp.tool()
async def get_racing_dates() -> str:
    """Get available racing dates."""
    endpoint = "/v1/tab-info-service/racing/dates"
    
    try:
        data = await make_tab_api_request(endpoint)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching racing dates: {str(e)}"


@mcp.tool()
async def get_racing_meetings(date: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get racing meetings for a specific date.
    
    Args:
        date: The date in YYYY-MM-DD format
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/racing/dates/{date}/meetings"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching racing meetings for {date}: {str(e)}"


@mcp.tool()
async def get_racing_races(date: str, meeting_code: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get races for a specific meeting.
    
    Args:
        date: The date in YYYY-MM-DD format
        meeting_code: The meeting code (e.g., R/MEL for Melbourne Racing)
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/racing/dates/{date}/meetings/{meeting_code}/races"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching races for meeting {meeting_code} on {date}: {str(e)}"


def main():
    """Run the TAB API MCP server."""
    parser = argparse.ArgumentParser(description='Run TAB API MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    parser.add_argument('--no-prompt', action='store_true', help='Skip prompting for credentials')
    args = parser.parse_args()

    print("=== TAB API MCP Server ===")
    
    if not args.no_prompt:
        prompt_for_credentials()
        prompt_for_jurisdiction()
    
    # Get the MCP server
    mcp_server = mcp._mcp_server  # noqa: WPS437
    
    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    print(f"\nStarting TAB API MCP server on {args.host}:{args.port}")
    print("TAB API MCP server started with sports and racing tools")
    
    try:
        uvicorn.run(starlette_app, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\nTAB API MCP server stopped.")
    except Exception as e:
        print(f"\nError running TAB API MCP server: {str(e)}")
        print("TAB API MCP server stopped.")


if __name__ == "__main__":
    main()
from typing import Any, Dict, List, Optional
import httpx
import os
import json
import getpass
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import uvicorn

# Initialize FastMCP server for TAB API tools (SSE)
mcp = FastMCP("tab-api")

# Constants
TAB_API_BASE = "https://api.beta.tab.com.au"
TOKEN_ENDPOINT = f"{TAB_API_BASE}/oauth/token"
DEFAULT_JURISDICTION = "NSW"

# Client credentials (will be prompted)
CLIENT_ID = ""
CLIENT_SECRET = ""

# Cache for the access token
access_token_cache = {
    "token": None,
    "expires_at": 0
}

def prompt_for_credentials():
    """Prompt the user for TAB API credentials."""
    global CLIENT_ID, CLIENT_SECRET
    
    # Try to read from environment variables first
    CLIENT_ID = os.environ.get("TAB_CLIENT_ID", "")
    CLIENT_SECRET = os.environ.get("TAB_CLIENT_SECRET", "")
    
    # If not set, prompt the user
    if not CLIENT_ID:
        CLIENT_ID = input("Enter your TAB API Client ID: ")
    
    if not CLIENT_SECRET:
        CLIENT_SECRET = getpass.getpass("Enter your TAB API Client Secret: ")
    
    # Validate
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Both Client ID and Client Secret are required.")
        exit(1)
    
    print("TAB API credentials set successfully.")

async def get_access_token() -> str:
    """Get an access token for the TAB API using client credentials."""
    if not CLIENT_ID or not CLIENT_SECRET:
        raise ValueError("TAB API credentials are not set")
    
    # Check if we have a valid token in cache
    import time
    current_time = int(time.time())
    if access_token_cache["token"] and access_token_cache["expires_at"] > current_time:
        return access_token_cache["token"]
    
    # Request a new token
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(TOKEN_ENDPOINT, data=data, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        
        # Cache the token
        access_token_cache["token"] = token_data["access_token"]
        access_token_cache["expires_in"] = token_data.get("expires_in", 3600)
        access_token_cache["expires_at"] = current_time + token_data.get("expires_in", 3600)
        
        return token_data["access_token"]

async def make_tab_api_request(endpoint: str, method: str = "GET", params: Dict = None, data: Dict = None) -> Dict[str, Any]:
    """Make a request to the TAB API with proper error handling."""
    token = await get_access_token()
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    
    url = f"{TAB_API_BASE}{endpoint}"
    
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, headers=headers, params=params)
            elif method == "POST":
                headers["Content-Type"] = "application/json"
                response = await client.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            error_message = f"HTTP error: {e.response.status_code}"
            try:
                error_data = e.response.json()
                if "error" in error_data:
                    error_message = f"{error_message} - {error_data['error'].get('message', '')}"
            except:
                pass
            raise Exception(error_message)
        except Exception as e:
            raise Exception(f"Error making TAB API request: {str(e)}")

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

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can serve the provided mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )

def prompt_for_jurisdiction():
    """Prompt the user for the default jurisdiction."""
    global DEFAULT_JURISDICTION
    
    jurisdictions = ["NSW", "VIC", "QLD", "SA", "TAS", "ACT", "NT"]
    
    print("\nAvailable jurisdictions:")
    for i, jurisdiction in enumerate(jurisdictions, 1):
        print(f"{i}. {jurisdiction}")
    
    while True:
        try:
            choice = input(f"\nSelect default jurisdiction (1-{len(jurisdictions)}, default is NSW): ")
            if not choice:
                break  # Keep default
            
            choice = int(choice)
            if 1 <= choice <= len(jurisdictions):
                DEFAULT_JURISDICTION = jurisdictions[choice - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(jurisdictions)}")
        except ValueError:
            print("Please enter a valid number")
    
    print(f"Default jurisdiction set to: {DEFAULT_JURISDICTION}")

# Use os.path for path manipulation to ensure cross-platform compatibility
def get_config_path():
    """Get the path to the configuration file."""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "chat-config.json")

if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run TAB API MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    parser.add_argument('--no-prompt', action='store_true', help='Skip prompting for credentials')
    args = parser.parse_args()

    print("=== TAB API MCP Server ===")
    
    if not args.no_prompt:
        prompt_for_credentials()
        prompt_for_jurisdiction()
    
    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    print(f"\nStarting TAB API MCP server on {args.host}:{args.port}")
    print(f"Available tools: {[tool.name for tool in mcp._mcp_server.tools]}")
    
    uvicorn.run(starlette_app, host=args.host, port=args.port)
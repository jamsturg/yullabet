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
mcp = FastMCP("tab-api-betting")

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

# Account Management Tools

@mcp.tool()
async def get_account_details() -> str:
    """Get details about the user's TAB account."""
    endpoint = "/v1/account-service/accounts"
    
    try:
        data = await make_tab_api_request(endpoint)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching account details: {str(e)}"

@mcp.tool()
async def get_account_balance() -> str:
    """Get the current balance of the user's TAB account."""
    endpoint = "/v1/account-service/accounts/balance"
    
    try:
        data = await make_tab_api_request(endpoint)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching account balance: {str(e)}"

@mcp.tool()
async def get_transaction_history(from_date: str = None, to_date: str = None, transaction_type: str = None) -> str:
    """Get transaction history for the user's TAB account.
    
    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        transaction_type: Type of transaction (e.g., DEPOSIT, WITHDRAWAL, BET, RETURN)
    """
    endpoint = "/v1/account-service/accounts/transactions"
    params = {}
    
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    if transaction_type:
        params["transactionType"] = transaction_type
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching transaction history: {str(e)}"

# Betting Tools

@mcp.tool()
async def place_bet(
    bet_type: str, 
    selections: List[Dict], 
    stake: float, 
    bet_option: str = "SINGLE"
) -> str:
    """Place a bet on the TAB platform.
    
    Args:
        bet_type: Type of bet (e.g., WIN, PLACE, EACH_WAY)
        selections: List of selections, each with eventId, marketId, and selectionId
        stake: Amount to bet
        bet_option: Betting option (SINGLE, MULTI, etc.)
    """
    endpoint = "/v1/tab-betting-service/bets"
    
    data = {
        "betType": bet_type,
        "selections": selections,
        "stake": stake,
        "betOption": bet_option
    }
    
    try:
        response = await make_tab_api_request(endpoint, method="POST", data=data)
        return json.dumps(response, indent=2)
    except Exception as e:
        return f"Error placing bet: {str(e)}"

@mcp.tool()
async def get_bet_history(from_date: str = None, to_date: str = None, status: str = None) -> str:
    """Get betting history for the user's TAB account.
    
    Args:
        from_date: Start date in YYYY-MM-DD format
        to_date: End date in YYYY-MM-DD format
        status: Bet status (e.g., SETTLED, PENDING, CANCELLED)
    """
    endpoint = "/v1/tab-betting-service/bets"
    params = {}
    
    if from_date:
        params["fromDate"] = from_date
    if to_date:
        params["toDate"] = to_date
    if status:
        params["status"] = status
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching bet history: {str(e)}"

@mcp.tool()
async def get_active_bets() -> str:
    """Get all active (unsettled) bets for the user's TAB account."""
    endpoint = "/v1/tab-betting-service/bets/active"
    
    try:
        data = await make_tab_api_request(endpoint)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching active bets: {str(e)}"

@mcp.tool()
async def cancel_bet(bet_id: str) -> str:
    """Cancel a pending bet.
    
    Args:
        bet_id: ID of the bet to cancel
    """
    endpoint = f"/v1/tab-betting-service/bets/{bet_id}/cancel"
    
    try:
        response = await make_tab_api_request(endpoint, method="POST")
        return json.dumps(response, indent=2)
    except Exception as e:
        return f"Error cancelling bet: {str(e)}"

# Markets and Odds Tools

@mcp.tool()
async def get_markets(event_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get available markets for a specific event.
    
    Args:
        event_id: ID of the event
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/events/{event_id}/markets"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching markets for event {event_id}: {str(e)}"

@mcp.tool()
async def get_odds(market_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get odds for a specific market.
    
    Args:
        market_id: ID of the market
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/markets/{market_id}/odds"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching odds for market {market_id}: {str(e)}"

@mcp.tool()
async def get_live_odds(event_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get live odds updates for a specific event.
    
    Args:
        event_id: ID of the event
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/events/{event_id}/live-odds"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching live odds for event {event_id}: {str(e)}"

# Additional Sports and Racing Data Tools

@mcp.tool()
async def get_event_details(event_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get detailed information about a specific event.
    
    Args:
        event_id: ID of the event
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/events/{event_id}"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching details for event {event_id}: {str(e)}"

@mcp.tool()
async def get_race_details(race_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get detailed information about a specific race.
    
    Args:
        race_id: ID of the race
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/racing/races/{race_id}"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching details for race {race_id}: {str(e)}"

@mcp.tool()
async def get_runner_details(race_id: str, runner_id: str, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get detailed information about a specific runner in a race.
    
    Args:
        race_id: ID of the race
        runner_id: ID of the runner
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    endpoint = f"/v1/tab-info-service/racing/races/{race_id}/runners/{runner_id}"
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching details for runner {runner_id} in race {race_id}: {str(e)}"

@mcp.tool()
async def get_sport_events(sport_name: str, competition_id: str = None, jurisdiction: str = DEFAULT_JURISDICTION) -> str:
    """Get events for a specific sport and optionally a specific competition.
    
    Args:
        sport_name: Name of the sport (e.g., Rugby League, Soccer)
        competition_id: Optional ID of a specific competition
        jurisdiction: The jurisdiction code (e.g., NSW, VIC, QLD)
    """
    if competition_id:
        endpoint = f"/v1/tab-info-service/sports/{sport_name}/competitions/{competition_id}/events"
    else:
        endpoint = f"/v1/tab-info-service/sports/{sport_name}/events"
    
    params = {"jurisdiction": jurisdiction}
    
    try:
        data = await make_tab_api_request(endpoint, params=params)
        return json.dumps(data, indent=2)
    except Exception as e:
        return f"Error fetching events for sport {sport_name}: {str(e)}"

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

if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run TAB API Betting MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8082, help='Port to listen on')
    parser.add_argument('--no-prompt', action='store_true', help='Skip prompting for credentials')
    args = parser.parse_args()

    print("=== TAB API Betting MCP Server ===")
    
    if not args.no_prompt:
        prompt_for_credentials()
    
    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    print(f"\nStarting TAB API Betting MCP server on {args.host}:{args.port}")
    print("TAB API Betting MCP server started with betting and account management tools")
    
    uvicorn.run(starlette_app, host=args.host, port=args.port)
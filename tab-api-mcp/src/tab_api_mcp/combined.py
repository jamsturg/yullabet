"""Combined TAB API MCP Server with all functionality."""

import json
import argparse
from typing import Dict, List
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
mcp = FastMCP("tab-api-combined")

# Sports and Racing Information Tools

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


def main():
    """Run the combined TAB API MCP server."""
    parser = argparse.ArgumentParser(description='Run Combined TAB API MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    parser.add_argument('--no-prompt', action='store_true', help='Skip prompting for credentials')
    args = parser.parse_args()

    print("=== Combined TAB API MCP Server ===")
    
    if not args.no_prompt:
        prompt_for_credentials()
        prompt_for_jurisdiction()
    
    # Get the MCP server
    mcp_server = mcp._mcp_server  # noqa: WPS437
    
    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    print(f"\nStarting Combined TAB API MCP server on {args.host}:{args.port}")
    print("Combined TAB API MCP server started with all sports, racing, betting, and account management tools")
    
    try:
        uvicorn.run(starlette_app, host=args.host, port=args.port)
    except KeyboardInterrupt:
        print("\nCombined TAB API MCP server stopped.")
    except Exception as e:
        print(f"\nError running Combined TAB API MCP server: {str(e)}")
        print("Combined TAB API MCP server stopped.")


if __name__ == "__main__":
    main()
# TAB API MCP Server

This package provides an MCP (Model Context Protocol) server for the TAB API, allowing AI assistants to interact with the TAB betting platform.

## Features

- **Combined TAB API MCP Server**: Provides all sports, racing, betting, and account management tools in a single server
- **Individual Servers**: Also provides separate servers for basic sports/racing information and betting functionality if needed

## Installation

```bash
# Install the package
pip install -e .
```

## Usage

### Starting the Server

```bash
# Start the combined TAB API MCP server (recommended)
python -m tab_api_mcp --port 8080

# Or use the provided scripts
./start-tab-api-mcp-combined.sh  # macOS/Linux
start-tab-api-mcp-combined.bat   # Windows
```

### Starting Individual Servers (if needed)

```bash
# Start the basic TAB API MCP server
python -m tab_api_mcp server --port 8081

# Start the TAB API Betting MCP server
python -m tab_api_mcp betting --port 8082
```

### Available Tools

#### Sports and Racing Information

- `get_sports`: Get a list of available sports
- `get_sport_competitions`: Get competitions for a specific sport
- `get_sport_events`: Get events for a specific sport and optionally a specific competition
- `get_racing_dates`: Get available racing dates
- `get_racing_meetings`: Get racing meetings for a specific date
- `get_racing_races`: Get races for a specific meeting
- `get_event_details`: Get detailed information about a specific event
- `get_race_details`: Get detailed information about a specific race
- `get_runner_details`: Get detailed information about a specific runner in a race

#### Account Management

- `get_account_details`: Get details about the user's TAB account
- `get_account_balance`: Get the current balance of the user's TAB account
- `get_transaction_history`: Get transaction history for the user's TAB account

#### Betting

- `place_bet`: Place a bet on the TAB platform
- `get_bet_history`: Get betting history for the user's TAB account
- `get_active_bets`: Get all active (unsettled) bets for the user's TAB account
- `cancel_bet`: Cancel a pending bet

#### Markets and Odds

- `get_markets`: Get available markets for a specific event
- `get_odds`: Get odds for a specific market
- `get_live_odds`: Get live odds updates for a specific event
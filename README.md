# Yullabet

This repository contains configuration for setting up MCP servers for AI agent interaction.

## Requirements

### MCP-Chat Requirements
- Node.js (v14 or higher)
- npm (v6 or higher)
- The following npm packages:
  - @modelcontextprotocol/server-filesystem
  - mcp
  - express
  - socket.io

### Freqtrade-MCP Requirements
- Python 3.10+
- The following Python packages:
  - freqtrade-client
  - mcp[cli]
- A running Freqtrade instance with the REST API enabled

### TAB API MCP Requirements
- Python 3.10+
- The following Python packages:
  - httpx
  - mcp[server]
  - starlette
  - uvicorn
  - python-dotenv
- TAB API credentials (will be prompted when starting the server)

## Setup

This repository includes:

1. **MCP-Chat Configuration**: A configuration file for the MCP-Chat server that includes the filesystem MCP server, the freqtrade-mcp server, and the TAB API MCP server.

2. **Configuration Script**: A PowerShell script to copy the configuration to the MCP-Chat directory.

3. **TAB API MCP Server**: A Python-based MCP server that provides tools for interacting with the TAB API.

### Installation

1. **Install MCP-Chat Dependencies**:
   ```bash
   cd mcp-chat
   npm install
   ```

2. **Install Freqtrade-MCP Dependencies**:
   ```bash
   cd freqtrade-mcp
   pip install -r requirements.txt
   # Or using uv
   uv add freqtrade-client "mcp[cli]"
   ```

3. **Install TAB API MCP Dependencies**:
   ```bash
   pip install httpx mcp[server] starlette uvicorn python-dotenv
   # Or using uv
   uv add httpx "mcp[server]" starlette uvicorn python-dotenv
   ```

## Usage

### 1. Copy the Configuration

Run the PowerShell script to copy the configuration to the MCP-Chat directory:

```powershell
cd config
.\copy-config.ps1
```

This will create a new chat configuration in the `.mcpchat/chats` directory with all MCP servers included.

### 2. Start the MCP Servers

Start the TAB API MCP server:

```bash
.\start-tab-api-mcp.bat
```

When the TAB API MCP server starts, it will prompt you for:
- TAB API Client ID
- TAB API Client Secret
- Default jurisdiction (NSW, VIC, QLD, etc.)

### 3. Start MCP-Chat

Start the MCP-Chat server:

```bash
.\start-mcp-chat.bat
```

### 4. Select the Configuration

Open the MCP-Chat web interface (usually at http://localhost:3000) and select the newly created chat configuration.

## MCP Servers

### 1. Filesystem MCP Server

Provides access to the filesystem.

Command:
```
npx -y @modelcontextprotocol/server-filesystem C://
```

### 2. Freqtrade MCP Server

Provides integration with the Freqtrade cryptocurrency trading bot.

Command:
```
uv --directory C:/Users/adam/Desktop/freqtrade-mcp run __main__.py
```

Environment variables:
- FREQTRADE_API_URL: The URL of the Freqtrade API (default: http://127.0.0.1:8080)
- FREQTRADE_USERNAME: The username for the Freqtrade API
- FREQTRADE_PASSWORD: The password for the Freqtrade API

### 3. TAB API MCP Server

Provides integration with the TAB API for sports and racing information.

Command:
```
python C:/Users/adam/Desktop/yullabet/tab-api-mcp.py --port 8081
```

Command-line options:
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to listen on (default: 8081)
- `--no-prompt`: Skip prompting for credentials (useful if set in environment variables)

Environment variables (optional, will be prompted if not set):
- TAB_CLIENT_ID: The client ID for the TAB API
- TAB_CLIENT_SECRET: The client secret for the TAB API

## Available Tools

### Freqtrade MCP Tools

The freqtrade-mcp server provides the following tools:

- `fetch_market_data`: Fetch OHLCV data for a pair
- `fetch_bot_status`: Get open trade status
- `fetch_profit`: Get profit summary
- `fetch_balance`: Get account balance
- `fetch_performance`: Get performance metrics
- `fetch_whitelist`: Get whitelist of pairs
- `fetch_blacklist`: Get blacklist of pairs
- `fetch_trades`: Get trade history
- `fetch_config`: Get bot configuration
- `fetch_locks`: Get trade locks
- `place_trade`: Place a buy/sell trade
- `start_bot`: Start the bot
- `stop_bot`: Stop the bot
- `reload_config`: Reload bot configuration
- `add_blacklist`: Add pair to blacklist
- `delete_blacklist`: Remove pair from blacklist
- `delete_lock`: Delete a trade lock

### TAB API MCP Tools

The TAB API MCP server provides the following tools:

- `get_sports`: Get a list of available sports
- `get_sport_competitions`: Get competitions for a specific sport
- `get_racing_dates`: Get available racing dates
- `get_racing_meetings`: Get racing meetings for a specific date
- `get_racing_races`: Get races for a specific meeting
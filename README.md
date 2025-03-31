# Yullabet

This repository contains configuration for setting up MCP servers for AI agent interaction.

## Setup

This repository includes:

1. **MCP-Chat Configuration**: A configuration file for the MCP-Chat server that includes both the filesystem MCP server and the freqtrade-mcp server.

2. **Configuration Script**: A PowerShell script to copy the configuration to the MCP-Chat directory.

## Usage

### 1. Copy the Configuration

Run the PowerShell script to copy the configuration to the MCP-Chat directory:

```powershell
cd config
.\copy-config.ps1
```

This will create a new chat configuration in the `.mcpchat/chats` directory with the freqtrade-mcp server included.

### 2. Start MCP-Chat

Start the MCP-Chat server:

```bash
cd path/to/mcp-chat
npm start
```

### 3. Select the Configuration

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
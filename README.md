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

1. **MCP-Chat Configuration**: A configuration file for the MCP-Chat server that includes multiple MCP servers for enhanced functionality.

2. **Configuration Script**: Scripts to copy the configuration to the MCP-Chat directory.

3. **TAB API MCP Server**: A Python-based MCP server that provides tools for interacting with the TAB API.

4. **Setup Scripts**: Scripts for setting up the environment and MCP servers on Windows and macOS.

### Automated Setup for MCP Servers

#### Windows:

```powershell
# Run the setup script for MCP servers
.\setup-mcp-servers.ps1
```

This script will:
1. Check and verify Node.js and npm installation
2. Check and install Python dependencies
3. Install Smithery CLI
4. Install UV and UVX
5. Clone and set up freqtrade-mcp
6. Install all Smithery MCP servers:
   - @smithery-ai/server-sequential-thinking
   - @browserbasehq/mcp-browserbase
   - @ashley-ha/mcp-manus
   - @IzumiSy/mcp-duckdb-memory-server
   - @capecoma/winterm-mcp
   - mcp-server-ccxt
   - @simonb97/server-win-cli
   - @sidharthrajaram/mcp-sse

#### macOS:

```bash
# Make the script executable
chmod +x setup-mcp-servers.sh

# Run the setup script for MCP servers
./setup-mcp-servers.sh
```

This script performs the same setup steps as the Windows version, but adapted for macOS.

### Automated Setup for Environment (macOS)

For macOS users, a comprehensive environment setup script is also provided:

```bash
# Make the script executable
chmod +x setup-mac.sh

# Run the setup script
./setup-mac.sh
```

This script will:
1. Make all shell scripts executable
2. Check and verify Node.js and npm installation
3. Check and install Python dependencies
4. Set up MCP-Chat
5. Copy the configuration to the .mcpchat/chats directory

### Manual Installation

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

#### Windows:
```powershell
cd config
.\copy-config.ps1
```

#### macOS/Linux:
```bash
cd config
# Make the script executable if needed
chmod +x copy-config.sh
./copy-config.sh
```

This will create a new chat configuration in the `.mcpchat/chats` directory with all MCP servers included.

### 2. Start the MCP Servers

Start the TAB API MCP server:

#### Windows:
```bash
.\start-tab-api-mcp.bat
```

#### macOS/Linux:
```bash
# Make the script executable if needed
chmod +x start-tab-api-mcp.sh
./start-tab-api-mcp.sh
```

When the TAB API MCP server starts, it will prompt you for:
- TAB API Client ID
- TAB API Client Secret
- Default jurisdiction (NSW, VIC, QLD, etc.)

### 3. Start MCP-Chat

#### Windows:
```bash
.\start-mcp-chat.bat
```

#### macOS/Linux:
```bash
# Make the script executable if needed
chmod +x start-mcp-chat.sh
./start-mcp-chat.sh
```

### 4. Select the Configuration

Open the MCP-Chat web interface (usually at http://localhost:3000) and select the newly created chat configuration.

## MCP Servers

### 1. Filesystem MCP Server

Provides access to the filesystem.

### 2. Freqtrade MCP Server

Provides integration with the Freqtrade cryptocurrency trading bot.

Environment variables:
- FREQTRADE_API_URL: The URL of the Freqtrade API (default: http://127.0.0.1:8080)
- FREQTRADE_USERNAME: The username for the Freqtrade API
- FREQTRADE_PASSWORD: The password for the Freqtrade API

### 3. TAB API MCP Server

Provides integration with the TAB API for sports and racing information.

Command-line options:
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`: Port to listen on (default: 8081)
- `--no-prompt`: Skip prompting for credentials (useful if set in environment variables)

Environment variables (optional, will be prompted if not set):
- TAB_CLIENT_ID: The client ID for the TAB API
- TAB_CLIENT_SECRET: The client secret for the TAB API

### 4. Additional MCP Servers

The configuration includes several additional MCP servers:

- **@smithery-ai/server-sequential-thinking**: Provides sequential thinking capabilities
- **@browserbasehq/mcp-browserbase**: Provides browser automation capabilities
- **@ashley-ha/mcp-manus**: Provides additional functionality
- **@IzumiSy/mcp-duckdb-memory-server**: Provides DuckDB database capabilities
- **@capecoma/winterm-mcp**: Provides terminal access
- **mcp-server-aidd**: Provides AI-driven development capabilities
- **mcp-server-ccxt**: Provides cryptocurrency exchange integration
- **@simonb97/server-win-cli**: Provides Windows CLI capabilities
- **@sidharthrajaram/mcp-sse**: Provides SSE-based MCP server capabilities

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
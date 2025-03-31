@echo off
echo Starting MCP-Chat server...

set ANTHROPIC_API_KEY=%ANTHROPIC_API_KEY%
if "%ANTHROPIC_API_KEY%"=="" (
    echo ERROR: ANTHROPIC_API_KEY environment variable is not set
    echo Please set your Anthropic API key and try again
    exit /b 1
)

cd mcp-chat
npx mcp-chat --config "../config/chat-config.json"

echo MCP-Chat server stopped.
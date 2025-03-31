@echo off
echo Starting TAB API MCP server...

REM Load environment variables from .env file
for /f "tokens=*" %%a in (.env) do (
    set "%%a"
)

REM Start the TAB API MCP server
python tab-api-mcp.py --port 8081

echo TAB API MCP server stopped.
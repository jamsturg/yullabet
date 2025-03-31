@echo off
echo Starting Combined TAB API MCP server...

set TAB_CLIENT_ID=%TAB_CLIENT_ID%
if "%TAB_CLIENT_ID%"=="" (
    echo WARNING: TAB_CLIENT_ID environment variable is not set
    echo You will be prompted to enter your TAB API Client ID
)

set TAB_CLIENT_SECRET=%TAB_CLIENT_SECRET%
if "%TAB_CLIENT_SECRET%"=="" (
    echo WARNING: TAB_CLIENT_SECRET environment variable is not set
    echo You will be prompted to enter your TAB API Client Secret
)

python -m tab_api_mcp --port 8083

echo Combined TAB API MCP server stopped.
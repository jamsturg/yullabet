@echo off
echo Installing TAB API MCP...

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.11 or later.
    exit /b 1
)

:: Install the package in development mode
pip install -e .

echo TAB API MCP installed successfully.
echo You can now run the server using:
echo   .\start-tab-api-mcp-combined.bat (recommended)
echo Or run individual servers:
echo   .\start-tab-api-mcp.bat
echo   .\start-tab-api-betting-mcp.bat
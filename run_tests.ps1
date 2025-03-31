# PowerShell script to run all tests

# Function to print section headers
function Write-Header {
    param (
        [string]$Title
    )
    
    Write-Host ""
    Write-Host "===== $Title ====="
    Write-Host ""
}

# Function to run a test file
function Run-Test {
    param (
        [string]$TestFile
    )
    
    Write-Host "Running test: $TestFile"
    python -m unittest $TestFile
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Test failed: $TestFile" -ForegroundColor Red
        return $false
    } else {
        Write-Host "Test passed: $TestFile" -ForegroundColor Green
        return $true
    }
}

# Main function
function Main {
    Write-Header "Running Tests"
    
    # Change to the project directory
    $projectDir = $PSScriptRoot
    Set-Location $projectDir
    
    # Install test dependencies
    Write-Header "Installing Test Dependencies"
    pip install pytest pytest-asyncio httpx requests
    
    # Run the TAB API MCP server tests
    Write-Header "Running TAB API MCP Server Tests"
    $tabApiTestResult = Run-Test "tests.test_tab_api_mcp"
    
    # Run the setup scripts tests
    Write-Header "Running Setup Scripts Tests"
    $setupScriptsTestResult = Run-Test "tests.test_setup_scripts"
    
    # Run the TAB API MCP server integration tests
    Write-Header "Running TAB API MCP Server Integration Tests"
    $tabApiIntegrationTestResult = Run-Test "tests.test_tab_api_mcp_integration"
    
    # Print the test results
    Write-Header "Test Results"
    if ($tabApiTestResult -and $setupScriptsTestResult -and $tabApiIntegrationTestResult) {
        Write-Host "All tests passed!" -ForegroundColor Green
    } else {
        Write-Host "Some tests failed!" -ForegroundColor Red
    }
}

# Run the main function
Main
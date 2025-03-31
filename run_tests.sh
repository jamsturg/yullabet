#!/bin/bash

# Shell script to run all tests

# Function to print section headers
print_header() {
    echo ""
    echo "===== $1 ====="
    echo ""
}

# Function to run a test file
run_test() {
    echo "Running test: $1"
    python3 -m unittest $1
    
    if [ $? -ne 0 ]; then
        echo -e "\033[0;31mTest failed: $1\033[0m"
        return 1
    else
        echo -e "\033[0;32mTest passed: $1\033[0m"
        return 0
    fi
}

# Main function
main() {
    print_header "Running Tests"
    
    # Change to the project directory
    project_dir=$(dirname "$0")
    cd "$project_dir"
    
    # Install test dependencies
    print_header "Installing Test Dependencies"
    pip3 install pytest pytest-asyncio httpx requests
    
    # Run the TAB API MCP server tests
    print_header "Running TAB API MCP Server Tests"
    run_test "tests.test_tab_api_mcp"
    tab_api_test_result=$?
    
    # Run the setup scripts tests
    print_header "Running Setup Scripts Tests"
    run_test "tests.test_setup_scripts"
    setup_scripts_test_result=$?
    
    # Run the TAB API MCP server integration tests
    print_header "Running TAB API MCP Server Integration Tests"
    run_test "tests.test_tab_api_mcp_integration"
    tab_api_integration_test_result=$?
    
    # Print the test results
    print_header "Test Results"
    if [ $tab_api_test_result -eq 0 ] && [ $setup_scripts_test_result -eq 0 ] && [ $tab_api_integration_test_result -eq 0 ]; then
        echo -e "\033[0;32mAll tests passed!\033[0m"
    else
        echo -e "\033[0;31mSome tests failed!\033[0m"
    fi
}

# Run the main function
main
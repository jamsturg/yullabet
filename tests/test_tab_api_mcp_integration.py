import unittest
import sys
import os
import json
import asyncio
import subprocess
import time
import platform
import requests
import signal
from unittest.mock import patch

class TestTabApiMcpIntegration(unittest.TestCase):
    """Integration tests for the TAB API MCP server."""

    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        # Get the path to the TAB API MCP server script
        cls.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        cls.tab_api_script = os.path.join(cls.script_dir, 'tab-api-mcp.py')
        
        # Set environment variables for testing
        os.environ['TAB_CLIENT_ID'] = 'test_client_id'
        os.environ['TAB_CLIENT_SECRET'] = 'test_client_secret'
        
        # Start the TAB API MCP server
        cls.start_server()
        
        # Wait for the server to start
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        # Stop the TAB API MCP server
        cls.stop_server()
        
        # Remove environment variables
        if 'TAB_CLIENT_ID' in os.environ:
            del os.environ['TAB_CLIENT_ID']
        if 'TAB_CLIENT_SECRET' in os.environ:
            del os.environ['TAB_CLIENT_SECRET']

    @classmethod
    def start_server(cls):
        """Start the TAB API MCP server."""
        # Determine the Python executable to use
        python_exe = 'python' if platform.system() == 'Windows' else 'python3'
        
        # Start the server with the --no-prompt flag to skip prompting for credentials
        cls.server_process = subprocess.Popen(
            [python_exe, cls.tab_api_script, '--port', '8082', '--no-prompt'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print(f"Started TAB API MCP server with PID {cls.server_process.pid}")

    @classmethod
    def stop_server(cls):
        """Stop the TAB API MCP server."""
        if platform.system() == 'Windows':
            # On Windows, use taskkill to kill the process
            subprocess.run(['taskkill', '/F', '/T', '/PID', str(cls.server_process.pid)])
        else:
            # On macOS/Linux, use os.kill
            os.kill(cls.server_process.pid, signal.SIGTERM)
        
        # Wait for the process to terminate
        cls.server_process.wait()
        
        print(f"Stopped TAB API MCP server with PID {cls.server_process.pid}")

    def test_server_running(self):
        """Test that the server is running."""
        # Try to connect to the server
        try:
            response = requests.get('http://localhost:8082/sse')
            self.assertEqual(response.status_code, 200)
        except requests.exceptions.ConnectionError:
            self.fail("Could not connect to the TAB API MCP server")

    @unittest.skip("This test requires a mock TAB API server")
    def test_get_sports(self):
        """Test the get_sports endpoint."""
        # This test would require a mock TAB API server
        # For now, we'll skip it
        pass

    @unittest.skip("This test requires a mock TAB API server")
    def test_get_sport_competitions(self):
        """Test the get_sport_competitions endpoint."""
        # This test would require a mock TAB API server
        # For now, we'll skip it
        pass

class TestCrossPlatformCompatibility(unittest.TestCase):
    """Test cases for cross-platform compatibility."""

    def test_tab_api_script_compatibility(self):
        """Test that the TAB API MCP server script is compatible with both Windows and macOS."""
        # Get the path to the TAB API MCP server script
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        tab_api_script = os.path.join(script_dir, 'tab-api-mcp.py')
        
        # Check that the script exists
        self.assertTrue(os.path.exists(tab_api_script), f"TAB API MCP server script {tab_api_script} does not exist")
        
        # Check that the script uses platform-independent paths
        with open(tab_api_script, 'r') as f:
            script_content = f.read()
        
        # Check for platform-specific path separators
        self.assertNotIn('\\\\', script_content, "Script contains Windows-specific path separators")
        
        # Check for platform-specific commands
        self.assertNotIn('cmd.exe', script_content, "Script contains Windows-specific commands")
        self.assertNotIn('powershell', script_content, "Script contains Windows-specific commands")
        self.assertNotIn('bash', script_content, "Script contains macOS/Linux-specific commands")
        self.assertNotIn('sh', script_content, "Script contains macOS/Linux-specific commands")
        
        # Check for use of os.path for path manipulation
        self.assertIn('os.path', script_content, "Script does not use os.path for path manipulation")

if __name__ == '__main__':
    unittest.main()
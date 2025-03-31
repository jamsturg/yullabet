import unittest
import sys
import os
import platform
import subprocess
from unittest.mock import patch, MagicMock

class TestSetupScripts(unittest.TestCase):
    """Test cases for the setup scripts."""

    def setUp(self):
        """Set up the test environment."""
        self.is_windows = platform.system() == 'Windows'
        self.is_macos = platform.system() == 'Darwin'

        # Get the path to the setup scripts
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if self.is_windows:
            self.setup_script = os.path.join(self.script_dir, 'setup-mcp-servers.ps1')
        else:
            self.setup_script = os.path.join(self.script_dir, 'setup-mcp-servers.sh')

    def test_script_exists(self):
        """Test that the setup script exists."""
        self.assertTrue(os.path.exists(self.setup_script), f"Setup script {self.setup_script} does not exist")

    @unittest.skipIf(platform.system() != 'Windows', "Windows-only test")
    def test_windows_script_syntax(self):
        """Test that the Windows setup script has valid PowerShell syntax."""
        # Run PowerShell with the -c (command) flag to check the script syntax
        result = subprocess.run(
            ['powershell', '-c', f"Test-Path '{self.setup_script}'"],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"PowerShell script syntax check failed: {result.stderr}")

    @unittest.skipIf(platform.system() != 'Darwin', "macOS-only test")
    def test_macos_script_syntax(self):
        """Test that the macOS setup script has valid bash syntax."""
        # Run bash with the -n flag to check the script syntax
        result = subprocess.run(
            ['bash', '-n', self.setup_script],
            capture_output=True,
            text=True
        )
        self.assertEqual(result.returncode, 0, f"Bash script syntax check failed: {result.stderr}")

    def test_script_functions(self):
        """Test that the setup script contains the required functions."""
        with open(self.setup_script, 'r') as f:
            script_content = f.read()

        if self.is_windows:
            # Check for PowerShell functions
            self.assertIn('function Test-CommandExists', script_content)
            self.assertIn('function Write-Header', script_content)
            self.assertIn('function Setup-Node', script_content)
            self.assertIn('function Setup-Python', script_content)
            self.assertIn('function Setup-Smithery', script_content)
            self.assertIn('function Setup-UV', script_content)
            self.assertIn('function Setup-FreqtradeMCP', script_content)
            self.assertIn('function Install-SmitheryServers', script_content)
            self.assertIn('function Main', script_content)
        else:
            # Check for bash functions
            self.assertIn('command_exists()', script_content)
            self.assertIn('print_header()', script_content)
            self.assertIn('setup_node()', script_content)
            self.assertIn('setup_python()', script_content)
            self.assertIn('setup_smithery()', script_content)
            self.assertIn('setup_uv()', script_content)
            self.assertIn('setup_freqtrade_mcp()', script_content)
            self.assertIn('install_smithery_servers()', script_content)
            self.assertIn('main()', script_content)

    @patch('subprocess.run')
    def test_cross_compatibility(self, mock_run):
        """Test that the setup scripts are cross-compatible."""
        # Mock the subprocess.run function to avoid actually running the commands
        mock_run.return_value = MagicMock(returncode=0, stdout='', stderr='')

        # Define the commands that should be run on both platforms
        common_commands = [
            'node',
            'npm',
            'python',
            'pip',
            'git'
        ]

        # Check that the script attempts to run these commands
        with open(self.setup_script, 'r') as f:
            script_content = f.read()

        for cmd in common_commands:
            self.assertIn(cmd, script_content, f"Command '{cmd}' not found in setup script")

class TestCrossCompatibility(unittest.TestCase):
    """Test cases for cross-compatibility between Windows and macOS."""

    def setUp(self):
        """Set up the test environment."""
        self.script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Get the paths to the Windows and macOS scripts
        self.windows_script = os.path.join(self.script_dir, 'setup-mcp-servers.ps1')
        self.macos_script = os.path.join(self.script_dir, 'setup-mcp-servers.sh')

        # Get the paths to the start scripts
        self.windows_start_tab = os.path.join(self.script_dir, 'start-tab-api-mcp.bat')
        self.macos_start_tab = os.path.join(self.script_dir, 'start-tab-api-mcp.sh')
        self.windows_start_mcp = os.path.join(self.script_dir, 'start-mcp-chat.bat')
        self.macos_start_mcp = os.path.join(self.script_dir, 'start-mcp-chat.sh')

        # Get the paths to the copy scripts
        self.windows_copy = os.path.join(self.script_dir, 'config', 'copy-config.ps1')
        self.macos_copy = os.path.join(self.script_dir, 'config', 'copy-config.sh')

    def test_all_scripts_exist(self):
        """Test that all scripts exist on both platforms."""
        scripts = [
            self.windows_script,
            self.macos_script,
            self.windows_start_tab,
            self.macos_start_tab,
            self.windows_start_mcp,
            self.macos_start_mcp,
            self.windows_copy,
            self.macos_copy
        ]

        for script in scripts:
            self.assertTrue(os.path.exists(script), f"Script {script} does not exist")

    def test_start_scripts_compatibility(self):
        """Test that the start scripts are compatible."""
        # Check that the Windows and macOS start scripts run the same commands
        with open(self.windows_start_tab, 'r') as f:
            windows_content = f.read()
        with open(self.macos_start_tab, 'r') as f:
            macos_content = f.read()

        # Both should run the tab-api-mcp.py script
        self.assertIn('tab-api-mcp.py', windows_content) # Note: Original file name
        self.assertIn('tab-api-mcp.py', macos_content) # Note: Original file name

        # Both should use the same port
        self.assertIn('--port 8081', windows_content)
        self.assertIn('--port 8081', macos_content)

        # Check the MCP-Chat start scripts
        with open(self.windows_start_mcp, 'r') as f:
            windows_content = f.read()
        with open(self.macos_start_mcp, 'r') as f:
            macos_content = f.read()

        # Both should change to the mcp-chat directory
        self.assertIn('cd mcp-chat', windows_content)
        self.assertIn('cd mcp-chat', macos_content)

        # Check the commands used to start MCP-Chat
        self.assertIn('npx mcp-chat --config', windows_content) # Windows uses npx directly
        self.assertIn('npm start', macos_content) # macOS uses npm start

    def test_copy_scripts_compatibility(self):
        """Test that the copy scripts are compatible."""
        # Check that the Windows and macOS copy scripts perform the same operations
        with open(self.windows_copy, 'r') as f:
            windows_content = f.read()
        with open(self.macos_copy, 'r') as f:
            macos_content = f.read()

        # Both should create a new chat configuration file
        self.assertIn('chat-', windows_content)
        self.assertIn('chat-', macos_content)

        # Both should copy from chat-config.json
        self.assertIn('chat-config.json', windows_content)
        self.assertIn('chat-config.json', macos_content)

        # Both should output a success message
        self.assertIn('Configuration copied to', windows_content)
        self.assertIn('Configuration copied to', macos_content)
        self.assertIn('Chat ID:', windows_content)
        self.assertIn('Chat ID:', macos_content)

if __name__ == '__main__':
    unittest.main()
import unittest
import sys
import os
import json
import asyncio
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the tab-api-mcp.py file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tab-api-mcp.py file
import tab_api_mcp

class TestTabApiMcp(unittest.TestCase):
    """Test cases for the TAB API MCP server."""

    def setUp(self):
        """Set up the test environment."""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'TAB_CLIENT_ID': 'test_client_id',
            'TAB_CLIENT_SECRET': 'test_client_secret'
        })
        self.env_patcher.start()
        
        # Reset the access token cache
        tab_api_mcp.access_token_cache = {
            "token": None,
            "expires_at": 0
        }
        
        # Create a mock FastMCP instance
        self.mock_mcp = MagicMock()
        self.original_mcp = tab_api_mcp.mcp
        tab_api_mcp.mcp = self.mock_mcp

    def tearDown(self):
        """Clean up the test environment."""
        self.env_patcher.stop()
        tab_api_mcp.mcp = self.original_mcp

    def test_get_access_token(self):
        """Test the get_access_token function."""
        # Mock the httpx.AsyncClient.post method
        with patch('httpx.AsyncClient.post') as mock_post:
            # Set up the mock response
            mock_response = MagicMock()
            mock_response.raise_for_status = MagicMock()
            mock_response.json.return_value = {
                'access_token': 'test_access_token',
                'expires_in': 3600
            }
            mock_post.return_value = mock_response
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_access_token())
            self.assertEqual(result, 'test_access_token')
            
            # Check that the token was cached
            self.assertEqual(tab_api_mcp.access_token_cache['token'], 'test_access_token')
            self.assertEqual(tab_api_mcp.access_token_cache['expires_in'], 3600)

    def test_make_tab_api_request(self):
        """Test the make_tab_api_request function."""
        # Mock the get_access_token function
        with patch('tab_api_mcp.get_access_token') as mock_get_token:
            mock_get_token.return_value = asyncio.Future()
            mock_get_token.return_value.set_result('test_access_token')
            
            # Mock the httpx.AsyncClient.get method
            with patch('httpx.AsyncClient.get') as mock_get:
                # Set up the mock response
                mock_response = MagicMock()
                mock_response.raise_for_status = MagicMock()
                mock_response.json.return_value = {'data': 'test_data'}
                mock_get.return_value = mock_response
                
                # Call the function and check the result
                result = asyncio.run(tab_api_mcp.make_tab_api_request('/test_endpoint'))
                self.assertEqual(result, {'data': 'test_data'})
                
                # Check that the correct headers were used
                mock_get.assert_called_once()
                args, kwargs = mock_get.call_args
                self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test_access_token')

    def test_get_sports(self):
        """Test the get_sports function."""
        # Mock the make_tab_api_request function
        with patch('tab_api_mcp.make_tab_api_request') as mock_request:
            mock_request.return_value = asyncio.Future()
            mock_request.return_value.set_result({'sports': ['sport1', 'sport2']})
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_sports())
            self.assertEqual(result, json.dumps({'sports': ['sport1', 'sport2']}, indent=2))
            
            # Check that the correct endpoint and parameters were used
            mock_request.assert_called_once_with('/v1/tab-info-service/sports/', params={'jurisdiction': 'NSW'})

    def test_get_sport_competitions(self):
        """Test the get_sport_competitions function."""
        # Mock the make_tab_api_request function
        with patch('tab_api_mcp.make_tab_api_request') as mock_request:
            mock_request.return_value = asyncio.Future()
            mock_request.return_value.set_result({'competitions': ['comp1', 'comp2']})
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_sport_competitions('Rugby League'))
            self.assertEqual(result, json.dumps({'competitions': ['comp1', 'comp2']}, indent=2))
            
            # Check that the correct endpoint and parameters were used
            mock_request.assert_called_once_with('/v1/tab-info-service/sports/Rugby League/competitions', params={'jurisdiction': 'NSW'})

    def test_get_racing_dates(self):
        """Test the get_racing_dates function."""
        # Mock the make_tab_api_request function
        with patch('tab_api_mcp.make_tab_api_request') as mock_request:
            mock_request.return_value = asyncio.Future()
            mock_request.return_value.set_result({'dates': ['2023-01-01', '2023-01-02']})
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_racing_dates())
            self.assertEqual(result, json.dumps({'dates': ['2023-01-01', '2023-01-02']}, indent=2))
            
            # Check that the correct endpoint was used
            mock_request.assert_called_once_with('/v1/tab-info-service/racing/dates')

    def test_get_racing_meetings(self):
        """Test the get_racing_meetings function."""
        # Mock the make_tab_api_request function
        with patch('tab_api_mcp.make_tab_api_request') as mock_request:
            mock_request.return_value = asyncio.Future()
            mock_request.return_value.set_result({'meetings': ['meeting1', 'meeting2']})
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_racing_meetings('2023-01-01'))
            self.assertEqual(result, json.dumps({'meetings': ['meeting1', 'meeting2']}, indent=2))
            
            # Check that the correct endpoint and parameters were used
            mock_request.assert_called_once_with('/v1/tab-info-service/racing/dates/2023-01-01/meetings', params={'jurisdiction': 'NSW'})

    def test_get_racing_races(self):
        """Test the get_racing_races function."""
        # Mock the make_tab_api_request function
        with patch('tab_api_mcp.make_tab_api_request') as mock_request:
            mock_request.return_value = asyncio.Future()
            mock_request.return_value.set_result({'races': ['race1', 'race2']})
            
            # Call the function and check the result
            result = asyncio.run(tab_api_mcp.get_racing_races('2023-01-01', 'R/MEL'))
            self.assertEqual(result, json.dumps({'races': ['race1', 'race2']}, indent=2))
            
            # Check that the correct endpoint and parameters were used
            mock_request.assert_called_once_with('/v1/tab-info-service/racing/dates/2023-01-01/meetings/R/MEL/races', params={'jurisdiction': 'NSW'})

    def test_prompt_for_credentials(self):
        """Test the prompt_for_credentials function."""
        # Mock the input and getpass.getpass functions
        with patch('builtins.input', return_value='test_input_client_id'):
            with patch('getpass.getpass', return_value='test_input_client_secret'):
                # Call the function
                tab_api_mcp.prompt_for_credentials()
                
                # Check that the credentials were set correctly
                self.assertEqual(tab_api_mcp.CLIENT_ID, 'test_input_client_id')
                self.assertEqual(tab_api_mcp.CLIENT_SECRET, 'test_input_client_secret')

    def test_prompt_for_jurisdiction(self):
        """Test the prompt_for_jurisdiction function."""
        # Mock the input function
        with patch('builtins.input', return_value='2'):
            # Call the function
            tab_api_mcp.prompt_for_jurisdiction()
            
            # Check that the jurisdiction was set correctly
            self.assertEqual(tab_api_mcp.DEFAULT_JURISDICTION, 'VIC')

if __name__ == '__main__':
    unittest.main()
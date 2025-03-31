import unittest
import sys
import os
import json
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

# Add the parent directory to the path so we can import the tab_api_mcp module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tab_api_mcp module
import tab_api_mcp

class TestTabApiMcp(unittest.IsolatedAsyncioTestCase): # Inherit from IsolatedAsyncioTestCase
    """Test cases for the TAB API MCP server."""

    def setUp(self):
        """Set up the test environment."""
        # Mock environment variables - these won't directly affect module globals after import
        self.env_patcher = patch.dict('os.environ', {
            'TAB_CLIENT_ID': 'env_client_id',
            'TAB_CLIENT_SECRET': 'env_client_secret'
        }, clear=True) # Clear existing env vars for isolation
        self.env_patcher.start()

        # Reset the access token cache before each test
        tab_api_mcp.access_token_cache = {
            "token": None,
            "expires_at": 0
        }

        # Explicitly set module globals for tests that need them pre-set
        tab_api_mcp.CLIENT_ID = "test_client_id"
        tab_api_mcp.CLIENT_SECRET = "test_client_secret"
        tab_api_mcp.DEFAULT_JURISDICTION = "NSW" # Reset default jurisdiction

    def tearDown(self):
        """Clean up the test environment."""
        self.env_patcher.stop()
        # Reset module globals to avoid side effects between tests
        tab_api_mcp.CLIENT_ID = ""
        tab_api_mcp.CLIENT_SECRET = ""
        tab_api_mcp.DEFAULT_JURISDICTION = "NSW"

    @patch('httpx.AsyncClient.post', new_callable=AsyncMock) # Use AsyncMock for async methods
    async def test_get_access_token(self, mock_post): # Make test async
        """Test the get_access_token function."""
        # Set up the mock response
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            'access_token': 'test_access_token',
            'expires_in': 3600
        }
        # Configure the AsyncMock to return the mock response when awaited
        mock_post.return_value = mock_response

        # Call the async function and check the result
        result = await tab_api_mcp.get_access_token() # Use await
        self.assertEqual(result, 'test_access_token')

        # Check that the token was cached
        self.assertEqual(tab_api_mcp.access_token_cache['token'], 'test_access_token')
        self.assertGreater(tab_api_mcp.access_token_cache['expires_at'], 0)

        # Check that httpx.AsyncClient.post was called correctly
        mock_post.assert_awaited_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs['data']['client_id'], 'test_client_id')
        self.assertEqual(kwargs['data']['client_secret'], 'test_client_secret')

    @patch('tab_api_mcp.get_access_token', new_callable=AsyncMock)
    @patch('httpx.AsyncClient.get', new_callable=AsyncMock)
    async def test_make_tab_api_request(self, mock_get, mock_get_token): # Make test async
        """Test the make_tab_api_request function."""
        mock_get_token.return_value = 'test_access_token' # Mock the token directly

        # Set up the mock response for httpx get
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {'data': 'test_data'}
        mock_get.return_value = mock_response

        # Call the async function and check the result
        result = await tab_api_mcp.make_tab_api_request('/test_endpoint') # Use await
        self.assertEqual(result, {'data': 'test_data'})

        # Check that the correct headers were used
        mock_get.assert_awaited_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test_access_token')

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_sports(self, mock_request): # Make test async
        """Test the get_sports function."""
        mock_request.return_value = {'sports': ['sport1', 'sport2']} # Mock the API response

        # Call the async function and check the result
        result = await tab_api_mcp.get_sports() # Use await
        self.assertEqual(result, json.dumps({'sports': ['sport1', 'sport2']}, indent=2))

        # Check that the correct endpoint and parameters were used
        mock_request.assert_awaited_once_with('/v1/tab-info-service/sports/', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_sport_competitions(self, mock_request): # Make test async
        """Test the get_sport_competitions function."""
        mock_request.return_value = {'competitions': ['comp1', 'comp2']}

        result = await tab_api_mcp.get_sport_competitions('Rugby League') # Use await
        self.assertEqual(result, json.dumps({'competitions': ['comp1', 'comp2']}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/sports/Rugby League/competitions', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_racing_dates(self, mock_request): # Make test async
        """Test the get_racing_dates function."""
        mock_request.return_value = {'dates': ['2023-01-01', '2023-01-02']}

        result = await tab_api_mcp.get_racing_dates() # Use await
        self.assertEqual(result, json.dumps({'dates': ['2023-01-01', '2023-01-02']}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/racing/dates')

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_racing_meetings(self, mock_request): # Make test async
        """Test the get_racing_meetings function."""
        mock_request.return_value = {'meetings': ['meeting1', 'meeting2']}

        result = await tab_api_mcp.get_racing_meetings('2023-01-01') # Use await
        self.assertEqual(result, json.dumps({'meetings': ['meeting1', 'meeting2']}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/racing/dates/2023-01-01/meetings', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_racing_races(self, mock_request): # Make test async
        """Test the get_racing_races function."""
        mock_request.return_value = {'races': ['race1', 'race2']}

        result = await tab_api_mcp.get_racing_races('2023-01-01', 'R/MEL') # Use await
        self.assertEqual(result, json.dumps({'races': ['race1', 'race2']}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/racing/dates/2023-01-01/meetings/R/MEL/races', params={'jurisdiction': 'NSW'})

    @patch('builtins.input', return_value='test_input_client_id')
    @patch('getpass.getpass', return_value='test_input_client_secret')
    def test_prompt_for_credentials(self, mock_getpass, mock_input): # This is synchronous
        """Test the prompt_for_credentials function when env vars are NOT set."""
        # Temporarily clear module globals to force prompt
        tab_api_mcp.CLIENT_ID = ""
        tab_api_mcp.CLIENT_SECRET = ""

        # Temporarily clear environment variables for this test
        with patch.dict('os.environ', {}, clear=True):
            # Call the function
            tab_api_mcp.prompt_for_credentials()

        # Check that the credentials were set correctly from input
        self.assertEqual(tab_api_mcp.CLIENT_ID, 'test_input_client_id')
        self.assertEqual(tab_api_mcp.CLIENT_SECRET, 'test_input_client_secret')
        mock_input.assert_called_once_with("Enter your TAB API Client ID: ")
        mock_getpass.assert_called_once_with("Enter your TAB API Client Secret: ")

    @patch('builtins.input', return_value='test_input_client_id')
    @patch('getpass.getpass', return_value='test_input_client_secret')
    def test_prompt_for_credentials_with_env(self, mock_getpass, mock_input): # This is synchronous
        """Test the prompt_for_credentials function when env vars ARE set."""
        # Set environment variables for this test
        with patch.dict('os.environ', {'TAB_CLIENT_ID': 'env_id', 'TAB_CLIENT_SECRET': 'env_secret'}, clear=True):
            # Call the function
            tab_api_mcp.prompt_for_credentials()

        # Check that the credentials were set correctly from environment
        self.assertEqual(tab_api_mcp.CLIENT_ID, 'env_id')
        self.assertEqual(tab_api_mcp.CLIENT_SECRET, 'env_secret')
        # Ensure input/getpass were NOT called
        mock_input.assert_not_called()
        mock_getpass.assert_not_called()

    @patch('builtins.input', return_value='2') # Mock input to select VIC
    def test_prompt_for_jurisdiction(self, mock_input): # This is synchronous
        """Test the prompt_for_jurisdiction function."""
        # Call the function
        tab_api_mcp.prompt_for_jurisdiction()

        # Check that the jurisdiction was set correctly
        self.assertEqual(tab_api_mcp.DEFAULT_JURISDICTION, 'VIC')
        # Check input was called correctly (might need more specific assertion depending on exact prompt)
        mock_input.assert_called()

if __name__ == '__main__':
    unittest.main()
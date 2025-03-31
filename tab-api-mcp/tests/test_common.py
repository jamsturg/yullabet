"""Tests for the common module."""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os
import json

# Add the parent directory to the path so we can import the tab_api_mcp module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the tab_api_mcp module
from tab_api_mcp.common import (
    get_access_token,
    make_tab_api_request,
    create_starlette_app,
)


class TestCommon(unittest.IsolatedAsyncioTestCase):
    """Test cases for the common module."""

    def setUp(self):
        """Set up the test environment."""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'TAB_CLIENT_ID': 'test_client_id',
            'TAB_CLIENT_SECRET': 'test_client_secret'
        }, clear=True)
        self.env_patcher.start()

        # Import the module after patching the environment
        import tab_api_mcp.common
        
        # Reset the access token cache
        tab_api_mcp.common.access_token_cache = {
            "token": None,
            "expires_at": 0
        }

        # Explicitly set module globals for tests
        tab_api_mcp.common.CLIENT_ID = "test_client_id"
        tab_api_mcp.common.CLIENT_SECRET = "test_client_secret"
        tab_api_mcp.common.DEFAULT_JURISDICTION = "NSW"

    def tearDown(self):
        """Clean up the test environment."""
        self.env_patcher.stop()
        
        # Reset module globals to avoid side effects between tests
        import tab_api_mcp.common
        tab_api_mcp.common.CLIENT_ID = ""
        tab_api_mcp.common.CLIENT_SECRET = ""
        tab_api_mcp.common.DEFAULT_JURISDICTION = "NSW"

    @patch('tab_api_mcp.common.httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_get_access_token(self, mock_post):
        """Test the get_access_token function."""
        # Mock the response from the TAB API
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        # Call the function
        token = await get_access_token()

        # Check the result
        self.assertEqual(token, "test_token")
        
        # Check that the token was cached
        import tab_api_mcp.common
        self.assertEqual(tab_api_mcp.common.access_token_cache["token"], "test_token")
        self.assertGreater(tab_api_mcp.common.access_token_cache["expires_at"], 0)

    @patch('tab_api_mcp.common.get_access_token', new_callable=AsyncMock)
    @patch('tab_api_mcp.common.httpx.AsyncClient.get', new_callable=AsyncMock)
    async def test_make_tab_api_request_get(self, mock_get, mock_get_token):
        """Test the make_tab_api_request function with GET method."""
        # Mock the response from the TAB API
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_get.return_value = mock_response
        
        # Mock the token
        mock_get_token.return_value = "test_token"

        # Call the function
        result = await make_tab_api_request("/test/endpoint", params={"param": "value"})

        # Check the result
        self.assertEqual(result, {"data": "test_data"})
        
        # Check that the correct URL and headers were used
        mock_get.assert_awaited_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")
        self.assertEqual(kwargs["params"], {"param": "value"})

    @patch('tab_api_mcp.common.get_access_token', new_callable=AsyncMock)
    @patch('tab_api_mcp.common.httpx.AsyncClient.post', new_callable=AsyncMock)
    async def test_make_tab_api_request_post(self, mock_post, mock_get_token):
        """Test the make_tab_api_request function with POST method."""
        # Mock the response from the TAB API
        mock_response = MagicMock()
        mock_response.raise_for_status = MagicMock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_post.return_value = mock_response
        
        # Mock the token
        mock_get_token.return_value = "test_token"

        # Call the function
        result = await make_tab_api_request("/test/endpoint", method="POST", data={"data": "value"})

        # Check the result
        self.assertEqual(result, {"data": "test_data"})
        
        # Check that the correct URL and headers were used
        mock_post.assert_awaited_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["headers"]["Authorization"], "Bearer test_token")
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/json")
        self.assertEqual(kwargs["json"], {"data": "value"})


if __name__ == '__main__':
    unittest.main()
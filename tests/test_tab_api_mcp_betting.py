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

class TestTabApiMcpBetting(unittest.IsolatedAsyncioTestCase):
    """Test cases for the TAB API MCP server betting functionality."""

    def setUp(self):
        """Set up the test environment."""
        # Mock environment variables
        self.env_patcher = patch.dict('os.environ', {
            'TAB_CLIENT_ID': 'test_client_id',
            'TAB_CLIENT_SECRET': 'test_client_secret'
        }, clear=True)
        self.env_patcher.start()

        # Reset the access token cache
        tab_api_mcp.access_token_cache = {
            "token": None,
            "expires_at": 0
        }

        # Explicitly set module globals for tests
        tab_api_mcp.CLIENT_ID = "test_client_id"
        tab_api_mcp.CLIENT_SECRET = "test_client_secret"
        tab_api_mcp.DEFAULT_JURISDICTION = "NSW"

    def tearDown(self):
        """Clean up the test environment."""
        self.env_patcher.stop()
        # Reset module globals to avoid side effects between tests
        tab_api_mcp.CLIENT_ID = ""
        tab_api_mcp.CLIENT_SECRET = ""
        tab_api_mcp.DEFAULT_JURISDICTION = "NSW"

    # Account Management Tests

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_account_details(self, mock_request):
        """Test the get_account_details function."""
        mock_request.return_value = {'accountId': '12345', 'name': 'Test User'}

        result = await tab_api_mcp.get_account_details()
        self.assertEqual(result, json.dumps({'accountId': '12345', 'name': 'Test User'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/account-service/accounts')

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_account_balance(self, mock_request):
        """Test the get_account_balance function."""
        mock_request.return_value = {'balance': 100.50, 'currency': 'AUD'}

        result = await tab_api_mcp.get_account_balance()
        self.assertEqual(result, json.dumps({'balance': 100.50, 'currency': 'AUD'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/account-service/accounts/balance')

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_transaction_history(self, mock_request):
        """Test the get_transaction_history function."""
        mock_request.return_value = {'transactions': [{'id': '1', 'amount': 50.0, 'type': 'DEPOSIT'}]}

        # Test with no parameters
        result = await tab_api_mcp.get_transaction_history()
        self.assertEqual(result, json.dumps({'transactions': [{'id': '1', 'amount': 50.0, 'type': 'DEPOSIT'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/account-service/accounts/transactions', params={})

        # Test with parameters
        mock_request.reset_mock()
        result = await tab_api_mcp.get_transaction_history('2023-01-01', '2023-01-31', 'DEPOSIT')
        self.assertEqual(result, json.dumps({'transactions': [{'id': '1', 'amount': 50.0, 'type': 'DEPOSIT'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/account-service/accounts/transactions', 
                                        params={'fromDate': '2023-01-01', 'toDate': '2023-01-31', 'transactionType': 'DEPOSIT'})

    # Betting Tests

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_place_bet(self, mock_request):
        """Test the place_bet function."""
        mock_request.return_value = {'betId': '12345', 'status': 'ACCEPTED'}

        selections = [{'eventId': 'event1', 'marketId': 'market1', 'selectionId': 'selection1'}]
        result = await tab_api_mcp.place_bet('WIN', selections, 10.0)
        self.assertEqual(result, json.dumps({'betId': '12345', 'status': 'ACCEPTED'}, indent=2))

        mock_request.assert_awaited_once_with(
            '/v1/tab-betting-service/bets', 
            method='POST', 
            data={
                'betType': 'WIN',
                'selections': selections,
                'stake': 10.0,
                'betOption': 'SINGLE'
            }
        )

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_bet_history(self, mock_request):
        """Test the get_bet_history function."""
        mock_request.return_value = {'bets': [{'id': '1', 'status': 'SETTLED'}]}

        # Test with no parameters
        result = await tab_api_mcp.get_bet_history()
        self.assertEqual(result, json.dumps({'bets': [{'id': '1', 'status': 'SETTLED'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/tab-betting-service/bets', params={})

        # Test with parameters
        mock_request.reset_mock()
        result = await tab_api_mcp.get_bet_history('2023-01-01', '2023-01-31', 'SETTLED')
        self.assertEqual(result, json.dumps({'bets': [{'id': '1', 'status': 'SETTLED'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/tab-betting-service/bets', 
                                        params={'fromDate': '2023-01-01', 'toDate': '2023-01-31', 'status': 'SETTLED'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_active_bets(self, mock_request):
        """Test the get_active_bets function."""
        mock_request.return_value = {'bets': [{'id': '1', 'status': 'PENDING'}]}

        result = await tab_api_mcp.get_active_bets()
        self.assertEqual(result, json.dumps({'bets': [{'id': '1', 'status': 'PENDING'}]}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-betting-service/bets/active')

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_cancel_bet(self, mock_request):
        """Test the cancel_bet function."""
        mock_request.return_value = {'status': 'CANCELLED'}

        result = await tab_api_mcp.cancel_bet('12345')
        self.assertEqual(result, json.dumps({'status': 'CANCELLED'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-betting-service/bets/12345/cancel', method='POST')

    # Markets and Odds Tests

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_markets(self, mock_request):
        """Test the get_markets function."""
        mock_request.return_value = {'markets': [{'id': 'market1', 'name': 'Win'}]}

        result = await tab_api_mcp.get_markets('event1')
        self.assertEqual(result, json.dumps({'markets': [{'id': 'market1', 'name': 'Win'}]}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/events/event1/markets', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_odds(self, mock_request):
        """Test the get_odds function."""
        mock_request.return_value = {'odds': [{'selectionId': 'selection1', 'price': 2.5}]}

        result = await tab_api_mcp.get_odds('market1')
        self.assertEqual(result, json.dumps({'odds': [{'selectionId': 'selection1', 'price': 2.5}]}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/markets/market1/odds', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_live_odds(self, mock_request):
        """Test the get_live_odds function."""
        mock_request.return_value = {'odds': [{'marketId': 'market1', 'selectionId': 'selection1', 'price': 2.5}]}

        result = await tab_api_mcp.get_live_odds('event1')
        self.assertEqual(result, json.dumps({'odds': [{'marketId': 'market1', 'selectionId': 'selection1', 'price': 2.5}]}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/events/event1/live-odds', params={'jurisdiction': 'NSW'})

    # Additional Sports and Racing Data Tests

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_event_details(self, mock_request):
        """Test the get_event_details function."""
        mock_request.return_value = {'id': 'event1', 'name': 'Test Event'}

        result = await tab_api_mcp.get_event_details('event1')
        self.assertEqual(result, json.dumps({'id': 'event1', 'name': 'Test Event'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/events/event1', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_race_details(self, mock_request):
        """Test the get_race_details function."""
        mock_request.return_value = {'id': 'race1', 'name': 'Test Race'}

        result = await tab_api_mcp.get_race_details('race1')
        self.assertEqual(result, json.dumps({'id': 'race1', 'name': 'Test Race'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/racing/races/race1', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_runner_details(self, mock_request):
        """Test the get_runner_details function."""
        mock_request.return_value = {'id': 'runner1', 'name': 'Test Runner'}

        result = await tab_api_mcp.get_runner_details('race1', 'runner1')
        self.assertEqual(result, json.dumps({'id': 'runner1', 'name': 'Test Runner'}, indent=2))

        mock_request.assert_awaited_once_with('/v1/tab-info-service/racing/races/race1/runners/runner1', params={'jurisdiction': 'NSW'})

    @patch('tab_api_mcp.make_tab_api_request', new_callable=AsyncMock)
    async def test_get_sport_events(self, mock_request):
        """Test the get_sport_events function."""
        mock_request.return_value = {'events': [{'id': 'event1', 'name': 'Test Event'}]}

        # Test without competition_id
        result = await tab_api_mcp.get_sport_events('Rugby League')
        self.assertEqual(result, json.dumps({'events': [{'id': 'event1', 'name': 'Test Event'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/tab-info-service/sports/Rugby League/events', params={'jurisdiction': 'NSW'})

        # Test with competition_id
        mock_request.reset_mock()
        result = await tab_api_mcp.get_sport_events('Rugby League', 'comp1')
        self.assertEqual(result, json.dumps({'events': [{'id': 'event1', 'name': 'Test Event'}]}, indent=2))
        mock_request.assert_awaited_with('/v1/tab-info-service/sports/Rugby League/competitions/comp1/events', params={'jurisdiction': 'NSW'})

if __name__ == '__main__':
    unittest.main()
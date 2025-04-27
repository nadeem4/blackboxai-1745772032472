import unittest
from unittest.mock import patch, MagicMock
from fivetran_client import FiveTranClient

class TestFiveTranClient(unittest.TestCase):
    @patch('fivetran_client.requests.get')
    def test_list_connectors_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'data': []}
        mock_get.return_value = mock_response

        client = FiveTranClient()
        result = client.list_connectors()
        self.assertEqual(result, {'data': []})

    @patch('fivetran_client.requests.post')
    def test_trigger_sync_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'sync': 'started'}
        mock_post.return_value = mock_response

        client = FiveTranClient()
        result = client.trigger_sync('connector_id')
        self.assertEqual(result, {'sync': 'started'})

if __name__ == '__main__':
    unittest.main()

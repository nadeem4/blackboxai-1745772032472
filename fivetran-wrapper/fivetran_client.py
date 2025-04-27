import os
import requests
from logger import logger

class FiveTranClient:
    def __init__(self):
        self.api_key = os.getenv('FIVETRAN_API_KEY')
        self.api_secret = os.getenv('FIVETRAN_API_SECRET')
        self.base_url = "https://api.fivetran.com/v1"
        if not self.api_key or not self.api_secret:
            raise ValueError("FIVETRAN_API_KEY and FIVETRAN_API_SECRET must be set in environment variables")

    def _get_headers(self):
        return {
            "Authorization": f"Basic {self._encode_credentials()}",
            "Content-Type": "application/json"
        }

    def _encode_credentials(self):
        import base64
        credentials = f"{self.api_key}:{self.api_secret}"
        return base64.b64encode(credentials.encode()).decode()

    def list_connectors(self):
        url = f"{self.base_url}/connectors"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to list connectors: {response.text}")
            response.raise_for_status()
        return response.json()

    def get_connector_schema(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}/schemas"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to get connector schema: {response.text}")
            response.raise_for_status()
        return response.json()

    def extract_data(self, connector_id):
        logger.info(f"Extracting data for connector {connector_id}")
        return self.get_connector_schema(connector_id)

    def trigger_sync(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}/force"
        response = requests.post(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to trigger sync for connector {connector_id}: {response.text}")
            response.raise_for_status()
        return response.json()

    def get_sync_status(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}/sync"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to get sync status for connector {connector_id}: {response.text}")
            response.raise_for_status()
        return response.json().get('data', {}).get('status', {})

    def create_connector(self, connector_config):
        url = f"{self.base_url}/connectors"
        response = requests.post(url, json=connector_config, headers=self._get_headers())
        if response.status_code != 201:
            logger.error(f"Failed to create connector: {response.text}")
            response.raise_for_status()
        return response.json()

    def delete_connector(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}"
        response = requests.delete(url, headers=self._get_headers())
        if response.status_code != 204:
            logger.error(f"Failed to delete connector {connector_id}: {response.text}")
            response.raise_for_status()
        return True

    def pause_connector(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}/pause"
        response = requests.post(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to pause connector {connector_id}: {response.text}")
            response.raise_for_status()
        return response.json()

    def resume_connector(self, connector_id):
        url = f"{self.base_url}/connectors/{connector_id}/resume"
        response = requests.post(url, headers=self._get_headers())
        if response.status_code != 200:
            logger.error(f"Failed to resume connector {connector_id}: {response.text}")
            response.raise_for_status()
        return response.json()

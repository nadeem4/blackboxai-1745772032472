import time
from logger import logger

class ConnectorManager:
    def __init__(self, fivetran_client):
        self.fivetran_client = fivetran_client

    def initialize_connector(self, connector_id):
        logger.info(f"Initializing connector {connector_id}")

    def trigger_sync(self, connector_id):
        logger.info(f"Triggering sync for connector {connector_id}")
        try:
            response = self.fivetran_client.trigger_sync(connector_id)
            return response
        except Exception as e:
            logger.error(f"Error triggering sync for connector {connector_id}: {e}")
            raise

    def check_sync_status(self, connector_id):
        logger.info(f"Checking sync status for connector {connector_id}")
        try:
            status = self.fivetran_client.get_sync_status(connector_id)
            return status
        except Exception as e:
            logger.error(f"Error checking sync status for connector {connector_id}: {e}")
            raise

    def extract_all_connectors(self):
        connectors_data = {}
        connectors = self.fivetran_client.list_connectors()
        for connector in connectors.get('data', []):
            connector_id = connector.get('id')
            connector_name = connector.get('name')
            try:
                self.initialize_connector(connector_id)
                self.trigger_sync(connector_id)
                for _ in range(10):
                    status = self.check_sync_status(connector_id)
                    if status.get('status') == 'success':
                        break
                    elif status.get('status') == 'failed':
                        raise Exception(f"Sync failed for connector {connector_name}")
                    time.sleep(10)
                data = self.fivetran_client.extract_data(connector_id)
                connectors_data[connector_name] = data
            except Exception as e:
                logger.error(f"Failed to extract data for connector {connector_name}: {e}")
        return connectors_data

    def create_connector(self, connector_config):
        try:
            response = self.fivetran_client.create_connector(connector_config)
            logging.info(f"Connector created: {response}")
            return response
        except Exception as e:
            logging.error(f"Failed to create connector: {e}")
            raise

    def delete_connector(self, connector_id):
        try:
            result = self.fivetran_client.delete_connector(connector_id)
            logging.info(f"Connector deleted: {connector_id}")
            return result
        except Exception as e:
            logging.error(f"Failed to delete connector {connector_id}: {e}")
            raise

    def pause_connector(self, connector_id):
        try:
            response = self.fivetran_client.pause_connector(connector_id)
            logging.info(f"Connector paused: {connector_id}")
            return response
        except Exception as e:
            logging.error(f"Failed to pause connector {connector_id}: {e}")
            raise

    def resume_connector(self, connector_id):
        try:
            response = self.fivetran_client.resume_connector(connector_id)
            logging.info(f"Connector resumed: {connector_id}")
            return response
        except Exception as e:
            logging.error(f"Failed to resume connector {connector_id}: {e}")
            raise

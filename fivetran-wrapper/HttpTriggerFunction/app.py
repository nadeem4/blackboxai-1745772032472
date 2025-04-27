import logging
import azure.functions as func
from fivetran_client import FiveTranClient
from connector_manager import ConnectorManager
import json

app = func.FunctionApp()

fivetran_client = FiveTranClient()
connector_manager = ConnectorManager(fivetran_client)

@app.function_name(name="ExtractData")
@app.route(route="extract", methods=["GET"])
def extract(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Extract data request received.')
    try:
        data = connector_manager.extract_all_connectors()
        return func.HttpResponse(json.dumps(data), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error during data extraction: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.function_name(name="CreateConnector")
@app.route(route="connector/create", methods=["POST"])
def create_connector(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Create connector request received.')
    try:
        connector_config = req.get_json()
        response = connector_manager.create_connector(connector_config)
        return func.HttpResponse(json.dumps(response), status_code=201, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error creating connector: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.function_name(name="DeleteConnector")
@app.route(route="connector/delete/{connector_id}", methods=["DELETE"])
def delete_connector(req: func.HttpRequest) -> func.HttpResponse:
    connector_id = req.route_params.get('connector_id')
    logging.info(f'Delete connector request received for {connector_id}.')
    try:
        connector_manager.delete_connector(connector_id)
        return func.HttpResponse(f"Connector {connector_id} deleted.", status_code=200)
    except Exception as e:
        logging.error(f"Error deleting connector {connector_id}: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.function_name(name="PauseConnector")
@app.route(route="connector/pause/{connector_id}", methods=["POST"])
def pause_connector(req: func.HttpRequest) -> func.HttpResponse:
    connector_id = req.route_params.get('connector_id')
    logging.info(f'Pause connector request received for {connector_id}.')
    try:
        response = connector_manager.pause_connector(connector_id)
        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error pausing connector {connector_id}: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

@app.function_name(name="ResumeConnector")
@app.route(route="connector/resume/{connector_id}", methods=["POST"])
def resume_connector(req: func.HttpRequest) -> func.HttpResponse:
    connector_id = req.route_params.get('connector_id')
    logging.info(f'Resume connector request received for {connector_id}.')
    try:
        response = connector_manager.resume_connector(connector_id)
        return func.HttpResponse(json.dumps(response), status_code=200, mimetype="application/json")
    except Exception as e:
        logging.error(f"Error resuming connector {connector_id}: {e}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

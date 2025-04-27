# FiveTran Wrapper Azure Function

This project is an Azure Function app that provides a wrapper around FiveTran API to manage data extraction from all available data source connectors. It includes full lifecycle management of connectors, logging, monitoring, and deployment support.

## Features

- Extract data from all FiveTran connectors
- Create, delete, pause, resume connectors
- Lifecycle management with sync triggering and status polling
- Logging and monitoring with Application Insights
- Configuration management interface
- Docker support for containerized deployment
- Azure DevOps pipeline for CI/CD

## Setup

1. Clone the repository
2. Set environment variables in `local.settings.json` or Azure Function App settings:
   - `FIVETRAN_API_KEY`
   - `FIVETRAN_API_SECRET`
   - `APPINSIGHTS_INSTRUMENTATIONKEY`
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run locally using Azure Functions Core Tools:
   ```
   func start
   ```

## Deployment

- Build and push Docker image using the provided `Dockerfile`
- Deploy using Kubernetes YAML or Azure DevOps pipeline

## Testing

Run unit tests with:
```
python -m unittest discover tests
```

## Usage

The Azure Function exposes the following HTTP endpoints:

- `GET /api/extract` - Extract data from all connectors
- `POST /api/connector/create` - Create a new connector (JSON body)
- `DELETE /api/connector/delete/{connector_id}` - Delete a connector
- `POST /api/connector/pause/{connector_id}` - Pause a connector
- `POST /api/connector/resume/{connector_id}` - Resume a connector

## Logging and Monitoring

Uses Application Insights for logging and monitoring with support for custom properties.

## Configuration

Use the `config_manager.py` module to manage connector configuration files efficiently.

## License

MIT License

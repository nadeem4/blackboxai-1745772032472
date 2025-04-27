import logging
import os
from applicationinsights import TelemetryClient

class AppInsightsLogger:
    def __init__(self):
        self.instrumentation_key = os.getenv('APPINSIGHTS_INSTRUMENTATIONKEY')
        self.tc = None
        if self.instrumentation_key:
            self.tc = TelemetryClient(self.instrumentation_key)
        self.logger = logging.getLogger('fivetran-wrapper')
        self.logger.setLevel(logging.INFO)
        if not self.logger.hasHandlers():
            ch = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def info(self, message, **kwargs):
        self.logger.info(message)
        if self.tc:
            self.tc.track_trace(message, properties=kwargs)
            self.tc.flush()

    def error(self, message, **kwargs):
        self.logger.error(message)
        if self.tc:
            self.tc.track_exception(exception=Exception(message), properties=kwargs)
            self.tc.flush()

logger = AppInsightsLogger()

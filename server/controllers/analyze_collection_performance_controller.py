

import logging
from server.services.analyze_collection_performance_service import AnalyzeCollectionPerformanceService

class AnalyzeCollectionPerformanceController:
    def __init__(self):
        self.service = AnalyzeCollectionPerformanceService()

    def analyze_collection_performance(self, collection_id, action, params):
        try:
            if action == 'ANALYZE_PERFORMANCE':
                self.service.analyze_performance(collection_id, params)
            elif action == 'GENERATE_ACQUISITION_RECOMMENDATIONS':
                self.service.generate_acquisition_recommendations(collection_id, params)
            elif action == 'REBALANCE_COLLECTION':
                self.service.rebalance_collection(collection_id, params)
            self.log_analysis_completion(collection_id, action)
        except Exception as e:
            logging.error(f"Error analyzing collection performance: {str(e)}")

    def log_analysis_completion(self, collection_id, action):
        logging.info(f"Analysis completion for collection {collection_id} with action {action}")
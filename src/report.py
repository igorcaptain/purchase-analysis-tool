import os
from datetime import datetime
from analysis import SalesAnalyzer
from classification import CustomerSegmentation
from recommendation import RecommendationEngine
from utils import print_formatted_analysis_results, print_formatted_classification_results, print_formatted_recommendation_results

FILE_PATH = 'test_data/purchase_data_50k.csv'
CUSTOMER = 'C063'

os.makedirs('output', exist_ok=True)
report_name = f"output/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
with open(report_name, 'w') as file:
    analyzer = SalesAnalyzer(FILE_PATH)
    analysis_result = analyzer.get_full_analysis()
    print_formatted_analysis_results(analysis_result, 'full', file)

    segmentation = CustomerSegmentation(FILE_PATH, high_percentile=0.80, medium_percentile=0.60, recency_std_multiplier=1.5)
    segmentation_result = segmentation.perform_clustering()
    print_formatted_classification_results(segmentation_result, False, file)

    engine = RecommendationEngine(FILE_PATH)
    recommendations_result = engine.get_recommendations(CUSTOMER)
    print_formatted_recommendation_results(recommendations_result, file)
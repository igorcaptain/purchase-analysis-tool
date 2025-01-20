import argparse
import json
from analysis import SalesAnalyzer
from classification import CustomerSegmentation
from recommendation import RecommendationEngine
from utils import print_formatted_analysis_results, print_formatted_classification_results, print_formatted_recommendation_results

def analyze_command(args):
    """Handle analysis commands"""
    analyzer = SalesAnalyzer(args.data)
    
    if args.type == 'products':
        result = analyzer.get_top_products(args.limit)
    elif args.type == 'categories':
        result = analyzer.get_category_analysis()
    elif args.type == 'customers':
        result = analyzer.get_customer_analysis(args.limit)
    else:  # full analysis
        result = analyzer.get_full_analysis(args.limit, args.limit)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_formatted_analysis_results(result, args.type)

def classify_command(args):
    """Handle classification commands"""
    segmentation = CustomerSegmentation(
        args.data,
        args.clusters,
        args.high_percentile,
        args.medium_percentile,
        args.recency_multiplier
    )
    
    if args.customer:
        result = segmentation.get_customer_segment(args.customer)
        if result is None:
            print(f"Customer {args.customer} not found")
            return
    else:
        result = segmentation.perform_clustering()
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_formatted_classification_results(result, is_customer_specific=bool(args.customer))

def recommend_command(args):
    """Handle recommendation commands"""
    engine = RecommendationEngine(data_path=args.data)
    result = engine.get_recommendations(args.customer, args.num)
    
    if result['error']:
        print(result['error'])
        return
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_formatted_recommendation_results(result)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Sales Data Tools')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Analysis parser
    analyze_parser = subparsers.add_parser('analyze', help='Analyze sales data')
    analyze_parser.add_argument('--data', type=str, default='purchase_data.csv',
                              help='Path to data file')
    analyze_parser.add_argument('--type', type=str, 
                              choices=['products', 'categories', 'customers', 'full'],
                              default='full', help='Type of analysis to perform')
    analyze_parser.add_argument('--limit', type=int, default=5,
                              help='Limit for top products/customers')
    analyze_parser.add_argument('--json', action='store_true',
                              help='Output in JSON format')
    
    classify_parser = subparsers.add_parser('classify', help='Classify products')
    classify_parser.add_argument('--data', type=str, default='purchase_data.csv',
                       help='Path to data file')
    classify_parser.add_argument('--clusters', type=int, default=5,
                       help='Number of clusters')
    classify_parser.add_argument('--customer', type=str,
                       help='Get segment for specific customer ID')
    classify_parser.add_argument('--high-percentile', type=float, default=0.75,
                       help='Percentile for high-value thresholds')
    classify_parser.add_argument('--medium-percentile', type=float, default=0.50,
                       help='Percentile for medium-value thresholds')
    classify_parser.add_argument('--recency-multiplier', type=float, default=1.0,
                       help='Multiplier for recency threshold calculation')
    classify_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    recommend_parser = subparsers.add_parser('recommend', help='Get product recommendations')
    recommend_parser.add_argument('--data', type=str, default='purchase_data.csv', help='Path to data file')
    recommend_parser.add_argument('--customer', type=str, help='Customer ID')
    recommend_parser.add_argument('--num', type=int, default=5, help='Number of recommendations')
    recommend_parser.add_argument('--json', action='store_true', help='Output in JSON format')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        analyze_command(args)
    elif args.command == 'classify':
        classify_command(args)
    elif args.command == 'recommend':
        recommend_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
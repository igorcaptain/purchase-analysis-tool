from typing import Any, Dict

def _write_line(text: str, file_handler=None):
    if file_handler:
        file_handler.write(text + '\n')
    else:
        print(text)

def print_formatted_analysis_results(result: Dict[str, Any], analysis_type: str, file_handler=None):
    """Helper function to print formatted results"""
    _write_line("\n======================", file_handler)
    _write_line("\n|| Analysis Results ||", file_handler)
    _write_line("\n======================", file_handler)
    if analysis_type == 'products':
        _write_line("\n\t- Top Selling Products -", file_handler)
        for product in result.get('top_products', []):
            _write_line(f"Product {product['Product ID']}: "
                  f"${product['sum']:.2f} ({product['count']} sales)", file_handler)
    
    elif analysis_type == 'categories':
        _write_line("\n\t- Top Selling Categories -", file_handler)
        for category in result.get('category_sales', []):
            _write_line(f"{category['Product Category']}: "
                  f"${category['sum']:.2f} ({category['count']} sales)", file_handler)
    
    elif analysis_type == 'customers':
        _write_line("\n\t- Customer Spending Analysis -", file_handler)
        stats = result.get('summary_stats', {})
        _write_line(f"Average Spending per Customer:", file_handler)
        _write_line(f"Mean: ${stats.get('mean_spending', 0):.2f}", file_handler)
        _write_line(f"Median: ${stats.get('median_spending', 0):.2f}", file_handler)
        _write_line("\nTop Customers by Total Spend:", file_handler)
        for customer in result.get('top_customers', []):
            _write_line(f"Customer {customer['Customer ID']}: "
                  f"${customer['sum']:.2f} ({customer['count']} purchases)", file_handler)
    
    elif analysis_type == 'full':
        # Handle full analysis results
        _write_line("\n\t- Top Selling Products -", file_handler)
        for product in result.get('products_analysis', {}).get('top_products', []):
            _write_line(f"Product {product['Product ID']}: "
                  f"${product['sum']:.2f} ({product['count']} sales)", file_handler)
        
        _write_line("\n\t- Top Selling Categories -", file_handler)
        for category in result.get('category_analysis', {}).get('category_sales', []):
            _write_line(f"{category['Product Category']}: "
                  f"${category['sum']:.2f} ({category['count']} sales)", file_handler)
        
        _write_line("\n\t- Customer Spending Analysis -", file_handler)
        stats = result.get('customer_analysis', {}).get('summary_stats', {})
        _write_line(f"Average Spending per Customer:", file_handler)
        _write_line(f"Mean: ${stats.get('mean_spending', 0):.2f}", file_handler)
        _write_line(f"Median: ${stats.get('median_spending', 0):.2f}", file_handler)
        _write_line("\n\t- Top Customers by Total Spend -", file_handler)
        for customer in result.get('customer_analysis', {}).get('top_customers', []):
            _write_line(f"Customer {customer['Customer ID']}: "
                  f"${customer['sum']:.2f} ({customer['count']} purchases)", file_handler)

def print_formatted_classification_results(result: Dict[str, Any], is_customer_specific: bool, file_handler=None):
    """Helper function to print formatted results"""
    _write_line("\n============================", file_handler)
    _write_line("\n|| Classification Results ||", file_handler)
    _write_line("\n============================", file_handler)
    if is_customer_specific:
        _write_line(f"\n\t- Customer Segment Analysis for {result['customer_id']} -", file_handler)
        _write_line(f"Segment: {result['segment']}", file_handler)
        _write_line(f"Total Spending: ${result['total_spending']:.2f}", file_handler)
        _write_line(f"Purchase Frequency: {result['purchase_frequency']}", file_handler)
        _write_line(f"Average Order Value: ${result['average_order_value']:.2f}", file_handler)
        _write_line(f"Days Since Last Purchase: {result['days_since_last_purchase']}", file_handler)
        _write_line("\n\t- Segmentation Thresholds -", file_handler)
        _write_line(f"High Spending: ${result['thresholds']['spending']['high']:.2f}", file_handler)
        _write_line(f"Medium Spending: ${result['thresholds']['spending']['medium']:.2f}", file_handler)
        _write_line(f"High Frequency: {result['thresholds']['frequency']['high']:.1f}", file_handler)
        _write_line(f"Medium Frequency: {result['thresholds']['frequency']['medium']:.1f}", file_handler)
        _write_line(f"Recency Threshold: {result['thresholds']['recency']:.1f} days", file_handler)
    else:
        _write_line("\n\t- Customer Segmentation Analysis -", file_handler)
        _write_line(f"Total Customers: {result['summary']['total_customers']}", file_handler)
        _write_line(f"Number of Segments: {result['summary']['number_of_segments']}", file_handler)
        
        _write_line("\n\t- Segmentation Thresholds -", file_handler)
        thresholds = result['summary']['thresholds']
        _write_line(f"High Spending: ${thresholds['spending']['high']:.2f}", file_handler)
        _write_line(f"Medium Spending: ${thresholds['spending']['medium']:.2f}", file_handler)
        _write_line(f"High Frequency: {thresholds['frequency']['high']:.1f}", file_handler)
        _write_line(f"Medium Frequency: {thresholds['frequency']['medium']:.1f}", file_handler)
        _write_line(f"Recency Threshold: {thresholds['recency']:.1f} days", file_handler)
        
        _write_line("\n\t- Segment Details -", file_handler)
        for segment in result['segments']:
            _write_line(f"{segment['segment_name']}", file_handler)
            _write_line(f"\tCustomer Count: {segment['customer_count']}", file_handler)
            _write_line(f"\tAverage Spending: ${segment['avg_spending']:.2f}", file_handler)
            _write_line(f"\tAverage Purchase Frequency: {segment['avg_frequency']:.1f}", file_handler)
            _write_line(f"\tAverage Order Value: ${segment['avg_order_value']:.2f}", file_handler)
            _write_line(f"\tAverage Days Since Purchase: {segment['avg_days_since_purchase']:.1f}\n", file_handler)   

def print_formatted_recommendation_results(result: Dict[str, Any], file_handler=None):
    """Helper function to print formatted results"""
    _write_line("\n============================", file_handler)
    _write_line("\n|| Recommendation Results ||", file_handler)
    _write_line("\n============================", file_handler)
    _write_line(f"\nTop {len(result['recommendations'])} Recommended Products for Customer {result['customer_id']}:", file_handler)
    for i, rec in enumerate(result['recommendations'], 1):
        _write_line(f"{i}. Product {rec['product_id']} ({rec['category']}) - Predicted Rating: {rec['predicted_rating']:.2f}", file_handler)
import pandas as pd
from typing import Dict, Any

class SalesAnalyzer:
    def __init__(self, data_path: str):
        """Initialize the sales analyzer with data path
        
        Args:
            data_path (str): Path to the CSV file containing sales data
            
        Attributes:
            data_path (str): Stored path to the data file
            df (pd.DataFrame): DataFrame to store the sales data
        """
        self.data_path = data_path
        self.df = None
        self._load_data()
    
    def _load_data(self):
        """Load the sales dataset from CSV file into pandas DataFrame
        
        Reads the CSV file specified in self.data_path and stores it in self.df
        Private method called during initialization
        """
        self.df = pd.read_csv(self.data_path)
    
    def get_top_products(self, limit: int = 5) -> Dict[str, Any]:
        """Analyze and return top-selling products based on total sales amount
        
        Args:
            limit (int, optional): Number of top products to return. Defaults to 5
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - top_products: List of dictionaries with product details including:
                    * Product ID
                    * sum (total sales amount)
                    * count (number of sales)
                - total_products: Total number of unique products in dataset
        """
        product_sales = (self.df.groupby('Product ID')['Purchase Amount']
                        .agg(['sum', 'count'])
                        .sort_values('sum', ascending=False))
        
        top_products = product_sales.head(limit).reset_index()
        return {
            'top_products': top_products.to_dict(orient='records'),
            'total_products': len(product_sales)
        }
    
    def get_category_analysis(self) -> Dict[str, Any]:
        """Analyze sales performance by product category
        
        Aggregates sales data by product category to show total sales and 
        number of transactions per category
        
        Returns:
            Dict[str, Any]: Dictionary containing:
                - category_sales: List of dictionaries with category details including:
                    * Product Category
                    * sum (total sales amount)
                    * count (number of sales)
                - total_categories: Total number of unique categories
        """
        category_sales = (self.df.groupby('Product Category')['Purchase Amount']
                         .agg(['sum', 'count'])
                         .sort_values('sum', ascending=False))
        
        return {
            'category_sales': category_sales.reset_index().to_dict(orient='records'),
            'total_categories': len(category_sales)
        }
    
    def get_customer_analysis(self, top_n: int = 5) -> Dict[str, Any]:
        """Analyze customer spending patterns and identify top customers
        
        Calculates various spending metrics per customer and returns summary statistics
        along with details of top spenders
        
        Args:
            top_n (int, optional): Number of top customers to return. Defaults to 5
            
        Returns:
            Dict[str, Any]: Dictionary containing:
                - summary_stats: Dictionary with overall customer metrics:
                    * mean_spending: Average spending per customer
                    * median_spending: Median spending per customer
                    * total_customers: Total number of unique customers
                - top_customers: List of dictionaries with top customer details:
                    * Customer ID
                    * sum (total spending)
                    * count (number of purchases)
                    * mean (average purchase amount)
        """
        customer_spending = (self.df.groupby('Customer ID')['Purchase Amount']
                           .agg(['sum', 'count', 'mean'])
                           .sort_values('sum', ascending=False))
        
        return {
            'summary_stats': {
                'mean_spending': float(customer_spending['mean'].mean()),
                'median_spending': float(customer_spending['mean'].median()),
                'total_customers': len(customer_spending)
            },
            'top_customers': customer_spending.head(top_n).reset_index().to_dict(orient='records')
        }
    
    def get_full_analysis(self, top_products: int = 5, top_customers: int = 5) -> Dict[str, Any]:
        """Generate a comprehensive analysis report combining all available metrics
        
        Combines results from top products analysis, category analysis, and
        customer analysis into a single report
        
        Args:
            top_products (int, optional): Number of top products to include. Defaults to 5
            top_customers (int, optional): Number of top customers to include. Defaults to 5
            
        Returns:
            Dict[str, Any]: Dictionary containing combined results from:
                - products_analysis: Results from get_top_products()
                - category_analysis: Results from get_category_analysis()
                - customer_analysis: Results from get_customer_analysis()
        """
        return {
            'products_analysis': self.get_top_products(top_products),
            'category_analysis': self.get_category_analysis(),
            'customer_analysis': self.get_customer_analysis(top_customers)
        }

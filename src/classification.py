import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime
from typing import Dict, Any, Optional

class CustomerSegmentation:
    def __init__(self, data_path: str = 'purchase_data.csv', n_clusters: int = 5,
                 high_percentile: float = 0.75, medium_percentile: float = 0.50,
                 recency_std_multiplier: float = 1.0):
        """Initialize the customer segmentation engine with customizable thresholds.
        
        Args:
            data_path (str): Path to the CSV file containing purchase data
            n_clusters (int): Number of clusters for KMeans clustering
            high_percentile (float): Percentile threshold for high-value metrics (0.0-1.0)
            medium_percentile (float): Percentile threshold for medium-value metrics (0.0-1.0)
            recency_std_multiplier (float): Multiplier for recency threshold calculation
        """
        self.data_path = data_path
        self.n_clusters = n_clusters
        self.high_percentile = high_percentile
        self.medium_percentile = medium_percentile
        self.recency_std_multiplier = recency_std_multiplier
        self.df = None
        self.features = None
        self.scaler = StandardScaler()
        self._load_and_process_data()
    
    def _load_and_process_data(self):
        """Load and preprocess the purchase data from CSV file.
        
        Reads the CSV file, converts purchase dates to datetime format,
        and initializes feature preparation through _prepare_features().
        """
        self.df = pd.read_csv(self.data_path)
        self.df['Purchase Date'] = pd.to_datetime(self.df['Purchase Date'])
        self._prepare_features()
    
    def _prepare_features(self):
        """Prepare and calculate customer features for segmentation analysis.
        
        Calculates key metrics including:
        - Total spending per customer
        - Purchase frequency
        - Average purchase amount
        - Days since last purchase
        - Category preferences (as percentage of total spending)
        
        Creates a feature matrix combining all metrics for clustering.
        """
        current_date = datetime.now()
        
        # Calculate basic metrics
        self.df['Total Spending'] = self.df.groupby('Customer ID')['Purchase Amount'].transform('sum')
        self.df['Purchase Frequency'] = self.df.groupby('Customer ID')['Purchase Date'].transform('count')
        self.df['Average Purchase Amount'] = self.df['Total Spending'] / self.df['Purchase Frequency']
        self.df['Days Since Last Purchase'] = (
            current_date - self.df.groupby('Customer ID')['Purchase Date'].transform('max')
        ).dt.days
        
        # Create category preferences
        category_pivot = pd.pivot_table(
            self.df, 
            values='Purchase Amount',
            index='Customer ID',
            columns='Product Category',
            aggfunc='sum',
            fill_value=0
        )
        category_pivot = category_pivot.div(category_pivot.sum(axis=1), axis=0)
        
        # Combine all features
        self.features = self.df.groupby('Customer ID').agg({
            'Total Spending': 'first',
            'Purchase Frequency': 'first',
            'Average Purchase Amount': 'first',
            'Days Since Last Purchase': 'first'
        }).join(category_pivot)
    
    def _calculate_thresholds(self) -> Dict[str, float]:
        """Calculate dynamic thresholds for customer segmentation.
        
        Returns:
            Dict containing thresholds for:
            - spending: Dict with 'high' and 'medium' spending thresholds
            - frequency: Dict with 'high' and 'medium' purchase frequency thresholds
            - recency: Single threshold for days since last purchase
            
        Thresholds are calculated based on percentiles and standard deviations
        of the actual data distribution.
        """
        # Calculate percentiles for different metrics
        spending_thresholds = {
            'high': self.features['Total Spending'].quantile(self.high_percentile),
            'medium': self.features['Total Spending'].quantile(self.medium_percentile)
        }
        
        frequency_thresholds = {
            'high': self.features['Purchase Frequency'].quantile(self.high_percentile),
            'medium': self.features['Purchase Frequency'].quantile(self.medium_percentile)
        }
        
        # Calculate recency threshold (days since purchase)
        recency_mean = self.features['Days Since Last Purchase'].mean()
        recency_std = self.features['Days Since Last Purchase'].std()
        recency_threshold = recency_mean + (recency_std * self.recency_std_multiplier)
        
        return {
            'spending': spending_thresholds,
            'frequency': frequency_thresholds,
            'recency': recency_threshold
        }

    def _label_segment(self, row: pd.Series) -> str:
        """Assign a descriptive segment label to a customer based on their metrics.
        
        Args:
            row (pd.Series): Customer data row containing spending, frequency, and recency metrics
            
        Returns:
            str: Segment label from one of:
                - "Inactive Customers"
                - "High-Value Frequent Buyers"
                - "Big Spenders"
                - "Frequent Low-Value Buyers"
                - "Regular Customers"
                - "Occasional Buyers"
                
        Labels are assigned based on comparison with dynamic thresholds calculated
        from the data distribution.
        """
        if not hasattr(self, '_thresholds'):
            self._thresholds = self._calculate_thresholds()
        
        # Get thresholds
        spending_high = self._thresholds['spending']['high']
        spending_medium = self._thresholds['spending']['medium']
        frequency_high = self._thresholds['frequency']['high']
        frequency_medium = self._thresholds['frequency']['medium']
        recency_threshold = self._thresholds['recency']
        
        # Determine segment
        if row['Days Since Last Purchase'] > recency_threshold:
            return "Inactive Customers"
        elif row['Total Spending'] > spending_high and row['Purchase Frequency'] > frequency_high:
            return "High-Value Frequent Buyers"
        elif row['Total Spending'] > spending_high:
            return "Big Spenders"
        elif row['Purchase Frequency'] > frequency_high:
            return "Frequent Low-Value Buyers"
        elif (row['Total Spending'] > spending_medium and 
              row['Purchase Frequency'] > frequency_medium):
            return "Regular Customers"
        else:
            return "Occasional Buyers"
    
    def perform_clustering(self) -> Dict[str, Any]:
        """Perform customer segmentation using KMeans clustering.
        
        Process:
        1. Scales features using StandardScaler
        2. Applies KMeans clustering
        3. Assigns descriptive segment labels
        
        Returns:
            Dict containing detailed segmentation results including:
            - Summary statistics
            - Segment-wise metrics
            - Threshold values
        """
        # Scale features
        features_scaled = self.scaler.fit_transform(self.features)
        
        # Perform clustering
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)
        self.features['Cluster'] = kmeans.fit_predict(features_scaled)
        
        # Apply segment labels
        self.features['Segment'] = self.features.apply(self._label_segment, axis=1)
        
        return self.get_segmentation_results()
    
    def get_segmentation_results(self) -> Dict[str, Any]:
        """Generate detailed results and statistics for all customer segments.
        
        Returns:
            Dict containing:
            - summary: Overall statistics including total customers, segment count,
                      analysis date, and threshold values
            - segments: List of segment-wise statistics including customer count,
                       average spending, frequency, order value, and recency metrics
                       
        Performs clustering if not already done.
        """
        if 'Segment' not in self.features.columns:
            self.perform_clustering()
        
        # Calculate thresholds for reference
        thresholds = self._calculate_thresholds()
        
        segments_summary = []
        for segment in self.features['Segment'].unique():
            segment_data = self.features[self.features['Segment'] == segment]
            segments_summary.append({
                'segment_name': segment,
                'customer_count': int(segment_data.shape[0]),
                'avg_spending': float(segment_data['Total Spending'].mean()),
                'avg_frequency': float(segment_data['Purchase Frequency'].mean()),
                'avg_order_value': float(segment_data['Average Purchase Amount'].mean()),
                'avg_days_since_purchase': float(segment_data['Days Since Last Purchase'].mean())
            })
        
        return {
            'summary': {
                'total_customers': len(self.features),
                'number_of_segments': len(segments_summary),
                'analysis_date': datetime.now().isoformat(),
                'thresholds': {
                    'spending': {
                        'high': float(thresholds['spending']['high']),
                        'medium': float(thresholds['spending']['medium'])
                    },
                    'frequency': {
                        'high': float(thresholds['frequency']['high']),
                        'medium': float(thresholds['frequency']['medium'])
                    },
                    'recency': float(thresholds['recency'])
                }
            },
            'segments': segments_summary
        }
    
    def get_customer_segment(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve detailed segment information for a specific customer.
        
        Args:
            customer_id (str): Unique identifier for the customer
            
        Returns:
            Dict containing customer's:
            - segment assignment
            - key metrics (spending, frequency, order value, recency)
            - relevant threshold values
            Returns None if customer_id is not found.
            
        Performs clustering if not already done.
        """
        if customer_id not in self.features.index:
            return None
        
        if 'Segment' not in self.features.columns:
            self.perform_clustering()
        
        customer_data = self.features.loc[customer_id]
        return {
            'customer_id': customer_id,
            'segment': customer_data['Segment'],
            'total_spending': float(customer_data['Total Spending']),
            'purchase_frequency': int(customer_data['Purchase Frequency']),
            'average_order_value': float(customer_data['Average Purchase Amount']),
            'days_since_last_purchase': int(customer_data['Days Since Last Purchase']),
            'thresholds': self._calculate_thresholds()
        }

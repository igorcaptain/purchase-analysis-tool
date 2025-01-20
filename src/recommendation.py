import pandas as pd
import numpy as np
from scipy.sparse.linalg import svds

class RecommendationEngine:
    def __init__(self, data_path: str, n_factors=10):
        """Initialize the recommendation engine with data path and number of latent factors
        
        Args:
            data_path (str): Path to the CSV file containing purchase data
            n_factors (int): Number of latent factors for matrix factorization (default: 10)
                           Higher values capture more complex patterns but risk overfitting
        
        Attributes:
            predictions_df: DataFrame containing predicted ratings for all user-item pairs
            purchase_matrix: Sparse matrix of actual user purchases
            df: Raw purchase data DataFrame
        """
        self.data_path = data_path
        self.n_factors = n_factors
        self.predictions_df = None
        self.purchase_matrix = None
        self.df = None
        self._load_and_process_data()
    
    def _load_and_process_data(self):
        """Load and preprocess the purchase data for recommendation generation
        
        This method performs several key steps:
        1. Loads purchase data from CSV file
        2. Creates a user-item purchase matrix where each cell represents purchase amount
        3. Performs matrix factorization using SVD (Singular Value Decomposition):
           - Normalizes the data by subtracting user means
           - Decomposes matrix into U (user features), sigma (weights), Vt (item features)
           - Reconstructs the matrix with predicted ratings
           - Adds back user means to get final predictions
        
        The resulting predictions_df contains estimated purchase amounts for all
        user-item combinations, including those that haven't been purchased yet.
        """
        # Load data
        self.df = pd.read_csv(self.data_path)
        self.df['Purchase Date'] = pd.to_datetime(self.df['Purchase Date'])
        
        # Create user-item purchase matrix
        self.purchase_matrix = self.df.pivot_table(
            index='Customer ID',
            columns='Product ID', 
            values='Purchase Amount',
            aggfunc='sum',
            fill_value=0
        )
        
        # Perform matrix factorization
        matrix = self.purchase_matrix.values
        user_means = np.mean(matrix, axis=1)
        matrix_norm = matrix - user_means.reshape(-1, 1)
        
        # SVD
        U, sigma, Vt = svds(matrix_norm, k=self.n_factors)
        
        # Reconstruct the normalized matrix
        sigma_diag = np.diag(sigma)
        predicted_norm = np.dot(np.dot(U, sigma_diag), Vt)
        predicted_ratings = predicted_norm + user_means.reshape(-1, 1)
        
        # Convert predictions to DataFrame
        self.predictions_df = pd.DataFrame(
            predicted_ratings,
            index=self.purchase_matrix.index,
            columns=self.purchase_matrix.columns
        )

    def get_recommendations(self, customer_id, n_recommendations=5):
        """Generate personalized product recommendations for a specific customer
        
        Args:
            customer_id: Unique identifier for the customer
            n_recommendations (int): Number of recommendations to generate (default: 5)
        
        Returns:
            dict: Contains:
                - error: Error message if customer not found, None otherwise
                - recommendations: List of dicts with recommended products, including:
                    * product_id: Unique identifier for the product
                    * category: Product category
                    * predicted_rating: Estimated purchase amount/rating
                - customer_id: Input customer_id
        
        Process:
        1. Checks if customer exists in the database
        2. Identifies products the customer hasn't purchased yet
        3. Gets predicted ratings for those products
        4. Returns top N products with highest predicted ratings
        """
        if customer_id not in self.predictions_df.index:
            return {
                'error': f"Customer {customer_id} not found in database",
                'recommendations': [],
                'customer_id': customer_id
            }
            
        # Get products the user hasn't purchased
        user_purchases = self.purchase_matrix.loc[customer_id]
        not_purchased = user_purchases[user_purchases == 0].index
        
        # Get predicted ratings for not purchased items
        predicted_ratings = self.predictions_df.loc[customer_id, not_purchased]
        
        # Sort and get top N recommendations
        top_recommendations = predicted_ratings.sort_values(ascending=False)[:n_recommendations]
        
        recommendations = []
        for prod_id, pred_rating in top_recommendations.items():
            category = self.df[self.df['Product ID'] == prod_id]['Product Category'].iloc[0]
            recommendations.append({
                'product_id': prod_id,
                'category': category,
                'predicted_rating': float(pred_rating)  # Convert to float for JSON serialization
            })
        
        return {
            'error': None,
            'recommendations': recommendations,
            'customer_id': customer_id
        }

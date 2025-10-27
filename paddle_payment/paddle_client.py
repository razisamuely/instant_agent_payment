"""
Paddle API Client

This module provides a client for interacting with Paddle's payment API.
It supports both sandbox and production environments, allowing for smooth
transition from testing to live transactions.
"""

import os
from typing import Dict, List, Optional, Any
import requests
from dotenv import load_dotenv


class PaddleClient:
    """
    Client for interacting with Paddle's payment API.
    
    Supports listing products, fetching price IDs, and creating checkout links
    for both subscriptions and one-time purchases in sandbox and production environments.
    """
    
    # Paddle API endpoints
    SANDBOX_API_URL = "https://sandbox-api.paddle.com"
    PRODUCTION_API_URL = "https://api.paddle.com"
    
    def __init__(self, api_key: Optional[str] = None, environment: Optional[str] = None):
        """
        Initialize the Paddle client.
        
        Args:
            api_key (str, optional): Paddle API key. If not provided, will load from environment.
            environment (str, optional): Environment to use ('sandbox' or 'production').
                                        If not provided, will load from environment.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Determine environment
        self.environment = environment or os.getenv("PADDLE_ENVIRONMENT", "sandbox")
        
        # Validate environment
        if self.environment not in ["sandbox", "production"]:
            raise ValueError("Environment must be 'sandbox' or 'production'")
        
        # Get API key
        if api_key:
            self.api_key = api_key
        elif self.environment == "sandbox":
            self.api_key = os.getenv("PADDLE_SANDBOX_API_KEY")
        else:
            self.api_key = os.getenv("PADDLE_PRODUCTION_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                f"API key not found for {self.environment} environment. "
                "Please set PADDLE_SANDBOX_API_KEY or PADDLE_PRODUCTION_API_KEY in .env file or pass api_key parameter."
            )
        
        # Set base URL
        self.base_url = (
            self.SANDBOX_API_URL if self.environment == "sandbox" 
            else self.PRODUCTION_API_URL
        )
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Paddle API.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint path
            params (dict, optional): Query parameters
            data (dict, optional): Request body data
            
        Returns:
            dict: JSON response from the API
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Ensure endpoint starts with /
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_msg = f"Paddle API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_detail = e.response.json()
                    # Extract meaningful error information
                    if isinstance(error_detail, dict):
                        if 'error' in error_detail:
                            error_msg += f" - {error_detail['error']}"
                        elif 'message' in error_detail:
                            error_msg += f" - {error_detail['message']}"
                        else:
                            error_msg += f" - {error_detail}"
                    else:
                        error_msg += f" - {error_detail}"
                except ValueError:
                    error_msg += f" - {e.response.text}"
            raise requests.exceptions.RequestException(error_msg)
    
    def list_products(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List all products from Paddle.
        
        Args:
            params (dict, optional): Additional query parameters for filtering/pagination
                                    (e.g., {'status': 'active', 'per_page': 50})
        
        Returns:
            list: List of product objects
            
        Example:
            >>> client = PaddleClient()
            >>> products = client.list_products()
            >>> for product in products:
            ...     print(f"Product: {product['name']} (ID: {product['id']})")
        """
        response = self._make_request("GET", "/products", params=params)
        return response.get("data", [])
    
    def get_product(self, product_id: str) -> Dict[str, Any]:
        """
        Get details of a specific product.
        
        Args:
            product_id (str): The ID of the product
            
        Returns:
            dict: Product details
            
        Example:
            >>> client = PaddleClient()
            >>> product = client.get_product("pro_01h1234567890abcdef")
            >>> print(f"Product: {product['name']}")
        """
        response = self._make_request("GET", f"/products/{product_id}")
        return response.get("data", {})
    
    def list_prices(
        self, 
        product_id: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        List prices (price IDs) for products.
        
        Args:
            product_id (str, optional): Filter prices by product ID
            params (dict, optional): Additional query parameters
            
        Returns:
            list: List of price objects
            
        Example:
            >>> client = PaddleClient()
            >>> prices = client.list_prices(product_id="pro_01h1234567890abcdef")
            >>> for price in prices:
            ...     print(f"Price ID: {price['id']}, Amount: {price['unit_price']['amount']}")
        """
        if params is None:
            params = {}
        
        if product_id:
            params["product_id"] = product_id
        
        response = self._make_request("GET", "/prices", params=params)
        return response.get("data", [])
    
    def get_price(self, price_id: str) -> Dict[str, Any]:
        """
        Get details of a specific price.
        
        Args:
            price_id (str): The ID of the price
            
        Returns:
            dict: Price details
            
        Example:
            >>> client = PaddleClient()
            >>> price = client.get_price("pri_01h1234567890abcdef")
            >>> print(f"Price: {price['unit_price']['amount']} {price['unit_price']['currency_code']}")
        """
        response = self._make_request("GET", f"/prices/{price_id}")
        return response.get("data", {})
    
    def create_checkout(
        self,
        items: List[Dict[str, Any]],
        customer_email: Optional[str] = None,
        customer_id: Optional[str] = None,
        custom_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a checkout session for subscriptions or one-time purchases.
        
        Args:
            items (list): List of items to checkout. Each item should have:
                         - price_id (str): The price ID to checkout
                         - quantity (int, optional): Quantity (default: 1)
            customer_email (str, optional): Customer email address
            customer_id (str, optional): Existing customer ID
            custom_data (dict, optional): Custom data to attach to the transaction
            **kwargs: Additional checkout options (e.g., success_url, billing_details)
            
        Returns:
            dict: Checkout session details including checkout URL
            
        Example:
            >>> client = PaddleClient()
            >>> checkout = client.create_checkout(
            ...     items=[{"price_id": "pri_01h1234567890abcdef", "quantity": 1}],
            ...     customer_email="customer@example.com"
            ... )
            >>> print(f"Checkout URL: {checkout['url']}")
        """
        data = {
            "items": items
        }
        
        if customer_email:
            data["customer_email"] = customer_email
        
        if customer_id:
            data["customer_id"] = customer_id
        
        if custom_data:
            data["custom_data"] = custom_data
        
        # Add any additional parameters
        data.update(kwargs)
        
        response = self._make_request("POST", "/checkouts", data=data)
        return response.get("data", {})
    
    def get_checkout_link(
        self,
        items: List[Dict[str, Any]],
        customer_email: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Convenience method to create a checkout and return just the URL.
        
        Args:
            items (list): List of items to checkout
            customer_email (str, optional): Customer email address
            **kwargs: Additional checkout options
            
        Returns:
            str: The checkout URL
            
        Example:
            >>> client = PaddleClient()
            >>> url = client.get_checkout_link(
            ...     items=[{"price_id": "pri_01h1234567890abcdef"}],
            ...     customer_email="customer@example.com"
            ... )
            >>> print(f"Send customer to: {url}")
        """
        checkout = self.create_checkout(items, customer_email, **kwargs)
        return checkout.get("url", "")
    
    def list_customers(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List customers.
        
        Args:
            params (dict, optional): Query parameters for filtering/pagination
            
        Returns:
            list: List of customer objects
        """
        response = self._make_request("GET", "/customers", params=params)
        return response.get("data", [])
    
    def get_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Get details of a specific customer.
        
        Args:
            customer_id (str): The ID of the customer
            
        Returns:
            dict: Customer details
        """
        response = self._make_request("GET", f"/customers/{customer_id}")
        return response.get("data", {})
    
    def list_subscriptions(self, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        List subscriptions.
        
        Args:
            params (dict, optional): Query parameters for filtering/pagination
                                    (e.g., {'status': 'active', 'customer_id': 'ctm_01h...'})
            
        Returns:
            list: List of subscription objects
        """
        response = self._make_request("GET", "/subscriptions", params=params)
        return response.get("data", [])
    
    def get_subscription(self, subscription_id: str) -> Dict[str, Any]:
        """
        Get details of a specific subscription.
        
        Args:
            subscription_id (str): The ID of the subscription
            
        Returns:
            dict: Subscription details
        """
        response = self._make_request("GET", f"/subscriptions/{subscription_id}")
        return response.get("data", {})
    
    def get_environment_info(self) -> Dict[str, str]:
        """
        Get information about the current environment configuration.
        
        Returns:
            dict: Environment information (environment, base_url)
            
        Example:
            >>> client = PaddleClient()
            >>> info = client.get_environment_info()
            >>> print(f"Using {info['environment']} environment at {info['base_url']}")
        """
        return {
            "environment": self.environment,
            "base_url": self.base_url,
            "is_sandbox": self.environment == "sandbox"
        }

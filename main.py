# main.py - Paddle Integration Module

from dotenv import load_dotenv
import requests
import os

load_dotenv()

# ============================================
# CONFIGURATION
# ============================================

ENVIRONMENT = os.getenv("PADDLE_ENVIRONMENT", "sandbox")
API_KEY = os.getenv("API_KEY")

API_URLS = {
    "sandbox": "https://sandbox-api.paddle.com",
    "production": "https://api.paddle.com"
}

BASE_URL = API_URLS[ENVIRONMENT]

HEADER = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# ============================================
# PADDLE FUNCTIONS
# ============================================

def create_checkout_link(price_id, agent_id, customer_phone, agent_phone, quantity=1):
    """
    Create a Paddle checkout link with agent tracking data.
    
    Args:
        price_id: Paddle price ID
        agent_id: Unique agent identifier
        customer_phone: Customer phone number
        agent_phone: Agent phone number
        quantity: Quantity of items (default: 1)
    
    Returns:
        str: Checkout URL or None if failed
    """
    url = f"{BASE_URL}/transactions"
    
    data = {
        "items": [{"price_id": price_id, "quantity": quantity}],
        "custom_data": {
            "agent_id": agent_id,
            "customer_phone": customer_phone,
            "agent_phone": agent_phone
        }
    }
    
    try:
        response = requests.post(url, headers=HEADER, json=data, timeout=10)
        
        if response.status_code == 201:
            result = response.json()
            if "data" in result and "checkout" in result["data"]:
                return result["data"]["checkout"]["url"]
        
        return None
        
    except requests.exceptions.RequestException:
        return None

def list_products():
    """List all products in Paddle catalog."""
    url = f"{BASE_URL}/products"
    response = requests.get(url, headers=HEADER)
    return response.json()

def list_prices():
    """List all prices in Paddle catalog."""
    url = f"{BASE_URL}/prices"
    response = requests.get(url, headers=HEADER)
    return response.json()

# ============================================
# LOCAL TESTING
# ============================================

if __name__ == "__main__":
    print(f"🌍 Environment: {ENVIRONMENT}")
    print(f"📡 API URL: {BASE_URL}\n")
    
    # Test: List prices
    prices = list_prices()
    if prices.get("data"):
        price_id = prices["data"][0]["id"]
        print(f"✅ Price ID: {price_id}\n")
        
        # Test: Create checkout link
        checkout_url = create_checkout_link(
            price_id=price_id,
            agent_id="test_agent_123",
            customer_phone="+972501234567",
            agent_phone="+14155551234"
        )
        
        if checkout_url:
            print(f"✅ Checkout URL created:")
            print(f"🔗 {checkout_url}")
        else:
            print("❌ Failed to create checkout")
    else:
        print("❌ No prices found")
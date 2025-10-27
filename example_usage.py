"""
Example Usage of Paddle Payment Integration

This script demonstrates how to use the Paddle payment integration
for listing products, fetching prices, and creating checkout links.
"""

from paddle_payment import PaddleClient


def main():
    """Demonstrate basic usage of the Paddle client."""
    
    print("=" * 60)
    print("Paddle Payment Integration - Example Usage")
    print("=" * 60)
    
    # Initialize the client (will use environment variables from .env)
    try:
        client = PaddleClient()
        
        # Display environment info
        env_info = client.get_environment_info()
        print(f"\n✓ Connected to Paddle {env_info['environment'].upper()} environment")
        print(f"  API URL: {env_info['base_url']}")
        
    except ValueError as e:
        print(f"\n✗ Error initializing client: {e}")
        print("\nPlease ensure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Set your Paddle API key in the .env file")
        print("3. Set the PADDLE_ENVIRONMENT variable ('sandbox' or 'production')")
        return
    
    print("\n" + "-" * 60)
    print("1. Listing Products")
    print("-" * 60)
    
    try:
        products = client.list_products()
        if products:
            print(f"\nFound {len(products)} product(s):")
            for product in products[:5]:  # Show first 5
                print(f"  • {product.get('name', 'N/A')} (ID: {product.get('id', 'N/A')})")
                print(f"    Description: {product.get('description', 'No description')[:50]}...")
        else:
            print("\nNo products found. Create products in your Paddle dashboard first.")
    except Exception as e:
        print(f"\n✗ Error listing products: {e}")
    
    print("\n" + "-" * 60)
    print("2. Listing Prices")
    print("-" * 60)
    
    try:
        prices = client.list_prices()
        if prices:
            print(f"\nFound {len(prices)} price(s):")
            for price in prices[:5]:  # Show first 5
                unit_price = price.get('unit_price', {})
                amount = unit_price.get('amount', 'N/A')
                currency = unit_price.get('currency_code', 'N/A')
                billing = price.get('billing_cycle', {})
                interval = billing.get('interval', 'one_time') if billing else 'one_time'
                
                print(f"  • Price ID: {price.get('id', 'N/A')}")
                print(f"    Amount: {amount} {currency}")
                print(f"    Type: {interval}")
                print(f"    Product ID: {price.get('product_id', 'N/A')}")
        else:
            print("\nNo prices found. Create prices in your Paddle dashboard first.")
    except Exception as e:
        print(f"\n✗ Error listing prices: {e}")
    
    print("\n" + "-" * 60)
    print("3. Creating a Checkout Link (Example)")
    print("-" * 60)
    
    print("\nTo create a checkout link, you need a valid price ID.")
    print("Example code:")
    print("""
    # For a one-time purchase or subscription
    checkout_url = client.get_checkout_link(
        items=[
            {"price_id": "pri_01h...", "quantity": 1}
        ],
        customer_email="customer@example.com"
    )
    print(f"Checkout URL: {checkout_url}")
    
    # Or get full checkout details
    checkout = client.create_checkout(
        items=[
            {"price_id": "pri_01h...", "quantity": 1}
        ],
        customer_email="customer@example.com",
        custom_data={"order_id": "12345"}
    )
    print(f"Checkout URL: {checkout['url']}")
    print(f"Checkout ID: {checkout['id']}")
    """)
    
    print("\n" + "-" * 60)
    print("4. Working with Customers and Subscriptions")
    print("-" * 60)
    
    print("\nList customers:")
    print("  customers = client.list_customers()")
    
    print("\nGet a specific customer:")
    print("  customer = client.get_customer('ctm_01h...')")
    
    print("\nList subscriptions:")
    print("  subscriptions = client.list_subscriptions()")
    print("  active_subs = client.list_subscriptions({'status': 'active'})")
    
    print("\nGet a specific subscription:")
    print("  subscription = client.get_subscription('sub_01h...')")
    
    print("\n" + "=" * 60)
    print("Environment Switching")
    print("=" * 60)
    
    print("""
To switch between sandbox and production:

1. Update your .env file:
   PADDLE_ENVIRONMENT=production
   
2. Or pass environment directly:
   client = PaddleClient(environment='production')
   
3. Or use a different API key:
   client = PaddleClient(
       api_key='your_prod_api_key',
       environment='production'
   )
""")
    
    print("\n" + "=" * 60)
    print("Example Complete!")
    print("=" * 60)
    print("\nFor more information, check the README.md file.")
    print()


if __name__ == "__main__":
    main()

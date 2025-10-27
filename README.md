# Paddle Payment Integration

A Python library for integrating with [Paddle's](https://www.paddle.com/) payment API. This project provides a clean, easy-to-use interface for managing subscriptions and one-time purchases through Paddle's billing platform.

## Features

✨ **Complete Paddle API Integration**
- List and retrieve products from your Paddle catalog
- Fetch price IDs for products (subscriptions and one-time purchases)
- Create checkout links for customer payment flows
- Manage customers and subscriptions

🌍 **Environment Support**
- Seamless switching between Sandbox and Production environments
- Environment-specific API key management
- Easy transition from testing to live transactions

🔒 **Secure Configuration**
- API key management through environment variables
- Uses `python-dotenv` for secure credential handling
- Never commit sensitive data to version control

📦 **Simple & Clean**
- Intuitive Python API
- Comprehensive error handling
- Type hints for better IDE support

## Installation

1. Clone this repository:
```bash
git clone https://github.com/razisamuely/instant_agent_payment.git
cd instant_agent_payment
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
```bash
cp .env.example .env
# Edit .env with your Paddle API keys
```

## Configuration

### Environment Variables

Create a `.env` file in the project root with your Paddle API credentials:

```env
# Sandbox Environment (for testing)
PADDLE_SANDBOX_API_KEY=your_sandbox_api_key_here
PADDLE_SANDBOX_ENVIRONMENT=sandbox

# Production Environment (for live transactions)
PADDLE_PRODUCTION_API_KEY=your_production_api_key_here
PADDLE_PRODUCTION_ENVIRONMENT=production

# Active Environment (set to 'sandbox' or 'production')
PADDLE_ENVIRONMENT=sandbox
```

### Getting Your API Keys

1. **Sandbox API Key**: 
   - Log in to your [Paddle Sandbox Dashboard](https://sandbox-vendors.paddle.com/)
   - Go to Developer Tools → Authentication
   - Create a new API key

2. **Production API Key**:
   - Log in to your [Paddle Dashboard](https://vendors.paddle.com/)
   - Go to Developer Tools → Authentication
   - Create a new API key

## Usage

### Quick Start

```python
from paddle_payment import PaddleClient

# Initialize client (uses .env configuration)
client = PaddleClient()

# List all products
products = client.list_products()
for product in products:
    print(f"Product: {product['name']} (ID: {product['id']})")

# List prices for a product
prices = client.list_prices(product_id="pro_01h...")
for price in prices:
    print(f"Price: {price['unit_price']['amount']} {price['unit_price']['currency_code']}")

# Create a checkout link
checkout_url = client.get_checkout_link(
    items=[{"price_id": "pri_01h...", "quantity": 1}],
    customer_email="customer@example.com"
)
print(f"Send customer to: {checkout_url}")
```

### Detailed Examples

#### 1. Working with Products

```python
from paddle_payment import PaddleClient

client = PaddleClient()

# List all products
products = client.list_products()

# Get a specific product
product = client.get_product("pro_01h1234567890abcdef")
print(f"Product: {product['name']}")
print(f"Description: {product['description']}")
```

#### 2. Working with Prices

```python
# List all prices
all_prices = client.list_prices()

# List prices for a specific product
product_prices = client.list_prices(product_id="pro_01h...")

# Get a specific price
price = client.get_price("pri_01h1234567890abcdef")
print(f"Amount: {price['unit_price']['amount']}")
print(f"Currency: {price['unit_price']['currency_code']}")

# Check if it's a subscription
if 'billing_cycle' in price:
    interval = price['billing_cycle']['interval']
    print(f"Billing: {interval}")
```

#### 3. Creating Checkouts

```python
# Simple one-time purchase
checkout = client.create_checkout(
    items=[{"price_id": "pri_01h...", "quantity": 1}],
    customer_email="customer@example.com"
)
print(f"Checkout URL: {checkout['url']}")

# Subscription with custom data
checkout = client.create_checkout(
    items=[{"price_id": "pri_01h...", "quantity": 1}],
    customer_email="customer@example.com",
    custom_data={"user_id": "12345", "plan": "premium"}
)

# Get just the checkout URL
url = client.get_checkout_link(
    items=[{"price_id": "pri_01h..."}],
    customer_email="customer@example.com"
)
```

#### 4. Managing Customers

```python
# List all customers
customers = client.list_customers()

# Get a specific customer
customer = client.get_customer("ctm_01h1234567890abcdef")
print(f"Customer: {customer['email']}")
```

#### 5. Managing Subscriptions

```python
# List all subscriptions
subscriptions = client.list_subscriptions()

# List only active subscriptions
active_subs = client.list_subscriptions(params={"status": "active"})

# Get a specific subscription
subscription = client.get_subscription("sub_01h1234567890abcdef")
print(f"Status: {subscription['status']}")
print(f"Next billing date: {subscription['next_billed_at']}")
```

### Environment Switching

#### Using .env file
```python
# Set PADDLE_ENVIRONMENT=production in .env
client = PaddleClient()  # Will use production
```

#### Programmatically
```python
# Use sandbox
sandbox_client = PaddleClient(environment='sandbox')

# Use production
prod_client = PaddleClient(environment='production')

# Or provide API key directly
client = PaddleClient(
    api_key='your_api_key',
    environment='production'
)
```

#### Check current environment
```python
env_info = client.get_environment_info()
print(f"Environment: {env_info['environment']}")
print(f"API URL: {env_info['base_url']}")
print(f"Is Sandbox: {env_info['is_sandbox']}")
```

## Example Script

Run the included example script to see the integration in action:

```bash
python example_usage.py
```

This will demonstrate:
- Listing products
- Fetching prices
- Creating checkout links
- Working with customers and subscriptions

## Project Structure

```
instant_agent_payment/
├── paddle_payment/           # Main package
│   ├── __init__.py          # Package initialization
│   └── paddle_client.py     # Core Paddle API client
├── example_usage.py         # Example usage script
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## API Reference

### PaddleClient

#### Initialization
```python
PaddleClient(api_key=None, environment=None)
```
- `api_key` (str, optional): Paddle API key. If not provided, loads from environment.
- `environment` (str, optional): 'sandbox' or 'production'. If not provided, loads from environment.

#### Methods

**Products**
- `list_products(params=None)` - List all products
- `get_product(product_id)` - Get a specific product

**Prices**
- `list_prices(product_id=None, params=None)` - List prices
- `get_price(price_id)` - Get a specific price

**Checkouts**
- `create_checkout(items, customer_email=None, customer_id=None, custom_data=None, **kwargs)` - Create a checkout session
- `get_checkout_link(items, customer_email=None, **kwargs)` - Get checkout URL directly

**Customers**
- `list_customers(params=None)` - List customers
- `get_customer(customer_id)` - Get a specific customer

**Subscriptions**
- `list_subscriptions(params=None)` - List subscriptions
- `get_subscription(subscription_id)` - Get a specific subscription

**Utilities**
- `get_environment_info()` - Get current environment information

## Error Handling

The client raises `requests.exceptions.RequestException` for API errors:

```python
from paddle_payment import PaddleClient
import requests

client = PaddleClient()

try:
    products = client.list_products()
except requests.exceptions.RequestException as e:
    print(f"API Error: {e}")
except ValueError as e:
    print(f"Configuration Error: {e}")
```

## Testing Strategy

### Sandbox Environment

1. Start with the sandbox environment for all testing
2. Create test products and prices in your Paddle Sandbox dashboard
3. Test the complete checkout flow
4. Verify webhook handling

### Production Migration

1. Create products and prices in production
2. Update `.env` to use production environment
3. Test with small transactions first
4. Monitor transactions in Paddle dashboard

## Dependencies

- **python-dotenv** (>=1.0.0) - Environment variable management
- **requests** (>=2.31.0) - HTTP client for API calls

## Security Best Practices

1. ✅ Never commit `.env` file to version control
2. ✅ Use different API keys for sandbox and production
3. ✅ Rotate API keys regularly
4. ✅ Use sandbox for all testing
5. ✅ Validate webhook signatures in production
6. ✅ Use HTTPS for all checkout redirects

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for integration with Paddle's payment platform.

## Support

For Paddle API documentation, visit: https://developer.paddle.com/

For issues with this integration, please open an issue on GitHub.

## Acknowledgments

Built for seamless Paddle payment integration with support for both sandbox and production environments.
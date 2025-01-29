# Shopify MCP Server

A Model Context Protocol (MCP) server to connect clients like Claude with Shopify store data. This server exposes tools for retrieving product and customer information from your Shopify store.

## Features

- `get-product-list`: Retrieve a list of products from your Shopify store
- `get-customer-list`: Retrieve a list of customers from your Shopify store

## Prerequisites

- Python 3.12 or higher
- A Shopify store with API access
- Shopify API credentials (API Key, Password, and Access Token)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/siddhantbajaj/shopify-mcp-server.git
cd shopify-mcp-server
```

2. Create and activate a virtual environment using `uv`:
```bash
uv venv
source .venv/bin/activate  # On Unix/MacOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install the package:
```bash
uv pip install -e .
```

## Configuration

1. Create a `.env` file in the root directory with your Shopify credentials:
```env
SHOPIFY_SHOP_URL="your-store.myshopify.com"
SHOPIFY_API_KEY="your_api_key"
SHOPIFY_PASSWORD="your_api_password"
SHOPIFY_ACCESS_TOKEN="your_access_token"
```

Replace the placeholder values with your actual Shopify API credentials.

## Usage

1. Start the MCP server:
```bash
python -m shopify_mcp_server.server
```

2. The server exposes two tools:

### get-product-list
Retrieves a list of products from your Shopify store.
- Optional parameter: `limit` (default: 10) - Maximum number of products to return

### get-customer-list
Retrieves a list of customers from your Shopify store.
- Optional parameter: `limit` (default: 10) - Maximum number of customers to return

## Tool Response Format

### Products
```
Products (showing X):

Title: Product Name
ID: 123456789
Product Type: Type
Vendor: Vendor Name
Status: active
Price: $XX.XX
---
```

### Customers
```
Customers (showing X):

Name: John Doe
ID: 123456789
Email: john@example.com
Orders Count: X
Total Spent: $XX.XX
---
```

## Development

This project uses:
- [MCP (Model Context Protocol)](https://www.anthropic.com/news/model-context-protocol) for building AI-powered tools
- [Shopify Python API](https://github.com/Shopify/shopify_python_api) for Shopify integration
- [UV](https://github.com/astral-sh/uv) for dependency management

## Security

- Never commit your `.env` file to version control
- Keep your Shopify API credentials secure
- Use environment variables for sensitive information

## License

[TODO]

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

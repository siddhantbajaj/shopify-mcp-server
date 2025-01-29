from typing import Any
import asyncio
import shopify
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server.lowlevel import NotificationOptions, Server
import mcp.server.stdio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize server
server = Server("shopify")

# Configure Shopify client
def init_shopify():
    """Initialize Shopify API client with credentials"""
    shop_url = os.getenv("SHOPIFY_SHOP_URL")
    api_key = os.getenv("SHOPIFY_API_KEY")
    password = os.getenv("SHOPIFY_PASSWORD")
    access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    if not all([shop_url, api_key, password]):
        raise ValueError("Missing required Shopify credentials in environment variables")

    session = shopify.Session(shop_url, '2025-01', access_token)
    shopify.ShopifyResource.activate_session(session)

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available Shopify tools"""
    return [
        types.Tool(
            name="get-product-list",
            description="Get a list of products from the Shopify store",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of products to return (default: 10)",
                    },
                },
            },
        ),
        types.Tool(
            name="get-customer-list",
            description="Get a list of customers from the Shopify store",
            inputSchema={
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "number",
                        "description": "Maximum number of customers to return (default: 10)",
                    },
                },
            },
        ),
    ]

def format_product(product: shopify.Product) -> str:
    """Format a Shopify product into a readable string"""
    return (
        f"Title: {product.title}\n"
        f"ID: {product.id}\n"
        f"Product Type: {product.product_type}\n"
        f"Vendor: {product.vendor}\n"
        f"Status: {product.status}\n"
        f"Price: ${product.variants[0].price if product.variants else 'N/A'}\n"
        "---"
    )

def format_customer(customer: shopify.Customer) -> str:
    """Format a Shopify customer into a readable string"""
    return (
        f"Name: {customer.first_name} {customer.last_name}\n"
        f"ID: {customer.id}\n"
        f"Email: {customer.email}\n"
        f"Orders Count: {customer.orders_count}\n"
        f"Total Spent: ${customer.total_spent}\n"
        "---"
    )

@server.call_tool()
async def handle_call_tool(
    name: str,
    arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle Shopify tool execution requests"""
    if not arguments:
        arguments = {}

    try:
        init_shopify()

        if name == "get-product-list":
            limit = int(arguments.get("limit", 10))
            products = shopify.Product.find(limit=limit)

            if not products:
                return [types.TextContent(type="text", text="No products found")]

            formatted_products = [format_product(product) for product in products]
            products_text = f"Products (showing {len(formatted_products)}):\n\n" + "\n".join(formatted_products)

            return [types.TextContent(type="text", text=products_text)]

        elif name == "get-customer-list":
            limit = int(arguments.get("limit", 10))
            customers = shopify.Customer.find(limit=limit)

            if not customers:
                return [types.TextContent(type="text", text="No customers found")]

            formatted_customers = [format_customer(customer) for customer in customers]
            customers_text = f"Customers (showing {len(formatted_customers)}):\n\n" + "\n".join(formatted_customers)

            return [types.TextContent(type="text", text=customers_text)]

        else:
            raise ValueError(f"Unknown tool: {name}")

    except Exception as e:
        return [types.TextContent(type="text", text=f"Error executing tool: {str(e)}")]

async def main():
    """Run the Shopify MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="shopify",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())




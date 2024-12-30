import requests
import json
import argparse
from datetime import datetime, timedelta

class ZenskarAPIClient:
    def __init__(self, api_key, org_id):
        """
        Initialize Zenskar API Client
        
        :param api_key: Zenskar API authentication key
        """
        self.base_url = "https://api.zenskar.com"
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "x-api-key": api_key,
            "organisation": org_id
        }
    
    def create_customer(self, name, phone, address):
        """
        Create a customer in Zenskar 
        
        :param name: Customer name
        :param phone: Customer phone number
        :param address: Customer address
        :return: Created customer details
        """
        endpoint = f"{self.base_url}/customers"
        payload = {
            "customer_name": name,
            "phone_number": phone,
            "address": {
                "line1": address,
                "city": "New York",
                "state": "NY",
                "country": "United States",
                "zipCode": "10001"
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating customer: {e}")
            return None
    
    def create_product(self, name, product_type, description=""):
        """
        Create a product in Zenskar
        
        :param name: Product name
        :param product_type: Product type (Subscription Fee or Usage Fee)
        :param description: Product description
        :return: Created product details
        """
        endpoint = f"{self.base_url}/products"
        
        payload = {
            "name": name,
            "description": description or f"{name} - {product_type}",
            "type": "product",
            "is_active": True
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating product {name}: {e}")
            print(f"Response content: {response.text}")
            return None

    def add_product_pricing(self, product_id, name, price, billing_frequency, product_type, billing_offset="prepaid", quantity=None):
        """
        Add pricing to a product in Zenskar
        
        :param product_id: ID of the product to add pricing to
        :param name: Name of the pricing plan
        :param price: Price amount
        :param billing_frequency: Frequency of billing (monthly, yearly, etc.)
        :param product_type: Type of product (Subscription Fee or Usage Fee)
        :param billing_offset: prepaid or postpaid
        :param quantity: Optional quantity for usage-based products
        :return: Created pricing details
        """
        endpoint = f"{self.base_url}/products/{product_id}/pricing"
        
        # Base pricing data structure
        pricing_data = {
            "currency": "USD",
            "label": name,
            "pricing_period": {
                "cadence": billing_frequency
            },
            "unit_amount": price
        }

        # Configure pricing type based on product type
        if product_type == "Usage Fee":
            # Per-unit pricing for Monthly User Fee
            pricing_data.update({
                "pricing_type": "per_unit",
                "unit": "user"
            })
            if quantity is not None:
                pricing_data["quantity"] = {
                    "type": "metered",
                    "label": "Number of Users",
                    "quantity": quantity,
                    "unit": "user"
                }
        else:
            # Flat fee for One Time Fee and Monthly Platform Fee
            pricing_data.update({
                "pricing_type": "flat_fee",
                "unit": "unit"
            })

        payload = {
            "name": name,
            "description": f"Pricing for {name}",
            "pricing_data": pricing_data,
            "is_recurring": billing_frequency != "P0",
            "billing_period": {
                "cadence": billing_frequency,
                "offset": billing_offset
            }
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error adding pricing to product: {e}")
            print(f"Response content: {response.text}")
            return None
    
    def create_contract(self, customer_id, products, start_date, end_date):
        """
        Create a contract in Zenskar
        
        :param customer_id: ID of the customer
        :param products: List of product details including pricing IDs
        :param start_date: Contract start date
        :param end_date: Contract end date
        :return: Created contract details
        """
        endpoint = f"{self.base_url}/contract_v2"

        # Create two phases:
        # Phase 1 (Jan-Mar): All products
        # Phase 2 (Apr-Dec): All products except Monthly Platform Fee
        phases = [
            {
                "name": "Phase 1 - All Products",
                "description": "January to March with all products",
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-03-31T23:59:59",
                "pricings": [
                    {
                        "pricing_id": product["pricing_id"],
                        "product_id": product["id"],
                        "start_date": "2024-01-01T00:00:00",
                        "end_date": "2024-03-31T23:59:59"
                    } for product in products
                ]
            },
            {
                "name": "Phase 2 - Excluding Platform Fee",
                "description": "April to December without Monthly Platform Fee",
                "start_date": "2024-04-01T00:00:00",
                "end_date": "2024-12-31T23:59:59",
                "pricings": [
                    {
                        "pricing_id": product["pricing_id"],
                        "product_id": product["id"],
                        "start_date": "2024-04-01T00:00:00",
                        "end_date": "2024-12-31T23:59:59"
                    } for product in products if product["name"] != "Monthly Platform Fee"
                ]
            }
        ]
        payload = {
            "status": "active",
            "name": "Annual Contract 2024",
            "description": "Annual contract with varying product phases",
            "currency": "USD",
            "start_date": "2024-01-01T00:00:00",
            "end_date": "2024-12-31T23:59:59",
            "customer_id": customer_id,
            "phases": phases
            # "renewal_policy": "renew_with_default_contract"
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error creating contract: {e}")
            print(f"Response content: {response.text}")
            return None

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Zenskar API Integration Script")
    parser.add_argument("--api-key", required=True, help="Zenskar API Key")
    parser.add_argument("--organisation-id", required=True, help="Zenskar Organisation ID")
    parser.add_argument("--user-count", type=int, default=10, help="Number of users for Monthly User Fee (default: 10)")
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize Zenskar API Client
    client = ZenskarAPIClient(args.api_key, args.organisation_id)
    
    # 1. Create Customer
    customer = client.create_customer(
        name="Example Customer", 
        phone="+12345678900", 
        address="123 Frost Street"
    )
    
    if not customer:
        print("Failed to create customer")
        return
    
    # Store products and their pricing information
    products_info = []
    
    # 2. Create Products and their pricing
    # One Time Fee
    one_time_fee = client.create_product(
        name="One Time Fee",
        product_type="Subscription Fee",
        description="One-time subscription fee"
    )
    if one_time_fee:
        one_time_pricing = client.add_product_pricing(
            product_id=one_time_fee["id"],
            name="One Time Fee Pricing",
            price=5000,
            billing_frequency="P0",
            product_type="Subscription Fee",
            billing_offset="prepaid"
        )
        if one_time_pricing:
            products_info.append({
                "id": one_time_fee["id"],
                "pricing_id": one_time_pricing["id"],
                "name": "One Time Fee"
            })
    
    # Monthly Platform Fee
    monthly_platform_fee = client.create_product(
        name="Monthly Platform Fee",
        product_type="Subscription Fee",
        description="Monthly platform subscription fee"
    )
    if monthly_platform_fee:
        platform_pricing = client.add_product_pricing(
            product_id=monthly_platform_fee["id"],
            name="Monthly Platform Fee Pricing",
            price=10000,
            billing_frequency="P1M",
            product_type="Subscription Fee",
            billing_offset="postpaid"
        )
        if platform_pricing:
            products_info.append({
                "id": monthly_platform_fee["id"],
                "pricing_id": platform_pricing["id"],
                "name": "Monthly Platform Fee"
            })
    
    # Monthly User Fee
    monthly_user_fee = client.create_product(
        name="Monthly User Fee",
        product_type="Usage Fee",
        description="Monthly per-user fee"
    )
    if monthly_user_fee:
        user_pricing = client.add_product_pricing(
            product_id=monthly_user_fee["id"],
            name="Monthly User Fee Pricing",
            price=60,
            billing_frequency="P1M",
            product_type="Usage Fee",
            billing_offset="postpaid",
            quantity=args.user_count
        )
        if user_pricing:
            products_info.append({
                "id": monthly_user_fee["id"],
                "pricing_id": user_pricing["id"],
                "name": "Monthly User Fee"
            })
    
    # 3. Create Contract with phases
    # print(products_info,"306")
    # print(customer["id"])
    if products_info:
        contract = client.create_contract(
            customer_id=customer["id"],
            products=products_info,
            start_date="2024-01-01T00:00:00Z",
            end_date="2024-12-31T23:59:59Z"
        )
        
        if contract:
            print("Contract created successfully!")
        else:
            print("Failed to create contract")
    else:
        print("No products created successfully, cannot create contract")

if __name__ == "__main__":
    main()

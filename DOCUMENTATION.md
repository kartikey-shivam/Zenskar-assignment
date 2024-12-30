# Zenskar API Integration Documentation

## Table of Contents
1. [Environment Setup](#environment-setup)
2. [API Endpoints](#api-endpoints)
3. [Script Explanation](#script-explanation)
4. [Sample API Responses](#sample-api-responses)

## Environment Setup

### Prerequisites
1. Install Python 3.7 or higher
2. Install Git (optional, for version control)
3. Have your Zenskar API credentials ready:
   - API Key
   - Organization ID

### Step-by-Step Setup
1. **Create a Project Directory**
   ```bash
   mkdir zenskar-integration
   cd zenskar-integration
   ```

2. **Set Up Virtual Environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows
   .\venv\Scripts\activate
   # On Unix/MacOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Script**
   ```bash
   python zenskar_api_integration.py --api-key YOUR_API_KEY --organisation-id YOUR_ORG_ID [--user-count USER_COUNT]
   ```
   
## API Endpoints

The script uses the following Zenskar API endpoints:

1. **Customer Creation**
   - Endpoint: `POST https://api.zenskar.com/customers`
   - Purpose: Create a new customer
   - Headers Required:
     ```json
     {
       "accept": "application/json",
       "content-type": "application/json",
       "x-api-key": "YOUR_API_KEY"
     }
     ```

2. **Product Creation**
   - Endpoint: `POST https://api.zenskar.com/products`
   - Purpose: Create a new product
   - Headers: Same as above

3. **Product Pricing**
   - Endpoint: `POST https://api.zenskar.com/products/{product_id}/pricing`
   - Purpose: Add pricing configuration to a product
   - Headers: Same as above

4. **Contract Creation**
   - Endpoint: `POST https://api.zenskar.com/contract_v2`
   - Purpose: Create a contract with phases
   - Headers: Same as above

## Script Explanation

### Class Structure
The script is organized around the `ZenskarAPIClient` class with these main methods:

1. **`__init__(self, api_key, org_id)`**
   - Initializes the API client with credentials
   - Sets up common headers and base URL

2. **`create_customer(self, name, phone, address)`**
   - Creates a customer with basic information
   - Returns customer details including ID

3. **`create_product(self, name, product_type, description="")`**
   - Creates a basic product
   - Supports different product types (Subscription Fee, Usage Fee)

4. **`add_product_pricing(self, product_id, name, price, billing_frequency, product_type, billing_offset="prepaid", quantity=None)`**
   - Adds pricing configuration to a product
   - Handles different pricing types (flat fee, per-unit)
   - Configures billing frequency and offset

5. **`create_contract(self, customer_id, products, start_date, end_date)`**
   - Creates a phased contract
   - Handles different product combinations per phase

### Main Workflow
1. Parse command-line arguments
2. Create customer
3. Create and configure products:
   - One Time Fee (flat fee)
   - Monthly Platform Fee (flat fee)
   - Monthly User Fee (per-unit)
4. Create contract with two phases:
   - Phase 1: All products (Jan-Mar)
   - Phase 2: Excluding Platform Fee (Apr-Dec)

## Sample API Responses

### 1. Customer Creation Response
```json
{
    "id": "cust_12345",
    "name": "Example Customer",
    "phone": "+1234567890",
    "address": {
        "line1": "123 Frost Street",
        "city": "New York",
        "state": "NY",
        "country": "United States",
        "zip": "10001"
    }
}
```

### 2. Product Creation Response
```json
{
    "id": "prod_12345",
    "name": "One Time Fee",
    "description": "One-time subscription fee",
    "type": "product",
    "is_active": true
}
```

### 3. Product Pricing Response
```json
{
    "id": "price_12345",
    "name": "One Time Fee Pricing",
    "pricing_data": {
        "currency": "USD",
        "label": "One Time Fee Pricing",
        "unit": "unit",
        "pricing_period": {
            "cadence": "one_time"
        },
        "unit_amount": 5000,
        "pricing_type": "flat"
    },
    "is_recurring": false,
    "billing_period": {
        "cadence": "one_time",
        "offset": "prepaid"
    }
}
```

### 4. Contract Creation Response
```json
{
    "id": "cont_12345",
    "status": "active",
    "name": "Annual Contract 2024",
    "description": "Annual contract with varying product phases",
    "currency": "USD",
    "start_date": "2024-01-01T00:00:00Z",
    "end_date": "2024-12-31T23:59:59Z",
    "customer_id": "cust_12345",
    "phases": [
        {
            "name": "Phase 1 - All Products",
            "description": "January to March with all products",
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": "2024-03-31T23:59:59Z",
            "pricings": [
                // Array of pricing configurations
            ],
            "phase_type": "active"
        },
        {
            "name": "Phase 2 - Excluding Platform Fee",
            "description": "April to December without Monthly Platform Fee",
            "start_date": "2024-04-01T00:00:00Z",
            "end_date": "2024-12-31T23:59:59Z",
            "pricings": [
                // Array of pricing configurations
            ],
            "phase_type": "active"
        }
    ],
    "renewal_policy": "renew_with_default_contract"
}
```

## Error Handling

The script includes comprehensive error handling:

1. **API Errors**
   - HTTP errors are caught and logged
   - Response content is printed for debugging
   - Appropriate error messages are displayed

2. **Validation**
   - Checks for successful product creation before pricing
   - Validates product creation before contract creation
   - Ensures required parameters are provided

3. **Common Issues**
   - Invalid API credentials
   - Network connectivity problems
   - Invalid request payloads
   - Missing required fields

## Best Practices

1. **Security**
   - Use environment variables for credentials
   - Never hardcode sensitive information
   - Use HTTPS for all API calls

2. **Error Handling**
   - Always check API responses
   - Log errors appropriately
   - Provide meaningful error messages

3. **Code Organization**
   - Use clear method names
   - Document code with docstrings
   - Follow PEP 8 style guide

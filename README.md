# Zenskar API Integration Script

## Overview
This Python script demonstrates integration with the Zenskar API to programmatically create customers, products, and contracts. It implements a specific use case with three different types of products and a phased contract structure.

## Products Created
1. **One Time Fee**
   - Type: Subscription Fee
   - Billing: Prepaid
   - Frequency: One-time
   - Price: $5,000
   - Pricing Type: Flat fee

2. **Monthly Platform Fee**
   - Type: Subscription Fee
   - Billing: Postpaid
   - Frequency: Monthly
   - Price: $10,000
   - Pricing Type: Flat fee
   - Special Condition: Only active for first 3 months (Jan-Mar 2024)

3. **Monthly User Fee**
   - Type: Usage Fee
   - Billing: Postpaid
   - Frequency: Monthly
   - Price: $60 per user
   - Pricing Type: Per-unit pricing
   - Quantity: Configurable via command line argument

## Contract Structure
The script creates a contract with two phases:
1. **Phase 1 (January - March 2024)**
   - Includes all three products
   - Duration: 3 months

2. **Phase 2 (April - December 2024)**
   - Includes One Time Fee and Monthly User Fee
   - Excludes Monthly Platform Fee
   - Duration: 9 months

## Prerequisites
- Python 3.7+
- `requests` library
- Zenskar API Key
- Zenskar Organization ID

## Installation
1. Clone the repository
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
Run the script from the command line with the following required arguments:

```bash
python zenskar_api_integration.py --api-key YOUR_API_KEY --organisation-id YOUR_ORG_ID [--user-count USER_COUNT]
```

### Required Arguments
- `--api-key`: Your Zenskar API Key
- `--organisation-id`: Your Zenskar Organization ID

### Optional Arguments
- `--user-count`: Number of users for Monthly User Fee (default: 10)

## Script Workflow
1. Creates a customer with default details:
   - Name: "Example Customer"
   - Phone: "+1234567890"
   - Address: "123 Frost Street"

2. Creates three products with their respective pricing configurations

3. Creates an active contract that:
   - Starts on January 1st, 2024
   - Ends on December 31st, 2024
   - Has two phases for different product combinations
   - Uses appropriate pricing types for each product

## Error Handling
- The script includes comprehensive error handling for API requests
- Prints detailed error messages and API response content
- Validates successful creation of products before proceeding to contract creation

## API Documentation
For more details about the Zenskar API, refer to:
- [Zenskar Documentation](https://www.zenskar.com/docs/introduction-to-zenskar)
- [API Reference](https://www.zenskar.com/reference/authentication)

## Troubleshooting
- Ensure you have valid API credentials
- Check your internet connection
- Verify the API endpoints are accessible
- Review the error messages in case of failures

## Security Notes
- Never commit your API key to version control
- Use environment variables or secure credential management for API keys
- The script uses HTTPS for all API calls

## Support
For support:
1. Check the [Zenskar Documentation](https://www.zenskar.com/docs)
2. Contact Zenskar support
3. Open an issue in this repository

## License
[Your License Here]
# Zenskar-assignment

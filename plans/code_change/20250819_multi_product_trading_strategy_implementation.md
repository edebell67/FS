# Multi-Product Trading Strategy Implementation Plan

## Overview
This document outlines the approach to modify the existing live trading strategies to support multiple currency pairs instead of just GBP. The implementation will allow trading across a configurable list of products including EUR, AUD, CHF, and JPY in addition to GBP.

## Implementation Checklist

### 1. Configuration Management
- [ ] Define a global list of tradable products: `PRODUCTS_TO_TRADE = ["gbp", "eur", "aud", "chf", "jpy"]`
- [ ] Create a configuration system that allows specifying products per strategy
- [ ] Update all strategy files to use the new product list instead of hardcoded "gbp"

### 2. API Endpoint Modifications
- [ ] Update `API_ENDPOINT` to support filtering by multiple products or remove product filter to get all products
- [ ] Modify `OPEN_TRADES_ENDPOINT` to handle multiple products
- [ ] Update `get_best_signal_and_price` function to process signals for all products
- [ ] Modify `has_open_trade` function to check open trades for each product separately

### 3. Core Logic Updates
- [ ] Modify the main loop to iterate through each product in `PRODUCTS_TO_TRADE`
- [ ] Update signal selection to work per product
- [ ] Adjust open trade checking to be product-specific
- [ ] Ensure trade execution includes the correct product information

### 4. Data Structure Changes
- [ ] Update data processing functions to handle multiple products
- [ ] Modify data filtering to separate signals by product
- [ ] Ensure price fetching works for all products in the list

### 5. Risk Management
- [ ] Implement product-specific position sizing
- [ ] Add product-specific risk limits
- [ ] Ensure portfolio-level risk controls still function correctly

### 6. Logging and Monitoring
- [ ] Update logging to include product information in all messages
- [ ] Modify log file naming to include product identifiers
- [ ] Ensure monitoring dashboards can track multiple products

### 7. Testing
- [ ] Create test cases for each product
- [ ] Verify that strategies work correctly with multiple concurrent products
- [ ] Test edge cases like API failures for specific products
- [ ] Validate that existing GBP functionality is preserved

### 8. Documentation
- [ ] Update strategy documentation to reflect multi-product support
- [ ] Document the configuration options for product selection
- [ ] Provide examples of how to customize the product list

### 9. Deployment
- [ ] Create deployment scripts that can handle multiple product configurations
- [ ] Implement rollback procedures in case of issues
- [ ] Set up monitoring for all products

## Detailed Implementation Steps

### Step 1: Configuration Management
1. Replace hardcoded `PRODUCT_TO_TRADE = "gbp"` with a list
2. Add configuration loading from a file or environment variables
3. Implement a mechanism to specify which products each strategy should trade

### Step 2: API Endpoint Modifications
1. Update API calls to either fetch data for all products or make separate calls per product
2. Modify data parsing functions to handle multiple products in the response
3. Ensure error handling works correctly when some products have issues

### Step 3: Core Logic Updates
1. Change the main loop to iterate through products
2. For each product:
   - Fetch signals
   - Check for existing open trades
   - Evaluate trade conditions
   - Execute trades if conditions are met
3. Implement proper concurrency controls to avoid conflicts

### Step 4: Data Structure Changes
1. Update data structures to include product information
2. Modify filtering functions to work with product-tagged data
3. Ensure backward compatibility with existing data formats

### Step 5: Risk Management
1. Implement per-product position limits
2. Add portfolio-level risk controls
3. Update stop loss and profit target mechanisms for multiple products

### Step 6: Logging and Monitoring
1. Add product identifiers to all log messages
2. Create separate log files per product or clearly mark product in logs
3. Update monitoring dashboards to track multiple products

### Step 7: Testing
1. Create unit tests for each product
2. Implement integration tests with multiple products
3. Test failure scenarios and recovery procedures
4. Validate performance with concurrent product trading

### Step 8: Documentation
1. Update all strategy documentation
2. Create configuration guides
3. Provide troubleshooting documentation for multi-product scenarios

### Step 9: Deployment
1. Create deployment scripts
2. Implement monitoring and alerting
3. Set up rollback procedures
4. Plan for gradual rollout to minimize risk

## Approval
Please review and approve this implementation plan. Once approved, we can begin working through the checklist systematically.
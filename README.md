# Checkout Payment API Tests

This project contains API tests for the checkout payment endpoint. It was developed as part of the Digipay QA practical task.

The tests cover three payment methods:

- Online payment
- Wallet
- BNPL (Buy Now, Pay Later)

The API response is checked for required fields, data types, payment method availability, and BNPL option rules.

## Tools

- Python
- Playwright API (`APIRequestContext`)
- Pytest
- Pytest-BDD
- Gherkin
- Pytest-HTML

## Project Structure

```text
digipay-checkout-api-automation/
├── apis/
│   └── payment_client.py
├── features/
│   └── checkout_payment.feature
├── mock_server/
│   └── server.py
├── reports/
├── steps/
│   └── checkout_steps.py
├── validators/
│   └── payment_validator.py
├── testdata/
├── .github/
│   └── workflows/
│       └── ci.yml
├── conftest.py
├── .env.example
├── pytest.ini
├── requirements.txt
└── README.md
```

## Test Environment

A local fake API server is used to provide the payment responses. This makes it possible to test different response conditions without connecting to the actual Digipay service.

**Base URL:**

```text
http://localhost:8080
```

**Endpoint:**

```http
GET /payment/?CellNumber=09123456789
```

The `CellNumber` parameter is sent as a query parameter in this implementation. The `scenario` parameter is used internally by the fake server to return specific test data.

## Setup

Python 3.12 is recommended and was used for testing.

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

Default environment variables:

```env
BASE_URL=http://localhost:8080
CELL_NUMBER=09123456789
```

## Running the Tests

First, start the fake API server:

```powershell
python mock_server/server.py
```

Keep the server running and open another terminal.

Run the tests:

```powershell
pytest
```

## Test Scenarios

The feature file contains 16 scenarios covering:

- Successful payment methods response
- Blocked BNPL payment method
- Insufficient credit
- Inactive BNPL options
- Multiple default options
- Missing required fields
- Incorrect data types
- HTTP errors
- Non-success response status
- Missing wallet source ID
- Missing BNPL options
- Invalid price type
- Empty payment methods
- Empty options for a clickable BNPL method

For negative scenarios, the test passes when the validator detects the expected error.

## Test Report

An HTML report is generated after each test run:

```text
reports/report.html
```

Open the file in a browser to see the test results.

## Notes

- The fake server is used only for local testing.
- No real payment is processed.
- Bank redirection, OTP, and payment settlement are not covered.
- The `scenario` parameter is only for generating test responses in the fake server.

## Test Result

Latest local execution: **16 passed**.
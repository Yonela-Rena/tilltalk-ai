# TillTalk AI

**An AI-powered price lookup assistant for supermarket cashiers.**

TillTalk AI is a prototype designed to help supermarket cashiers retrieve product prices using natural-language queries. It combines AI-powered query understanding with structured product resolution and database-backed price validation.

The project is inspired by a real checkout problem: cashiers may need to leave the till to check the price of a product that a customer wants to purchase.

**Data disclaimer:** TillTalk uses a synthetic product catalogue for demonstration. It is not connected to SPAR's internal systems or databases.

## Features

* Natural-language product price queries
* AI-based extraction of product names, brands and sizes
* Product resolution using product names and sizes
* Store-specific product availability and pricing
* Promotion-aware price lookup
* Clarification when a product has multiple possible sizes
* Handling of unknown products and unavailable sizes
* REST API built with FastAPI
* SQLite database for products, stores, prices and promotions
* Automated tests for core price lookup and resolution logic

## Architecture

```text
Cashier Query
     |
     v
AI Query Understanding
     |
     v
Product Resolution
     |
     v
SQLite Product Catalogue
     |
     v
Price and Promotion Validation
     |
     v
Structured API Response
```

**Core design principle:** AI interprets the request; the database is the source of truth for prices. The AI does not generate or guess product prices.

## Technology Stack

* Python
* FastAPI
* SQLite
* Pydantic
* Google Gemini API
* python-dotenv
* pytest
* Git and GitHub

## Getting Started

### Prerequisites

* Python 3.13 or a compatible Python version
* A Google Gemini API key for AI-powered query understanding

### 1. Clone the repository

```bash
git clone https://github.com/Yonela-Rena/tilltalk-ai.git
cd tilltalk-ai
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and add your own Gemini API key using the variable name expected by `app/query_parser.py`.

Do not commit `.env` or publish your API key.

### 5. Initialise the database

```powershell
python -m app.database
python -m app.seed_data
```

These commands create the database tables and load the synthetic demonstration data.

### 6. Start the API

```powershell
python -m uvicorn app.main:app --reload
```

Open the following URLs in your browser:

* API root: `http://127.0.0.1:8000/`
* Health check: `http://127.0.0.1:8000/health`
* Interactive API documentation: `http://127.0.0.1:8000/docs`

## Example Query

A cashier could ask:

> How much is 200ml of Apple Purity?

TillTalk extracts the product and size, resolves them against the catalogue, and retrieves the applicable price from the database.

The response depends on the demonstration data and the date of the query. Prices shown by this prototype are not real supermarket prices.

## Testing

Run the automated test suite:

```powershell
python -m pytest
```

The current development milestone has **9 passing automated tests** covering product resolution, size handling, store-specific prices, promotions and query outcomes.

## Roadmap

* Improve product retrieval with semantic search and confidence scoring
* Add speech-to-text for voice queries
* Add text-to-speech for spoken responses
* Build an administration dashboard for product and price management
* Support promotion management and price history
* Add query logging and retrieval evaluation metrics
* Containerise the application with Docker
* Publish a demonstration and evaluation results

## Data and Limitations

The product catalogue, barcodes and prices are synthetic examples created for this prototype. They are not authoritative retail information.

TillTalk is a development prototype. It is not integrated with any supermarket's internal pricing, stock or point-of-sale systems.

## Author

**Yonela Mhloluvele**

Aspiring AI Engineer | Computer Science & Chemistry

GitHub: [Yonela-Rena](https://github.com/Yonela-Rena)


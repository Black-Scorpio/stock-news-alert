# Stock Price Monitor and News Alert

## Description

This Python script monitors the daily stock prices of a specified company using the Alpha Vantage API. If a significant change (greater than 5%) in the closing price is detected compared to the previous day, it fetches the latest news articles related to the company from the News API. The script then sends the top 3 news headlines and descriptions via SMS using the Twilio API.

## Features

- Monitors daily stock prices using the Alpha Vantage API.
- Detects significant changes in stock prices.
- Fetches the latest news articles related to the company from the News API.
- Sends news headlines and descriptions via SMS using the Twilio API.
- Uses a `.env` file to securely store sensitive information.

## Requirements

- Python 3.x
- `requests` library
- `twilio` library
- `python-dotenv` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Black-Scorpio/stock-news-alert
    cd stock-news-alert
    ```

2. Create a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

3. Install the required packages:
    ```sh
    pip install requests twilio python-dotenv
    ```

4. Create a `.env` file in the project directory and add your API keys and tokens:
    ```plaintext
    ALPHA_API_KEY=your_alpha_api_key
    NEWS_API_KEY=your_news_api_key
    TWILIO_ACCOUNT_SID=your_twilio_account_sid
    TWILIO_AUTH_TOKEN=your_twilio_auth_token
    TWILIO_PHONE_NUMBER=your_twilio_phone_number
    MY_PHONE_NUMBER=your_phone_number
    ```

## Usage

1. Run the script:
    ```sh
    python main.py
    ```

2. The script will monitor the stock prices and send SMS alerts if significant changes are detected.



import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Constants for stock and company information
STOCK_NAME = "NVDA"
COMPANY_NAME = "NVIDIA"

# API endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# API keys and credentials from environment variables
ALPHA_API_KEY = os.getenv('ALPHA_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
MY_PHONE_NUMBER = os.getenv('MY_PHONE_NUMBER')

# Function to fetch stock data from Alpha Vantage
def fetch_stock_data(stock_name):
    stock_url = f'{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={stock_name}&apikey={ALPHA_API_KEY}'
    response = requests.get(stock_url)
    data = response.json()
    return data.get('Time Series (Daily)', {})

# Function to calculate the percentage difference between two values
def calculate_percentage_difference(value1, value2):
    difference = value1 - value2
    percentage_difference = (abs(difference) / value2) * 100
    return percentage_difference, difference

# Function to fetch news articles related to a company
def fetch_news(company_name):
    news_url = f'{NEWS_ENDPOINT}?q={company_name}&apiKey={NEWS_API_KEY}'
    response = requests.get(news_url)
    data = response.json()
    return data['articles']

# Function to send messages via Twilio
def send_twilio_messages(messages):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    for message in messages:
        msg = client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=MY_PHONE_NUMBER
        )
        print(f"Message sent: {msg.sid}")

# Main script logic
def main():
    # Fetch stock data
    time_series_daily = fetch_stock_data(STOCK_NAME)
    dates = sorted(time_series_daily.keys(), reverse=True)

    # Check if we have enough data
    if len(dates) < 2:
        print("Not enough data to compare stock prices.")
        return

    # Get closing prices for the last two days
    yesterday_close = float(time_series_daily[dates[0]]['4. close'])
    day_before_yesterday_close = float(time_series_daily[dates[1]]['4. close'])

    # Calculate percentage difference in closing prices
    percentage_difference, difference = calculate_percentage_difference(yesterday_close, day_before_yesterday_close)
    direction_symbol = "↑" if difference > 0 else "↓"

    # Print out the company name, closing prices, dates, and the percentage difference
    print(f"Company: {COMPANY_NAME} ({STOCK_NAME})")
    print(f"Yesterday's close on {dates[0]}: {yesterday_close}")
    print(f"Day before yesterday's close on {dates[1]}: {day_before_yesterday_close}")
    print(f"Percentage difference: {percentage_difference:.2f}% {direction_symbol}")

    # If the percentage difference is greater than 5%, fetch and send news articles
    if percentage_difference > 5:
        print("Significant change in stock price detected. Fetching news articles...")

        # Fetch news articles related to the company
        articles = fetch_news(COMPANY_NAME)

        # Get the first 3 articles
        first_3_articles = articles[:3]

        # Create a list of messages with headlines and descriptions
        articles_list = [
            f"Headline: {article['title']}\nDescription: {article['description']}"
            for article in first_3_articles
        ]

        # Send the articles via Twilio
        send_twilio_messages(articles_list)
    else:
        print("No significant change in stock price.")

# Run the main script
if __name__ == "__main__":
    main()

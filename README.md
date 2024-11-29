
# MEXC Spot Trading Bot

A high-performance, customizable bot for spot trading on the MEXC Exchange. The bot utilizes technical indicators such as **MACD** and **ATR** for automated trading of selected crypto pairs. Designed for **quick execution** and **dynamic trailing stops**, it optimizes trade management with the goal of maximizing profits while minimizing risks.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Setup](#setup)
    1. [Clone the Repository](#clone-the-repository)
    2. [Install Dependencies](#install-dependencies)
    3. [Configuration](#configuration)
    4. [API Key Setup](#api-key-setup)
5. [Usage](#usage)
6. [How it Works](#how-it-works)
7. [Bot Logic](#bot-logic)
8. [License](#license)

---

## Overview

This **spot trading bot** is designed to automate cryptocurrency trading using the **MEXC Exchange**. It monitors a list of selected crypto pairs, calculates **MACD** and **ATR**, and uses these indicators to make buy or sell decisions. The bot implements a **dynamic trailing stop** strategy to lock in profits and mitigate losses as market conditions change.

---

## Features

- **Automated Spot Trading**: Execute buy and sell orders based on live market data.
- **Customizable Trading Pairs**: Trade multiple crypto pairs like PEPE/USDT, DOGE/USDT, BNB/USDT, etc.
- **Technical Indicators**: Uses **MACD** and **ATR** to guide trading decisions.
- **Dynamic Trailing Stop**: Adjusts the trailing stop dynamically to lock in profits as prices increase.
- **Real-time Trading**: Designed for high-frequency trading with a 1-minute timeframe.
- **Risk Management**: Limits the size of trades to a percentage of your available balance.

---

## Requirements

- Python 3.7+
- [ccxt](https://github.com/ccxt/ccxt) – Cryptocurrency trading library
- [pandas](https://pandas.pydata.org/) – Data manipulation
- [numpy](https://numpy.org/) – Numerical calculations
- [dotenv](https://pypi.org/project/python-dotenv/) – Environment variable management
- MEXC API keys for access to your account

---

## Setup

### Clone the Repository

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/mexc-spot-trading-bot.git
cd mexc-spot-trading-bot
```

### Install Dependencies

Use `pip` to install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

### Configuration

The bot requires an **API key** and **secret key** for interacting with the MEXC Exchange. These keys should be stored in an `.env` file for security.

Create a `.env` file in the root directory and add your API credentials:

```
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

> **Important:** Ensure your `.env` file is **not** uploaded to GitHub. It should be ignored in your `.gitignore`.

### API Key Setup

1. Go to the [MEXC API management](https://www.mexc.com) page.
2. Create an API key with **spot trading permissions**.
3. Copy the API key and secret and store them in your `.env` file.

---

## Usage

Once the setup is complete, you can run the bot by executing the `script.py` file:

```bash
python script.py
```

The bot will begin trading the predefined crypto pairs based on the strategy outlined in the code.

### Key Parameters

You can adjust the following parameters directly in the script for better control over the trading behavior:

- **CRYPTO_PAIRS**: The list of pairs the bot will trade (e.g., `['PEPE/USDT', 'BNB/USDT']`).
- **TRADE_SIZE_PERCENT**: The percentage of your available balance to use for each trade (default is `0.1` or 10%).
- **ATR_MULTIPLIER**: The multiplier used to calculate the trailing stop (default is `2`).
- **MAX_TRADES**: The maximum number of open trades at a time.
- **TRADE_COOLDOWN**: The cooldown period (in seconds) between checks for new signals.

---

## How it Works

1. **Data Fetching**: The bot fetches historical price data (OHLCV) for the selected trading pairs.
2. **Indicator Calculation**:
   - **MACD**: The bot calculates the **MACD** (Moving Average Convergence Divergence) indicator to identify buy/sell signals.
   - **ATR**: The **Average True Range** (ATR) is calculated to determine the **volatility** of the market and set trailing stops.
3. **Signal Generation**: 
   - If the MACD crosses above the signal line, a **buy signal** is generated.
   - The bot dynamically adjusts a **trailing stop** based on ATR, locking in profits as the price moves higher.
4. **Trade Execution**: The bot places buy or sell orders when conditions are met, and monitors the position for potential closing based on trailing stops.

---

## Bot Logic

1. **Initialize Portfolio**: The bot loads your available balance and configures the initial trading parameters.
2. **Buy Signal**: The bot checks for a **buy signal** when the MACD line crosses above the signal line.
3. **Trade Management**: When a position is open:
   - The bot dynamically calculates a **trailing stop** based on the ATR.
   - If the price falls below the trailing stop, a **sell order** is triggered.
4. **Risk Management**: The bot limits the size of each trade and ensures it does not exceed a specified percentage of your available balance.

---

## License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## Contributions

Contributions are welcome! If you'd like to suggest improvements or report bugs, please create a pull request or open an issue. 

---


### Notes

- The bot is **not** guaranteed to make a profit. Use at your own risk and start with small amounts to test.
- Be sure to monitor your bot regularly and adjust settings as needed.

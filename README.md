# Financial Engineering Application: Simple Guide

This app offers three main features to help you understand and test stock trading strategies:

## 1. Simple Backtest

This feature shows you how well a trading strategy would have performed in the past. It adapts to different risk levels (Low, Medium, High) which change how the strategy buys and sells stocks.

### How it works:

- The app looks at two things: moving averages (MA) and the Relative Strength Index (RSI).
- It buys stocks when:
  - The short-term average price goes above the long-term average, or
  - The RSI (a measure of price momentum) falls below a certain point.
- It sells stocks when:
  - The short-term average falls below the long-term average, or
  - The RSI goes above a certain point.
- It also uses a "stop-loss" to limit potential losses.

### Risk Levels:

- Low Risk: Plays it safe with longer observation periods and smaller stop-losses.
- Medium Risk: A balance between safety and potential gains.
- High Risk: More aggressive, with shorter observation periods and larger stop-losses.

The app shows you how this strategy would have performed, considering your initial investment and trading fees.

## 2. Black-Scholes Model (With Stock Data)

This feature helps estimate the value of stock options (bets on future stock prices).

- It uses real stock data to calculate how much the stock price tends to change (volatility).
- It creates a 3D graph showing how the option's value changes based on:
  - The current stock price
  - How long until the option expires
  - The agreed-upon future stock price (strike price)

## 3. Black-Scholes Model (Without Stock Data)

Similar to the previous feature, but for when you don't have real stock data:

- You manually input the stock price and how much you think it might change (volatility).
- It then creates the same type of 3D graph to help you understand potential option values.

This app helps you visualize and understand different aspects of stock trading and option pricing, from testing trading strategies to estimating option values.
import yfinance as yf
import pandas as pd
import numpy as np

# 1. Fetch 6 months of data
stock = yf.Ticker("RELIANCE.NS")
df = stock.history(period="6mo", interval="1d")

# 2. RSI Calculation (14-Day)
delta = df["Close"].diff()
gains = delta.where(delta > 0, 0).rolling(window=14).mean()
losses = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gains / (losses + 1e-9)
df["RSI"] = 100 - (100 / (1 + rs))

# 3. Daily Returns Calculation
df["Daily_Return"] = df["Close"].pct_change()
clean_returns = df["Daily_Return"].dropna()

# 4. Volatility & 95% VaR
annual_volatility = clean_returns.std() * np.sqrt(252) * 100
var_95_daily = np.percentile(clean_returns, 5) * 100  # 5th percentile = 95% confidence

# 5. Extract Latest Values
latest_price = df["Close"].iloc[-1]
latest_rsi = df["RSI"].iloc[-1]

print("=" * 45)
print("📊 BULLSEYE QUANT ENGINE - METRIC TEST")
print("=" * 45)
print(f"Ticker:               RELIANCE.NS")
print(f"Current Price:        ₹{latest_price:.2f}")
print(f"14-Day RSI:           {latest_rsi:.2f}")
print(f"Annual Volatility:    {annual_volatility:.2f}%")
print(f"95% Daily VaR:        {var_95_daily:.2f}% (Max expected 1-day drop)")
print("=" * 45)
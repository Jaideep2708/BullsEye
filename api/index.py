from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd
import numpy as np

app = FastAPI(title="BullsEye Quant Engine")

# Allow browser frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/analyze")
def analyze(ticker: str = Query(..., description="Stock symbol, e.g. RELIANCE.NS, NVDA")):
    try:
        symbol = ticker.strip().upper()
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo", interval="1d")

        if df.empty or len(df) < 30:
            raise HTTPException(status_code=404, detail="Invalid ticker or insufficient data.")

        df = df.reset_index()
        close = df["Close"]

        # 1. RSI (14-day)
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        df["RSI"] = 100 - (100 / (1 + rs))

        # 2. EMAs (20-day vs 50-day)
        df["EMA_20"] = close.ewm(span=20, adjust=False).mean()
        df["EMA_50"] = close.ewm(span=50, adjust=False).mean()

        # 3. Volatility & 95% VaR
        returns = close.pct_change().dropna()
        annual_volatility = float(returns.std() * np.sqrt(252) * 100)
        var_95 = float(np.percentile(returns, 5) * 100)

        # 4. Latest data extraction
        latest_price = float(close.iloc[-1])
        prev_price = float(close.iloc[-2])
        change_pct = float(((latest_price - prev_price) / prev_price) * 100)
        latest_rsi = float(df["RSI"].iloc[-1])
        latest_ema20 = float(df["EMA_20"].iloc[-1])
        latest_ema50 = float(df["EMA_50"].iloc[-1])

        # 5. Algorithmic Decision Engine
        if latest_rsi < 35 and latest_ema20 > latest_ema50:
            verdict = "STRONG BUY"
            verdict_class = "buy"
        elif latest_rsi > 70:
            verdict = "OVERBOUGHT / TRIM"
            verdict_class = "sell"
        elif latest_ema20 > latest_ema50:
            verdict = "BULLISH TREND"
            verdict_class = "buy"
        else:
            verdict = "NEUTRAL / HOLD"
            verdict_class = "neutral"

        # 6. Chart history (last 30 trading days)
        chart_data = df.tail(30)
        dates = [d.strftime("%b %d") for d in chart_data["Date"]]
        prices = [round(float(p), 2) for p in chart_data["Close"]]
        ema20_vals = [round(float(e), 2) for e in chart_data["EMA_20"]]

        return {
            "symbol": symbol,
            "current_price": round(latest_price, 2),
            "change_pct": round(change_pct, 2),
            "verdict": verdict,
            "verdict_class": verdict_class,
            "metrics": {
                "rsi": round(latest_rsi, 2),
                "annual_volatility": round(annual_volatility, 2),
                "var_95": round(var_95, 2),
                "ema_20": round(latest_ema20, 2),
                "ema_50": round(latest_ema50, 2)
            },
            "chart": {
                "labels": dates,
                "prices": prices,
                "ema20": ema20_vals
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import yfinance as yf
import pandas as pd
import numpy as np
import os

app = FastAPI(title="BullsEye Quant Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. API Route
@app.get("/api/analyze")
def analyze(ticker: str = Query(..., description="Stock symbol, e.g. RELIANCE.NS, NVDA")):
    try:
        symbol = ticker.strip().upper()
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo", interval="1d")

        if df.empty or len(df) < 30:
            raise HTTPException(status_code=404, detail="Invalid ticker or insufficient data.")

        df = df.reset_index()
        close = df["Close"]

        # RSI (14-day)
        delta = close.diff()
        gain = delta.where(delta > 0, 0).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / (loss + 1e-9)
        df["RSI"] = 100 - (100 / (1 + rs))

        # EMAs
        df["EMA_20"] = close.ewm(span=20, adjust=False).mean()
        df["EMA_50"] = close.ewm(span=50, adjust=False).mean()

        # Risk Metrics
        returns = close.pct_change().dropna()
        annual_volatility = float(returns.std() * np.sqrt(252) * 100)
        var_95 = float(np.percentile(returns, 5) * 100)

        latest_price = float(close.iloc[-1])
        prev_price = float(close.iloc[-2])
        change_pct = float(((latest_price - prev_price) / prev_price) * 100)
        latest_rsi = float(df["RSI"].iloc[-1])
        latest_ema20 = float(df["EMA_20"].iloc[-1])
        latest_ema50 = float(df["EMA_50"].iloc[-1])

        # Algorithmic Verdict
        if latest_rsi < 35 and latest_ema20 > latest_ema50:
            verdict = "STRONG BUY"
            verdict_class = "buy"
        elif latest_rsi > 70:
            verdict = "OVERBOUGHT / TRIM"
            verdict_class = "sell"
        elif latest_ema20 > latest_ema50:
            verdict = "BULLISH TREND"
            verdict_class = "buy"
        else:
            verdict = "NEUTRAL / HOLD"
            verdict_class = "neutral"

        chart_data = df.tail(30)
        dates = [d.strftime("%b %d") for d in chart_data["Date"]]
        prices = [round(float(p), 2) for p in chart_data["Close"]]
        ema20_vals = [round(float(e), 2) for e in chart_data["EMA_20"]]

        return {
            "symbol": symbol,
            "current_price": round(latest_price, 2),
            "change_pct": round(change_pct, 2),
            "verdict": verdict,
            "verdict_class": verdict_class,
            "metrics": {
                "rsi": round(latest_rsi, 2),
                "annual_volatility": round(annual_volatility, 2),
                "var_95": round(var_95, 2),
                "ema_20": round(latest_ema20, 2),
                "ema_50": round(latest_ema50, 2)
            },
            "chart": {
                "labels": dates,
                "prices": prices,
                "ema20": ema20_vals
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 2. Serve Frontend
@app.get("/")
def serve_home():
    return FileResponse("public/index.html")
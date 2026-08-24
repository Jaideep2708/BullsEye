# BullsEye 🎯 — Quantitative Stock Screener & Risk Analytics Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?logo=vercel&logoColor=white)](https://vercel.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**BullsEye** is a full-stack, serverless quantitative analysis platform designed to screen equities in real time across international (US) and Indian (NSE/BSE) markets. It integrates mathematical momentum models, trend-following filters, and parametric downside risk analytics via a lightweight, high-performance web dashboard.

---

## 🚀 Live Demo

- **Production Deployment:** [https://bullseye.vercel.app](https://bullseye.vercel.app) *(Replace with your live Vercel URL)*
- **Interactive Swagger API Docs:** `https://<your-vercel-domain>/docs`

---

## 📊 Quantitative Mechanics & Financial Math

BullsEye processes historical market data to calculate key technical and risk parameters:

### 1. Relative Strength Index (14-Period RSI)
Measures the magnitude and speed of directional price changes:

$$\text{RS} = \frac{\text{EMA}_{14}(\text{Upward Gains})}{\text{EMA}_{14}(\text{Downward Losses})}$$

$$\text{RSI} = 100 - \left( \frac{100}{1 + \text{RS}} \right)$$

- **RSI > 70:** Overbought condition (high risk of mean reversion).
- **RSI < 30:** Oversold condition (potential accumulation/reversal zone).

### 2. Exponential Moving Averages (20 EMA vs. 50 EMA)
Unlike Simple Moving Averages (SMA), EMAs apply exponentially decreasing weight to older prices, minimizing signal lag:

$$\text{EMA}_t = \left( \text{Close}_t \times \alpha \right) + \left( \text{EMA}_{t-1} \times (1 - \alpha) \right) \quad \text{where} \quad \alpha = \frac{2}{N + 1}$$

- **Bullish Bias:** Fast EMA ($20$) > Slow EMA ($50$).
- **Bearish Bias:** Fast EMA ($20$) < Slow EMA ($50$).

### 3. Annualized Volatility ($\sigma_{\text{ann}}$)
Measures standard dispersion of continuous daily percentage returns ($R_t$), scaled across an annual trading horizon ($252$ trading days):

$$\sigma_{\text{ann}} = \text{std}(R_t) \times \sqrt{252} \times 100$$

### 4. 95% Daily Value at Risk (VaR)
A parametric risk metric calculated as the 5th percentile empirical distribution of historical daily returns:

$$\text{VaR}_{0.95} = \text{Percentile}(R, 5)$$

*Interpretation:* With 95% statistical confidence, the maximum portfolio drawdown for a single trading day will not exceed this threshold under normal market conditions.

---

## 🏗️ System Architecture

```text
┌─────────────────┐       GET /api/analyze?ticker=SYMBOL       ┌──────────────────────┐
│                 │ ─────────────────────────────────────────> │                      │
│ Vanilla JS +    │                                            │ FastAPI Backend      │
│ Chart.js UI     │ <───────────────────────────────────────── │ (Serverless Runtime) │
│                 │          JSON Response (Metrics & OHLCV)   └──────────┬───────────┘
└─────────────────┘                                                       │
                                                                          │ Fetch OHLCV
                                                                          ▼
                                                               ┌──────────────────────┐
                                                               │ Yahoo Finance API    │
                                                               └──────────────────────┘
```

---

## 📁 Repository Structure

```text
BullsEye/
├── api/
│   └── index.py            # FastAPI backend with analytical endpoints
├── public/
│   └── index.html          # Responsive Chart.js client dashboard
├── .gitignore              # Ignored files (venv, caches, env)
├── requirements.txt        # Production Python dependencies
├── vercel.json             # Vercel serverless routing rewrite rules
└── test_data.py            # Standalone financial math verification script
```

---

## 🛠️ Local Development Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/Jaideep2708/BullsEye.git](https://github.com/Jaideep2708/BullsEye.git)
cd BullsEye
```

### 2. Set Up Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Local Development Server
```bash
uvicorn api.index:app --reload --port 8000
```

Access the UI at `http://127.0.0.1:8000` and API documentation at `http://127.0.0.1:8000/docs`.

---

## 🌐 API Reference

### `GET /api/analyze`

#### Query Parameters:
- `ticker` (string, required): The target stock symbol (e.g., `RELIANCE.NS`, `TCS.NS`, `NVDA`, `AAPL`).

#### Response Example (`200 OK`):
```json
{
  "symbol": "RELIANCE.NS",
  "current_price": 1309.80,
  "change_pct": -0.47,
  "verdict": "NEUTRAL / HOLD",
  "verdict_class": "neutral",
  "metrics": {
    "rsi": 57.01,
    "annual_volatility": 22.54,
    "var_95": -2.17,
    "ema_20": 1311.19,
    "ema_50": 1311.99
  },
  "chart": {
    "labels": ["Jul 14", "Jul 15", "Jul 16", "..."],
    "prices": [1293.0, 1295.5, 1296.6, "..."],
    "ema20": [1303.34, 1302.59, 1302.02, "..."]
  }
}
```

---

## 📜 License

This project is open-source under the [MIT License](LICENSE).
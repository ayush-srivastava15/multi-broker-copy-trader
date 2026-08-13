
# 🦅 Multi-Broker Copy Trading Engine & Quant Dashboard

An ultra-low latency, multi-threaded Copy Trading Engine designed to replicate orders from a **Master Broker (Zerodha)** to multiple **Child Accounts (Zerodha, Angel One, Upstox)** in real-time. Paired with a sci-fi styled **Streamlit Command Center** for real-time portfolio metrics, risk analysis, and execution tracking.

---

## ⚡ Key Features

* **Multi-Threaded Order Execution:** Uses Python's `ThreadPoolExecutor` for parallel execution across all child brokers in milliseconds.
* **Smart Token Mapping:** Automatic downloading and local caching of Angel One's instrument token master JSON (`NSE` & `NFO`).
* **Multi-Broker Architecture:** Supports Zerodha (Kite Connect), Angel One (SmartAPI with TOTP 2FA), and Upstox API integrations.
* **Sci-Fi Analytics Dashboard:** Live Streamlit-based UI displaying:
  * Consolidated real-time P&L
  * Execution latency metrics
  * Win-rate analytics & visual performance charts (Plotly)
  * Account-level status monitoring
* **Secure Environment Design:** Built-in `.env` security to ensure zero exposure of API keys, client codes, or TOTP secrets.

---

## 🏗️ System Architecture

```text
       ┌─────────────────────────┐
       │   Zerodha Master Account│
       └────────────┬────────────┘
                    │
            [Order Executed]
                    │
                    ▼
     ┌──────────────────────────────┐
     │  Copy Trading Engine (Python)│
     └──────────────┬───────────────┘
                    │
     ┌──────────────┼──────────────┐
     │ (ThreadPool) │ (ThreadPool) │
     ▼              ▼              ▼
┌─────────┐   ┌───────────┐   ┌──────────┐
│ Zerodha │   │ Angel One │   │  Upstox  │
│ Child 1 │   │  Child 1  │   │  Child 1 │
└─────────┘   └───────────┘   └──────────┘
🛠️ Tech Stack
Language: Python 3.10+

Frameworks & Libraries: Streamlit, Pandas, Plotly, PyOTP, Requests

Broker APIs: kiteconnect, SmartApi

Concurrency: concurrent.futures.ThreadPoolExecutor

Configuration: python-dotenv

🚀 Getting Started

1. Prerequisites
Ensure you have Python 3.9+ installed along with valid API credentials for your broker accounts.

2. Installation
Clone the repository and install dependencies:

Bash
git clone [https://github.com/ayush-srivastava15/multi-broker-copy-trader.git](https://github.com/ayush-srivastava15/multi-broker-copy-trader.git)
cd multi-broker-copy-trader

pip install -r requirements.txt

(Create a requirements.txt file in your repository with: kiteconnect, smartapi-python, streamlit, pandas, plotly, pyotp, python-dotenv, requests)

3. Environment Setup
Copy .env.example to .env and fill in your API credentials:


Bash
cp .env.example .env
Edit your .env file:

Code snippet:

ZERODHA_MASTER_API_KEY=your_zerodha_master_api_key
ZERODHA_CHILD_1_API_KEY=your_child_api_key
ANGEL_1_API_KEY=your_angel_api_key
ANGEL_1_CLIENT_CODE=your_client_code
ANGEL_1_PASSWORD=your_mpin
ANGEL_1_TOTP_SECRET=your_totp_secret

💻 Running the Application
Start the Execution Engine:

Bash
python super_trade.py
Launch the Analytics Dashboard:
Bash
streamlit run dashboard_pro.py
🔒 Security & Best Practices
.gitignore Enabled: Credentials and API keys are explicitly excluded from source control.

Non-Custodial Logic: Trade execution is managed via session tokens generated on runtime.

👨‍💻 Author
Ayush Srivastava

GitHub: @ayush-srivastava15

LinkedIn: [(https://www.linkedin.com/in/ayush-kumar-411359402/)]

Disclaimer: This software is built for educational and algorithmic research purposes. Ensure compliance with exchange guidelines before deploying in live environments.

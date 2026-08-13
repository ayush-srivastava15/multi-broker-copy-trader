import logging
import time
import threading
import os
import requests
import pyotp
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from kiteconnect import KiteConnect
from SmartApi import SmartConnect

# Load Environment Variables from .env file
load_dotenv()

# --- CONFIGURATION SECTION (Fetched safely from Environment) ---
ZERODHA_MASTER = {
    "name": "👑 MASTER", 
    "api_key": os.getenv("ZERODHA_MASTER_API_KEY", "YOUR_ZERODHA_MASTER_API_KEY")
}

ZERODHA_CHILDREN = [
    {"name": "⚡ Z_Child_1", "api_key": os.getenv("ZERODHA_CHILD_1_API_KEY", "YOUR_CHILD_1_API_KEY")},
    {"name": "⚡ Z_Child_2", "api_key": os.getenv("ZERODHA_CHILD_2_API_KEY", "YOUR_CHILD_2_API_KEY")}
]

UPSTOX_ACCOUNTS = [
    {"name": "🚀 Upstox_1", "api_key": os.getenv("UPSTOX_1_API_KEY", "YOUR_UPSTOX_API_KEY")}
]

ANGEL_ACCOUNTS = [
    {
        "name": "💎 Angel_1", 
        "api_key": os.getenv("ANGEL_1_API_KEY", "YOUR_KEY"), 
        "client_code": os.getenv("ANGEL_1_CLIENT_CODE", "CLIENT_CODE"), 
        "password": os.getenv("ANGEL_1_PASSWORD", "MPIN"), 
        "totp_secret": os.getenv("ANGEL_1_TOTP_SECRET", "TOTP_SECRET_KEY")
    }
]

# --- GLOBAL STORAGE ---
active_sessions = []
angel_token_map = {}

def load_angel_tokens():
    print("⏳ Downloading Angel One Script Master Data...")
    try:
        url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"
        data = requests.get(url).json()
        for item in data:
            if item['exch_seg'] in ['NFO', 'NSE']:
                angel_token_map[item['symbol']] = item['token']
        print(f"✅ Tokens Loaded Successfully! Total Symbols: {len(angel_token_map)}")
    except Exception as e:
        print(f"❌ Failed to load Angel Tokens: {e}")

def connect_angel():
    for acc in ANGEL_ACCOUNTS:
        try:
            smartApi = SmartConnect(api_key=acc['api_key'])
            totp = pyotp.TOTP(acc['totp_secret']).now()
            data = smartApi.generateSession(acc['client_code'], acc['password'], totp)
            if data['status']:
                active_sessions.append({"type": "ANGEL", "api": smartApi, "name": acc['name']})
                print(f"✅ Connected: {acc['name']}")
        except Exception as e:
            print(f"❌ Angel Login Error ({acc['name']}): {e}")

def connect_zerodha_child():
    for acc in ZERODHA_CHILDREN:
        print(f"\n👉 Login Zerodha Child: {acc['name']}")
        kite = KiteConnect(api_key=acc['api_key'])
        print(f"Login URL: {kite.login_url()}")
        token = input(f"Enter Access Token for {acc['name']}: ")
        kite.set_access_token(token)
        active_sessions.append({"type": "ZERODHA", "api": kite, "name": acc['name']})
        print(f"✅ Connected: {acc['name']}")

def place_order_worker(session, symbol, trans_type, qty):
    try:
        if session['type'] == "ANGEL":
            token = angel_token_map.get(symbol)
            if not token:
                print(f"⚠️ Token missing for symbol {symbol}")
                return
            exchange = "NFO" if any(x in symbol for x in ["CE", "PE", "FUT"]) else "NSE"
            orderparams = {
                "variety": "NORMAL", "tradingsymbol": symbol, "symboltoken": token,
                "transactiontype": trans_type, "exchange": exchange, "ordertype": "MARKET",
                "producttype": "INTRADAY", "duration": "DAY", "quantity": qty
            }
            session['api'].placeOrder(orderparams)

        elif session['type'] == "ZERODHA":
            exchange = "NFO" if any(x in symbol for x in ["CE", "PE", "FUT"]) else "NSE"
            session['api'].place_order(
                variety="regular", exchange=exchange, tradingsymbol=symbol,
                transaction_type=trans_type, quantity=qty, product="MIS", order_type="MARKET"
            )

        print(f"🚀 FIRED: {session['name']} | {trans_type} {symbol} | Qty: {qty}")
    except Exception as e:
        print(f"❌ ERROR in {session['name']}: {e}")

def blast_orders(order):
    symbol = order['tradingsymbol']
    trans_type = order['transaction_type']
    qty = order['quantity']
    
    print("\n" + "="*50)
    print(f"🚨 TRADE SIGNAL DETECTED FROM MASTER: {trans_type} {symbol} ({qty} Qty)")
    print("="*50)
    
    with ThreadPoolExecutor() as executor:
        for session in active_sessions:
            executor.submit(place_worker, session, symbol, trans_type, qty)

if __name__ == "__main__":
    print("\n🚀 INITIALIZING COPY TRADER ENGINE...")
    load_angel_tokens()
    connect_angel()
    connect_zerodha_child()
    
    print("\n👑 Connecting Master Account...")
    kite_master = KiteConnect(api_key=ZERODHA_MASTER['api_key'])
    print("Master Login URL: ", kite_master.login_url())
    master_token = input("Enter Master Access Token: ")
    kite_master.set_access_token(master_token)
    
    print("\n✅ SYSTEM ONLINE. Listening for Order Updates...")
    last_id = 0
    try:
        orders = kite_master.orders()
        if orders: last_id = orders[-1]['order_id']
    except: pass
    
    while True:
        try:
            orders = kite_master.orders()
            if orders:
                latest = orders[-1]
                if latest['order_id'] != last_id and latest['status'] == 'COMPLETE':
                    blast_orders(latest)
                    last_id = latest['order_id']
            time.sleep(0.1)
        except Exception as e:
            time.sleep(1)
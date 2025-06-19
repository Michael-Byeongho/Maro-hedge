
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import time

st.set_page_config(page_title="📊 매크로 지표 모니터링", layout="wide")

st.title("📊 매크로 지표 모니터링")

# 관심 종목: 티커와 라벨
tickers = {
    "USD/KRW": "KRW=X",
    "EUR/USD": "EURUSD=X",
    "USD/JPY": "JPY=X",
    "USD/CNY": "CNY=X",
    "DXY": "DX-Y.NYB",
    "LME Copper 3M (예시)": "HG=F",
    "NASDAQ": "^IXIC",
    "S&P 500": "^GSPC",
    "WTI": "CL=F",
    "Brent": "BZ=F"
}

def get_price_change(ticker):
    try:
        data = yf.download(ticker, period="2d", interval="1d", progress=False)
        if len(data) < 2:
            return None, None
        prev_close = data['Close'].iloc[0]
        latest_close = data['Close'].iloc[1]
        pct_change = ((latest_close - prev_close) / prev_close) * 100
        return latest_close, pct_change
    except:
        return None, None

col1, col2, col3 = st.columns(3)
cols = [col1, col2, col3]

i = 0
for label, ticker in tickers.items():
    price, change = get_price_change(ticker)
    if price is not None:
        delta_text = f"{change:.2f}%"
        cols[i % 3].metric(label, f"{price:,.2f}", delta_text)
        i += 1
    else:
        cols[i % 3].metric(label, "N/A", "N/A")
        i += 1

# 1초마다 새로고침
st_autorefresh = st.empty()
st_autorefresh.text(f"⏱️ 마지막 갱신 시각: {datetime.now().strftime('%H:%M:%S')}")
time.sleep(1)


import streamlit as st
import yfinance as yf
import pandas as pd
import ta
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="تحليل الذهب XAU/USD", layout="centered")
st.title("📈 تحليل الذهب XAU/USD (تحديث كل 10 دقائق)")

# تحميل البيانات
@st.cache_data(ttl=600)  # تحديث كل 10 دقائق
def load_data():
    df = yf.download("XAUUSD=X", period="1d", interval="5m")
    df.dropna(inplace=True)
    df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
    df["MACD"] = ta.trend.MACD(df["Close"]).macd_diff()
    df["EMA20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
    df["SMA50"] = ta.trend.SMAIndicator(df["Close"], window=50).sma_indicator()
    return df

df = load_data()

# تحليل آخر شمعة
latest = df.iloc[-1]
rsi = latest["RSI"]
macd = latest["MACD"]
ema = latest["EMA20"]
sma = latest["SMA50"]
price = latest["Close"]

# التحليل الذكي
signals = []
if rsi < 30:
    signals.append("🔵 RSI يشير إلى تشبع بيعي (فرصة شراء)")
elif rsi > 70:
    signals.append("🔴 RSI يشير إلى تشبع شرائي (فرصة بيع)")

if macd > 0:
    signals.append("🟢 MACD إيجابي")
else:
    signals.append("🔴 MACD سلبي")

if ema > sma:
    signals.append("📈 تقاطع إيجابي (EMA > SMA)")
else:
    signals.append("📉 تقاطع سلبي (EMA < SMA)")

# عرض التحليل
st.subheader(f"سعر الذهب الحالي: ${price:.2f}")
st.markdown("### 🧠 نتائج التحليل:")

for s in signals:
    st.markdown(f"- {s}")

# توصية نهائية
if rsi < 30 and macd > 0 and ema > sma:
    st.success("✅ توصية قوية بالشراء (Strong Buy)")
elif rsi > 70 and macd < 0 and ema < sma:
    st.error("❌ توصية قوية بالبيع (Strong Sell)")
else:
    st.warning("⚠️ لا توجد توصية واضحة حالياً")

# توقيت التحديث
st.markdown(f"🔄 تم التحديث في: {datetime.utcnow().strftime('%H:%M:%S')} UTC")

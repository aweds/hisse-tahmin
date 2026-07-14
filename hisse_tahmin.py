import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Hisse Fiyat Aralığı Tahmini", layout="wide")
st.title("📈 Hisse Senedi Fiyat Aralık Tahmin Uygulaması")
st.markdown("6 indikatör ile **1 gün sonrası** ve **1 hafta sonrası** için fiyat aralığı tahmini.")

hisse_kodu = st.text_input("Hisse Kodu (örn: THYAO.IS, GARAN.IS, AAPL):", value="THYAO.IS")
tahmin_tarihi = st.date_input("Tahmin hangi tarih itibarıyla yapılsın? (Son 1 gün öncesi veriler kullanılır)", 
                              value=datetime.today() - timedelta(days=1))

def tum_indikatorleri_hesapla(df):
    kapanis = df['Close']
    yuksek = df['High']
    dusuk = df['Low']
    hacim = df['Volume']
    
    sma_50 = kapanis.rolling(50).mean()
    sma_200 = kapanis.rolling(200).mean()
    
    ema_12 = kapanis.ewm(span=12, adjust=False).mean()
    ema_26 = kapanis.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    sinyal = macd.ewm(span=9, adjust=False).mean()
    macd_hist = macd - sinyal
    
    delta = kapanis.diff()
    kazanc = delta.clip(lower=0)
    kayip = -delta.clip(upper=0)
    ortalama_kazanc = kazanc.rolling(14).mean()
    ortalama_kayip = kayip.rolling(14).mean()
    rs = ortalama_kazanc / ortalama_kayip
    rsi = 100 - (100 / (1 + rs))
    
    sma_20 = kapanis.rolling(20).mean()
    std_20 = kapanis.rolling(20).std()
    bollinger_ust = sma_20 + 2 * std_20
    bollinger_alt = sma_20 - 2 * std_20
    
    high_low = yuksek - dusuk
    high_close = np.abs(yuksek - kapanis.shift())
    low_close = np.abs(dusuk - kapanis.shift())
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    
    yon = np.sign(kapanis.diff()).fillna(0)
    obv = (yon * hacim).cumsum()
    
    indikatorler = pd.DataFrame({
        'Close': kapanis,
        'SMA_50': sma_50,
        'SMA_200': sma_200,
        'MACD': macd,
        'MACD_Sinyal': sinyal,
        'MACD_Hist': macd_hist,
        'RSI': rsi,
        'Bollinger_Ust': bollinger_ust,
        'Bollinger_Alt': bollinger_alt,
        'ATR': atr,
        'OBV': obv
    }, index=df.index)
    return indikatorler

def fiyat_aralik_tahmini(ind_df, son_kapanis, gun_sayisi=1):
    son = ind_df.iloc[-1]
    
    trend_puani = 0
    if son['Close'] > son['SMA_50']: trend_puani += 1
    if son['SMA_50'] > son['SMA_200']: trend_puani += 1
    if son['MACD'] > son['MACD_Sinyal']: trend_puani += 1
    if 50 < son['RSI'] < 70: trend_puani += 1
    if son['OBV'] > ind_df['OBV'].rolling(5).mean().iloc[-1]: trend_puani += 1
    
    if trend_puani >= 3:
        yon = 1
    elif trend_puani <= 1:
        yon = -1
    else:
        yon = 0
    
    gunluk_getiri = ind_df['Close'].pct_change().dropna()
    son_20_gun = gunluk_getiri.tail(20)
    ortalama_getiri = son_20_gun.mean()
    std_getiri = son_20_gun.std()
    
    if gun_sayisi == 1:
        atr_deger = son['ATR']
        tahmini_kapanis = son_kapanis * (1 + ortalama_getiri * yon * 0.5)
        bollinger_genislik = (son['Bollinger_Ust'] - son['Bollinger_Alt']) / son_kapanis
        aralik = atr_deger * 0.8
        yuksek = tahmini_kapanis + aralik/2
        dusuk = tahmini_kapanis - aralik/2
    else:
        atr_haftalik = son['ATR'] * np.sqrt(5)
        haftalik_getiri = son_20_gun.rolling(5).sum().dropna().mean()
        tahmini_kapanis = son_kapanis * (1 + haftalik_getiri * yon * 0.5)
        aralik = atr_haftalik * 0.8
        yuksek = tahmini_kapanis + aralik/2
        dusuk = tahmini_kapanis - aralik/2
    
    min_aralik = son_kapanis * 0.005
    if (yuksek - dusuk) < min_aralik:
        yuksek = tahmini_kapanis + min_aralik/2
        dusuk = tahmini_kapanis - min_aralik/2
    
    return {
        'yon': 'YÜKSELİŞ' if yon==1 else ('DÜŞÜŞ' if yon==-1 else 'YATAY'),
        'tahmini_kapanis': round(tahmini_kapanis, 2),
        'yuksek': round(yuksek, 2),
        'dusuk': round(dusuk, 2),
        'guven_skoru': trend_puani / 5 * 100
    }

if st.button("Tahmini Hesapla"):
    try:
        baslangic = tahmin_tarihi - timedelta(days=365)
        veri = yf.download(hisse_kodu, start=baslangic, end=tahmin_tarihi, progress=False)
        if veri.empty:
            st.error("Hisse bulunamadı veya yeterli veri yok.")
        else:
            ind_df = tum_indikatorleri_hesapla(veri)
            son_gun = ind_df.dropna().iloc[-1]
            son_kapanis = son_gun['Close']
            
            tahmin_gun = fiyat_aralik_tahmini(ind_df.dropna(), son_kapanis, gun_sayisi=1)
            tahmin_hafta = fiyat_aralik_tahmini(ind_df.dropna(), son_kapanis, gun_sayisi=5)
            
            gostergeler = pd.DataFrame({
                'İndikatör': ['SMA 50', 'SMA 200', 'MACD', 'MACD Sinyal', 'RSI', 
                              'Bollinger Üst', 'Bollinger Alt', 'ATR', 'OBV'],
                'Son Değer': [round(son_gun['SMA_50'],2), round(son_gun['SMA_200'],2),
                              round(son_gun['MACD'],2), round(son_gun['MACD_Sinyal'],2),
                              round(son_gun['RSI'],2), round(son_gun['Bollinger_Ust'],2),
                              round(son_gun['Bollinger_Alt'],2), round(son_gun['ATR'],2),
                              round(son_gun['OBV'],2)]
            })
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("📊 Son Kapanış")
                st.metric("Fiyat", f"{son_kapanis:.2f} TL")
            with col2:
                st.subheader("🔮 1 Gün Sonrası Tahmin")
                st.markdown(f"**Yön:** {tahmin_gun['yon']} (Güven: %{tahmin_gun['guven_skoru']:.0f})")
                st.metric("Tahmini Aralık", f"{tahmin_gun['dusuk']} - {tahmin_gun['yuksek']}")
                st.caption(f"Orta Nokta: {tahmin_gun['tahmini_kapanis']}")
            with col3:
                st.subheader("🗓️ 1 Hafta Sonrası Tahmin")
                st.markdown(f"**Yön:** {tahmin_hafta['yon']} (Güven: %{tahmin_hafta['guven_skoru']:.0f})")
                st.metric("Tahmini Aralık", f"{tahmin_hafta['dusuk']} - {tahmin_hafta['yuksek']}")
                st.caption(f"Orta Nokta: {tahmin_hafta['tahmini_kapanis']}")
            
            st.subheader("📋 Kullanılan İndikatör Değerleri")
            st.table(gostergeler)
            
            st.subheader("📈 Son Dönem Fiyat Hareketi ve Bollinger Bantları")
            grafik_verisi = ind_df.dropna().tail(90)
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=grafik_verisi.index, y=grafik_verisi['Close'], name='Kapanış'))
            fig.add_trace(go.Scatter(x=grafik_verisi.index, y=grafik_verisi['Bollinger_Ust'], 
                                     line=dict(dash='dash'), name='Bollinger Üst'))
            fig.add_trace(go.Scatter(x=grafik_verisi.index, y=grafik_verisi['Bollinger_Alt'], 
                                     line=dict(dash='dash'), name='Bollinger Alt'))
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Hata oluştu: {e}")

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import accuracy_score

# ---------------------------
# GÜNCEL BIST 100 HİSSE LİSTESİ
# ---------------------------
HISSE_LISTESI = [
    {"sembol": "AEFES.IS", "isim": "Anadolu Efes"},
    {"sembol": "AGHOL.IS", "isim": "AG Anadolu Grubu Holding"},
    {"sembol": "AKBNK.IS", "isim": "Akbank"},
    {"sembol": "AKFGY.IS", "isim": "Akfen GMYO"},
    {"sembol": "AKSA.IS", "isim": "Aksa"},
    {"sembol": "AKSEN.IS", "isim": "Aksa Enerji"},
    {"sembol": "ALARK.IS", "isim": "Alarko Holding"},
    {"sembol": "ALBRK.IS", "isim": "Albaraka Türk"},
    {"sembol": "ARCLK.IS", "isim": "Arçelik"},
    {"sembol": "ASELS.IS", "isim": "Aselsan"},
    {"sembol": "ASTOR.IS", "isim": "Astor Enerji"},
    {"sembol": "BIMAS.IS", "isim": "BİM Mağazalar"},
    {"sembol": "BRSAN.IS", "isim": "Borusan Mannesmann"},
    {"sembol": "BRYAT.IS", "isim": "Borusan Yatırım"},
    {"sembol": "CCOLA.IS", "isim": "Coca-Cola İçecek"},
    {"sembol": "CIMSA.IS", "isim": "Çimsa"},
    {"sembol": "CLEBI.IS", "isim": "Çelebi Hava Servisi"},
    {"sembol": "DEVA.IS", "isim": "Deva Holding"},
    {"sembol": "DOAS.IS", "isim": "Doğuş Otomotiv"},
    {"sembol": "DOHOL.IS", "isim": "Doğan Holding"},
    {"sembol": "ECILC.IS", "isim": "Eczacıbaşı İlaç"},
    {"sembol": "ECZYT.IS", "isim": "Eczacıbaşı Yatırım"},
    {"sembol": "EGEEN.IS", "isim": "Ege Endüstri"},
    {"sembol": "EKGYO.IS", "isim": "Emlak Konut GMYO"},
    {"sembol": "ENJSA.IS", "isim": "Enerjisa"},
    {"sembol": "ENKAI.IS", "isim": "Enka İnşaat"},
    {"sembol": "EREGL.IS", "isim": "Ereğli Demir Çelik"},
    {"sembol": "FENER.IS", "isim": "Fenerbahçe Sportif"},
    {"sembol": "FROTO.IS", "isim": "Ford Otosan"},
    {"sembol": "GARAN.IS", "isim": "Garanti Bankası"},
    {"sembol": "GUBRF.IS", "isim": "Gübre Fabrikaları"},
    {"sembol": "HALKB.IS", "isim": "Halk Bankası"},
    {"sembol": "HEKTS.IS", "isim": "Hektaş"},
    {"sembol": "ISCTR.IS", "isim": "İş Bankası (C)"},
    {"sembol": "ISGYO.IS", "isim": "İş GMYO"},
    {"sembol": "KCHOL.IS", "isim": "Koç Holding"},
    {"sembol": "KLSER.IS", "isim": "Kaleseramik"},
    {"sembol": "KONTR.IS", "isim": "Kontron"},
    {"sembol": "KONYA.IS", "isim": "Konya Çimento"},
    {"sembol": "KORDSA.IS", "isim": "Kordsa"},
    {"sembol": "KOZAA.IS", "isim": "Koza Anadolu Metal"},
    {"sembol": "KOZAL.IS", "isim": "Koza Altın"},
    {"sembol": "KRDMD.IS", "isim": "Kardemir (D)"},
    {"sembol": "MAVI.IS", "isim": "Mavi Giyim"},
    {"sembol": "MGROS.IS", "isim": "Migros"},
    {"sembol": "ODAS.IS", "isim": "Odaş Elektrik"},
    {"sembol": "OYAKC.IS", "isim": "Oyak Çimento"},
    {"sembol": "PENTA.IS", "isim": "Penta Teknoloji"},
    {"sembol": "PETKM.IS", "isim": "Petkim"},
    {"sembol": "PGSUS.IS", "isim": "Pegasus"},
    {"sembol": "QUAGR.IS", "isim": "Qua Granite"},
    {"sembol": "SAHOL.IS", "isim": "Sabancı Holding"},
    {"sembol": "SASA.IS", "isim": "Sasa Polyester"},
    {"sembol": "SELEC.IS", "isim": "Selçuk Ecza Deposu"},
    {"sembol": "SISE.IS", "isim": "Şişe Cam"},
    {"sembol": "SKBNK.IS", "isim": "Şekerbank"},
    {"sembol": "SMRTG.IS", "isim": "Smart Güneş Enerjisi"},
    {"sembol": "SOKM.IS", "isim": "Şok Marketler"},
    {"sembol": "TAVHL.IS", "isim": "TAV Havalimanları"},
    {"sembol": "TCELL.IS", "isim": "Turkcell"},
    {"sembol": "THYAO.IS", "isim": "Türk Hava Yolları"},
    {"sembol": "TKFEN.IS", "isim": "Tekfen Holding"},
    {"sembol": "TOASO.IS", "isim": "Tofaş"},
    {"sembol": "TSKB.IS", "isim": "TSKB"},
    {"sembol": "TTKOM.IS", "isim": "Türk Telekom"},
    {"sembol": "TUPRS.IS", "isim": "TÜPRAŞ"},
    {"sembol": "ULKER.IS", "isim": "Ülker"},
    {"sembol": "VAKBN.IS", "isim": "VakıfBank"},
    {"sembol": "VESBE.IS", "isim": "Vestel Beyaz Eşya"},
    {"sembol": "VESTL.IS", "isim": "Vestel"},
    {"sembol": "YKBNK.IS", "isim": "Yapı Kredi Bankası"},
    {"sembol": "YYLGD.IS", "isim": "Yayla Gıda"},
    {"sembol": "ZOREN.IS", "isim": "Zorlu Enerji"},
]
SEMBOL_ISIM = {h["sembol"]: h["isim"] for h in HISSE_LISTESI}

# Session state
if "secili_sembol" not in st.session_state:
    st.session_state.secili_sembol = None

st.set_page_config(page_title="Hisse Fiyat Tahmini Pro", layout="wide")
st.title("📈 Hisse Senedi Fiyat Tahmin Uygulaması (Pro)")
st.markdown("8 indikatör + ML + olasılık + Al/Sat simülasyonu + Kesişim dedektörü + Yön tahmini + Sağlık Karnesi + Destek/Direnç")

# ---------------------------
# 8 İNDİKATÖR HESAPLAMA
# ---------------------------
def tum_indikatorleri_hesapla(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    kapanis = df['Close'].squeeze().ffill().dropna()
    yuksek = df['High'].squeeze().ffill().dropna()
    dusuk = df['Low'].squeeze().ffill().dropna()
    hacim = df['Volume'].squeeze().fillna(0)

    sma_50 = kapanis.rolling(50).mean()
    sma_200 = kapanis.rolling(200).mean()

    ema_12 = kapanis.ewm(span=12, adjust=False).mean()
    ema_26 = kapanis.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    sinyal = macd.ewm(span=9, adjust=False).mean()

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

    dusuk_14 = dusuk.rolling(14).min()
    yuksek_14 = yuksek.rolling(14).max()
    stok_k = (kapanis - dusuk_14) / (yuksek_14 - dusuk_14) * 100
    stok_d = stok_k.rolling(3).mean()

    artis = yuksek.diff()
    dusus = -dusuk.diff()
    pdm = pd.Series(np.where((artis > dusus) & (artis > 0), artis, 0), index=kapanis.index)
    ndm = pd.Series(np.where((dusus > artis) & (dusus > 0), dusus, 0), index=kapanis.index)
    tr14 = tr.rolling(14).mean()
    pdm14 = pdm.rolling(14).mean()
    ndm14 = ndm.rolling(14).mean()
    pdi = 100 * pdm14 / tr14
    ndi = 100 * ndm14 / tr14
    dx = 100 * np.abs(pdi - ndi) / (pdi + ndi)
    adx = dx.rolling(14).mean()

    indikatorler = pd.DataFrame({
        'Close': kapanis,
        'SMA_50': sma_50, 'SMA_200': sma_200,
        'MACD': macd, 'MACD_Sinyal': sinyal,
        'RSI': rsi,
        'Bollinger_Ust': bollinger_ust, 'Bollinger_Alt': bollinger_alt,
        'ATR': atr, 'OBV': obv,
        'Stokastik_K': stok_k, 'Stokastik_D': stok_d,
        'ADX': adx,
        'Volume': hacim,
        'High': yuksek,
        'Low': dusuk
    }, index=kapanis.index)
    return indikatorler

# ---------------------------
# TAHMİN FONKSİYONLARI
# ---------------------------
def fiyat_aralik_tahmini(ind_df, son_kapanis, gun_sayisi=1):
    son = ind_df.iloc[-1]
    trend_puani = 0
    if son['Close'] > son['SMA_50']: trend_puani += 1
    if son['SMA_50'] > son['SMA_200']: trend_puani += 1
    if son['MACD'] > son['MACD_Sinyal']: trend_puani += 1
    if 50 < son['RSI'] < 70: trend_puani += 1
    if son['OBV'] > ind_df['OBV'].rolling(5).mean().iloc[-1]: trend_puani += 1
    if son['Stokastik_K'] > son['Stokastik_D']: trend_puani += 1
    if son['ADX'] > 25: trend_puani += 1

    yon = 1 if trend_puani >= 4 else (-1 if trend_puani <= 2 else 0)
    gunluk_getiri = ind_df['Close'].pct_change().dropna()
    son_20_gun = gunluk_getiri.tail(20)
    ortalama_getiri = son_20_gun.mean()

    if gun_sayisi == 1:
        atr_deger = son['ATR']
        tahmini_kapanis = son_kapanis * (1 + ortalama_getiri * yon * 0.5)
        aralik = atr_deger * 0.8
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
        'guven_skoru': trend_puani / 7 * 100
    }

# ---------------------------
# İLERİ ANALİZ FONKSİYONLARI
# ---------------------------
def hedef_olasilik(df, son_kapanis, gun=50, hedef_yuzde=5):
    kapanis = df['Close']
    sma = kapanis.rolling(gun).mean()
    sinyal = kapanis > sma
    getiri = kapanis.pct_change(5).shift(-5) * 100
    kosul = sinyal & sinyal.shift(1)
    hedef = getiri >= hedef_yuzde
    ortak = kosul & hedef.notna()
    olasilik = hedef[ortak].mean() * 100 if ortak.any() else 0
    return olasilik

def ml_tahmin_araligi(ind_df):
    ozellikler = ['SMA_50', 'SMA_200', 'MACD', 'RSI', 'ATR', 'Stokastik_K', 'ADX']
    X = ind_df[ozellikler].dropna()
    y = ind_df['Close'].pct_change(5).shift(-5) * 100
    ortak = X.index.intersection(y.dropna().index)
    X, y = X.loc[ortak], y.loc[ortak]
    if len(X) < 100:
        return None
    son_x = X.iloc[-1:].values
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X[:-1], y[:-1])
    tahmin = model.predict(son_x)[0]
    son_20_pred = model.predict(X.iloc[-20:])
    hatalar = y.iloc[-20:].values - son_20_pred
    std_hata = np.std(hatalar)
    son_fiyat = ind_df['Close'].iloc[-1]
    return {
        'alt_fiyat': round(son_fiyat * (1 + (tahmin - 1.96*std_hata)/100), 2),
        'ust_fiyat': round(son_fiyat * (1 + (tahmin + 1.96*std_hata)/100), 2),
        'tahmini_fiyat': round(son_fiyat * (1 + tahmin/100), 2)
    }

def yon_tahmini_modeli(ind_df):
    ozellikler = ['SMA_50', 'SMA_200', 'MACD', 'RSI', 'ATR', 'Stokastik_K', 'ADX']
    df = ind_df.dropna(subset=ozellikler).copy()
    df['Hedef'] = (df['Close'].shift(-5) > df['Close']).astype(int)
    df = df.dropna(subset=['Hedef'])
    if len(df) < 200:
        return None
    split_idx = int(len(df) * 0.8)
    train = df.iloc[:split_idx]
    test = df.iloc[split_idx:]
    X_train = train[ozellikler]
    y_train = train['Hedef']
    X_test = test[ozellikler]
    y_test = test['Hedef']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred) * 100
    son_x = df[ozellikler].iloc[-1:].values
    son_tahmin = model.predict(son_x)[0]
    yon = 'YUKARI ↑' if son_tahmin == 1 else 'AŞAĞI ↓'
    return {'dogruluk': round(acc, 1), 'son_tahmin': yon, 'test_boyutu': len(test)}

def max_drawdown(seri):
    tepe = seri.expanding(min_periods=1).max()
    drawdown = (seri - tepe) / tepe * 100
    return drawdown.min()

def al_sat_sinyalleri_uret(ind_df):
    df = ind_df.copy()
    df['MACD_kesisme'] = (df['MACD'] > df['MACD_Sinyal']) & (df['MACD'].shift(1) <= df['MACD_Sinyal'].shift(1))
    df['MACD_asagi_kesisme'] = (df['MACD'] < df['MACD_Sinyal']) & (df['MACD'].shift(1) >= df['MACD_Sinyal'].shift(1))
    al_sinyali = df['MACD_kesisme'] & (df['RSI'] < 70)
    sat_sinyali = df['MACD_asagi_kesisme'] | (df['RSI'] >= 70)
    df['Sinyal'] = 0
    df.loc[al_sinyali, 'Sinyal'] = 1
    df.loc[sat_sinyali, 'Sinyal'] = -1
    return df

def strateji_simulasyonu(df):
    sinyal_df = al_sat_sinyalleri_uret(df)
    pozisyon = 0
    alis_fiyat = 0
    islemler = []
    for i in range(len(sinyal_df)):
        if sinyal_df['Sinyal'].iloc[i] == 1 and pozisyon == 0:
            pozisyon = 1
            alis_fiyat = sinyal_df['Close'].iloc[i]
            islemler.append({'Tarih': sinyal_df.index[i], 'Tip': 'AL', 'Fiyat': alis_fiyat})
        elif sinyal_df['Sinyal'].iloc[i] == -1 and pozisyon == 1:
            pozisyon = 0
            satis_fiyat = sinyal_df['Close'].iloc[i]
            islemler.append({'Tarih': sinyal_df.index[i], 'Tip': 'SAT', 'Fiyat': satis_fiyat})
            getiri = (satis_fiyat - alis_fiyat) / alis_fiyat * 100
            islemler[-1]['Getiri (%)'] = round(getiri, 2)
    if len(islemler) < 2:
        return None, None
    kazananlar = [i for i in islemler if i.get('Getiri (%)', 0) > 0]
    toplam_getiri = sum(i.get('Getiri (%)', 0) for i in islemler)
    kazanc_orani = len(kazananlar) / (len(islemler) // 2) * 100 if len(islemler) // 2 > 0 else 0
    return islemler, {
        'Toplam Getiri (%)': round(toplam_getiri, 2),
        'İşlem Sayısı': len(islemler) // 2,
        'Kazanma Oranı (%)': round(kazanc_orani, 1),
        'Maksimum Drawdown (%)': round(max_drawdown(sinyal_df['Close']), 2)
    }

def kesişim_dedektoru(ind_df):
    df = ind_df.dropna(subset=['SMA_50', 'SMA_200']).copy()
    if len(df) < 20:
        return None
    son_fark = df['SMA_50'].iloc[-1] - df['SMA_200'].iloc[-1]
    fark_serisi = df['SMA_50'] - df['SMA_200']
    y = fark_serisi.iloc[-20:].values
    x = np.arange(len(y))
    if np.std(y) < 1e-9:
        return None
    egim, intercept = np.polyfit(x, y, 1)
    if abs(egim) < 1e-9:
        return None
    x_kesişim = -intercept / egim
    kalan_gun = x_kesişim - (len(y) - 1)
    if kalan_gun < 0:
        return {'tip': 'none', 'gun': 0, 'son_fark': son_fark}
    if son_fark < 0 and egim > 0:
        tip = 'Golden Cross'
    elif son_fark > 0 and egim < 0:
        tip = 'Death Cross'
    else:
        tip = 'Belirsiz'
    return {'tip': tip, 'gun': round(kalan_gun), 'son_fark': son_fark}

def teknik_puanlama(ind_df):
    son = ind_df.iloc[-1]
    trend = 0
    if son['SMA_50'] > son['SMA_200']: trend += 4
    if son['Close'] > son['SMA_50']: trend += 3
    if son['Close'] > son['SMA_200']: trend += 3
    trend = min(trend, 10)

    momentum = 0
    rsi = son['RSI']
    if rsi > 60: momentum += 4
    elif rsi > 50: momentum += 3
    elif rsi > 30: momentum += 1
    else: momentum += 2
    if son['MACD'] > son['MACD_Sinyal']: momentum += 4
    if son['Stokastik_K'] > son['Stokastik_D']: momentum += 2
    momentum = min(momentum, 10)

    volatilite = 5
    fiyat = son['Close']
    sma20 = (son['Bollinger_Ust'] + son['Bollinger_Alt']) / 2
    bant_genisligi = (son['Bollinger_Ust'] - son['Bollinger_Alt']) / sma20 * 100
    fark_yuzde = abs(fiyat - sma20) / sma20 * 100
    if fark_yuzde < 1: volatilite += 3
    elif fark_yuzde < 2: volatilite += 1
    if bant_genisligi < 5: volatilite += 2
    ortalama_atr = ind_df['ATR'].rolling(20).mean().iloc[-1]
    if son['ATR'] < ortalama_atr: volatilite += 2
    else: volatilite -= 1
    volatilite = max(0, min(volatilite, 10))

    hacim_p = 0
    obv_ortalama = ind_df['OBV'].rolling(5).mean().iloc[-1]
    if son['OBV'] > obv_ortalama: hacim_p += 5
    ortalama_hacim = ind_df['Volume'].rolling(20).mean().iloc[-1]
    if son['Volume'] > ortalama_hacim: hacim_p += 5
    hacim_p = min(hacim_p, 10)

    genel = round((trend + momentum + volatilite + hacim_p) / 4, 1)
    return {
        'trend': trend,
        'momentum': momentum,
        'volatilite': volatilite,
        'hacim': hacim_p,
        'genel': genel
    }

def destek_direnc_bul(df, pencere=5):
    """Yerel pivot noktalarını tespit eder, seviyeleri döndürür."""
    yuksek = df['High']
    dusuk = df['Low']
    kapanis = df['Close']
    pivot_tepeler = []
    pivot_dipler = []

    for i in range(pencere, len(df)-pencere):
        if yuksek.iloc[i] == yuksek.iloc[i-pencere:i+pencere+1].max():
            pivot_tepeler.append({'tarih': yuksek.index[i], 'fiyat': yuksek.iloc[i]})
        if dusuk.iloc[i] == dusuk.iloc[i-pencere:i+pencere+1].min():
            pivot_dipler.append({'tarih': dusuk.index[i], 'fiyat': dusuk.iloc[i]})

    tolerans = kapanis.iloc[-1] * 0.01
    destek_seviyeleri = []
    for dip in pivot_dipler:
        eklendi = False
        for seviye in destek_seviyeleri:
            if abs(dip['fiyat'] - seviye['fiyat']) < tolerans:
                seviye['sayi'] += 1
                seviye['tarihler'].append(dip['tarih'])
                eklendi = True
                break
        if not eklendi:
            destek_seviyeleri.append({'fiyat': dip['fiyat'], 'sayi': 1, 'tarihler': [dip['tarih']]})

    direnc_seviyeleri = []
    for tepe in pivot_tepeler:
        eklendi = False
        for seviye in direnc_seviyeleri:
            if abs(tepe['fiyat'] - seviye['fiyat']) < tolerans:
                seviye['sayi'] += 1
                seviye['tarihler'].append(tepe['tarih'])
                eklendi = True
                break
        if not eklendi:
            direnc_seviyeleri.append({'fiyat': tepe['fiyat'], 'sayi': 1, 'tarihler': [tepe['tarih']]})

    guclu_destek = [s for s in destek_seviyeleri if s['sayi'] >= 2]
    guclu_direnc = [s for s in direnc_seviyeleri if s['sayi'] >= 2]
    return guclu_destek, guclu_direnc

# ---------------------------
# ARAYÜZ
# ---------------------------
st.subheader("🔍 Hisse Seçimi")
arama_metni = st.text_input("Hisse adı veya kodu yazın:", placeholder="Örn: THYAO veya Türk Hava")
if arama_metni:
    arama_lower = arama_metni.lower()
    oneriler = [h for h in HISSE_LISTESI if arama_lower in h["sembol"].lower() or arama_lower in h["isim"].lower()]
    oneriler.insert(0, {"sembol": arama_metni.strip().upper(), "isim": "Manuel giriş"})
    st.write("**Bulunan hisseler:**")
    for i in range(0, len(oneriler), 2):
        cols = st.columns(2)
        for j in range(2):
            idx = i + j
            if idx < len(oneriler):
                h = oneriler[idx]
                with cols[j]:
                    st.button(f"{h['sembol']} - {h['isim']}",
                              key=f"sec_{h['sembol']}",
                              on_click=lambda s=h['sembol']: st.session_state.update({"secili_sembol": s}),
                              use_container_width=True)
else:
    st.info("Hisse aramaya başlayın...")

if st.session_state.secili_sembol:
    secili = st.session_state.secili_sembol
    isim = SEMBOL_ISIM.get(secili, "Manuel hisse")
    st.success(f"✅ Seçili hisse: **{secili}** – {isim}")

    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Farklı hisse seç"):
            for key in ["tahmin_gun", "tahmin_hafta", "olasilik", "ml_sonuc", "ind_df",
                        "son_kapanis", "veri", "sim_islemler", "sim_metrikler", "sim_ind_sim",
                        "kesişim_sonuc", "yon_tahmin", "teknik_puan", "destek_direnc"]:
                st.session_state.pop(key, None)
            st.session_state.secili_sembol = None
    with col2:
        # Bugünün tarihi varsayılan, en son verileri de alır
        tahmin_tarihi = st.date_input("Tahmin tarihi:",
                                      value=datetime.today(),
                                      max_value=datetime.today())

    if st.button("📊 Tahmini Hesapla", type="primary"):
        with st.spinner("Hesaplanıyor..."):
            try:
                # Sabit 1 yıllık (365 gün) veri çek
                baslangic = tahmin_tarihi - timedelta(days=365)
                veri = yf.download(secili, start=baslangic, end=tahmin_tarihi, progress=False)
                if veri.empty:
                    st.error("Hisse bulunamadı.")
                else:
                    st.info(f"📦 {len(veri)} işlem günü verisi çekildi (1 yıllık).")
                    ind_df = tum_indikatorleri_hesapla(veri).dropna()
                    if len(ind_df) < 50:
                        st.error("Yeterli indikatör verisi hesaplanamadı (en az 50 gün gerekli).")
                    else:
                        son_kapanis = ind_df['Close'].iloc[-1]
                        tahmin_gun = fiyat_aralik_tahmini(ind_df, son_kapanis, 1)
                        tahmin_hafta = fiyat_aralik_tahmini(ind_df, son_kapanis, 5)
                        olasilik = hedef_olasilik(veri, son_kapanis)
                        ml_sonuc = ml_tahmin_araligi(ind_df)
                        kesişim = kesişim_dedektoru(ind_df)
                        yon_tahmin = yon_tahmini_modeli(ind_df)
                        teknik_puan = teknik_puanlama(ind_df)
                        guclu_destek, guclu_direnc = destek_direnc_bul(veri.tail(90))

                        st.session_state["tahmin_gun"] = tahmin_gun
                        st.session_state["tahmin_hafta"] = tahmin_hafta
                        st.session_state["olasilik"] = olasilik
                        st.session_state["ml_sonuc"] = ml_sonuc
                        st.session_state["ind_df"] = ind_df
                        st.session_state["son_kapanis"] = son_kapanis
                        st.session_state["veri"] = veri
                        st.session_state["kesişim_sonuc"] = kesişim
                        st.session_state["yon_tahmin"] = yon_tahmin
                        st.session_state["teknik_puan"] = teknik_puan
                        st.session_state["destek_direnc"] = (guclu_destek, guclu_direnc)
                        st.rerun()
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

    if "tahmin_gun" in st.session_state:
        tahmin_gun = st.session_state["tahmin_gun"]
        tahmin_hafta = st.session_state["tahmin_hafta"]
        olasilik = st.session_state["olasilik"]
        ml_sonuc = st.session_state["ml_sonuc"]
        ind_df = st.session_state["ind_df"]
        son_kapanis = st.session_state["son_kapanis"]
        veri = st.session_state["veri"]
        kesişim = st.session_state.get("kesişim_sonuc", None)
        yon_tahmin = st.session_state.get("yon_tahmin", None)
        teknik_puan = st.session_state.get("teknik_puan", None)
        guclu_destek, guclu_direnc = st.session_state.get("destek_direnc", ([], []))

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Tahmin Sonuçları",
            "📈 İleri Analiz",
            "📊 İndikatörler",
            "📉 Strateji Simülasyonu",
            "🏥 Sağlık Karnesi"
        ])

        with tab1:
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("📊 Son Kapanış")
                st.metric("Fiyat", f"{son_kapanis:.2f} TL")
            with col2:
                st.subheader("🔮 1 Gün Sonrası")
                st.markdown(f"**Yön:** {tahmin_gun['yon']} (Güven: %{tahmin_gun['guven_skoru']:.0f})")
                st.metric("Aralık", f"{tahmin_gun['dusuk']} - {tahmin_gun['yuksek']}")
            with col3:
                st.subheader("🗓️ 1 Hafta Sonrası")
                st.markdown(f"**Yön:** {tahmin_hafta['yon']} (Güven: %{tahmin_hafta['guven_skoru']:.0f})")
                st.metric("Aralık", f"{tahmin_hafta['dusuk']} - {tahmin_hafta['yuksek']}")

            st.subheader("📅 Haftalık Bant Geçmişi ve Tahmin")
            df_haftalik = veri['Close'].resample('W').ohlc().dropna().tail(10)
            fig = go.Figure()
            for i, row in df_haftalik.iterrows():
                fig.add_trace(go.Scatter(x=[i, i], y=[row['low'], row['high']],
                                         mode='lines', line=dict(color='gray', width=2), showlegend=False))
            gelecek = df_haftalik.index[-1] + pd.Timedelta(weeks=1)
            fig.add_trace(go.Scatter(x=[gelecek, gelecek],
                                     y=[tahmin_hafta['dusuk'], tahmin_hafta['yuksek']],
                                     mode='lines+markers', line=dict(color='orange', width=4, dash='dash'),
                                     name='Tahmin'))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.subheader("🎯 Koşullu Olasılık Analizi")
            st.metric(f"50 Günlük Ort. Üstünde İken 5 Gün Sonra %5 Yükseliş Olasılığı",
                      f"%{olasilik:.1f}")

            if ml_sonuc:
                st.subheader("🤖 ML 5 Günlük Güven Aralığı (Random Forest %95)")
                st.metric("Tahmini Fiyat", f"{ml_sonuc['tahmini_fiyat']} TL")
                st.write(f"**Alt sınır:** {ml_sonuc['alt_fiyat']} TL / **Üst sınır:** {ml_sonuc['ust_fiyat']} TL")
            else:
                st.warning("ML güven aralığı için yeterli veri yok.")

            st.subheader("🧠 Yön Tahmini Modeli (Sınıflandırma)")
            if yon_tahmin is None:
                st.warning("Yön tahmini için yeterli veri yok (en az 200 gün).")
            else:
                col_yt1, col_yt2 = st.columns(2)
                with col_yt1:
                    st.metric("Test Doğruluğu", f"%{yon_tahmin['dogruluk']}")
                    st.caption(f"Test verisi: son {yon_tahmin['test_boyutu']} işlem günü")
                with col_yt2:
                    st.metric("5 Günlük Yön Tahmini", yon_tahmin['son_tahmin'])

            st.subheader("⚡ Hareketli Ortalama Kesişim Dedektörü")
            if kesişim is None:
                st.warning("Kesişim analizi için yeterli veri yok.")
            elif kesişim['tip'] == 'none':
                st.info("Yakın zamanda bir kesişim beklenmiyor.")
            elif kesişim['tip'] == 'Belirsiz':
                st.info("Kesişim yönü belirsiz, ancak ortalamalar birbirine yaklaşıyor olabilir.")
            else:
                if kesişim['tip'] == 'Golden Cross':
                    st.success(f"🔔 **{kesişim['tip']}** yaklaşıyor! Tahmini {kesişim['gun']} işlem günü içinde.")
                elif kesişim['tip'] == 'Death Cross':
                    st.error(f"⚠️ **{kesişim['tip']}** yaklaşıyor! Tahmini {kesişim['gun']} işlem günü içinde.")
                st.caption(f"Son fark (SMA50 - SMA200): {kesişim['son_fark']:.4f}")

            st.subheader("📊 Basit Hacim Profili (Son 90 Gün)")
            son_veri = veri.tail(90)
            fiyat_aralik = np.linspace(son_veri['Low'].min(), son_veri['High'].max(), 15)
            hacimler = []
            for i in range(len(fiyat_aralik)-1):
                alt, ust = fiyat_aralik[i], fiyat_aralik[i+1]
                hacimler.append(son_veri[(son_veri['Close'] >= alt) & (son_veri['Close'] < ust)]['Volume'].sum())
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=hacimler, y=[(fiyat_aralik[i]+fiyat_aralik[i+1])/2 for i in range(len(hacimler))],
                                 orientation='h', marker=dict(color='blue', opacity=0.5)))
            fig2.update_layout(xaxis_title="Hacim", yaxis_title="Fiyat", height=400)
            st.plotly_chart(fig2, use_container_width=True)

            st.subheader("🏗️ Otomatik Destek/Direnç Seviyeleri")
            if not guclu_destek and not guclu_direnc:
                st.info("Son 90 günde yeterli pivot noktası bulunamadı.")
            else:
                fig_dd = go.Figure()
                fig_dd.add_trace(go.Scatter(x=veri.index[-90:], y=veri['Close'].iloc[-90:], name='Kapanış'))
                for destek in guclu_destek:
                    fig_dd.add_hline(y=destek['fiyat'], line=dict(color='green', width=2, dash='dot'),
                                     annotation_text=f"Destek ({destek['sayi']})")
                for direnc in guclu_direnc:
                    fig_dd.add_hline(y=direnc['fiyat'], line=dict(color='red', width=2, dash='dot'),
                                     annotation_text=f"Direnç ({direnc['sayi']})")
                fig_dd.update_layout(height=500)
                st.plotly_chart(fig_dd, use_container_width=True)
                if guclu_destek:
                    en_yakin_destek = min(guclu_destek, key=lambda x: abs(x['fiyat'] - son_kapanis))
                    st.write(f"🟢 En yakın güçlü destek: **{en_yakin_destek['fiyat']:.2f}** TL ({en_yakin_destek['sayi']} dokunuş)")
                if guclu_direnc:
                    en_yakin_direnc = min(guclu_direnc, key=lambda x: abs(x['fiyat'] - son_kapanis))
                    st.write(f"🔴 En yakın güçlü direnç: **{en_yakin_direnc['fiyat']:.2f}** TL ({en_yakin_direnc['sayi']} dokunuş)")

        with tab3:
            st.subheader("📋 Tüm İndikatör Değerleri")
            ind_son = ind_df.iloc[-1]
            tablo = pd.DataFrame({
                'İndikatör': ['SMA 50', 'SMA 200', 'MACD', 'MACD Sinyal', 'RSI', 'Bollinger Üst',
                              'Bollinger Alt', 'ATR', 'OBV', 'Stokastik %K', 'Stokastik %D', 'ADX'],
                'Son Değer': [round(ind_son['SMA_50'],2), round(ind_son['SMA_200'],2),
                              round(ind_son['MACD'],2), round(ind_son['MACD_Sinyal'],2),
                              round(ind_son['RSI'],2), round(ind_son['Bollinger_Ust'],2),
                              round(ind_son['Bollinger_Alt'],2), round(ind_son['ATR'],2),
                              round(ind_son['OBV'],2), round(ind_son['Stokastik_K'],2),
                              round(ind_son['Stokastik_D'],2), round(ind_son['ADX'],2)]
            })
            st.table(tablo)
            st.subheader("📈 Bollinger Bantları")
            fig3 = go.Figure()
            fig3.add_trace(go.Scatter(x=ind_df.index, y=ind_df['Close'], name='Kapanış'))
            fig3.add_trace(go.Scatter(x=ind_df.index, y=ind_df['Bollinger_Ust'], line=dict(dash='dash'), name='Üst'))
            fig3.add_trace(go.Scatter(x=ind_df.index, y=ind_df['Bollinger_Alt'], line=dict(dash='dash'), name='Alt'))
            fig3.update_layout(height=400)
            st.plotly_chart(fig3, use_container_width=True)

        with tab4:
            st.subheader("📉 MACD + RSI Al/Sat Simülasyonu (Geçmiş Veri)")
            if st.button("🔄 Simülasyonu Çalıştır", key="sim_run"):
                with st.spinner("Simülasyon yapılıyor..."):
                    try:
                        baslangic_sim = tahmin_tarihi - timedelta(days=3*365)
                        veri_sim = yf.download(secili, start=baslangic_sim, end=tahmin_tarihi, progress=False)
                        if veri_sim.empty:
                            st.error("Simülasyon için yeterli veri yok.")
                        else:
                            ind_sim = tum_indikatorleri_hesapla(veri_sim).dropna()
                            islemler, metrikler = strateji_simulasyonu(ind_sim)
                            st.session_state["sim_islemler"] = islemler
                            st.session_state["sim_metrikler"] = metrikler
                            st.session_state["sim_ind_sim"] = ind_sim
                            st.rerun()
                    except Exception as e:
                        st.error(f"Simülasyon hatası: {e}")

            if "sim_metrikler" in st.session_state and st.session_state["sim_metrikler"]:
                metrikler = st.session_state["sim_metrikler"]
                islemler = st.session_state["sim_islemler"]
                st.success("Simülasyon tamamlandı!")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Toplam Getiri", f"%{metrikler['Toplam Getiri (%)']}")
                with col2:
                    st.metric("İşlem Sayısı", metrikler['İşlem Sayısı'])
                with col3:
                    st.metric("Kazanma Oranı", f"%{metrikler['Kazanma Oranı (%)']}")
                with col4:
                    st.metric("Maks. Drawdown", f"%{metrikler['Maksimum Drawdown (%)']}")

                if islemler and "sim_ind_sim" in st.session_state:
                    ind_sim = st.session_state["sim_ind_sim"]
                    fig_sim = go.Figure()
                    fig_sim.add_trace(go.Scatter(x=ind_sim.index, y=ind_sim['Close'], name='Kapanış'))
                    al_noktalari = [i for i in islemler if i['Tip'] == 'AL']
                    sat_noktalari = [i for i in islemler if i['Tip'] == 'SAT']
                    fig_sim.add_trace(go.Scatter(
                        x=[i['Tarih'] for i in al_noktalari],
                        y=[i['Fiyat'] for i in al_noktalari],
                        mode='markers', marker=dict(color='green', size=10, symbol='triangle-up'),
                        name='AL'))
                    fig_sim.add_trace(go.Scatter(
                        x=[i['Tarih'] for i in sat_noktalari],
                        y=[i['Fiyat'] for i in sat_noktalari],
                        mode='markers', marker=dict(color='red', size=10, symbol='triangle-down'),
                        name='SAT'))
                    fig_sim.update_layout(height=500)
                    st.plotly_chart(fig_sim, use_container_width=True)

                    st.subheader("İşlem Geçmişi")
                    islem_df = pd.DataFrame(islemler)
                    st.dataframe(islem_df, use_container_width=True)

        with tab5:
            st.subheader("🏥 Teknik Sağlık Karnesi (0-10 Puan)")
            if teknik_puan is None:
                st.warning("Henüz bir analiz yapılmadı.")
            else:
                genel = teknik_puan['genel']
                st.markdown(f"### Genel Teknik Puan: **{genel} / 10**")
                st.progress(genel / 10)

                col_p1, col_p2 = st.columns(2)
                with col_p1:
                    st.markdown("**Trend Puanı**")
                    st.progress(teknik_puan['trend'] / 10)
                    st.write(f"{teknik_puan['trend']}/10")

                    st.markdown("**Momentum Puanı**")
                    st.progress(teknik_puan['momentum'] / 10)
                    st.write(f"{teknik_puan['momentum']}/10")
                with col_p2:
                    st.markdown("**Volatilite/Destek-Direnç Puanı**")
                    st.progress(teknik_puan['volatilite'] / 10)
                    st.write(f"{teknik_puan['volatilite']}/10")

                    st.markdown("**Hacim Puanı**")
                    st.progress(teknik_puan['hacim'] / 10)
                    st.write(f"{teknik_puan['hacim']}/10")

                st.caption("Puanlama: 0-3 Zayıf, 4-6 Orta, 7-10 Güçlü")

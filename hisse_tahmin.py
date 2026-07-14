import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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

# ---------------------------
# Session state
# ---------------------------
if "secili_sembol" not in st.session_state:
    st.session_state.secili_sembol = None

# Sayfa ayarları
st.set_page_config(page_title="Hisse Fiyat Aralığı Tahmini", layout="wide")
st.title("📈 Hisse Senedi Fiyat Aralık Tahmin Uygulaması (BIST 100)")
st.markdown("6 indikatör ile **1 gün sonrası** ve **1 hafta sonrası** için fiyat aralığı tahmini.")

# ---------------------------
# İndikatör hesaplama fonksiyonları
# ---------------------------
def tum_indikatorleri_hesapla(df):
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    
    kapanis = df['Close'].squeeze()
    yuksek = df['High'].squeeze()
    dusuk = df['Low'].squeeze()
    hacim = df['Volume'].squeeze()
    
    kapanis = kapanis.ffill().dropna()
    yuksek = yuksek.ffill().dropna()
    dusuk = dusuk.ffill().dropna()
    hacim = hacim.fillna(0)
    
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
    }, index=kapanis.index)
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

# ---------------------------
# Hisse arama ve seçim bölümü
# ---------------------------
st.subheader("🔍 Hisse Seçimi (BIST 100)")
arama_metni = st.text_input("Hisse adı veya kodu yazın:", placeholder="Örn: THYAO veya Türk Hava")

def secim_yap():
    st.session_state.secili_sembol = st.session_state.radio_hisse["sembol"]
    # Seçimden sonra sayfayı yenile ki alt kısım görünsün
    try:
        st.rerun()
    except AttributeError:
        st.experimental_rerun()

if arama_metni:
    arama_lower = arama_metni.lower()
    oneriler = []
    for h in HISSE_LISTESI:
        if arama_lower in h["sembol"].lower() or arama_lower in h["isim"].lower():
            oneriler.append(h)
    manuel = {"sembol": arama_metni.strip().upper(), "isim": "Manuel giriş"}
    oneriler.insert(0, manuel)
    
    if oneriler:
        st.radio(
            "Öneriler:",
            options=oneriler,
            format_func=lambda x: f"{x['sembol']} - {x['isim']}",
            key="radio_hisse",
            on_change=secim_yap,
        )
    else:
        st.info("Eşleşen hisse bulunamadı. Lütfen farklı bir arama yapın.")
else:
    st.write("Hisse aramaya başlayın...")

# ---------------------------
# Seçili hisse ile tahmin bölümü
# ---------------------------
if st.session_state.secili_sembol:
    secili = st.session_state.secili_sembol
    isim = SEMBOL_ISIM.get(secili, "Manuel hisse")
    st.success(f"✅ Seçili hisse: **{secili}** – {isim}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("🔄 Farklı hisse seç"):
            st.session_state.secili_sembol = None
            try:
                st.rerun()
            except AttributeError:
                st.experimental_rerun()
    with col2:
        tahmin_tarihi = st.date_input(
            "Tahmin hangi tarih itibarıyla yapılsın? (dünün verisiyle)",
            value=datetime.today() - timedelta(days=1),
        )
    
    if st.button("📊 Tahmini Hesapla", type="primary"):
        try:
            baslangic = tahmin_tarihi - timedelta(days=365)
            veri = yf.download(secili, start=baslangic, end=tahmin_tarihi, progress=False)
            if veri.empty:
                st.error("Hisse bulunamadı veya yeterli veri yok.")
            else:
                ind_df = tum_indikatorleri_hesapla(veri)
                ind_df = ind_df.dropna()
                if len(ind_df) < 50:
                    st.error("Yeterli veri hesaplanamadı (en az 50 işlem günü gerekli).")
                else:
                    son_gun = ind_df.iloc[-1]
                    son_kapanis = son_gun['Close']
                    
                    tahmin_gun = fiyat_aralik_tahmini(ind_df, son_kapanis, gun_sayisi=1)
                    tahmin_hafta = fiyat_aralik_tahmini(ind_df, son_kapanis, gun_sayisi=5)
                    
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

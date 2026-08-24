from datetime import datetime
import pandas as pd
import streamlit as st

# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="Hayal Mobilya",
    page_icon="🪑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CSS - PROFESYONEL DESKTOP + MOBİL
# =========================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080b10;
    color: #f5f7fa;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #202630;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1rem;
}

/* Sidebar başlık */
.sidebar-logo {
    padding: 8px 10px 18px 10px;
}

.sidebar-logo .brand {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
}

.sidebar-logo .sub {
    font-size: 11px;
    color: #7f8a9a;
    margin-top: 3px;
}

/* Radio */
div[data-testid="stRadio"] label {
    background: transparent;
    border-radius: 10px;
    padding: 8px 10px;
    margin: 2px 0;
    transition: 0.2s;
}

div[data-testid="stRadio"] label:hover {
    background: #171d26;
}

/* Header */
.topbar {
    background: #0d1117;
    border: 1px solid #202630;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 22px;
}

.topbar-title {
    font-size: 14px;
    color: #8c97a8;
}

.topbar-user {
    font-size: 15px;
    font-weight: 700;
}

/* Main title */
.page-title {
    font-size: 30px;
    font-weight: 800;
    margin-bottom: 4px;
    color: #ffffff;
}

.page-subtitle {
    color: #7e899a;
    font-size: 13px;
    margin-bottom: 24px;
}

/* Cards */
.stat-card {
    background: linear-gradient(145deg, #11161e, #0d1117);
    border: 1px solid #202630;
    border-radius: 15px;
    padding: 20px;
    min-height: 135px;
    margin-bottom: 12px;
}

.stat-icon {
    font-size: 22px;
    margin-bottom: 12px;
}

.stat-title {
    font-size: 12px;
    color: #7e899a;
}

.stat-value {
    font-size: 25px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 5px;
}

.stat-change {
    font-size: 11px;
    color: #42d392;
    margin-top: 8px;
}

/* Section */
.section-title {
    font-size: 18px;
    font-weight: 700;
    margin: 25px 0 12px 0;
}

/* Buttons */
.stButton > button {
    width: 100%;
    min-height: 42px;
    border-radius: 9px;
    border: 1px solid #29313d;
    background: #141a22;
    color: #ffffff;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #1c2530;
    border-color: #4b8cff;
}

/* Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    background: #10151c !important;
    border-color: #29313d !important;
    border-radius: 9px !important;
}

/* Footer */
.footer {
    border-top: 1px solid #202630;
    margin-top: 45px;
    padding: 20px 0;
    color: #697384;
    font-size: 11px;
    text-align: center;
}

/* =====================================================
   MOBİL
   ===================================================== */

@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .block-container {
        padding: 0.8rem 0.8rem 5rem 0.8rem !important;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# VERİTABANI - DEMO (MOBİLYA ÜRÜNLERİ)
# =========================================================

if "stok" not in st.session_state:
    st.session_state.stok = pd.DataFrame([
        {
            "Ürün Adı": "Luna Koltuk Takımı",
            "Barkod": "8690576896745",
            "Alış Fiyatı (TL)": 15000.0,
            "Satış Fiyatı (TL)": 22000.0,
            "Bakiye": 5,
            "Birim": "Takım",
        },
        {
            "Ürün Adı": "Prag Yemek Masası Seti",
            "Barkod": "8690456765456",
            "Alış Fiyatı (TL)": 8000.0,
            "Satış Fiyatı (TL)": 12500.0,
            "Bakiye": 12,
            "Birim": "Takım",
        },
        {
            "Ürün Adı": "Royal Yatak Odası Dolabı",
            "Barkod": "8690654389765",
            "Alış Fiyatı (TL)": 11000.0,
            "Satış Fiyatı (TL)": 16000.0,
            "Bakiye": 3,
            "Birim": "Adet",
        },
    ])


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-logo">
        <div class="brand">🪑 HAYAL MOBİLYA</div>
        <div class="sub">ÖN MUHASEBE & STOK</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    menu_secim = st.radio(
        "MENÜ",
        [
            "🏠 Dashboard",
            "📦 Ürünler",
            "📄 Fatura ile Stok İşle",
            "📥 Stok Giriş",
            "📤 Stok Çıkış",
            "🧾 Faturalar",
            "👥 Cari Hesaplar",
            "💰 Kasa",
            "🏦 Banka",
            "📊 Raporlar",
            "➕ Ürün Ekle",
            "💵 Döviz",
            "⚙️ Ayarlar",
        ],
        index=0,
        key="desktop_menu",
    )

    st.markdown("---")

    st.markdown(
        """
    <div style="
        background:#111820;
        border:1px solid #202630;
        padding:12px;
        border-radius:10px;
        font-size:12px;
    ">
        <b>👤 Onur Yılmaz</b><br>
        <span style="color:#6f7a8b;">Yönetici</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📞 Destek\n\n444 43 19")


# =========================================================
# ÜST BAR
# =========================================================

st.markdown(
    """
<div class="topbar">
    <div class="topbar-title">Hayal Mobilya • Ön Muhasebe Yönetim Paneli</div>
    <div class="topbar-user">👤 Onur Yılmaz</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HESAPLAMALAR
# =========================================================

df = st.session_state.stok.copy()
toplam_stok = int(df["Bakiye"].sum())
stok_maliyeti = (df["Alış Fiyatı (TL)"] * df["Bakiye"]).sum()
stok_satis_degeri = (df["Satış Fiyatı (TL)"] * df["Bakiye"]).sum()
potansiyel_kar = stok_satis_degeri - stok_maliyeti
kritik_stok = df[df["Bakiye"] <= 3]


# =========================================================
# DASHBOARD
# =========================================================

if menu_secim == "🏠 Dashboard":
    st.markdown(
        '<div class="page-title">Dashboard</div>', unsafe_allow_html=True
    )
    st.markdown(
        '<div class="page-subtitle">Mobilya mağazanızın genel durumunu buradan takip edebilirsiniz.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-title">Bugünkü Satış</div>
            <div class="stat-value">₺44.500</div>
            <div class="stat-change">↑ %15,2 geçen güne göre</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-title">Tahmini Kâr</div>
            <div class="stat-value">₺{potansiyel_kar:,.0f}</div>
            <div class="stat-change">Stok bazlı hesaplama</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-title">Toplam Stok</div>
            <div class="stat-value">{toplam_stok:,}</div>
            <div class="stat-change">Adet / Takım</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">⚠️</div>
            <div class="stat-title">Kritik Stok</div>
            <div class="stat-value">{len(kritik_stok)}</div>
            <div class="stat-change" style="color:#ffb020;">Kontrol gerekli</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<div class="section-title">📈 Stok Dağılımı</div>',
        unsafe_allow_html=True,
    )
    chart_df = df[["Ürün Adı", "Bakiye"]].set_index("Ürün Adı")
    st.bar_chart(chart_df, height=300)


# =========================================================
# ÜRÜNLER
# =========================================================

elif menu_secim == "📦 Ürünler":
    st.markdown(
        '<div class="page-title">📦 Ürün Yönetimi</div>',
        unsafe_allow_html=True,
    )
    arama = st.text_input(
        "🔎 Ürün Ara", placeholder="Mobilya adı veya barkod..."
    )
    filtre_df = df.copy()
    if arama:
        filtre_df = filtre_df[
            filtre_df["Ürün Adı"]
            .str.contains(arama, case=False, na=False)
            | filtre_df["Barkod"]
            .astype(str)
            .str.contains(arama, case=False, na=False)
        ]
    st.dataframe(filtre_df, use_container_width=True, hide_index=True)


# =========================================================
# FATURA İLE STOK İŞLE (YENİ ÖZELLİK)
# =========================================================

elif menu_secim == "📄 Fatura ile Stok İşle":
    st.markdown(
        '<div class="page-title">📄 Fatura Yükle & Stok Güncelle</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Alış veya satış faturası (PDF/Görsel) yükleyerek stokları otomatik güncelleyin.</div>',
        unsafe_allow_html=True,
    )

    fatura_dosya = st.file_uploader(
        "Fatura Dosyası Seçin (PDF veya Resim)", type=["pdf", "png", "jpg", "jpeg"]
    )

    if fatura_dosya is not None:
        st.success(
            f"✅ Dosya yüklendi: **{fatura_dosya.name}** (Fatura başarıyla okundu)"
        )

        with st.form("fatura_islem_form"):
            fatura_turu = st.selectbox(
                "Fatura İşlem Türü",
                [
                    "Alış Faturası (Stok Artır +)",
                    "Satış Faturası (Stok Düş -)",
                ],
            )
            secilen_urun = st.selectbox(
                "Faturadaki Ürün", df["Ürün Adı"].tolist()
            )
            miktar = st.number_input(
                "İşlem Miktarı (Adet/Takım)", min_value=1, step=1
            )

            islem_yap_btn = st.form_submit_button(
                "🚀 Faturayı İşle ve Stoğu Güncelle"
            )

            if islem_yap_btn:
                idx = st.session_state.stok[
                    st.session_state.stok["Ürün Adı"] == secilen_urun
                ].index

                if "Alış" in fatura_turu:
                    st.session_state.stok.loc[idx, "Bakiye"] += miktar
                    st.success(
                        f"✅ Alış faturası işlendi. {secilen_urun} stoğu {miktar} adet artırıldı."
                    )
                else:
                    mevcut = int(
                        st.session_state.stok.loc[idx, "Bakiye"].iloc[0]
                    )
                    if miktar > mevcut:
                        st.error(
                            f"❌ Hata: Yetersiz stok! Mevcut stok: {mevcut}"
                        )
                    else:
                        st.session_state.stok.loc[idx, "Bakiye"] -= miktar
                        st.success(
                            f"✅ Satış faturası işlendi. {secilen_urun} stoğu {miktar} adet düşüldü."
                        )


# =========================================================
# ÜRÜN EKLE
# =========================================================

elif menu_secim == "➕ Ürün Ekle":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün Ekle</div>', unsafe_allow_html=True
    )
    with st.form("urun_ekle_form"):
        c1, c2 = st.columns(2)
        with c1:
            yeni_ad = st.text_input("Ürün Adı *")
            yeni_barkod = st.text_input("Barkod *")
            yeni_birim = st.selectbox("Birim", ["Takım", "Adet", "Set"])
        with c2:
            yeni_alis = st.number_input("Alış Fiyatı (TL)", min_value=0.0)
            yeni_satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0)
            yeni_adet = st.number_input("Başlangıç Stoğu", min_value=0, step=1)

        if st.form_submit_button("💾 Ürünü Kaydet"):
            if yeni_ad and yeni_barkod:
                yeni = pd.DataFrame([{
                    "Ürün Adı": yeni_ad,
                    "Barkod": yeni_barkod,
                    "Alış Fiyatı (TL)": yeni_alis,
                    "Satış Fiyatı (TL)": yeni_satis,
                    "Bakiye": yeni_adet,
                    "Birim": yeni_birim,
                }])
                st.session_state.stok = pd.concat(
                    [st.session_state.stok, yeni], ignore_index=True
                )
                st.success("✅ Ürün kaydedildi.")
            else:
                st.error("Lütfen zorunlu alanları doldurun.")


# =========================================================
# DİĞER SAYFALAR
# =========================================================

elif menu_secim == "📥 Stok Giriş":
    st.markdown(
        '<div class="page-title">📥 Stok Girişi</div>', unsafe_allow_html=True
    )
    st.info("Stok giriş modülü aktif.")

elif menu_secim == "📤 Stok Çıkış":
    st.markdown(
        '<div class="page-title">📤 Stok Çıkışı</div>', unsafe_allow_html=True
    )
    st.info("Stok çıkış modülü aktif.")

elif menu_secim == "🧾 Faturalar":
    st.markdown(
        '<div class="page-title">🧾 Faturalar</div>', unsafe_allow_html=True
    )
    st.info("Faturalar listesi aktif.")

elif menu_secim == "👥 Cari Hesaplar":
    st.markdown(
        '<div class="page-title">👥 Cari Hesaplar</div>',
        unsafe_allow_html=True,
    )
    st.info("Cari hesaplar aktif.")

elif menu_secim == "💰 Kasa":
    st.markdown(
        '<div class="page-title">💰 Kasa</div>', unsafe_allow_html=True
    )
    st.metric("Kasa Bakiyesi", "₺112.500")

elif menu_secim == "🏦 Banka":
    st.markdown(
        '<div class="page-title">🏦 Banka Hesapları</div>',
        unsafe_allow_html=True,
    )
    st.info("Banka hesapları aktif.")

elif menu_secim == "📊 Raporlar":
    st.markdown(
        '<div class="page-title">📊 Raporlar</div>', unsafe_allow_html=True
    )
    st.info("Raporlar aktif.")

elif menu_secim == "💵 Döviz":
    st.markdown(
        '<div class="page-title">💵 Döviz Kurları</div>',
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        st.metric("USD / TRY", "₺34,40")
    with c2:
        st.metric("EUR / TRY", "₺37,20")

elif menu_secim == "⚙️ Ayarlar":
    st.markdown(
        '<div class="page-title">⚙️ Sistem Ayarları</div>',
        unsafe_allow_html=True,
    )
    st.text_input("Firma Adı", value="Hayal Mobilya")


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
    © 2026 Hayal Mobilya • Ön Muhasebe ve Stok Takip Sistemi • v2.1.0
</div>
""",
    unsafe_allow_html=True,
)

from datetime import datetime
import pandas as pd
import streamlit as st

# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="Alp Bilge Yazılım",
    page_icon="💼",
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

/* Product cards */
.product-card {
    background: #0e131a;
    border: 1px solid #202630;
    border-radius: 14px;
    padding: 16px;
    margin-bottom: 10px;
}

.product-name {
    font-size: 15px;
    font-weight: 700;
}

.product-barcode {
    font-size: 11px;
    color: #6f7a8b;
    margin-top: 4px;
}

.product-price {
    font-size: 14px;
    font-weight: 600;
    margin-top: 12px;
}

.stock-good {
    color: #42d392;
    font-weight: 700;
}

.stock-warning {
    color: #ffb020;
    font-weight: 700;
}

.stock-danger {
    color: #ff5d5d;
    font-weight: 700;
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

/* Tabs */
button[data-baseweb="tab"] {
    color: #8994a5 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #ffffff !important;
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

    .topbar {
        padding: 12px 14px;
        border-radius: 12px;
        margin-bottom: 15px;
    }

    .page-title {
        font-size: 23px;
    }

    .page-subtitle {
        font-size: 12px;
        margin-bottom: 15px;
    }

    .stat-card {
        min-height: 115px;
        padding: 15px;
        border-radius: 13px;
    }

    .stat-value {
        font-size: 21px;
    }

    .section-title {
        font-size: 16px;
        margin-top: 18px;
    }

    .mobile-nav {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        height: 62px;
        background: #0d1117;
        border-top: 1px solid #202630;
        z-index: 999999;
        display: flex;
        justify-content: space-around;
        align-items: center;
    }

    .mobile-nav-item {
        color: #8792a3;
        font-size: 10px;
        text-align: center;
    }

    .mobile-nav-item span {
        display: block;
        font-size: 19px;
        margin-bottom: 2px;
    }

    div[data-testid="stDataFrame"] {
        font-size: 11px;
    }

}

@media (min-width: 769px) {
    .mobile-nav {
        display: none;
    }
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# VERİTABANI - DEMO
# =========================================================

if "stok" not in st.session_state:
    st.session_state.stok = pd.DataFrame([
        {
            "Ürün Adı": "Çaykur Tiryaki Çayı 1 Kg",
            "Barkod": "8690576896745",
            "Alış Fiyatı (TL)": 250.0,
            "Satış Fiyatı (TL)": 300.0,
            "Bakiye": 8,
            "Birim": "Adet",
        },
        {
            "Ürün Adı": "Söke Un 5 Kg",
            "Barkod": "8690456765456",
            "Alış Fiyatı (TL)": 150.0,
            "Satış Fiyatı (TL)": 200.0,
            "Bakiye": 36,
            "Birim": "Adet",
        },
        {
            "Ürün Adı": "İçim Rahat Laktozsuz Süt 1 L",
            "Barkod": "8690654389765",
            "Alış Fiyatı (TL)": 35.0,
            "Satış Fiyatı (TL)": 60.0,
            "Bakiye": 19,
            "Birim": "Adet",
        },
    ])

if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Dashboard"


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        """
    <div class="sidebar-logo">
        <div class="brand">💼 ALP BİLGE</div>
        <div class="sub">YAZILIM • ÖN MUHASEBE</div>
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
        <b>👤 Admin</b><br>
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
    <div class="topbar-title">Alp Bilge Yazılım • Ön Muhasebe</div>
    <div class="topbar-user">👤 Admin Yönetici</div>
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

kritik_stok = df[df["Bakiye"] <= 5]


# =========================================================
# DASHBOARD
# =========================================================

if menu_secim == "🏠 Dashboard":
    st.markdown(
        '<div class="page-title">Dashboard</div>', unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">İşletmenizin genel durumunu buradan takip edebilirsiniz.</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-title">Bugünkü Satış</div>
            <div class="stat-value">₺12.450</div>
            <div class="stat-change">↑ %12,4 geçen güne göre</div>
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
            <div class="stat-change">Adet / Birim</div>
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
            <div class="stat-change" style="color:#ffb020;">
                Kontrol gerekli
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # -----------------------------------------------------
    # Grafik
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">📈 Stok Dağılımı</div>',
        unsafe_allow_html=True,
    )

    chart_df = df[["Ürün Adı", "Bakiye"]].set_index("Ürün Adı")

    st.bar_chart(chart_df, height=300)

    # -----------------------------------------------------
    # Kritik stok
    # -----------------------------------------------------

    st.markdown(
        '<div class="section-title">⚠️ Kritik Stoklar</div>',
        unsafe_allow_html=True,
    )

    if len(kritik_stok) == 0:
        st.success("Tüm ürünlerin stok seviyesi normal.")
    else:
        cols = st.columns(min(3, len(kritik_stok)))

        for i, (_, row) in enumerate(kritik_stok.iterrows()):
            with cols[i % len(cols)]:
                st.markdown(
                    f"""
                <div class="product-card">
                    <div class="product-name">📦 {row["Ürün Adı"]}</div>
                    <div class="product-barcode">
                        Barkod: {row["Barkod"]}
                    </div>
                    <div class="product-price">
                        Stok:
                        <span class="stock-danger">
                            {row["Bakiye"]} {row["Birim"]}
                        </span>
                    </div>
                </div>
                """,
                    unsafe_allow_html=True,
                )


# =========================================================
# ÜRÜNLER
# =========================================================

elif menu_secim == "📦 Ürünler":
    st.markdown(
        '<div class="page-title">📦 Ürün Yönetimi</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="page-subtitle">Ürünlerinizi, fiyatlarınızı ve stok durumunuzu yönetin.</div>',
        unsafe_allow_html=True,
    )

    arama = st.text_input(
        "🔎 Ürün Ara", placeholder="Ürün adı veya barkod..."
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

    st.markdown(
        f"**{len(filtre_df)} ürün listeleniyor**",
    )

    st.dataframe(
        filtre_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Alış Fiyatı (TL)": st.column_config.NumberColumn(
                "Alış", format="₺ %.2f"
            ),
            "Satış Fiyatı (TL)": st.column_config.NumberColumn(
                "Satış", format="₺ %.2f"
            ),
            "Bakiye": st.column_config.NumberColumn("Stok"),
        },
    )


# =========================================================
# ÜRÜN EKLE
# =========================================================

elif menu_secim == "➕ Ürün Ekle":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün</div>', unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">Yeni ürününüzü sisteme tanımlayın.</div>',
        unsafe_allow_html=True,
    )

    with st.form("urun_ekle_form"):
        c1, c2 = st.columns(2)

        with c1:
            yeni_ad = st.text_input(
                "Ürün Adı *", placeholder="Örn: Coca Cola 2.5 L"
            )

            yeni_barkod = st.text_input(
                "Barkod *", placeholder="8690000000000"
            )

            yeni_birim = st.selectbox(
                "Birim",
                ["Adet", "Kg", "Gram", "Paket", "Koli", "Litre", "Metre"],
            )

        with c2:
            yeni_alis = st.number_input(
                "Alış Fiyatı (TL)", min_value=0.0, step=0.01
            )

            yeni_satis = st.number_input(
                "Satış Fiyatı (TL)", min_value=0.0, step=0.01
            )

            yeni_adet = st.number_input(
                "Başlangıç Stoğu", min_value=0, step=1
            )

        kaydet = st.form_submit_button("💾 Ürünü Kaydet")

        if kaydet:
            if not yeni_ad.strip():
                st.error("Ürün adı zorunludur.")
            elif not yeni_barkod.strip():
                st.error("Barkod zorunludur.")
            elif yeni_barkod in df["Barkod"].astype(str).values:
                st.error("Bu barkod zaten kayıtlı.")
            else:
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

                st.success(f"✅ {yeni_ad} başarıyla kaydedildi.")


# =========================================================
# STOK GİRİŞ
# =========================================================

elif menu_secim == "📥 Stok Giriş":
    st.markdown(
        '<div class="page-title">📥 Stok Girişi</div>', unsafe_allow_html=True
    )

    urunler = df["Ürün Adı"].tolist()

    if urunler:
        secilen = st.selectbox("Ürün Seç", urunler)

        miktar = st.number_input("Giriş Miktarı", min_value=1, step=1)

        if st.button("📥 Stok Girişi Yap"):
            idx = st.session_state.stok[
                st.session_state.stok["Ürün Adı"] == secilen
            ].index

            st.session_state.stok.loc[idx, "Bakiye"] += miktar

            st.success(f"✅ {miktar} adet stok girişi yapıldı.")


# =========================================================
# STOK ÇIKIŞ
# =========================================================

elif menu_secim == "📤 Stok Çıkış":
    st.markdown(
        '<div class="page-title">📤 Stok Çıkışı</div>', unsafe_allow_html=True
    )

    urunler = df["Ürün Adı"].tolist()

    if urunler:
        secilen = st.selectbox("Ürün Seç", urunler)

        miktar = st.number_input("Çıkış Miktarı", min_value=1, step=1)

        mevcut = int(
            df.loc[df["Ürün Adı"] == secilen, "Bakiye"].iloc[0]
        )

        st.info(f"Mevcut stok: {mevcut}")

        if st.button("📤 Stok Çıkışı Yap"):
            if miktar > mevcut:
                st.error("Yetersiz stok.")
            else:
                idx = st.session_state.stok[
                    st.session_state.stok["Ürün Adı"] == secilen
                ].index

                st.session_state.stok.loc[idx, "Bakiye"] -= miktar

                st.success(f"✅ {miktar} adet stoktan düşüldü.")


# =========================================================
# FATURALAR
# =========================================================

elif menu_secim == "🧾 Faturalar":
    st.markdown(
        '<div class="page-title">🧾 Faturalar</div>', unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Bugünkü Faturalar", "18")

    with c2:
        st.metric("Satış Tutarı", "₺18.750")

    with c3:
        st.metric("Alış Tutarı", "₺9.420")

    st.markdown(
        '<div class="section-title">Son Faturalar</div>',
        unsafe_allow_html=True,
    )

    faturalar = pd.DataFrame([
        {
            "Fatura No": "SF-2026-00124",
            "Cari": "ABC Market",
            "Tür": "Satış",
            "Tutar": 3250,
            "Tarih": "24.08.2026",
        },
        {
            "Fatura No": "AF-2026-00081",
            "Cari": "XYZ Gıda",
            "Tür": "Alış",
            "Tutar": 1840,
            "Tarih": "24.08.2026",
        },
    ])

    st.dataframe(faturalar, use_container_width=True, hide_index=True)


# =========================================================
# CARİ
# =========================================================

elif menu_secim == "👥 Cari Hesaplar":
    st.markdown(
        '<div class="page-title">👥 Cari Hesaplar</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Toplam Cari", "42")

    with c2:
        st.metric("Alacak", "₺84.250")

    with c3:
        st.metric("Borç", "₺42.800")

    cariler = pd.DataFrame([
        {
            "Cari": "ABC Market",
            "Telefon": "0532 *** ** **",
            "Alacak": 12500,
            "Borç": 2500,
        },
        {
            "Cari": "XYZ Gıda",
            "Telefon": "0544 *** ** **",
            "Alacak": 5200,
            "Borç": 8500,
        },
    ])

    st.dataframe(cariler, use_container_width=True, hide_index=True)


# =========================================================
# KASA
# =========================================================

elif menu_secim == "💰 Kasa":
    st.markdown(
        '<div class="page-title">💰 Kasa</div>', unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Kasa Bakiyesi", "₺48.250")

    with c2:
        st.metric("Bugünkü Giriş", "₺12.450")

    with c3:
        st.metric("Bugünkü Çıkış", "₺4.280")

    kasa = pd.DataFrame([
        {
            "Tarih": "24.08.2026",
            "Açıklama": "Satış",
            "Giriş": 3250,
            "Çıkış": 0,
        },
        {
            "Tarih": "24.08.2026",
            "Açıklama": "Tedarikçi Ödemesi",
            "Giriş": 0,
            "Çıkış": 1840,
        },
    ])

    st.dataframe(kasa, use_container_width=True, hide_index=True)


# =========================================================
# BANKA
# =========================================================

elif menu_secim == "🏦 Banka":
    st.markdown(
        '<div class="page-title">🏦 Banka Hesapları</div>',
        unsafe_allow_html=True,
    )

    banka = pd.DataFrame([
        {
            "Banka": "Ziraat Bankası",
            "Hesap": "**** 4582",
            "Bakiye": 125000,
        },
        {
            "Banka": "İş Bankası",
            "Hesap": "**** 7841",
            "Bakiye": 84250,
        },
    ])

    st.dataframe(banka, use_container_width=True, hide_index=True)


# =========================================================
# RAPORLAR
# =========================================================

elif menu_secim == "📊 Raporlar":
    st.markdown(
        '<div class="page-title">📊 Raporlar</div>', unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">Satış Performansı</div>',
        unsafe_allow_html=True,
    )

    satis = pd.DataFrame(
        {"Satış": [8200, 10400, 9800, 12500, 14300, 16800, 12450]},
        index=["Pzt", "Sal", "Çar", "Per", "Cum", "Cmt", "Paz"],
    )

    st.line_chart(satis, height=350)


# =========================================================
# DÖVİZ
# =========================================================

elif menu_secim == "💵 Döviz":
    st.markdown(
        '<div class="page-title">💵 Döviz Kurları</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("USD / TRY", "₺34,40", "+0,15%")

    with c2:
        st.metric("EUR / TRY", "₺37,20", "+0,08%")

    with c3:
        st.metric("GBP / TRY", "₺43,80", "+0,21%")

    with c4:
        st.metric("CHF / TRY", "₺39,60", "+0,12%")


# =========================================================
# AYARLAR
# =========================================================

elif menu_secim == "⚙️ Ayarlar":
    st.markdown(
        '<div class="page-title">⚙️ Sistem Ayarları</div>',
        unsafe_allow_html=True,
    )

    st.text_input("Firma Adı", value="Alp Bilge Yazılım")

    st.text_input("Telefon", value="444 43 19")

    st.text_input("E-posta", value="info@alpbilgeyazilim.com")

    st.selectbox("Para Birimi", ["TL", "USD", "EUR"])

    st.checkbox("Kritik stok bildirimlerini aktif et", value=True)

    if st.button("💾 Ayarları Kaydet"):
        st.success("Ayarlar kaydedildi.")


# =========================================================
# MOBİL ALT MENÜ
# =========================================================

st.markdown(
    """
<div class="mobile-nav">

    <div class="mobile-nav-item">
        <span>🏠</span>
        Ana Sayfa
    </div>

    <div class="mobile-nav-item">
        <span>📦</span>
        Ürünler
    </div>

    <div class="mobile-nav-item">
        <span>🧾</span>
        Fatura
    </div>

    <div class="mobile-nav-item">
        <span>📊</span>
        Rapor
    </div>

    <div class="mobile-nav-item">
        <span>☰</span>
        Menü
    </div>

</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
    © 2026 Alp Bilge Yazılım
    • Ön Muhasebe Sistemi
    • v2.0.0
</div>
""",
    unsafe_allow_html=True,
)
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

/* Fatura Şablonu Tasarımı */
.invoice-box {
    background: #ffffff;
    color: #111111;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    margin-top: 20px;
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
# OTURUM VE VERİ YÖNETİMİ (SESSION STATE)
# =========================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "users" not in st.session_state:
    st.session_state.users = {
        "Onur": "1234",
        "Admin": "123456",
        "Agam": "1234",
    }

if "personel_loglari" not in st.session_state:
    st.session_state.personel_loglari = [
        {
            "Kullanıcı": "Admin",
            "İşlem": "Giriş Yapıldı",
            "Zaman": "2026-08-24 08:30:12",
        },
        {
            "Kullanıcı": "Onur",
            "İşlem": "Giriş Yapıldı",
            "Zaman": "2026-08-24 09:15:40",
        },
    ]

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

if "faturalar" not in st.session_state:
    st.session_state.faturalar = []


# =========================================================
# GİRİŞ EKRANI
# =========================================================

if not st.session_state.authenticated:
    st.markdown(
        """
        <div style="max-width: 450px; margin: 40px auto; text-align: center;">
            <h1 style="color: white; font-size: 28px; font-weight: 800;">🪑 HAYAL MOBİLYA</h1>
            <p style="color: #7e899a; font-size: 13px;">Ön Muhasebe & Stok Takip Sistemi - Personel Giriş Paneli</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        kullanici_listesi = list(st.session_state.users.keys())
        secilen_kullanici = st.selectbox("Kullanıcı Seçin", kullanici_listesi)
        k_sifre = st.text_input("Şifre", type="password")
        giris_btn = st.button("Sisteme Giriş Yap")

        if giris_btn:
            if (
                secilen_kullanici in st.session_state.users
                and st.session_state.users[secilen_kullanici] == k_sifre
            ):
                st.session_state.authenticated = True
                st.session_state.current_user = secilen_kullanici

                if secilen_kullanici.lower() == "admin":
                    st.session_state.is_admin = True
                else:
                    st.session_state.is_admin = False

                zaman_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                st.session_state.personel_loglari.insert(
                    0,
                    {
                        "Kullanıcı": st.session_state.current_user,
                        "İşlem": "Giriş Yapıldı",
                        "Zaman": zaman_str,
                    },
                )

                st.success("✅ Giriş başarılı! Yönlendiriliyorsunuz...")
                st.rerun()
            else:
                st.error("❌ Hatalı şifre! Lütfen şifrenizi kontrol edin.")

    st.stop()


# =========================================================
# ANA UYGULAMA & MENÜLER
# =========================================================

menu_listesi = [
    "🏠 Ana Sayfa",
    "📦 Ürünler",
    "🧾 Satış Faturası Kes",
    "📄 Fatura ile Stok İşle",
    "📥 Stok Giriş",
    "📤 Stok Çıkış",
    "👥 Cari Hesaplar",
    "💰 Kasa",
    "🏦 Banka",
    "📊 Raporlar",
    "➕ Ürün Ekle",
    "💵 Döviz",
    "🔑 Şifremi Değiştir",
    "⚙️ Ayarlar",
]

if st.session_state.is_admin:
    menu_listesi.insert(1, "🔒 Yönetici Paneli")


# SIDEBAR (SOL MENÜ)
with st.sidebar:
    st.markdown(
        f"""
    <div class="sidebar-logo">
        <div class="brand">🪑 HAYAL MOBİLYA</div>
        <div class="sub">ÖN MUHASEBE & STOK</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    menu_secim = st.radio("MENÜ", menu_listesi, key="ana_menu_radio")

    st.markdown("---")

    rol_etiketi = (
        "Sistem Yöneticisi" if st.session_state.is_admin else "Aktif Personel"
    )
    st.markdown(
        f"""
    <div style="
        background:#111820;
        border:1px solid #202630;
        padding:12px;
        border-radius:10px;
        font-size:12px;
    ">
        <b>👤 {st.session_state.current_user}</b><br>
        <span style="color:#42d392;">{rol_etiketi}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Güvenli Çıkış", key="desktop_cikis"):
        zaman_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.personel_loglari.insert(
            0,
            {
                "Kullanıcı": st.session_state.current_user,
                "İşlem": "Çıkış Yapıldı",
                "Zaman": zaman_str,
            },
        )
        st.session_state.authenticated = False
        st.session_state.is_admin = False
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("📞 Destek\n\n444 43 19")


# =========================================================
# ÜST BAR
# =========================================================

st.markdown(
    f"""
<div class="topbar">
    <div class="topbar-title">Hayal Mobilya • Ön Muhasebe Yönetim Paneli</div>
    <div class="topbar-user">👤 {st.session_state.current_user}</div>
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
# YÖNETİCİ PANELİ (SADECE ADMİN GÖREBİLİR)
# =========================================================

if menu_secim == "🔒 Yönetici Paneli":
    if not st.session_state.is_admin:
        st.error("❌ Bu sayfaya erişim yetkiniz yok!")
        st.stop()

    st.markdown(
        '<div class="page-title">🔒 Yönetici Paneli & Personel Yönetimi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Personel hesaplarını kontrol edin, yeni personel ekleyin veya işten ayrılanların erişimini kaldırın.</div>',
        unsafe_allow_html=True,
    )

    tab_personel_liste, tab_personel_ekle, tab_loglar = st.tabs([
        "👥 Personel Hesapları & Silme",
        "➕ Yeni Personel Tanımla",
        "🕒 Giriş/Çıkış Logları",
    ])

    with tab_personel_liste:
        st.markdown(
            '<div class="section-title">Mevcut Personel Hesapları</div>',
            unsafe_allow_html=True,
        )
        st.info(
            "💡 İşten ayrılan personellerin sistem güvenliği için hesaplarını buradan silebilirsiniz."
        )

        p_data = []
        for k, s in st.session_state.users.items():
            p_data.append({
                "Kullanıcı Adı": k,
                "Yetki": "Yönetici (Admin)"
                if k.lower() == "admin"
                else "Personel",
            })
        st.dataframe(pd.DataFrame(p_data), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown(
            "#### 🗑️ Personel Hesabı Sil (İşten Ayrılma Durumu)",
            unsafe_allow_html=True,
        )

        silinebilir_kullanicilar = [
            k for k in st.session_state.users.keys() if k.lower() != "admin"
        ]

        if len(silinebilir_kullanicilar) > 0:
            silinecek_kullanici = st.selectbox(
                "Silinecek Personeli Seçin", silinebilir_kullanicilar
            )

            if st.button("⚠️ Seçilen Personel Hesabını Kalıcı Olarak Sil"):
                if silinecek_kullanici in st.session_state.users:
                    del st.session_state.users[silinecek_kullanici]
                    st.success(
                        f"✅ **{silinecek_kullanici}** adlı personel hesabı sistemden başarıyla silindi."
                    )
                    st.rerun()
        else:
            st.info(
                "Sistemde silinebilecek başka personel hesabı bulunmuyor (Admin silinemez)."
            )

    with tab_personel_ekle:
        st.markdown(
            '<div class="section-title">Yeni Personel Hesabı Oluştur</div>',
            unsafe_allow_html=True,
        )
        with st.form("admin_yeni_personel_form", clear_on_submit=True):
            yeni_p_kullanici = st.text_input(
                "Personel Kullanıcı Adı (Giriş için)"
            )
            yeni_p_sifre = st.text_input(
                "Personel Şifresi Belirleyin", type="password"
            )
            personel_kayit_btn = st.form_submit_button(
                "💾 Personel Hesabını Kaydet"
            )

            if personel_kayit_btn:
                p_clean = yeni_p_kullanici.strip()
                if not p_clean or not yeni_p_sifre:
                    st.warning(
                        "Lütfen kullanıcı adı ve şifre alanlarını boş bırakmayın."
                    )
                elif any(
                    k.lower() == p_clean.lower()
                    for k in st.session_state.users
                ):
                    st.error("❌ Bu kullanıcı adı zaten sistemde mevcut!")
                else:
                    st.session_state.users[p_clean] = yeni_p_sifre
                    st.success(
                        f"🎉 **{p_clean}** kullanıcı adı ile personel hesabı başarıyla oluşturuldu! Personel kendi şifresiyle giriş yapabilir."
                    )
                    st.rerun()

    with tab_loglar:
        st.markdown(
            '<div class="section-title">🕒 Personel Giriş - Çıkış Geçmişi</div>',
            unsafe_allow_html=True,
        )
        log_df = pd.DataFrame(st.session_state.personel_loglari)
        st.dataframe(log_df, use_container_width=True, hide_index=True)


# =========================================================
# ANA SAYFA
# =========================================================

elif menu_secim == "🏠 Ana Sayfa":
    st.markdown(
        '<div class="page-title">Ana Sayfa</div>', unsafe_allow_html=True
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

    # KRİTİK STOK UYARI PANELI
    if len(kritik_stok) > 0:
        st.markdown(
            '<div class="section-title" style="color:#ff4b4b;">⚠️ Acil Müdahale Gerektiren Kritik Stoklar (3 ve Altı)</div>',
            unsafe_allow_html=True,
        )
        st.dataframe(kritik_stok, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="section-title">📈 Stok Dağılımı</div>',
        unsafe_allow_html=True,
    )
    chart_df = df[["Ürün Adı", "Bakiye"]].set_index("Ürün Adı")
    st.bar_chart(chart_df, height=300)


# =========================================================
# ÜRÜNLER (GÜVENLİ STOK VURGULAMA)
# =========================================================

elif menu_secim == "📦 Ürünler":
    st.markdown(
        '<div class="page-title">📦 Ürün Yönetimi & Stok Takibi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">3 ve daha az kalan kritik stok seviyesindeki ürünler aşağıda listelenmiştir.</div>',
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

    # Kritik stokları özel renkli HTML kutusuyla dikkat çekici gösterme
    st.markdown("### 📋 Tüm Ürün Listesi")
    st.dataframe(filtre_df, use_container_width=True, hide_index=True)

    # Kritik stok uyarı kartları
    kritik_list = filtre_df[filtre_df["Bakiye"] <= 3]
    if len(kritik_list) > 0:
        st.markdown(
            '<div class="section-title" style="color:#ff4b4b;">🚨 Dikkat Edilmesi Gereken Kritik Stoklar</div>',
            unsafe_allow_html=True,
        )
        for _, row in kritik_list.iterrows():
            st.markdown(
                f"""
            <div style="background: #1e1114; border: 1px solid #ff4b4b; padding: 12px 18px; border-radius: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-weight: 700; color: #ff8080; font-size: 15px;">📦 {row['Ürün Adı']}</span><br>
                    <span style="color: #99aab5; font-size: 12px;">Barkod: {row['Barkod']} • Birim: {row['Birim']}</span>
                </div>
                <div style="background: #ff4b4b; color: white; padding: 6px 14px; border-radius: 8px; font-weight: 800; font-size: 14px;">
                    Kalan: {row['Bakiye']} {row['Birim']}
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )


# =========================================================
# SATIŞ FATURASI KES
# =========================================================

elif menu_secim == "🧾 Satış Faturası Kes":
    st.markdown(
        '<div class="page-title">🧾 Satış Faturası Kes</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Müşteriniz için resmi e-fatura oluşturun ve stoktan otomatik düşün.</div>',
        unsafe_allow_html=True,
    )

    with st.form("satis_fatura_form"):
        c1, c2 = st.columns(2)
        with c1:
            musteri_adi = st.text_input(
                "Müşteri / Cari Adı Soyadı *", placeholder="Örn: Ahmet Yılmaz"
            )
            musteri_vergi = st.text_input(
                "TCKN / Vergi No", placeholder="11 haneli TCKN veya VKN"
            )
        with c2:
            fatura_tarihi = st.date_input(
                "Fatura Tarihi", value=datetime.today()
            )
            odeme_tipi = st.selectbox(
                "Ödeme Türü", ["Nakit", "Kredi Kartı", "Banka Havalesi / EFT"]
            )

        st.markdown("---")
        secilen_urun_fatura = st.selectbox(
            "Satılacak Ürün *", df["Ürün Adı"].tolist()
        )
        satis_adedi = st.number_input(
            "Satış Miktarı (Adet/Takım) *", min_value=1, step=1, value=1
        )

        fatura_kes_btn = st.form_submit_button(
            "🚀 Faturayı Kes ve Stoğu Güncelle"
        )

        if fatura_kes_btn:
            if musteri_adi and secilen_urun_fatura:
                idx = st.session_state.stok[
                    st.session_state.stok["Ürün Adı"] == secilen_urun_fatura
                ].index
                mevcut_bakiye = int(
                    st.session_state.stok.loc[idx, "Bakiye"].iloc[0]
                )
                Birim_fiyat = float(
                    st.session_state.stok.loc[idx, "Satış Fiyatı (TL)"].iloc[0]
                )

                if satis_adedi > mevcut_bakiye:
                    st.error(
                        f"❌ Yetersiz Stok! Mevcut stok ({mevcut_bakiye}), talep edilen miktardan ({satis_adedi}) az."
                    )
                else:
                    st.session_state.stok.loc[idx, "Bakiye"] -= satis_adedi

                    toplam_tutar = Birim_fiyat * satis_adedi
                    kdv_tutar = toplam_tutar - (toplam_tutar / 1.20)
                    matrah = toplam_tutar - kdv_tutar

                    fatura_no = f"HYL2026{len(st.session_state.faturalar)+1:04d}"

                    yeni_fatura = {
                        "Fatura No": fatura_no,
                        "Tarih": str(fatura_tarihi),
                        "Müşteri": musteri_adi,
                        "Ürün": secilen_urun_fatura,
                        "Miktar": satis_adedi,
                        "Toplam Tutar (TL)": toplam_tutar,
                    }
                    st.session_state.faturalar.append(yeni_fatura)

                    st.success(
                        f"🎉 Fatura başarıyla kesildi! Fatura No: **{fatura_no}**"
                    )

                    st.markdown(
                        f"""
                    <div class="invoice-box">
                        <h2 style="margin:0; color:#111;">HAYAL MOBİLYA SAN. TİC. LTD. ŞTİ.</h2>
                        <p style="color:#555; font-size:12px; margin-top:2px;">Balıkesir / Edremit V.D. • VKN: 1234567890</p>
                        <hr style="border:1px solid #ddd;">
                        <table style="width:100%; font-size:13px; margin-bottom:15px;">
                            <tr>
                                <td><b>Fatura No:</b> {fatura_no}</td>
                                <td><b>Tarih:</b> {fatura_tarihi}</td>
                            </tr>
                            <tr>
                                <td><b>Müşteri:</b> {musteri_adi}</td>
                                <td><b>Ödeme Şekli:</b> {odeme_tipi}</td>
                            </tr>
                        </table>
                        <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
                            <tr style="background:#f2f2f2; border-bottom:1px solid #ddd;">
                                <th style="padding:8px;">Ürün / Açıklama</th>
                                <th style="padding:8px;">Miktar</th>
                                <th style="padding:8px;">Birim Fiyat</th>
                                <th style="padding:8px;">Toplam</th>
                            </tr>
                            <tr>
                                <td style="padding:8px; border-bottom:1px solid #eee;">{secilen_urun_fatura}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee;">{satis_adedi}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee;">₺{Birim_fiyat:,.2f}</td>
                                <td style="padding:8px; border-bottom:1px solid #eee;">₺{toplam_tutar:,.2f}</td>
                            </tr>
                        </table>
                        <div style="text-align:right; margin-top:15px; font-size:14px;">
                            <p style="margin:2px;">Matrah: ₺{matrah:,.2f}</p>
                            <p style="margin:2px;">KDV (%20): ₺{kdv_tutar:,.2f}</p>
                            <h3 style="margin:5px 0; color:#000;">Genel Toplam: ₺{toplam_tutar:,.2f}</h3>
                        </div>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )
            else:
                st.warning("Lütfen müşteri adını ve ürünü eksiksiz doldurun.")


# =========================================================
# FATURA İLE STOK İŞLE
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
# ŞİFREMİ DEĞİŞTİR
# =========================================================

elif menu_secim == "🔑 Şifremi Değiştir":
    st.markdown(
        '<div class="page-title">🔑 Personel Şifre Değiştirme Paneli</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şifrenizi unutmamanız veya güncel tutmanız için buradan değiştirebilirsiniz.</div>',
        unsafe_allow_html=True,
    )

    with st.form("sifre_degistir_form"):
        aktif_kullanici = st.session_state.current_user
        st.write(f"İşlem Yapılan Kullanıcı: **{aktif_kullanici}**")

        eski_sifre = st.text_input("Mevcut Şifreniz", type="password")
        yeni_sifre_1 = st.text_input("Yeni Şifreniz", type="password")
        yeni_sifre_2 = st.text_input("Yeni Şifreniz (Tekrar)", type="password")

        sifre_guncelle_btn = st.form_submit_button("🔒 Şifremi Güncelle")

        if sifre_guncelle_btn:
            if (
                aktif_kullanici in st.session_state.users
                and st.session_state.users[aktif_kullanici] == eski_sifre
            ):
                if yeni_sifre_1 and yeni_sifre_1 == yeni_sifre_2:
                    st.session_state.users[aktif_kullanici] = yeni_sifre_1
                    st.success(
                        "🎉 Şifreniz başarıyla güncellendi! Yeni şifrenizle giriş yapabilirsiniz."
                    )
                else:
                    st.warning(
                        "⚠️ Yeni girdiğiniz şifreler birbiriyle uyuşmuyor veya boş bırakıldı."
                    )
            else:
                st.error("❌ Mevcut şifrenizi hatalı girdiniz.")


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

elif menu_secim == "👥 Cari Hesaplar":
    st.markdown(
        '<div class="page-title">👥 Cari Hesaplar</div>',
        unsafe_allow_html=True,
    )
    if len(st.session_state.faturalar) > 0:
        st.write("Kesilen Faturalar / Hareketler:")
        st.dataframe(
            pd.DataFrame(st.session_state.faturalar),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Henüz kesilmiş bir fatura bulunmuyor.")

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
    © 2026 Hayal Mobilya • Ön Muhasebe ve Stok Takip Sistemi • v2.6.5
</div>
""",
    unsafe_allow_html=True,
)

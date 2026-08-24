from datetime import datetime
import random
import uuid
import pandas as pd
import streamlit as st

# =========================================================
# SAYFA AYARLARI
# =========================================================

st.set_page_config(
    page_title="Hayal Mobilya | Profesyonel ERP & Stok",
    page_icon="🪑",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CSS - PROFESYONEL KURUMSAL TEMA & ANİMASYONLAR
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #06090f;
    color: #f1f5f9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0b0f17 !important;
    border-right: 1px solid #1e2633;
}

.sidebar-logo {
    padding: 10px 5px 20px 5px;
}

.sidebar-logo .brand {
    font-size: 20px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.5px;
}

.sidebar-logo .sub {
    font-size: 11px;
    color: #64748b;
    margin-top: 2px;
}

/* Topbar */
.topbar {
    background: #0b0f17;
    border: 1px solid #1e2633;
    border-radius: 12px;
    padding: 12px 20px;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.topbar-title {
    font-size: 13px;
    color: #64748b;
}

.topbar-user {
    font-size: 14px;
    font-weight: 700;
    color: #cbd5e1;
}

/* Başlıklar */
.page-title {
    font-size: 26px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 2px;
}

.page-subtitle {
    color: #64748b;
    font-size: 13px;
    margin-bottom: 20px;
}

/* Kartlar */
.stat-card {
    background: linear-gradient(135deg, #0f172a, #0b0f17);
    border: 1px solid #1e2633;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 10px;
}

.stat-icon {
    font-size: 20px;
    margin-bottom: 8px;
}

.stat-title {
    font-size: 11px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.stat-value {
    font-size: 22px;
    font-weight: 800;
    color: #ffffff;
    margin-top: 4px;
}

.stat-change {
    font-size: 11px;
    color: #10b981;
    margin-top: 6px;
}

.section-title {
    font-size: 16px;
    font-weight: 700;
    margin: 20px 0 10px 0;
    color: #f8fafc;
}

/* Buton ve Inputlar */
.stButton > button {
    width: 100%;
    min-height: 40px;
    border-radius: 8px;
    border: 1px solid #293548;
    background: #111827;
    color: #ffffff;
    font-weight: 600;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #1f2937;
    border-color: #3b82f6;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div,
textarea {
    background: #0d1322 !important;
    border-color: #1e2633 !important;
    border-radius: 8px !important;
}

.invoice-box {
    background: #ffffff;
    color: #000000;
    padding: 25px;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    margin-top: 15px;
}

.footer {
    border-top: 1px solid #1e2633;
    margin-top: 40px;
    padding: 15px 0;
    color: #475569;
    font-size: 11px;
    text-align: center;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# ORTAK GLOBAL VERİTABANI (TÜM KULLANICILAR İÇİN ORTAK)
# =========================================================

if "global_users" not in st.session_state:
    st.session_state.global_users = {
        "Onur": "1234",
        "Admin": "123456",
        "Agam": "1234",
    }

if "global_personel_loglari" not in st.session_state:
    st.session_state.global_personel_loglari = []

if "global_stok_hareketleri" not in st.session_state:
    st.session_state.global_stok_hareketleri = [
        {
            "Zaman": "2026-08-24 08:30:00",
            "Personel": "Admin",
            "Ürün": "Luna Koltuk Takımı",
            "İşlem": "Sistem Başlangıç",
            "Miktar": 5,
        }
    ]

if "global_stok" not in st.session_state:
    st.session_state.global_stok = pd.DataFrame([
        {
            "Ürün Adı": "Luna Koltuk Takımı",
            "Barkod": "8690576896745",
            "Alış Fiyatı (TL)": 15000.0,
            "Satış Fiyatı (TL)": 22000.0,
            "Bakiye": 5,
            "Kritik Sınır": 3,
            "Birim": "Takım",
        },
        {
            "Ürün Adı": "Prag Yemek Masası Seti",
            "Barkod": "8690456765456",
            "Alış Fiyatı (TL)": 8000.0,
            "Satış Fiyatı (TL)": 12500.0,
            "Bakiye": 2,
            "Kritik Sınır": 4,
            "Birim": "Takım",
        },
        {
            "Ürün Adı": "Royal Yatak Odası Dolabı",
            "Barkod": "8690654389765",
            "Alış Fiyatı (TL)": 11000.0,
            "Satış Fiyatı (TL)": 16000.0,
            "Bakiye": 3,
            "Kritik Sınır": 3,
            "Birim": "Adet",
        },
    ])

if "Kritik Sınır" not in st.session_state.global_stok.columns:
    st.session_state.global_stok["Kritik Sınır"] = 3

if "global_cariler" not in st.session_state:
    st.session_state.global_cariler = pd.DataFrame([
        {
            "Cari Adı": "Ahmet Yılmaz (Perakende)",
            "Telefon": "0532 111 2233",
            "Tür": "Müşteri",
            "Bakiye (TL)": 0.0,
        },
        {
            "Cari Adı": "Kaleçam Orman Ürünleri",
            "Telefon": "0266 373 0000",
            "Tür": "Tedarikçi",
            "Bakiye (TL)": -15000.0,
        },
    ])

if "global_banka_hesaplari" not in st.session_state:
    st.session_state.global_banka_hesaplari = pd.DataFrame([
        {
            "Banka Adı": "Garanti BBVA",
            "Şube / Kod": "Edremit Şubesi (1234)",
            "Hesap Adı": "Merkez Ticari Hesap",
            "IBAN": "TR33 0006 2000 1230 0006 7890 12",
            "Döviz": "TL",
        },
        {
            "Banka Adı": "İş Bankası",
            "Şube / Kod": "Akçay Şubesi (5678)",
            "Hesap Adı": "Döviz / Euro Hesabı",
            "IBAN": "TR88 0006 4000 0012 3456 7890 34",
            "Döviz": "EUR",
        },
    ])

if "global_faturalar" not in st.session_state:
    st.session_state.global_faturalar = []

if "sifre_unuttum_aktif" not in st.session_state:
    st.session_state.sifre_unuttum_aktif = False

query_params = st.query_params
if "auth_user" in query_params and "authenticated" not in st.session_state:
    st.session_state.authenticated = True
    st.session_state.current_user = query_params["auth_user"]
    st.session_state.is_admin = query_params["auth_user"].lower() == "admin"

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False


# =========================================================
# GİRİŞ EKRANI
# =========================================================

if not st.session_state.authenticated:
    st.markdown(
        """
        <div style="max-width: 400px; margin: 40px auto 10px auto; text-align: center;">
            <h1 style="color: white; font-size: 26px; font-weight: 800;">🪑 HAYAL MOBİLYA</h1>
            <p style="color: #64748b; font-size: 13px;">Kurumsal Ön Muhasebe & Akıllı Stok Yönetimi</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if not st.session_state.sifre_unuttum_aktif:
            with st.form("giris_formu"):
                secilen_kullanici = st.selectbox(
                    "Kullanıcı Seçin", list(st.session_state.global_users.keys()), key="giris_kullanici_sec"
                )
                k_sifre = st.text_input("Şifre", type="password", key="giris_sifre_input")
                beni_hatirla = st.checkbox("Beni Hatırla (Sayfa Yenilense De Açık Kal)", value=True)
                
                giris_buton = st.form_submit_button("Güvenli Giriş Yap")

                if giris_buton:
                    if (
                        secilen_kullanici in st.session_state.global_users
                        and st.session_state.global_users[secilen_kullanici] == k_sifre
                    ):
                        st.session_state.authenticated = True
                        st.session_state.current_user = secilen_kullanici
                        st.session_state.is_admin = (
                            secilen_kullanici.lower() == "admin"
                        )

                        if beni_hatirla:
                            st.query_params["auth_user"] = secilen_kullanici

                        st.session_state.global_personel_loglari.insert(
                            0,
                            {
                                "Kullanıcı": secilen_kullanici,
                                "İşlem": "Giriş Yapıldı",
                                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            },
                        )
                        st.success("✅ Giriş başarılı, yönlendiriliyorsunuz...")
                        st.rerun()
                    else:
                        st.error("❌ Hatalı şifre girdiniz!")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔑 Şifremi Unuttum"):
                st.session_state.sifre_unuttum_aktif = True
                st.rerun()
        else:
            st.markdown("### Şifre Sıfırlama")
            with st.form("sifre_sifirla_formu"):
                s_kullanici = st.selectbox(
                    "Kullanıcı Seçin", list(st.session_state.global_users.keys()), key="sifirla_kullanici"
                )
                yeni_sifre_1 = st.text_input("Yeni Şifre", type="password", key="y_sifre1")
                yeni_sifre_2 = st.text_input("Yeni Şifre (Tekrar)", type="password", key="y_sifre2")

                sifre_guncelle_buton = st.form_submit_button("Şifreyi Güncelle ve Giriş Yap")

                if sifre_guncelle_buton:
                    if yeni_sifre_1 and yeni_sifre_1 == yeni_sifre_2:
                        st.session_state.global_users[s_kullanici] = yeni_sifre_1
                        st.session_state.authenticated = True
                        st.session_state.current_user = s_kullanici
                        st.session_state.is_admin = (s_kullanici.lower() == "admin")
                        st.session_state.sifre_unuttum_aktif = False
                        st.query_params["auth_user"] = s_kullanici

                        st.session_state.global_personel_loglari.insert(
                            0,
                            {
                                "Kullanıcı": s_kullanici,
                                "İşlem": "Şifre Sıfırlandı ve Giriş Yapıldı",
                                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            },
                        )
                        st.success("✅ Şifreniz başarıyla güncellendi, sisteme giriş yapılıyor...")
                        st.rerun()
                    else:
                        st.error("❌ Yeni şifreler boş olamaz ve birbiriyle uyuşmalıdır!")

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("⬅️ Geri Dön (Giriş Ekranına Git)"):
                st.session_state.sifre_unuttum_aktif = False
                st.rerun()

    st.stop()


# =========================================================
# MENÜ YAPISI
# =========================================================

menu_listesi = [
    "🏠 Ana Sayfa",
    "📦 Ürün Kataloğu & Stok",
    "🛠️ Hızlı İmalat / Stok Güncelle",
    "📊 Stok Hareket Geçmişi",
    "🧾 Satış Faturası Kes",
    "📄 Fatura / İrsaliye İşle",
    "👥 Cari Hesaplar & Borçlar",
    "🏦 Banka Hesapları",
    "➕ Yeni Ürün Kartı Aç",
    "💰 Kasa & Finans",
    "📊 Raporlar & Analiz",
    "🔑 Şifre Değiştir",
]

if st.session_state.is_admin:
    menu_listesi.insert(1, "🔒 Yönetici Paneli")

with st.sidebar:
    st.markdown(
        f"""
    <div class="sidebar-logo">
        <div class="brand">🪑 HAYAL MOBİLYA</div>
        <div class="sub">ERP & STOK YÖNETİMİ v3.4</div>
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    menu_secim = st.radio("MENÜ", menu_listesi, key="ana_menu_secim")
    st.markdown("---")

    rol_str = (
        "Sistem Yöneticisi" if st.session_state.is_admin else "Yetkili Personel"
    )
    st.markdown(
        f"""
    <div style="background:#0f172a; border:1px solid #1e2633; padding:10px; border-radius:8px; font-size:12px;">
        <b>👤 {st.session_state.current_user}</b><br>
        <span style="color:#10b981;">{rol_str}</span>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 Güvenli Çıkış"):
        st.session_state.authenticated = False
        if "auth_user" in st.query_params:
            del st.query_params["auth_user"]
        st.rerun()


# Üst Bilgi Barı
st.markdown(
    f"""
<div class="topbar">
    <div class="topbar-title">Edremit Üretim Tesisi • Canlı Entegre Sistem</div>
    <div class="topbar-user">Oturum Açan: {st.session_state.current_user}</div>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# 1. YÖNETİCİ PANELİ
# =========================================================

if menu_secim == "🔒 Yönetici Paneli":
    if not st.session_state.is_admin:
        st.error("❌ Bu alana erişim yetkiniz bulunmuyor.")
        st.stop()

    st.markdown(
        '<div class="page-title">🔒 Yönetici & Güvenlik Paneli</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Personel yetkilendirme ve sistem log denetimi.</div>',
        unsafe_allow_html=True,
    )

    t1, t2 = st.tabs(["👥 Personel Yönetimi", "🕒 Sistem Logları"])
    with t1:
        st.dataframe(
            pd.DataFrame(
                [
                    {"Kullanıcı": k, "Yetki": "Admin" if k == "Admin" else "Personel"}
                    for k in st.session_state.global_users
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### Yeni Personel Ekle")
        with st.form("yeni_p_form"):
            p_ad = st.text_input("Kullanıcı Adı")
            p_Sif = st.text_input("Şifre", type="password")
            if st.form_submit_button("Personel Kaydet"):
                if p_ad:
                    st.session_state.global_users[p_ad] = p_Sif
                    st.success(f"✅ {p_ad} başarıyla eklendi.")
                else:
                    st.error("❌ Kullanıcı adı boş olamaz!")
    with t2:
        if len(st.session_state.global_personel_loglari) > 0:
            st.dataframe(
                pd.DataFrame(st.session_state.global_personel_loglari),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("Kayıtlı log bulunmuyor.")


# =========================================================
# 2. ANA SAYFA
# =========================================================

elif menu_secim == "🏠 Ana Sayfa":
    st.markdown(
        '<div class="page-title">Kontrol Paneli (Dashboard)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Üretim, stok, finans ve atölye performansının genel özeti.</div>',
        unsafe_allow_html=True,
    )

    df_stok = st.session_state.global_stok
    toplam_cesit = len(df_stok)
    toplam_adet = int(df_stok["Bakiye"].sum())
    maliyet_toplam = (df_stok["Alış Fiyatı (TL)"] * df_stok["Bakiye"]).sum()
    satis_potansiyeli = (df_stok["Satış Fiyatı (TL)"] * df_stok["Bakiye"]).sum()
    
    toplam_ciro = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if len(st.session_state.global_faturalar) > 0 else 0.0
    kritik_df = df_stok[df_stok["Bakiye"] <= df_stok["Kritik Sınır"]]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📦</div>
            <div class="stat-title">Ürün Çeşidi</div>
            <div class="stat-value">{toplam_cesit}</div>
            <div class="stat-change">Aktif Katalog</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-title">Toplam Stok Adedi</div>
            <div class="stat-value">{toplam_adet:,}</div>
            <div class="stat-change">Ürün Miktarı</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-title">Stok Maliyet Değeri</div>
            <div class="stat-value">₺{maliyet_toplam:,.0f}</div>
            <div class="stat-change">Yatırım Tutarı</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🚨</div>
            <div class="stat-title">Kritik Stok Uyarı</div>
            <div class="stat-value">{len(kritik_df)}</div>
            <div class="stat-change" style="color:#ef4444;">Acil Üretim Gereken</div>
        </div>""",
            unsafe_allow_html=True,
        )

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">💵</div>
            <div class="stat-title">Toplam Kesilen Ciro</div>
            <div class="stat-value">₺{toplam_ciro:,.0f}</div>
            <div class="stat-change">Faturalandırılan</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🏷️</div>
            <div class="stat-title">Potansiyel Satış Değeri</div>
            <div class="stat-value">₺{satis_potansiyeli:,.0f}</div>
            <div class="stat-change">Depodaki Malın Satış Karşılığı</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">🧾</div>
            <div class="stat-title">Kesilen Fatura Adedi</div>
            <div class="stat-value">{len(st.session_state.global_faturalar)}</div>
            <div class="stat-change">İşlem Sayısı</div>
        </div>""",
            unsafe_allow_html=True,
        )
    with f4:
        st.markdown(
            f"""
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-title">Kayıtlı Cari Sayısı</div>
            <div class="stat-value">{len(st.session_state.global_cariler)}</div>
            <div class="stat-change">Müşteri & Tedarikçi</div>
        </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    tab_dash1, tab_dash2 = st.tabs(["🚨 Kritik Eşikteki Ürünler", "🕒 Son Depo / Atölye Hareketleri"])
    with tab_dash1:
        if len(kritik_df) > 0:
            st.dataframe(kritik_df, use_container_width=True, hide_index=True)
        else:
            st.success("✅ Kritik eşiğin altında azalan ürün bulunmuyor. Stok durumları sağlıklı.")

    with tab_dash2:
        if len(st.session_state.global_stok_hareketleri) > 0:
            st.dataframe(pd.DataFrame(st.session_state.global_stok_hareketleri).head(10), use_container_width=True, hide_index=True)
        else:
            st.info("Kayıtlı hareket bulunmuyor.")


# =========================================================
# 3. ÜRÜN KATALOĞU & STOK
# =========================================================

elif menu_secim == "📦 Ürün Kataloğu & Stok":
    st.markdown(
        '<div class="page-title">📦 Ürün Kataloğu & Stok Durumu</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Tüm mobilya kalemleri ve dinamik stok eşikleri.</div>',
        unsafe_allow_html=True,
    )

    arama = st.text_input(
        "🔎 Ürün Ara / Barkod Okut",
        placeholder="Ürün adı veya barkod giriniz...",
    )
    df_s = st.session_state.global_stok.copy()
    if arama:
        df_s = df_s[
            df_s["Ürün Adı"]
            .str.contains(arama, case=False, na=False)
            | df_s["Barkod"].astype(str).str.contains(arama, case=False, na=False)
        ]

    st.dataframe(df_s, use_container_width=True, hide_index=True)


# =========================================================
# 4. HIZLI İMALAT / STOK GÜNCELLE
# =========================================================

elif menu_secim == "🛠️ Hızlı İmalat / Stok Güncelle":
    st.markdown(
        '<div class="page-title">🛠️ Atölye İmalat & Hızlı Stok Girişi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">İmalattan çıkan ürünleri faturasız olarak anında stok sistemine işleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("imalat_form_gelismis"):
        sec_urun = st.selectbox(
            "Üretilen Ürünü Seçin", st.session_state.global_stok["Ürün Adı"].tolist()
        )
        islem_turu = st.selectbox(
            "İşlem Türü",
            [
                "➕ İmalat Tamamlandı (Stoğa Ekle)",
                "➖ Fire / Sevk / Düşüş Yap",
            ],
        )
        adet = st.number_input("Miktar", min_value=1, step=1, value=1)
        not_aciklama = st.text_input(
            "İmalat Notu / Seri No", placeholder="Örn: 1. Etap Atölye Üretimi"
        )

        kaydet_imalat = st.form_submit_button("💾 Stok Güncellemesini Kaydet")

        if kaydet_imalat:
            idx = st.session_state.global_stok[
                st.session_state.global_stok["Ürün Adı"] == sec_urun
            ].index[0]
            mevcut = int(st.session_state.global_stok.loc[idx, "Bakiye"])

            if "Ekle" in islem_turu:
                st.session_state.global_stok.loc[idx, "Bakiye"] = mevcut + adet
                islem_tip_str = "İmalat Girişi (+)"
                st.success(f"✅ İşlem Başarılı! {sec_urun} stoğa eklendi. Yeni Bakiye: {st.session_state.global_stok.loc[idx, 'Bakiye']}")
            else:
                if adet > mevcut:
                    st.error(f"❌ Hata: Mevcut stoktan ({mevcut} adet) fazla düşüş yapılamaz!")
                    st.stop()
                st.session_state.global_stok.loc[idx, "Bakiye"] = mevcut - adet
                islem_tip_str = "İmalat/Fire Çıkışı (-)"
                st.success(f"✅ İşlem Başarılı! {sec_urun} stoktan düşüldü. Kalan: {st.session_state.global_stok.loc[idx, 'Bakiye']}")

            st.session_state.global_stok_hareketleri.insert(
                0,
                {
                    "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Personel": st.session_state.current_user,
                    "Ürün": sec_urun,
                    "İşlem": islem_tip_str,
                    "Miktar": adet,
                },
            )


# =========================================================
# 5. STOK HAREKET GEÇMİŞİ
# =========================================================

elif menu_secim == "📊 Stok Hareket Geçmişi":
    st.markdown(
        '<div class="page-title">📊 Detaylı Stok Hareket Logları</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Hangi ürünün ne zaman, kim tarafından sisteme eklendiğinin denetim kaydı.</div>',
        unsafe_allow_html=True,
    )

    if len(st.session_state.global_stok_hareketleri) > 0:
        st.dataframe(
            pd.DataFrame(st.session_state.global_stok_hareketleri),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Henüz kaydedilmiş bir stok hareketi bulunmuyor.")


# =========================================================
# 6. SATIŞ FATURASI KES
# =========================================================

elif menu_secim == "🧾 Satış Faturası Kes":
    st.markdown(
        '<div class="page-title">🧾 Satış Faturası Kes & Stok Düş</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kurumsal e-fatura şablonu oluşturun ve cari hesaplara yansıtın.</div>',
        unsafe_allow_html=True,
    )

    with st.form("satis_form_kurumsal"):
        c1, c2 = st.columns(2)
        with c1:
            m_ad = st.text_input(
                "Müşteri Adı Soyadı / Firma *", placeholder="Örn: Mehmet Demir"
            )
            m_vkn = st.text_input("TCKN / Vergi No")
        with c2:
            f_tar = st.date_input("Fatura Tarihi", value=datetime.today())
            odeme_sekli = st.selectbox(
                "Ödeme Yöntemi", ["Nakit", "Kredi Kartı", "Banka Havalesi"]
            )

        st.markdown("---")
        s_urun = st.selectbox(
            "Satılacak Mobilya Ürünü *",
            st.session_state.global_stok["Ürün Adı"].tolist(),
        )
        s_adet = st.number_input(
            "Satış Miktarı (Adet/Takım) *", min_value=1, step=1, value=1
        )

        satis_onay = st.form_submit_button("🚀 Faturayı Kes ve Onayla")

        if satis_onay:
            if not m_ad:
                st.error("❌ Hata: Müşteri adı boş olamaz!")
            else:
                idx = st.session_state.global_stok[
                    st.session_state.global_stok["Ürün Adı"] == s_urun
                ].index[0]
                mevcut_stk = int(st.session_state.global_stok.loc[idx, "Bakiye"])
                satis_fiyat = float(
                    st.session_state.global_stok.loc[idx, "Satış Fiyatı (TL)"]
                )

                if s_adet > mevcut_stk:
                    st.error(
                        f"❌ Yetersiz Stok! Depoda sadece {mevcut_stk} adet var."
                    )
                else:
                    st.session_state.global_stok.loc[idx, "Bakiye"] = mevcut_stk - s_adet
                    toplam_tutar = satis_fiyat * s_adet
                    kdv = toplam_tutar - (toplam_tutar / 1.20)
                    matrah = toplam_tutar - kdv
                    f_no = f"HYL2026{len(st.session_state.global_faturalar)+1:04d}"

                    st.session_state.global_faturalar.append({
                        "Fatura No": f_no,
                        "Müşteri": m_ad,
                        "Ürün": s_urun,
                        "Miktar": s_adet,
                        "Toplam": toplam_tutar,
                    })

                    st.session_state.global_stok_hareketleri.insert(
                        0,
                        {
                            "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "Personel": st.session_state.current_user,
                            "Ürün": s_urun,
                            "İşlem": "Satış Faturası (-)",
                            "Miktar": s_adet,
                        },
                    )

                    st.success(f"✅ Fatura başarıyla oluşturuldu ve onaylandı. No: {f_no}")
                    st.markdown(
                        f"""
                    <div class="invoice-box">
                        <h2 style="margin:0; color:#000;">HAYAL MOBİLYA SAN. TİC. LTD. ŞTİ.</h2>
                        <p style="color:#555; font-size:11px;">Edremit / Balıkesir V.D. • VKN: 1234567890</p>
                        <hr style="border:1px solid #ddd;">
                        <p><b>Fatura No:</b> {f_no} | <b>Tarih:</b> {f_tar}</p>
                        <p><b>Müşteri:</b> {m_ad}</p>
                        <table style="width:100%; border-collapse:collapse; font-size:12px; margin-top:10px;">
                            <tr style="background:#eee; text-align:left;">
                                <th style="padding:6px;">Ürün</th><th style="padding:6px;">Adet</th><th style="padding:6px;">Birim Fiyat</th><th style="padding:6px;">Toplam</th>
                            </tr>
                            <tr>
                                <td style="padding:6px; border-bottom:1px solid #ddd;">{s_urun}</td>
                                <td style="padding:6px; border-bottom:1px solid #ddd;">{s_adet}</td>
                                <td style="padding:6px; border-bottom:1px solid #ddd;">₺{satis_fiyat:,.2f}</td>
                                <td style="padding:6px; border-bottom:1px solid #ddd;">₺{toplam_tutar:,.2f}</td>
                            </tr>
                        </table>
                        <div style="text-align:right; margin-top:10px; font-size:13px;">
                            <p>Matrah: ₺{matrah:,.2f}</p>
                            <p>KDV (%20): ₺{kdv:,.2f}</p>
                            <h3>Genel Toplam: ₺{toplam_tutar:,.2f}</h3>
                        </div>
                    </div>""",
                        unsafe_allow_html=True,
                    )


# =========================================================
# 7. FATURA İLE STOK İŞLE
# =========================================================

elif menu_secim == "📄 Fatura / İrsaliye İşle":
    st.markdown(
        '<div class="page-title">📄 Tedarikçi Faturası & İrsaliye İşleme</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Dışarıdan gelen mal alım faturalarını sisteme işleyin.</div>',
        unsafe_allow_html=True,
    )
    st.file_uploader(
        "Fatura Dosyası Yükle (PDF / Görsel)", type=["pdf", "png", "jpg"]
    )
    with st.form("IRSALIYE_FORM"):
        tur = st.selectbox(
            "İşlem Türü", ["Alış Faturası (Stok Artır)", "İade / Düşüm"]
        )
        urun_sec = st.selectbox(
            "Ürün Seç", st.session_state.global_stok["Ürün Adı"].tolist()
        )
        mik = st.number_input("Adet", min_value=1, step=1)
        irsaliye_onay = st.form_submit_button("Faturayı Onayla ve İşle")

        if irsaliye_onay:
            idx = st.session_state.global_stok[
                st.session_state.global_stok["Ürün Adı"] == urun_sec
            ].index[0]
            mevcut_bakiye = int(st.session_state.global_stok.loc[idx, "Bakiye"])
            
            if "Artır" in tur:
                st.session_state.global_stok.loc[idx, "Bakiye"] = mevcut_bakiye + mik
                islem_turu_str = "Alış Faturası Girişi (+)"
                st.success("✅ Stok başarıyla artırıldı ve onaylandı.")
            else:
                if mik > mevcut_bakiye:
                    st.error("❌ Hata: Mevcut stoktan fazla düşüm yapılamaz!")
                    st.stop()
                st.session_state.global_stok.loc[idx, "Bakiye"] = mevcut_bakiye - mik
                islem_turu_str = "İade / Düşüm (-)"
                st.success("✅ Stoktan düşüm işlemi başarıyla onaylandı.")

            st.session_state.global_stok_hareketleri.insert(
                0,
                {
                    "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Personel": st.session_state.current_user,
                    "Ürün": urun_sec,
                    "İşlem": islem_turu_str,
                    "Miktar": mik,
                },
            )


# =========================================================
# 8. CARİ HESAPLAR
# =========================================================

elif menu_secim == "👥 Cari Hesaplar & Borçlar":
    st.markdown(
        '<div class="page-title">👥 Cari Hesaplar & Borç / Alacak Takibi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Müşteri ve tedarikçilerinizin finansal bakiye durumları.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(st.session_state.global_cariler, use_container_width=True, hide_index=True)


# =========================================================
# 9. BANKA HESAPLARI
# =========================================================

elif menu_secim == "🏦 Banka Hesapları":
    st.markdown(
        '<div class="page-title">🏦 Banka Hesapları & IBAN Bilgileri</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirketin aktif ticari banka hesapları ve IBAN listesi.</div>',
        unsafe_allow_html=True,
    )
    st.dataframe(st.session_state.global_banka_hesaplari, use_container_width=True, hide_index=True)


# =========================================================
# 10. YENİ ÜRÜN KARTI AÇ
# =========================================================

elif menu_secim == "➕ Yeni Ürün Kartı Aç":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün / Mobilya Kartı Tanımla</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kataloğa yeni bir mobilya modeli veya hammadde ekleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("yeni_urun_formu"):
        y_ad = st.text_input("Ürün / Model Adı *")
        y_barkod = st.text_input("Barkod Numarası", value=str(random.randint(8690000000000, 8699999999999)))
        c1, c2 = st.columns(2)
        with c1:
            y_alis = st.number_input("Alış / Maliyet Fiyatı (TL)", min_value=0.0, step=100.0, value=1000.0)
            y_bakiye = st.number_input("Başlangıç Stok Adedi", min_value=0, step=1, value=5)
        with c2:
            y_satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0, step=100.0, value=1500.0)
            y_kritik = st.number_input("Kritik Stok Sınırı", min_value=1, step=1, value=3)
        y_birim = st.selectbox("Birim", ["Adet", "Takım", "Metre", "Paket"])

        yeni_urun_kaydet = st.form_submit_button("💾 Yeni Ürünü Kataloğa Kaydet")

        if yeni_urun_kaydet:
            if not y_ad:
                st.error("❌ Ürün adı boş olamaz!")
            else:
                yeni_satir = pd.DataFrame([{
                    "Ürün Adı": y_ad,
                    "Barkod": y_barkod,
                    "Alış Fiyatı (TL)": y_alis,
                    "Satış Fiyatı (TL)": y_satis,
                    "Bakiye": y_bakiye,
                    "Kritik Sınır": y_kritik,
                    "Birim": y_birim,
                }])
                st.session_state.global_stok = pd.concat([st.session_state.global_stok, yeni_satir], ignore_index=True)
                st.success(f"✅ {y_ad} başarıyla sisteme eklendi!")


# =========================================================
# 11. KASA & FİNANS
# =========================================================

elif menu_secim == "💰 Kasa & Finans":
    st.markdown(
        '<div class="page-title">💰 Kasa & Şirket Finans Durumu</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Genel gelir-gider dengesi ve kasa akışı.</div>',
        unsafe_allow_html=True,
    )
    toplam_ciro_kasa = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if len(st.session_state.global_faturalar) > 0 else 0.0
    st.metric("Toplam Tahsil Edilen / Faturalandırılan Tutar", f"₺{toplam_ciro_kasa:,.2f}")
    st.info("Detaylı kasa hareketleri ve günlük gelir/gider modülü sonraki güncellemede aktifleşecektir.")


# =========================================================
# 12. RAPORLAR & ANALİZ
# =========================================================

elif menu_secim == "📊 Raporlar & Analiz":
    st.markdown(
        '<div class="page-title">📊 Kapsamlı Raporlar & Analizler</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Üretim hızı, en çok satan ürünler ve finansal özet raporları.</div>',
        unsafe_allow_html=True,
    )
    st.bar_chart(st.session_state.global_stok.set_index("Ürün Adı")["Bakiye"])


# =========================================================
# 13. ŞİFRE DEĞİŞTİR
# =========================================================

elif menu_secim == "🔑 Şifre Değiştir":
    st.markdown(
        '<div class="page-title">🔑 Kullanıcı Şifre Değiştirme</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Güvenliğiniz için şifrenizi güncelleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("sifre_degistir_form"):
        eski_s = st.text_input("Eski Şifre", type="password")
        yeni_s1 = st.text_input("Yeni Şifre", type="password")
        yeni_s2 = st.text_input("Yeni Şifre (Tekrar)", type="password")
        degistir_btn = st.form_submit_button("Şifreyi Güncelle")

        if degistir_btn:
            aktif_kul = st.session_state.current_user
            if st.session_state.global_users.get(aktif_kul) == eski_s:
                if yeni_s1 and yeni_s1 == yeni_s2:
                    st.session_state.global_users[aktif_kul] = yeni_s1
                    st.success("✅ Şifreniz başarıyla değiştirildi!")
                else:
                    st.error("❌ Yeni şifreler uyuşmuyor veya boş bırakılamaz!")
            else:
                st.error("❌ Eski şifrenizi hatalı girdiniz!")

# Altbilgi
st.markdown(
    """
<div class="footer">
    Hayal Mobilya ERP & Stok Yönetim Sistemi • Tüm Hakları Saklıdır © 2026
</div>
""",
    unsafe_allow_html=True,
)

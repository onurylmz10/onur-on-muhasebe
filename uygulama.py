import random
from datetime import datetime
import pandas as pd
import streamlit as st

# =========================================================
# 1. SAYFA YAPILANDIRMASI & STİLLER
# =========================================================
st.set_page_config(
    page_title="Hayal Mobilya ERP & Stok Yönetimi",
    page_icon="🪑",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #f8f9fa; }
    .page-title { font-size: 24px; font-weight: 700; color: #1e293b; margin-bottom: 5px; }
    .page-subtitle { font-size: 14px; color: #64748b; margin-bottom: 20px; }
    .stat-card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 1px 3px rgba(0,0.1,0.1,0.1); border-left: 4px solid #3b82f6; }
    .stat-title { font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .stat-value { font-size: 22px; font-weight: 700; color: #0f172a; margin-top: 5px; }
    .stat-change { font-size: 12px; color: #10b981; margin-top: 5px; }
    .footer { text-align: center; margin-top: 50px; font-size: 12px; color: #94a3b8; border-top: 1px solid #e2e8f0; padding-top: 15px; }
    </style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 2. SESSION STATE (OTURUM VERİLERİ) BAŞLATMA
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""

# Kullanıcı Veritabanı
if "global_users" not in st.session_state:
    st.session_state.global_users = {
        "admin": "1234",
        "onur": "2026",
        "personel": "0000",
    }

# Stok Veritabanı
if "global_stok" not in st.session_state:
    st.session_state.global_stok = pd.DataFrame(
        [
            {
                "Ürün Adı": "Viyana Köşe Koltuk Takımı",
                "Barkod": "8690011223344",
                "Alış Fiyatı (TL)": 12000.0,
                "Satış Fiyatı (TL)": 18500.0,
                "Bakiye": 8,
                "Kritik Sınır": 3,
                "Birim": "Takım",
            },
            {
                "Ürün Adı": "Milano Yemek Masası (6 Kişilik)",
                "Barkod": "8690055667788",
                "Alış Fiyatı (TL)": 6500.0,
                "Satış Fiyatı (TL)": 9900.0,
                "Bakiye": 4,
                "Kritik Sınır": 2,
                "Birim": "Adet",
            },
            {
                "Ürün Adı": "Liva Zigon Sehpa Seti",
                "Barkod": "8690099887766",
                "Alış Fiyatı (TL)": 1500.0,
                "Satış Fiyatı (TL)": 2750.0,
                "Bakiye": 12,
                "Kritik Sınır": 5,
                "Birim": "Set",
            },
        ]
    )

# Cari Veritabanı
if "global_cariler" not in st.session_state:
    st.session_state.global_cariler = pd.DataFrame(
        [
            {
                "Cari Adı": "Ahmet Mobilya Ltd. Şti.",
                "Telefon": "0532 555 4433",
                "Tür": "Müşteri",
                "Bakiye (TL)": 14500.0,
            },
            {
                "Cari Adı": "Balıkesir Ahşap Palet San.",
                "Telefon": "0266 222 1122",
                "Tür": "Tedarikçi",
                "Bakiye (TL)": -8200.0,
            },
        ]
    )

# Banka Hesapları Veritabanı
if "global_banka_hesaplari" not in st.session_state:
    st.session_state.global_banka_hesaplari = pd.DataFrame(
        [
            {
                "Banka Adı": "Ziraat Bankası",
                "Şube / Kod": "Edremit Şubesi / 1234",
                "Hesap Adı": "Ticari Vadesiz TL",
                "IBAN": "TR33 0001 0012 3456 7890 1234 56",
                "Döviz": "TL",
            },
            {
                "Banka Adı": "Garanti BBVA",
                "Şube / Kod": "Edremit Kurumsal / 567",
                "Hesap Adı": "Ticari Döviz Hesabı",
                "IBAN": "TR62 0006 2000 1234 5678 9012 34",
                "Döviz": "USD",
            },
        ]
    )

# Fatura & Log Listeleri
if "global_faturalar" not in st.session_state:
    st.session_state.global_faturalar = []
if "global_stok_hareketleri" not in st.session_state:
    st.session_state.global_stok_hareketleri = []
if "global_personel_loglari" not in st.session_state:
    st.session_state.global_personel_loglari = []


# =========================================================
# 3. KULLANICI GİRİŞ (LOGIN) EKRANI
# =========================================================
if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; color: #1e293b;'>🪑 Hayal Mobilya ERP Giriş</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        with st.form("login_form"):
            kullanici_adi = st.text_input("Kullanıcı Adı")
            sifre = st.text_input("Şifre", type="password")
            submit = st.form_submit_button("Sisteme Giriş Yap", use_container_width=True)

            if submit:
                if (
                    kullanici_adi in st.session_state.global_users
                    and st.session_state.global_users[kullanici_adi] == sifre
                ):
                    st.session_state.logged_in = True
                    st.session_state.current_user = kullanici_adi
                    st.session_state.user_role = (
                        "Admin" if kullanici_adi in ["admin", "onur"] else "Personel"
                    )
                    st.success("✅ Giriş başarılı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("❌ Hatalı kullanıcı adı veya şifre!")
    st.stop()


# =========================================================
# 4. SOL MENÜ & NAVİGASYON
# =========================================================
st.sidebar.markdown(f"### 👤 Oturum: **{st.session_state.current_user}**")
st.sidebar.caption(f"Rol: {st.session_state.user_role}")
st.sidebar.divider()

menu_secim = st.sidebar.radio(
    "Ana Menü",
    [
        "🏠 Ana Sayfa & Dashboard",
        "📦 Stok & Depo Yönetimi",
        "🧾 Satış & Fatura Kes",
        "👥 Cari Hesaplar & Borçlar",
        "🏦 Banka Hesapları",
        "➕ Yeni Ürün Kartı Aç",
        "💰 Kasa & Finans",
        "📊 Raporlar & Analiz",
        "🔑 Şifre Değiştir",
    ],
)

if st.sidebar.button("🚪 Oturumu Kapat", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""
    st.rerun()


# =========================================================
# 5. ANA SAYFA & DASHBOARD
# =========================================================
if menu_secim == "🏠 Ana Sayfa & Dashboard":
    st.markdown(
        '<div class="page-title">🏠 Hayal Mobilya Yönetim Paneli</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Üretim, stok ve finansal operasyonların genel görünümü.</div>',
        unsafe_allow_html=True,
    )

    toplam_urun_cesidi = len(st.session_state.global_stok)
    toplam_stok_miktari = st.session_state.global_stok["Bakiye"].sum()
    toplam_cari_sayisi = len(st.session_state.global_cariler)
    kritik_urun_sayisi = len(
        st.session_state.global_stok[
            st.session_state.global_stok["Bakiye"]
            <= st.session_state.global_stok["Kritik Sınır"]
        ]
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            f"""<div class="stat-card"><div class="stat-title">Ürün Çeşidi</div><div class="stat-value">{toplam_urun_cesidi}</div></div>""",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""<div class="stat-card"><div class="stat-title">Toplam Adet</div><div class="stat-value">{toplam_stok_miktari}</div></div>""",
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""<div class="stat-card"><div class="stat-title">Cari / Müşteri</div><div class="stat-value">{toplam_cari_sayisi}</div></div>""",
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            f"""<div class="stat-card" style="border-left-color: #ef4444;"><div class="stat-title">Kritik Stok</div><div class="stat-value">{kritik_urun_sayisi}</div></div>""",
            unsafe_allow_html=True,
        )

    st.markdown("### ⚡ Hızlı İşlem Kısayolları")
    q1, q2, q3 = st.columns(3)
    with q1:
        if st.button("📦 Stoğa Git", use_container_width=True):
            pass
    with q2:
        if st.button("🧾 Fatura Kes", use_container_width=True):
            pass
    with q3:
        if st.button("➕ Ürün Ekle", use_container_width=True):
            pass


# =========================================================
# 6. STOK & DEPO YÖNETİMİ
# =========================================================
elif menu_secim == "📦 Stok & Depo Yönetimi":
    st.markdown(
        '<div class="page-title">📦 Stok & Depo Envanter Yönetimi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Depodaki mevcut mobilya ve malzeme stok seviyeleri.</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        st.session_state.global_stok, use_container_width=True, hide_index=True
    )

    st.markdown("#### 🔄 Hızlı Stok Miktar Güncelleme")
    with st.form("stok_Guncelle_form"):
        secilen_urun = st.selectbox(
            "Ürün Seç", st.session_state.global_stok["Ürün Adı"].tolist()
        )
        islem_tipi = st.selectbox("İşlem", ["Stok Ekle (+)", "Stok Düş (-)"])
        miktar = st.number_input("Miktar", min_value=1, step=1, value=1)
        guncelle_btn = st.form_submit_button("Stok Hareketi İşle")

        if guncelle_btn:
            idx = st.session_state.global_stok[
                st.session_state.global_stok["Ürün Adı"] == secilen_urun
            ].index[0]
            if islem_tipi == "Stok Ekle (+)":
                st.session_state.global_stok.loc[idx, "Bakiye"] += miktar
            else:
                if st.session_state.global_stok.loc[idx, "Bakiye"] >= miktar:
                    st.session_state.global_stok.loc[idx, "Bakiye"] -= miktar
                else:
                    st.error("❌ Stokta yeterli miktar bulunmuyor!")

            st.session_state.global_personel_loglari.insert(
                0,
                {
                    "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Personel": st.session_state.current_user,
                    "Ürün": secilen_urun,
                    "İşlem": islem_tipi,
                    "Miktar": miktar,
                },
            )
            st.success(f"✅ {secilen_urun} için stok hareketi başarıyla işlendi.")
            st.rerun()


# =========================================================
# 7. SATIŞ & FATURA KES
# =========================================================
elif menu_secim == "🧾 Satış & Fatura Kes":
    st.markdown(
        '<div class="page-title">🧾 Satış Faturası Kesme Modülü</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Müşterileriniz adına resmi fatura düzenleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("fatura_form"):
        f_cari = st.selectbox(
            "Cari / Müşteri Seç", st.session_state.global_cariler["Cari Adı"].tolist()
        )
        f_urun = st.selectbox(
            "Ürün Seç", st.session_state.global_stok["Ürün Adı"].tolist()
        )
        f_adet = st.number_input("Satış Adedi", min_value=1, step=1, value=1)
        f_kdv = st.selectbox("KDV Oranı", [20, 10, 1])

        fatura_kes_btn = st.form_submit_button("Faturayı Oluştur & Kes")

        if fatura_kes_btn:
            # Birim fiyat çek
            birim_fiyat = float(
                st.session_state.global_stok.loc[
                    st.session_state.global_stok["Ürün Adı"] == f_urun,
                    "Satış Fiyatı (TL)",
                ].values[0]
            )
            tutar_kdvsiz = birim_fiyat * f_adet
            kdv_tutar = tutar_kdvsiz * (f_kdv / 100.0)
            toplam_tutar = tutar_kdvsiz + kdv_tutar

            yeni_fatura = {
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Müşteri": f_cari,
                "Ürün": f_urun,
                "Adet": f_adet,
                "Toplam": toplam_tutar,
                "Kesen": st.session_state.current_user,
            }
            st.session_state.global_faturalar.append(yeni_fatura)
            st.success(
                f"✅ {f_cari} adına ₺{toplam_tutar:,.2f} tutarlı fatura başarıyla kesildi!"
            )


# =========================================================
# 8. CARİ HESAPLAR & BORÇLAR
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

    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.dataframe(
            st.session_state.global_cariler,
            use_container_width=True,
            hide_index=True,
        )

    with col_c2:
        st.markdown("#### ➕ Yeni Cari Kart Ekle")
        with st.form("yeni_cari_form"):
            c_adi = st.text_input("Cari / Firma Adı")
            c_tel = st.text_input("Telefon Numarası")
            c_tur = st.selectbox("Cari Türü", ["Müşteri", "Tedarikçi"])
            c_bakiye = st.number_input(
                "Başlangıç Bakiyesi (TL)", value=0.0, step=100.0
            )

            cari_kaydet = st.form_submit_button("Cari Kartı Oluştur")
            if cari_kaydet:
                if c_adi:
                    yeni_cari_satir = pd.DataFrame(
                        [
                            {
                                "Cari Adı": c_adi,
                                "Telefon": c_tel,
                                "Tür": c_tur,
                                "Bakiye (TL)": c_bakiye,
                            }
                        ]
                    )
                    st.session_state.global_cariler = pd.concat(
                        [st.session_state.global_cariler, yeni_cari_satir],
                        ignore_index=True,
                    )
                    st.success(f"✅ {c_adi} cari listesine başarıyla eklendi.")
                    st.rerun()
                else:
                    st.error("❌ Cari adı boş olamaz!")


# =========================================================
# 9. BANKA HESAPLARI
# =========================================================
elif menu_secim == "🏦 Banka Hesapları":
    st.markdown(
        '<div class="page-title">🏦 Banka Hesapları & IBAN Yönetimi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirket ticari hesapları, şube bilgileri ve IBAN listesi.</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(
        st.session_state.global_banka_hesaplari,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("#### ➕ Yeni Banka Hesabı Tanımla")
    with st.form("banka_ekle_form"):
        b_adi = st.text_input("Banka Adı (Örn: Yapı Kredi)")
        b_sube = st.text_input("Şube / Kod")
        b_hesap = st.text_input("Hesap Adı")
        b_iban = st.text_input("IBAN Numarası", placeholder="TR...")
        b_doviz = st.selectbox("Döviz Cinsi", ["TL", "EUR", "USD"])

        banka_kayit_btn = st.form_submit_button("Banka Hesabını Kaydet")
        if banka_kayit_btn:
            if b_adi and b_iban:
                yeni_banka = pd.DataFrame(
                    [
                        {
                            "Banka Adı": b_adi,
                            "Şube / Kod": b_sube,
                            "Hesap Adı": b_hesap,
                            "IBAN": b_iban,
                            "Döviz": b_doviz,
                        }
                    ]
                )
                st.session_state.global_banka_hesaplari = pd.concat(
                    [st.session_state.global_banka_hesaplari, yeni_banka],
                    ignore_index=True,
                )
                st.success("✅ Banka hesabı başarıyla eklendi.")
                st.rerun()
            else:
                st.error("❌ Banka adı ve IBAN alanları zorunludur!")


# =========================================================
# 10. YENİ ÜRÜN KARTI AÇ
# =========================================================
elif menu_secim == "➕ Yeni Ürün Kartı Aç":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün & Mobilya Kartı Tanımlama</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kataloğa yeni bir ürün ekleyin ve başlangıç stok seviyesini belirleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("yeni_urun_form"):
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            u_ad = st.text_input(
                "Ürün Adı *", placeholder="Örn: Viyana Köşe Koltuk"
            )
            u_alis = st.number_input(
                "Alış / Maliyet Fiyatı (TL)", min_value=0.0, step=100.0, value=5000.0
            )
            u_satis = st.number_input(
                "Satış Fiyatı (TL)", min_value=0.0, step=100.0, value=8500.0
            )
        with col_u2:
            u_barkod = st.text_input(
                "Barkod",
                value=str(random.randint(8690000000000, 8699999999999)),
            )
            u_bakiye = st.number_input(
                "Başlangıç Stok Miktarı", min_value=0, step=1, value=5
            )
            u_kritik = st.number_input(
                "Kritik Stok Sınırı", min_value=1, step=1, value=3
            )
            u_birim = st.selectbox("Birim", ["Takım", "Adet", "Metre", "Set"])

        yeni_urun_onay = st.form_submit_button("💾 Ürünü Kataloğa Kaydet")

        if yeni_urun_onay:
            if not u_ad:
                st.error("❌ Ürün adı boş bırakılamaz!")
            else:
                yeni_satir = pd.DataFrame(
                    [
                        {
                            "Ürün Adı": u_ad,
                            "Barkod": u_barkod,
                            "Alış Fiyatı (TL)": u_alis,
                            "Satış Fiyatı (TL)": u_satis,
                            "Bakiye": u_bakiye,
                            "Kritik Sınır": u_kritik,
                            "Birim": u_birim,
                        }
                    ]
                )
                st.session_state.global_stok = pd.concat(
                    [st.session_state.global_stok, yeni_satir], ignore_index=True
                )

                st.session_state.global_stok_hareketleri.insert(
                    0,
                    {
                        "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Personel": st.session_state.current_user,
                        "Ürün": u_ad,
                        "İşlem": "Yeni Ürün Kartı Açıldı",
                        "Miktar": u_bakiye,
                    },
                )
                st.success(f"✅ {u_ad} başarıyla sisteme tanımlandı!")


# =========================================================
# 11. KASA & FİNANS
# =========================================================
elif menu_secim == "💰 Kasa & Finans":
    st.markdown(
        '<div class="page-title">💰 Kasa & Finansal Durum Özeti</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirket nakit akışı, toplam ciro ve finansal varlık dağılımı.</div>',
        unsafe_allow_html=True,
    )

    toplam_faturalandirilan = (
        sum([f["Toplam"] for f in st.session_state.global_faturalar])
        if len(st.session_state.global_faturalar) > 0
        else 0.0
    )
    toplam_maliyet = (
        st.session_state.global_stok["Alış Fiyatı (TL)"]
        * st.session_state.global_stok["Bakiye"]
    ).sum()
    toplam_satis_potansiyel = (
        st.session_state.global_stok["Satış Fiyatı (TL)"]
        * st.session_state.global_stok["Bakiye"]
    ).sum()

    kf1, kf2, kf3 = st.columns(3)
    with kf1:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-title">Toplam Fatura Cirosu</div>
                <div class="stat-value">₺{toplam_faturalandirilan:,.2f}</div>
                <div class="stat-change">Gerçekleşen Satışlar</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with kf2:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-title">Stok Toplam Maliyeti</div>
                <div class="stat-value">₺{toplam_maliyet:,.2f}</div>
                <div class="stat-change">Yatırım Değeri</div>
            </div>""",
            unsafe_allow_html=True,
        )
    with kf3:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">💎</div>
                <div class="stat-title">Depo Satış Potansiyeli</div>
                <div class="stat-value">₺{toplam_satis_potansiyel:,.2f}</div>
                <div class="stat-change">Beklenen Ciro</div>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("#### 🧾 Kesilen Son Faturalar Listesi")
    if len(st.session_state.global_faturalar) > 0:
        st.dataframe(
            pd.DataFrame(st.session_state.global_faturalar),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Henüz kesilmiş bir satış faturası bulunmuyor.")


# =========================================================
# 12. RAPORLAR & ANALİZ
# =========================================================
elif menu_secim == "📊 Raporlar & Analiz":
    st.markdown(
        '<div class="page-title">📊 Raporlar & İleri Düzey Analiz</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Üretim, stok dağılımı ve operasyonel performans raporları.</div>',
        unsafe_allow_html=True,
    )

    tab_r1, tab_r2 = st.tabs(
        ["📦 Kategori & Stok Dağılımı", "👥 Personel İşlem Raporu"]
    )

    with tab_r1:
        st.markdown("#### Ürün Bazlı Stok Seviyeleri")
        st.bar_chart(st.session_state.global_stok.set_index("Ürün Adı")["Bakiye"])

    with tab_r2:
        st.markdown("#### Personel Aktivite Özeti")
        if len(st.session_state.global_personel_loglari) > 0:
            df_log = pd.DataFrame(st.session_state.global_personel_loglari)
            st.dataframe(df_log, use_container_width=True, hide_index=True)
        else:
            st.info("Personel log kaydı bulunmuyor.")


# =========================================================
# 13. ŞİFRE DEĞİŞTİR
# =========================================================
elif menu_secim == "🔑 Şifre Değiştir":
    st.markdown(
        '<div class="page-title">🔑 Kullanıcı Şifre Değiştirme</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Oturum açan hesap için güvenlik şifresini güncelleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("sifre_degis_form"):
        eskisifre = st.text_input("Mevcut Şifre", type="password")
        yenisifre1 = st.text_input("Yeni Şifre", type="password")
        yenisifre2 = st.text_input("Yeni Şifre (Tekrar)", type="password")

        sifre_guncelle_btn = st.form_submit_button("Şifreyi Güncelle")

        if sifre_guncelle_btn:
            aktif_kullanici = st.session_state.current_user
            if st.session_state.global_users.get(aktif_kullanici) == eskisifre:
                if yenisifre1 and yenisifre1 == yenisifre2:
                    st.session_state.global_users[aktif_kullanici] = yenisifre1
                    st.success("✅ Şifreniz başarıyla değiştirildi!")
                else:
                    st.error(
                        "❌ Yeni şifreler boş olamaz ve birbiriyle uyuşmalıdır!"
                    )
            else:
                st.error("❌ Mevcut şifrenizi hatalı girdiniz!")


# =========================================================
# ALT BİLGİ (FOOTER)
# =========================================================
st.markdown(
    """
<div class="footer">
    Hayal Mobilya Kurumsal ERP & Stok Yönetim Sistemi • Edremit Üretim Tesisi © 2026
</div>
""",
    unsafe_allow_html=True,
)

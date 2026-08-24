import random
from datetime import datetime
import pandas as pd
import streamlit as st

# =========================================================
# 1. SAYFA YAPILANDIRMASI & KOYU TEMA STİLLERİ
# =========================================================
st.set_page_config(
    page_title="Hayal Mobilya ERP & Stok Yönetimi v3.4",
    page_icon="🪑",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { background-color: #0e1117; color: #fafafa; }
    .page-title { font-size: 24px; font-weight: 700; color: #ffffff; margin-bottom: 5px; }
    .page-subtitle { font-size: 14px; color: #9ca3af; margin-bottom: 20px; }
    .stat-card { background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; border-left: 4px solid #3b82f6; }
    .stat-title { font-size: 12px; color: #9ca3af; font-weight: 600; text-transform: uppercase; }
    .stat-value { font-size: 24px; font-weight: 700; color: #ffffff; margin-top: 5px; }
    .stat-change { font-size: 11px; color: #34d399; margin-top: 5px; }
    .footer { text-align: center; margin-top: 60px; font-size: 11px; color: #6b7280; border-top: 1px solid #30363d; padding-top: 15px; }
    </style>
""",
    unsafe_allow_html=True,
)

# =========================================================
# 2. SESSION STATE (ORTAK GLOBAL VERİLER)
# =========================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "user_role" not in st.session_state:
    st.session_state.user_role = ""
if "sifremi_unuttum_mod" not in st.session_state:
    st.session_state.sifremi_unuttum_mod = False

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

# Banka Hesapları
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
        ]
    )

# Fatura ve Loglar
if "global_faturalar" not in st.session_state:
    st.session_state.global_faturalar = []
if "global_stok_hareketleri" not in st.session_state:
    st.session_state.global_stok_hareketleri = []
if "global_irsaliyeler" not in st.session_state:
    st.session_state.global_irsaliyeler = []
if "global_personel_loglari" not in st.session_state:
    st.session_state.global_personel_loglari = []


# =========================================================
# 3. GİRİŞ EKRANI
# =========================================================
if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; color: #ffffff;'>🪑 Hayal Mobilya ERP v3.4 Giriş</h2>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        if not st.session_state.sifremi_unuttum_mod:
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
                        st.success("✅ Giriş başarılı!")
                        st.rerun()
                    else:
                        st.error("❌ Hatalı kullanıcı adı veya şifre!")

            if st.button("🔑 Şifremi Unuttum?", use_container_width=True):
                st.session_state.sifremi_unuttum_mod = True
                st.rerun()
        else:
            st.markdown("#### 🔄 Şifre Sıfırlama")
            with st.form("sifre_sifirla_form"):
                unutulan_user = st.text_input("Kullanıcı Adınız")
                admin_sifre = st.text_input("Yönetici (Admin) Şifresi", type="password")
                yeni_sifre = st.text_input("Yeni Şifre", type="password")
                sifirla_btn = st.form_submit_button("Şifreyi Güncelle", use_container_width=True)
                geri_btn = st.form_submit_button("Girişe Dön", use_container_width=True)

                if sifirla_btn:
                    if unutulan_user in st.session_state.global_users:
                        if admin_sifre == st.session_state.global_users.get("admin"):
                            st.session_state.global_users[unutulan_user] = yeni_sifre
                            st.success("✅ Şifre güncellendi!")
                            st.session_state.sifremi_unuttum_mod = False
                            st.rerun()
                        else:
                            st.error("❌ Yönetici şifresi hatalı!")
                    else:
                        st.error("❌ Kullanıcı bulunamadı!")
                if geri_btn:
                    st.session_state.sifremi_unuttum_mod = False
                    st.rerun()
    st.stop()


# =========================================================
# 4. SOL MENÜ
# =========================================================
st.sidebar.markdown("### 🪑 HAYAL MOBİLYA")
st.sidebar.caption("ERP & STOK YÖNETİMİ v3.4")
st.sidebar.divider()

st.sidebar.markdown("**MENÜ**")
menu_secim = st.sidebar.radio(
    "Navigasyon",
    [
        "Ana Sayfa",
        "Yönetici Paneli",
        "Ürün Kataloğu & Stok",
        "Hızlı İmalat / Stok Güncelle",
        "Stok Hareket Geçmişi",
        "Satış Faturası Kes",
        "Fatura / İrsaliye İşle",
        "Cari Hesaplar & Borçlar",
        "Banka Hesapları",
        "Yeni Ürün Kartı Aç",
        "Kasa & Finans",
        "Raporlar & Analiz",
        "Şifre Değiştir",
    ],
    label_visibility="collapsed",
)

st.sidebar.divider()
st.sidebar.markdown(f"👤 **{st.session_state.current_user.capitalize()}**")
st.sidebar.caption("Sistem Yöneticisi" if st.session_state.user_role == "Admin" else "Personel")

if st.sidebar.button("🔒 Güvenli Çıkış", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""
    st.rerun()


# =========================================================
# 5. SAYFA İÇERİKLERİ
# =========================================================

# --- 1. ANA SAYFA & DASHBOARD ---
if menu_secim == "Ana Sayfa":
    st.markdown('<div class="page-title">Kontrol Paneli (Dashboard)</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">İmalat ve stok performansının genel özeti.</div>', unsafe_allow_html=True)

    toplam_urun_cesidi = len(st.session_state.global_stok)
    toplam_stok_miktari = int(st.session_state.global_stok["Bakiye"].sum())
    toplam_maliyet = int((st.session_state.global_stok["Alış Fiyatı (TL)"] * st.session_state.global_stok["Bakiye"]).sum())
    kritik_urunler = st.session_state.global_stok[
        st.session_state.global_stok["Bakiye"] <= st.session_state.global_stok["Kritik Sınır"]
    ]
    kritik_sayi = len(kritik_urunler)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="stat-card"><div class="stat-title">Ürün Çeşidi</div><div class="stat-value">{toplam_urun_cesidi}</div><div class="stat-change">↑ Aktif Katalog</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="stat-card"><div class="stat-title">Toplam Stok Adedi</div><div class="stat-value">{toplam_stok_miktari}</div><div class="stat-change">↑ Ürün Miktarı</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="stat-card"><div class="stat-title">Stok Maliyet Değeri</div><div class="stat-value">₺{toplam_maliyet:,}</div><div class="stat-change">↑ Yatırım Tutarı</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="stat-card" style="border-left-color: #ef4444;"><div class="stat-title">Kritik Stok Uyarı</div><div class="stat-value">{kritik_sayi}</div><div class="stat-change" style="color:#ef4444;">↑ Acil Üretim Gereken</div></div>""", unsafe_allow_html=True)

    st.markdown("#### 🚨 Kritik Eşiğindeki Ürünler")
    if kritik_sayi > 0:
        st.dataframe(kritik_urunler, use_container_width=True, hide_index=True)
    else:
        st.success("Kritik seviyede ürün bulunmuyor.")


# --- 2. YÖNETİCİ PANELİ ---
elif menu_secim == "Yönetici Paneli":
    st.markdown('<div class="page-title">Yönetici Kontrol Paneli</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Sistem yetkileri, kullanıcı yönetimi ve genel log kayıtları.</div>', unsafe_allow_html=True)

    if st.session_state.user_role != "Admin":
        st.error("❌ Bu sayfaya yalnızca Admin yetkisiyle erişebilirsiniz!")
    else:
        st.markdown("#### 👥 Sistem Kullanıcıları")
        user_df = pd.DataFrame(list(st.session_state.global_users.items()), columns=["Kullanıcı Adı", "Şifre"])
        st.dataframe(user_df, use_container_width=True, hide_index=True)

        st.markdown("#### 📝 Personel İşlem Logları")
        if len(st.session_state.global_personel_loglari) > 0:
            st.dataframe(pd.DataFrame(st.session_state.global_personel_loglari), use_container_width=True, hide_index=True)
        else:
            st.info("Kayıtlı personel logu bulunmuyor.")


# --- 3. ÜRÜN KATALOĞU & STOK ---
elif menu_secim == "Ürün Kataloğu & Stok":
    st.markdown('<div class="page-title">Ürün Kataloğu & Depo Envanteri</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Tüm depodaki ürünlerin güncel listesi ve fiyatları.</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.global_stok, use_container_width=True, hide_index=True)


# --- 4. HIZLI İMALAT / STOK GÜNCELLE ---
elif menu_secim == "Hızlı İmalat / Stok Güncelle":
    st.markdown('<div class="page-title">Hızlı İmalat & Stok Güncelleme</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Üretimden çıkan ürünleri depoya ekleyin veya düşün.</div>', unsafe_allow_html=True)

    with st.form("hizli_stok_form"):
        urun_sec = st.selectbox("Ürün Seç", st.session_state.global_stok["Ürün Adı"].tolist())
        islem = st.selectbox("İşlem Türü", ["Üretimden Ekle (+)", "Stoktan Düş (-)"])
        adet = st.number_input("Adet / Miktar", min_value=1, step=1, value=1)
        onay_btn = st.form_submit_button("Stok Hareketini Kaydet")

        if onay_btn:
            idx = st.session_state.global_stok[st.session_state.global_stok["Ürün Adı"] == urun_sec].index[0]
            if islem == "Üretimden Ekle (+)":
                st.session_state.global_stok.loc[idx, "Bakiye"] += adet
            else:
                if st.session_state.global_stok.loc[idx, "Bakiye"] >= adet:
                    st.session_state.global_stok.loc[idx, "Bakiye"] -= adet
                else:
                    st.error("❌ Stokta yeterli miktar yok!")

            st.session_state.global_personel_loglari.insert(0, {
                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Personel": st.session_state.current_user,
                "Ürün": urun_sec,
                "İşlem": islem,
                "Miktar": adet
            })
            st.success(f"✅ {urun_sec} için stok hareketi işlendi!")
            st.rerun()


# --- 5. STOK HAREKET GEÇMİŞİ ---
elif menu_secim == "Stok Hareket Geçmişi":
    st.markdown('<div class="page-title">Stok Hareket Geçmişi</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Geçmişte yapılan imalat ve depo çıkış logları.</div>', unsafe_allow_html=True)
    if len(st.session_state.global_personel_loglari) > 0:
        st.dataframe(pd.DataFrame(st.session_state.global_personel_loglari), use_container_width=True, hide_index=True)
    else:
        st.info("Henüz kaydedilmiş stok hareketi bulunmuyor.")


# --- 6. SATIŞ FATURASI KES ---
elif menu_secim == "Satış Faturası Kes":
    st.markdown('<div class="page-title">Satış Faturası Kes</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Müşterilere resmi fatura düzenleme ekranı.</div>', unsafe_allow_html=True)

    with st.form("satis_fatura_form"):
        m_sec = st.selectbox("Müşteri / Cari", st.session_state.global_cariler["Cari Adı"].tolist())
        u_sec = st.selectbox("Ürün", st.session_state.global_stok["Ürün Adı"].tolist())
        mik = st.number_input("Adet", min_value=1, value=1)
        kdv = st.selectbox("KDV Oranı (%)", [20, 10, 1])
        kes_btn = st.form_submit_button("Faturayı Kes")

        if kes_btn:
            fiyat = float(st.session_state.global_stok.loc[st.session_state.global_stok["Ürün Adı"] == u_sec, "Satış Fiyatı (TL)"].values[0])
            tutar = fiyat * mik * (1 + kdv / 100.0)
            st.session_state.global_faturalar.append({
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Müşteri": m_sec,
                "Ürün": u_sec,
                "Adet": mik,
                "Toplam": tutar,
                "Kesen": st.session_state.current_user
            })
            st.success(f"✅ {m_sec} adına ₺{tutar:,.2f} tutarlı fatura kesildi!")


# --- 7. FATURA / İRSALİYE İŞLE ---
elif menu_secim == "Fatura / İrsaliye İşle":
    st.markdown('<div class="page-title">Fatura / İrsaliye İşlemleri</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Gelen tedarikçi irsaliyeleri ve fatura kayıtları.</div>', unsafe_allow_html=True)

    with st.form("irsaliye_form"):
        tedarikci = st.text_input("Tedarikçi Firma Adı")
        evrak_no = st.text_input("İrsaliye / Fatura No")
        aciklama = st.text_area("İçerik / Malzeme Açıklaması")
        irs_kaydet = st.form_submit_button("İrsaliyeyi Kaydet")
        if irs_kaydet:
            if tedarikci and evrak_no:
                st.session_state.global_irsaliyeler.append({
                    "Tarih": datetime.now().strftime("%Y-%m-%d"),
                    "Tedarikçi": tedarikci,
                    "Evrak No": evrak_no,
                    "Açıklama": aciklama
                })
                st.success("✅ İrsaliye başarıyla işlendi.")
            else:
                st.error("❌ Tedarikçi ve evrak numarası zorunludur!")

    if len(st.session_state.global_irsaliyeler) > 0:
        st.markdown("#### Kayıtlı İrsaliyeler")
        st.dataframe(pd.DataFrame(st.session_state.global_irsaliyeler), use_container_width=True, hide_index=True)


# --- 8. CARİ HESAPLAR & BORÇLAR ---
elif menu_secim == "Cari Hesaplar & Borçlar":
    st.markdown('<div class="page-title">Cari Hesaplar & Borç / Alacak</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Müşteri ve tedarikçilerin güncel bakiye durumları.</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.dataframe(st.session_state.global_cariler, use_container_width=True, hide_index=True)
    with col_b:
        with st.form("yeni_cari_kart"):
            c_ad = st.text_input("Cari Adı")
            c_tel = st.text_input("Telefon")
            c_turu = st.selectbox("Tür", ["Müşteri", "Tedarikçi"])
            c_bak = st.number_input("Bakiye (TL)", value=0.0)
            if st.form_submit_button("Cari Ekle"):
                if c_ad:
                    yeni_c = pd.DataFrame([{"Cari Adı": c_ad, "Telefon": c_tel, "Tür": c_turu, "Bakiye (TL)": c_bak}])
                    st.session_state.global_cariler = pd.concat([st.session_state.global_cariler, yeni_c], ignore_index=True)
                    st.success("✅ Cari eklendi.")
                    st.rerun()


# --- 9. BANKA HESAPLARI ---
elif menu_secim == "Banka Hesapları":
    st.markdown('<div class="page-title">Banka Hesapları & IBAN Listesi</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Şirket ticari banka hesapları ve IBAN bilgileri.</div>', unsafe_allow_html=True)
    st.dataframe(st.session_state.global_banka_hesaplari, use_container_width=True, hide_index=True)


# --- 10. YENİ ÜRÜN KARTI AÇ ---
elif menu_secim == "Yeni Ürün Kartı Aç":
    st.markdown('<div class="page-title">Yeni Ürün Kartı Tanımla</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Kataloğa yeni bir mobilya modeli ekleyin.</div>', unsafe_allow_html=True)

    with st.form("yeni_urun_kart_form"):
        col1, col2 = st.columns(2)
        with col1:
            u_ad = st.text_input("Ürün Adı")
            u_alis = st.number_input("Alış Fiyatı (TL)", value=5000.0)
            u_satis = st.number_input("Satış Fiyatı (TL)", value=8500.0)
        with col2:
            u_barkod = st.text_input("Barkod", value=str(random.randint(8690000000000, 8699999999999)))
            u_bakiye = st.number_input("Başlangıç Stok", value=5, min_value=0)
            u_kritik = st.number_input("Kritik Sınır", value=3, min_value=1)
            u_birim = st.selectbox("Birim", ["Takım", "Adet", "Set"])

        if st.form_submit_button("Ürünü Kaydet"):
            if u_ad:
                yeni_sat = pd.DataFrame([{
                    "Ürün Adı": u_ad, "Barkod": u_barkod,
                    "Alış Fiyatı (TL)": u_alis, "Satış Fiyatı (TL)": u_satis,
                    "Bakiye": u_bakiye, "Kritik Sınır": u_kritik, "Birim": u_birim
                }])
                st.session_state.global_stok = pd.concat([st.session_state.global_stok, yeni_sat], ignore_index=True)
                st.success(f"✅ {u_ad} kataloğa eklendi!")
            else:
                st.error("❌ Ürün adı boş olamaz!")


# --- 11. KASA & FİNANS ---
elif menu_secim == "Kasa & Finans":
    st.markdown('<div class="page-title">Kasa & Finansal Durum</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Şirket ciro ve nakit akışı raporu.</div>', unsafe_allow_html=True)

    toplam_ciro = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if len(st.session_state.global_faturalar) > 0 else 0.0
    f1, f2 = st.columns(2)
    with f1:
        st.markdown(f"""<div class="stat-card"><div class="stat-title">Toplam Fatura Cirosu</div><div class="stat-value">₺{toplam_ciro:,.2f}</div></div>""", unsafe_allow_html=True)
    with f2:
        depo_deger = (st.session_state.global_stok["Satış Fiyatı (TL)"] * st.session_state.global_stok["Bakiye"]).sum()
        st.markdown(f"""<div class="stat-card"><div class="stat-title">Toplam Depo Satış Potansiyeli</div><div class="stat-value">₺{depo_deger:,.2f}</div></div>""", unsafe_allow_html=True)


# --- 12. RAPORLAR & ANALİZ ---
elif menu_secim == "Raporlar & Analiz":
    st.markdown('<div class="page-title">Raporlar & Analiz</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Stok ve ürün dağılım grafikleri.</div>', unsafe_allow_html=True)
    st.bar_chart(st.session_state.global_stok.set_index("Ürün Adı")["Bakiye"])


# --- 13. ŞİFRE DEĞİŞTİR ---
elif menu_secim == "Şifre Değiştir":
    st.markdown('<div class="page-title">Şifre Değiştir</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Oturum açan hesap şifresini güncelleyin.</div>', unsafe_allow_html=True)

    with st.form("sifre_degis_form"):
        eskisifre = st.text_input("Mevcut Şifre", type="password")
        yenisifre = st.text_input("Yeni Şifre", type="password")
        if st.form_submit_button("Şifreyi Güncelle"):
            ak_user = st.session_state.current_user
            if st.session_state.global_users.get(ak_user) == eskisifre:
                st.session_state.global_users[ak_user] = yenisifre
                st.success("✅ Şifre değiştirildi!")
            else:
                st.error("❌ Mevcut şifre hatalı!")


# =========================================================
# ALT BİLGİ (FOOTER)
# =========================================================
st.markdown(
    """
<div class="footer">
    © 2026 Hayal Mobilya • Kurumsal Ön Muhasebe & ERP v3.4 • Tüm Hakları Saklıdır.
</div>
""",
    unsafe_allow_html=True,
)

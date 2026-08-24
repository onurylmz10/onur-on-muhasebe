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

# =========================================================
# 2. SESSION STATE (ORTAK/GLOBAL OTURUM VERİLERİ)
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

# Ortak Stok Veritabanı (Tüm personeller aynı veriyi görür)
if "global_stok" not in st.session_state:
    st.session_state.global_stok = pd.DataFrame(
        [
            {
                "Ürün Adı": "Prag Yemek Masası Seti",
                "Barkod": "8690456765456",
                "Alış Fiyatı (TL)": 8000.0,
                "Satış Fiyatı (TL)": 12500.0,
                "Bakiye": 4,
                "Kritik Sınır": 2,
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
        ]
    )

# Ortak Cari Veritabanı
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
            }
        ]
    )

if "global_faturalar" not in st.session_state:
    st.session_state.global_faturalar = []
if "global_stok_hareketleri" not in st.session_state:
    st.session_state.global_stok_hareketleri = []
if "global_personel_loglari" not in st.session_state:
    st.session_state.global_personel_loglari = []


# =========================================================
# 3. KULLANICI GİRİŞ & ŞİFREMİ UNUTTUM EKRANI
# =========================================================
if not st.session_state.logged_in:
    st.markdown(
        "<h2 style='text-align: center; color: #1e293b;'>🪑 Hayal Mobilya ERP Giriş</h2>",
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
                            "Sistem Yöneticisi" if kullanici_adi in ["admin", "onur"] else "Personel"
                        )
                        st.success("✅ Giriş başarılı!")
                        st.rerun()
                    else:
                        st.error("❌ Hatalı kullanıcı adı veya şifre!")

            if st.button("🔑 Şifremi Unuttum?", use_container_width=True):
                st.session_state.sifremi_unuttum_mod = True
                st.rerun()
        else:
            st.markdown("#### 🔄 Şifre Sıfırlama Paneli")
            with st.form("sifremi_unuttum_form"):
                unutulan_user = st.text_input("Kullanıcı Adınız")
                admin_onay_sifre = st.text_input("Admin Şifresi", type="password")
                yeni_gecici_sifre = st.text_input("Yeni Şifre", type="password")
                
                sifirla_btn = st.form_submit_button("Şifreyi Sıfırla", use_container_width=True)
                geri_don_btn = st.form_submit_button("Geri Dön", use_container_width=True)

                if sifirla_btn:
                    if unutulan_user in st.session_state.global_users:
                        if admin_onay_sifre in [st.session_state.global_users.get("admin"), st.session_state.global_users.get("onur")]:
                            if yeni_gecici_sifre:
                                st.session_state.global_users[unutulan_user] = yeni_gecici_sifre
                                st.success("✅ Şifre başarıyla güncellendi!")
                                st.session_state.sifremi_unuttum_mod = False
                                st.rerun()
                            else:
                                st.error("❌ Yeni şifre boş olamaz!")
                        else:
                            st.error("❌ Yönetici şifresi hatalı!")
                    else:
                        st.error("❌ Kullanıcı bulunamadı!")

                if geri_don_btn:
                    st.session_state.sifremi_unuttum_mod = False
                    st.rerun()
    st.stop()


# =========================================================
# 4. SOL MENÜ & NAVİGASYON (Görselinizdeki Sıralama)
# =========================================================
st.sidebar.markdown(f"### 🪑 HAYAL MOBİLYA")
st.sidebar.caption("ERP & STOK YÖNETİMİ v3.4")
st.sidebar.divider()

menu_secim = st.sidebar.radio(
    "MENÜ",
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
)

st.sidebar.divider()
st.sidebar.markdown(f"👤 **{st.session_state.current_user.capitalize()}**")
st.sidebar.caption(f"{st.session_state.user_role}")

if st.sidebar.button("🚪 Güvenli Çıkış", use_container_width=True):
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""
    st.rerun()


# =========================================================
# 5. ANA SAYFA & DASHBOARD
# =========================================================
if menu_secim == "Ana Sayfa":
    st.markdown("### Kontrol Paneli (Dashboard)")
    st.caption("İmalat ve stok performansının genel özeti.")

    toplam_urun_cesidi = len(st.session_state.global_stok)
    toplam_stok_miktari = st.session_state.global_stok["Bakiye"].sum()
    toplam_maliyet_degeri = (st.session_state.global_stok["Alış Fiyatı (TL)"] * st.session_state.global_stok["Bakiye"]).sum()
    
    kritik_df = st.session_state.global_stok[
        st.session_state.global_stok["Bakiye"] <= st.session_state.global_stok["Kritik Sınır"]
    ]
    kritik_urun_sayisi = len(kritik_df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("ÜRÜN ÇEŞİDİ", toplam_urun_cesidi, "Aktif Katalog")
    with c2:
        st.metric("TOPLAM STOK ADEDİ", int(toplam_stok_miktari), "Ürün Miktarı")
    with c3:
        st.metric("STOK MALİYET DEĞERİ", f"₺{toplam_maliyet_degeri:,.0f}", "Yatırım Tutarı")
    with c4:
        st.metric("KRİTİK STOK UYARI", kritik_urun_sayisi, "Acil Üretim Gereken", delta_color="inverse")

    st.markdown("#### 🚨 Kritik Eşikteki Ürünler")
    if not kritik_df.empty:
        st.dataframe(kritik_df, use_container_width=True, hide_index=True)
    else:
        st.success("Kritik seviyede ürün bulunmuyor.")


# =========================================================
# 6. YÖNETİCİ PANELİ
# =========================================================
elif menu_secim == "Yönetici Paneli":
    st.markdown("### ⚙️ Sistem Yönetici Paneli")
    st.caption("Kullanıcı yetkileri ve genel sistem ayarları.")
    st.write("Kayıtlı Kullanıcılar:", list(st.session_state.global_users.keys()))


# =========================================================
# 7. ÜRÜN KATALOĞU & STOK
# =========================================================
elif menu_secim == "Ürün Kataloğu & Stok":
    st.markdown("### 📦 Ürün Kataloğu ve Genel Stok")
    st.dataframe(st.session_state.global_stok, use_container_width=True, hide_index=True)


# =========================================================
# 8. HIZLI İMALAT / STOK GÜNCELLE
# =========================================================
elif menu_secim == "Hızlı İmalat / Stok Güncelle":
    st.markdown("### ⚡ Hızlı İmalat & Stok Miktar Güncelleme")
    with st.form("hizli_stok_form"):
        secilen_urun = st.selectbox("Ürün Seç", st.session_state.global_stok["Ürün Adı"].tolist())
        islem_tipi = st.selectbox("İşlem", ["Stok Ekle (+)", "Stok Düş (-)"])
        miktar = st.number_input("Miktar", min_value=1, step=1, value=1)
        guncelle_btn = st.form_submit_button("Stok Hareketi İşle")

        if guncelle_btn:
            idx = st.session_state.global_stok[st.session_state.global_stok["Ürün Adı"] == secilen_urun].index[0]
            if islem_tipi == "Stok Ekle (+)":
                st.session_state.global_stok.loc[idx, "Bakiye"] += miktar
            else:
                if st.session_state.global_stok.loc[idx, "Bakiye"] >= miktar:
                    st.session_state.global_stok.loc[idx, "Bakiye"] -= miktar
                else:
                    st.error("❌ Stokta yeterli miktar yok!")

            st.session_state.global_stok_hareketleri.insert(0, {
                "Zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Personel": st.session_state.current_user,
                "Ürün": secilen_urun,
                "İşlem": islem_tipi,
                "Miktar": miktar
            })
            st.success(f"✅ {secilen_urun} güncellendi. Tüm personeller artık bu güncel stoğu görebilir!")
            st.rerun()


# =========================================================
# 9. STOK HAREKET GEÇMİŞİ
# =========================================================
elif menu_secim == "Stok Hareket Geçmişi":
    st.markdown("### 📜 Stok Hareket Geçmişi")
    if len(st.session_state.global_stok_hareketleri) > 0:
        st.dataframe(pd.DataFrame(st.session_state.global_stok_hareketleri), use_container_width=True, hide_index=True)
    else:
        st.info("Henüz stok hareketi kaydedilmedi.")


# =========================================================
# 10. SATIŞ FATURASI KES
# =========================================================
elif menu_secim == "Satış Faturası Kes":
    st.markdown("### 🧾 Satış Faturası Kesme Modülü")
    with st.form("fatura_form"):
        f_cari = st.selectbox("Müşteri / Cari", st.session_state.global_cariler["Cari Adı"].tolist())
        f_urun = st.selectbox("Ürün", st.session_state.global_stok["Ürün Adı"].tolist())
        f_adet = st.number_input("Adet", min_value=1, value=1)
        kes_btn = st.form_submit_button("Fatura Kes")

        if kes_btn:
            fiyat = float(st.session_state.global_stok.loc[st.session_state.global_stok["Ürün Adı"] == f_urun, "Satış Fiyatı (TL)"].values[0])
            toplam = fiyat * f_adet
            st.session_state.global_faturalar.append({
                "Tarih": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Müşteri": f_cari,
                "Ürün": f_urun,
                "Adet": f_adet,
                "Toplam": toplam,
                "Kesen": st.session_state.current_user
            })
            st.success(f"✅ Fatura kesildi! Tutar: ₺{toplam:,.2f}")


# =========================================================
# 11. FATURA / İRSALİYE İŞLE
# =========================================================
elif menu_secim == "Fatura / İrsaliye İşle":
    st.markdown("### 📄 Fatura & İrsaliye Arşivi")
    if len(st.session_state.global_faturalar) > 0:
        st.dataframe(pd.DataFrame(st.session_state.global_faturalar), use_container_width=True, hide_index=True)
    else:
        st.info("Kayıtlı fatura bulunmuyor.")


# =========================================================
# 12. CARİ HESAPLAR & BORÇLAR
# =========================================================
elif menu_secim == "Cari Hesaplar & Borçlar":
    st.markdown("### 👥 Cari Hesaplar & Borç / Alacak")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.dataframe(st.session_state.global_cariler, use_container_width=True, hide_index=True)
    with col2:
        with st.form("yeni_cari"):
            c_adi = st.text_input("Cari Adı")
            c_tel = st.text_input("Telefon")
            c_tur = st.selectbox("Tür", ["Müşteri", "Tedarikçi"])
            c_bak = st.number_input("Bakiye", value=0.0)
            if st.form_submit_button("Cari Ekle"):
                if c_adi:
                    yeni_c = pd.DataFrame([{"Cari Adı": c_adi, "Telefon": c_tel, "Tür": c_tur, "Bakiye (TL)": c_bak}])
                    st.session_state.global_cariler = pd.concat([st.session_state.global_cariler, yeni_c], ignore_index=True)
                    st.success("✅ Cari eklendi!")
                    st.rerun()


# =========================================================
# 13. BANKA HESAPLARI
# =========================================================
elif menu_secim == "Banka Hesapları":
    st.markdown("### 🏦 Banka Hesapları & IBAN")
    st.dataframe(st.session_state.global_banka_hesaplari, use_container_width=True, hide_index=True)


# =========================================================
# 14. YENİ ÜRÜN KARTI AÇ
# =========================================================
elif menu_secim == "Yeni Ürün Kartı Aç":
    st.markdown("### ➕ Yeni Ürün Kartı Tanımlama")
    with st.form("yeni_urun_form"):
        u_ad = st.text_input("Ürün Adı")
        u_barkod = st.text_input("Barkod", value=str(random.randint(8690000000000, 8699999999999)))
        u_alis = st.number_input("Alış Fiyatı (TL)", value=5000.0)
        u_satis = st.number_input("Satış Fiyatı (TL)", value=8500.0)
        u_bak = st.number_input("Başlangıç Stok Adedi", min_value=0, value=5)
        u_kritik = st.number_input("Kritik Sınır", min_value=1, value=2)
        u_birim = st.selectbox("Birim", ["Takım", "Adet", "Set"])

        if st.form_submit_button("Ürünü Kataloğa Kaydet"):
            if u_ad:
                yeni_u = pd.DataFrame([{
                    "Ürün Adı": u_ad,
                    "Barkod": u_barkod,
                    "Alış Fiyatı (TL)": u_alis,
                    "Satış Fiyatı (TL)": u_satis,
                    "Bakiye": u_bak,
                    "Kritik Sınır": u_kritik,
                    "Birim": u_birim
                }])
                st.session_state.global_stok = pd.concat([st.session_state.global_stok, yeni_u], ignore_index=True)
                st.success("✅ Ürün başarıyla eklendi! Artık tüm personeller bu ürünü görebilir.")
            else:
                st.error("❌ Ürün adı boş olamaz!")


# =========================================================
# 15. KASA & FİNANS
# =========================================================
elif menu_secim == "Kasa & Finans":
    st.markdown("### 💰 Kasa & Finansal Durum")
    toplam_ciro = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if st.session_state.global_faturalar else 0.0
    st.metric("Toplam Fatura Cirosu", f"₺{toplam_ciro:,.2f}")


# =========================================================
# 16. RAPORLAR & ANALİZ
# =========================================================
elif menu_secim == "Raporlar & Analiz":
    st.markdown("### 📊 Raporlar & Analiz")
    st.bar_chart(st.session_state.global_stok.set_index("Ürün Adı")["Bakiye"])


# =========================================================
# 17. ŞİFRE DEĞİŞTİR
# =========================================================
elif menu_secim == "Şifre Değiştir":
    st.markdown("### 🔑 Şifre Değiştir")
    with st.form("sifre_form"):
        eskisifre = st.text_input("Mevcut Şifre", type="password")
        yenisifre = st.text_input("Yeni Şifre", type="password")
        if st.form_submit_button("Güncelle"):
            user = st.session_state.current_user
            if st.session_state.global_users.get(user) == eskisifre:
                st.session_state.global_users[user] = yenisifre
                st.success("✅ Şifre değiştirildi!")
            else:
                st.error("❌ Mevcut şifre hatalı!")


# =========================================================
# ALT BİLGİ (FOOTER)
# =========================================================
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #94a3b8; font-size: 12px;'>© 2026 Hayal Mobilya • Kurumsal Ön Muhasebe & ERP v3.4 • Tüm Hakları Saklıdır.</div>",
    unsafe_allow_html=True,
)

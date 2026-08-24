# =========================================================
# 8. CARİ HESAPLAR (DEVAMI)
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
            c_bakiye = st.number_input("Başlangıç Bakiyesi (TL)", value=0.0, step=100.0)
            
            cari_kaydet = st.form_submit_button("Cari Kartı Oluştur")
            if cari_kaydet:
                if c_adi:
                    yeni_cari_satir = pd.DataFrame([{
                        "Cari Adı": c_adi,
                        "Telefon": c_tel,
                        "Tür": c_tur,
                        "Bakiye (TL)": c_bakiye
                    }])
                    st.session_state.global_cariler = pd.concat(
                        [st.session_state.global_cariler, yeni_cari_satir], ignore_index=True
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
                yeni_banka = pd.DataFrame([{
                    "Banka Adı": b_adi,
                    "Şube / Kod": b_sube,
                    "Hesap Adı": b_hesap,
                    "IBAN": b_iban,
                    "Döviz": b_doviz
                }])
                st.session_state.global_banka_hesaplari = pd.concat(
                    [st.session_state.global_banka_hesaplari, yeni_banka], ignore_index=True
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
            u_ad = st.text_input("Ürün Adı *", placeholder="Örn: Viyana Köşe Koltuk")
            u_alis = st.number_input("Alış / Maliyet Fiyatı (TL)", min_value=0.0, step=100.0, value=5000.0)
            u_satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0, step=100.0, value=8500.0)
        with col_u2:
            u_barkod = st.text_input("Barkod", value=str(random.randint(8690000000000, 8699999999999)))
            u_bakiye = st.number_input("Başlangıç Stok Miktarı", min_value=0, step=1, value=5)
            u_kritik = st.number_input("Kritik Stok Sınırı", min_value=1, step=1, value=3)
            u_birim = st.selectbox("Birim", ["Takım", "Adet", "Metre", "Set"])

        yeni_urun_onay = st.form_submit_button("💾 Ürünü Kataloğa Kaydet")

        if yeni_urun_onay:
            if not u_ad:
                st.error("❌ Ürün adı boş bırakılamaz!")
            else:
                yeni_satir = pd.DataFrame([{
                    "Ürün Adı": u_ad,
                    "Barkod": u_barkod,
                    "Alış Fiyatı (TL)": u_alis,
                    "Satış Fiyatı (TL)": u_satis,
                    "Bakiye": u_bakiye,
                    "Kritik Sınır": u_kritik,
                    "Birim": u_birim,
                }])
                st.session_state.global_stok = pd.concat(
                    [st.session_state.global_stok, yeni_satir], ignore_index=True
                )
                
                # Log ekle
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

    toplam_faturalandirilan = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if len(st.session_state.global_faturalar) > 0 else 0.0
    toplam_maliyet = (st.session_state.global_stok["Alış Fiyatı (TL)"] * st.session_state.global_stok["Bakiye"]).sum()
    toplam_satis_potansiyel = (st.session_state.global_stok["Satış Fiyatı (TL)"] * st.session_state.global_stok["Bakiye"]).sum()

    kf1, kf2, kf3 = st.columns(3)
    with kf1:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-title">Toplam Fatura Cirosu</div>
                <div class="stat-value">₺{toplam_faturalandirilan:,.2f}</div>
                <div class="stat-change">Gerçekleşen Satışlar</div>
            </div>""",
            unsafe_allow_html=True
        )
    with kf2:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-title">Stok Toplam Maliyeti</div>
                <div class="stat-value">₺{toplam_maliyet:,.2f}</div>
                <div class="stat-change">Yatırım Değeri</div>
            </div>""",
            unsafe_allow_html=True
        )
    with kf3:
        st.markdown(
            f"""<div class="stat-card">
                <div class="stat-icon">💎</div>
                <div class="stat-title">Depo Satış Potansiyeli</div>
                <div class="stat-value">₺{toplam_satis_potansiyel:,.2f}</div>
                <div class="stat-change">Beklenen Ciro</div>
            </div>""",
            unsafe_allow_html=True
        )

    st.markdown("#### 🧾 Kesilen Son Faturalar Listesi")
    if len(st.session_state.global_faturalar) > 0:
        st.dataframe(pd.DataFrame(st.session_state.global_faturalar), use_container_width=True, hide_index=True)
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

    tab_r1, tab_r2 = st.tabs(["📦 Kategori & Stok Dağılımı", "👥 Personel İşlem Raporu"])
    
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
                    st.error("❌ Yeni şifreler boş olamaz ve birbiriyle uyuşmalıdır!")
            else:
                st.error("❌ Mevcut şifrenizi hatalı girdiniz!")

# =========================================================
# FOOTER / ALT BİLGİ
# =========================================================

st.markdown(
    """
<div class="footer">
    Hayal Mobilya Kurumsal ERP & Stok Yönetim Sistemi • Edremit Üretim Tesisi © 2026
</div>
""",
    unsafe_allow_html=True,
)
# =========================================================
# 8. CARİ HESAPLAR (DÜZELTİLMİŞ)
# =========================================================

if menu_secim == "👥 Cari Hesaplar & Borçlar":
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
            c_bakiye = st.number_input("Başlangıç Bakiyesi (TL)", value=0.0, step=100.0)
            
            cari_kaydet = st.form_submit_button("Cari Kartı Oluştur")
            if cari_kaydet:
                if c_adi:
                    yeni_cari_satir = pd.DataFrame([{
                        "Cari Adı": c_adi,
                        "Telefon": c_tel,
                        "Tür": c_tur,
                        "Bakiye (TL)": c_bakiye
                    }])
                    st.session_state.global_cariler = pd.concat(
                        [st.session_state.global_cariler, yeni_cari_satir], ignore_index=True
                    )
                    st.success(f"✅ {c_adi} cari listesine başarıyla eklendi.")
                    st.rerun()
                else:
                    st.error("❌ Cari adı boş olamaz!")

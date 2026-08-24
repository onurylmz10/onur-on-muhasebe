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

    arama_cari = st.text_input("🔎 Cari Ara", placeholder="Müşteri veya tedarikçi adı girin...")
    df_c = st.session_state.global_cariler.copy()
    if arama_cari:
        df_c = df_c[df_c["Cari Adı"].str.contains(arama_cari, case=False, na=False)]

    st.dataframe(df_c, use_container_width=True, hide_index=True)

    st.markdown("#### Yeni Cari Hesap Ekle")
    with st.form("yeni_cari_form"):
        c_ad = st.text_input("Cari Adı / Firma Unvanı *")
        c_tel = st.text_input("Telefon Numarası")
        c_tur = st.selectbox("Cari Türü", ["Müşteri", "Tedarikçi"])
        c_bakiye = st.number_input("Başlangıç Bakiyesi (TL) (Borç için -, Alacak için +)", value=0.0, step=100.0)
        
        cari_kaydet = st.form_submit_button("Cari Hesabı Kaydet")
        if cari_kaydet:
            if c_ad:
                yeni_cari = pd.DataFrame([{
                    "Cari Adı": c_ad,
                    "Telefon": c_tel,
                    "Tür": c_tur,
                    "Bakiye (TL)": c_bakiye
                }])
                st.session_state.global_cariler = pd.concat([st.session_state.global_cariler, yeni_cari], ignore_index=True)
                st.success(f"✅ {c_ad} başarıyla cari hesaplara eklendi.")
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
        '<div class="page-subtitle">Şirketin ticari banka hesapları ve döviz varlıkları.</div>',
        unsafe_allow_html=True,
    )

    st.dataframe(st.session_state.global_banka_hesaplari, use_container_width=True, hide_index=True)

    st.markdown("#### Yeni Banka Hesabı Ekle")
    with st.form("yeni_banka_form"):
        b_adi = st.text_input("Banka Adı (Örn: Yapı Kredi)")
        b_sube = st.text_input("Şube ve Kod")
        b_hesap = st.text_input("Hesap Adı")
        b_iban = st.text_input("IBAN Numarası")
        b_doviz = st.selectbox("Döviz Cinsi", ["TL", "USD", "EUR"])

        banka_ekle_btn = st.form_submit_button("Banka Hesabını Kaydet")
        if banka_ekle_btn:
            if b_adi and b_iban:
                yeni_b = pd.DataFrame([{
                    "Banka Adı": b_adi,
                    "Şube / Kod": b_sube,
                    "Hesap Adı": b_hesap,
                    "IBAN": b_iban,
                    "Döviz": b_doviz
                }])
                st.session_state.global_banka_hesaplari = pd.concat([st.session_state.global_banka_hesaplari, yeni_b], ignore_index=True)
                st.success("✅ Banka hesabı başarıyla eklendi.")
                st.rerun()
            else:
                st.error("❌ Banka adı ve IBAN alanları zorunludur!")


# =========================================================
# 10. YENİ ÜRÜN KARTI AÇ
# =========================================================

elif menu_secim == "➕ Yeni Ürün Kartı Aç":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün & Model Tanımlama</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kataloğa yeni bir mobilya kalemi veya hammadde ekleyin.</div>',
        unsafe_allow_html=True,
    )

    with st.form("yeni_urun_kart_form"):
        u_ad = st.text_input("Ürün / Model Adı *")
        u_barkod = st.text_input("Barkod (Boş bırakılırsa otomatik üretilir)")
        c1, c2 = st.columns(2)
        with c1:
            u_alis = st.number_input("Alış / Maliyet Fiyatı (TL)", min_value=0.0, step=100.0)
            u_kritik = st.number_input("Kritik Stok Sınırı", min_value=1, value=3, step=1)
        with c2:
            u_satis = st.number_input("Satış Fiyatı (TL)", min_value=0.0, step=100.0)
            u_birim = st.selectbox("Birim", ["Adet", "Takım", "Metre", "Plaka"])

        yeni_urun_onay = st.form_submit_button("Kataloğa Ürünü Ekle")

        if yeni_urun_onay:
            if not u_ad:
                st.error("❌ Ürün adı boş olamaz!")
            else:
                if not u_barkod:
                    u_barkod = str(random.randint(8690000000000, 8699999999999))
                
                yeni_satir = pd.DataFrame([{
                    "Ürün Adı": u_ad,
                    "Barkod": u_barkod,
                    "Alış Fiyatı (TL)": u_alis,
                    "Satış Fiyatı (TL)": u_satis,
                    "Bakiye": 0,
                    "Kritik Sınır": u_kritik,
                    "Birim": u_birim,
                }])
                st.session_state.global_stok = pd.concat([st.session_state.global_stok, yeni_satir], ignore_index=True)
                st.success(f"✅ '{u_ad}' başarıyla sisteme tanımlandı! (Barkod: {u_barkod})")


# =========================================================
# 11. KASA & FİNANS
# =========================================================

elif menu_secim == "💰 Kasa & Finans":
    st.markdown(
        '<div class="page-title">💰 Kasa & Genel Finansal Durum</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirket nakit akışı ve genel finansal özet.</div>',
        unsafe_allow_html=True,
    )

    toplam_satis_ciro = sum([f["Toplam"] for f in st.session_state.global_faturalar]) if len(st.session_state.global_faturalar) > 0 else 0.0
    
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.metric("Toplam Tahsil Edilen / Ciro", f"₺{toplam_satis_ciro:,.2f}")
    with col_k2:
        toplam_borc_alacak = st.session_state.global_cariler["Bakiye (TL)"].sum()
        st.metric("Net Cari Bakiye Durumu", f"₺{toplam_borc_alacak:,.2f}")

    st.info("💡 Detaylı gelir-gider ve kasa hareketleri modülü yakında eklenecektir.")


# =========================================================
# 12. RAPORLAR & ANALİZ
# =========================================================

elif menu_secim == "📊 Raporlar & Analiz":
    st.markdown(
        '<div class="page-title">📊 Raporlar & İş Zekası Analizi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Stok dağılımları ve maliyet analizleri.</div>',
        unsafe_allow_html=True,
    )

    df_stk = st.session_state.global_stok
    if len(df_stk) > 0:
        st.markdown("#### Ürün Bazlı Stok Değer Dağılımı")
        df_stk["Toplam Değer"] = df_stk["Bakiye"] * df_stk["Satış Fiyatı (TL)"]
        st.bar_chart(df_stk.set_index("Ürün Adı")["Toplam Değer"])
    else:
        st.warning("Analiz için yeterli veri bulunmuyor.")


# =========================================================
# 13. ŞİFRE DEĞİŞTİR
# =========================================================

elif menu_secim == "🔑 Şifre Değiştir":
    st.markdown(
        '<div class="page-title">🔑 Kullanıcı Şifre Değiştirme</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Oturum açan hesap için güvenli şifre güncelleme.</div>',
        unsafe_allow_html=True,
    )

    with st.form("sifre_degis_form"):
        m_sifre = st.text_input("Mevcut Şifre", type="password")
        y_sifre1 = st.text_input("Yeni Şifre", type="password")
        y_sifre2 = st.text_input("Yeni Şifre (Tekrar)", type="password")
        
        degis_btn = st.form_submit_button("Şifreyi Güncelle")
        if degis_btn:
            aktif_kull = st.session_state.current_user
            if st.session_state.global_users.get(aktif_kull) == m_sifre:
                if y_sifre1 and y_sifre1 == y_sifre2:
                    st.session_state.global_users[aktif_kull] = y_sifre1
                    st.success("✅ Şifreniz başarıyla değiştirildi.")
                else:
                    st.error("❌ Yeni şifreler boş olamaz ve birbiriyle uyuşmalıdır!")
            else:
                st.error("❌ Mevcut şifrenizi hatalı girdiniz!")

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
<div class="footer">
    Hayal Mobilya Kurumsal ERP & Stok Yönetim Sistemi • Tüm Hakları Saklıdır © 2026
</div>
""",
    unsafe_allow_html=True,
)

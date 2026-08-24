import random
import pandas as pd
import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Hayal Mobilya Kurumsal ERP", page_icon="🛋️", layout="wide"
)

# Özel CSS Stilleri
st.markdown(
    """
    <style>
    .page-title {
        font-size: 26px;
        font-weight: 700;
        color: #2C3E50;
        margin-bottom: 5px;
    }
    .page-subtitle {
        font-size: 14px;
        color: #7F8C8D;
        margin-bottom: 20px;
    }
    .footer {
        text-align: center;
        font-size: 12px;
        color: #95A5A6;
        margin-top: 50px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session State Başlatma
if "global_users" not in st.session_state:
  st.session_state.global_users = {"admin": "1234", "onur": "1234"}

if "current_user" not in st.session_state:
  st.session_state.current_user = None

if "global_cariler" not in st.session_state:
  st.session_state.global_cariler = pd.DataFrame([
      {
          "Cari Adı": "Kaleçam Orman Ürünleri",
          "Telefon": "0266 373 0000",
          "Tür": "Tedarikçi",
          "Bakiye (TL)": -15000.0,
      },
      {
          "Cari Adı": "Ahşap Dünyası Ltd.",
          "Telefon": "0212 555 4433",
          "Tür": "Müşteri",
          "Bakiye (TL)": 12500.0,
      },
  ])

if "global_banka_hesaplari" not in st.session_state:
  st.session_state.global_banka_hesaplari = pd.DataFrame([
      {
          "Banka Adı": "Ziraat Bankası",
          "Şube / Kod": "Edremit / 1234",
          "Hesap Adı": "Ticari Ana Hesap",
          "IBAN": "TR33 0001 0012 3456 7890 1234 56",
          "Döviz": "TL",
      }
  ])

if "global_stok" not in st.session_state:
  st.session_state.global_stok = pd.DataFrame([
      {
          "Ürün Adı": "Lake Boyalı Mutfak Dolap Kapağı",
          "Barkod": "8691234567890",
          "Alış Fiyatı (TL)": 450.0,
          "Satış Fiyatı (TL)": 750.0,
          "Bakiye": 25,
          "Kritik Sınır": 5,
          "Birim": "Adet",
      },
      {
          "Ürün Adı": "MDFLAM 18mm Beyaz",
          "Barkod": "8699876543210",
          "Alış Fiyatı (TL)": 320.0,
          "Satış Fiyatı (TL)": 500.0,
          "Bakiye": 12,
          "Kritik Sınır": 4,
          "Birim": "Plaka",
      },
  ])

if "global_faturalar" not in st.session_state:
  st.session_state.global_faturalar = [
      {"Fatura No": "FTR-2026-001", "Müşteri": "Ahşap Dünyası Ltd.", "Toplam": 12500.0}
  ]

if "auth_mode" not in st.session_state:
  st.session_state.auth_mode = "Giriş Yap"


# Giriş ve Kimlik Doğrulama Ekranı
def auth_ekrani():
  st.markdown(
      "<h2 style='text-align:center;'>🛋️ Hayal Mobilya ERP</h2>",
      unsafe_allow_html=True,
  )
  col1, col2, col3 = st.columns([1, 2, 1])

  with col2:
    secim = st.radio(
        "İşlem Seçin",
        ["Giriş Yap", "Şifremi Unuttum", "Yeni Hesap Aç"],
        horizontal=True,
        label_visibility="collapsed",
    )

    if secim == "Giriş Yap":
      with st.form("login_form"):
        st.markdown("### Oturum Aç")
        k_adi = st.text_input("Kullanıcı Adı")
        sifre = st.text_input("Şifre", type="password")
        btn = st.form_submit_button("Giriş Yap", use_container_width=True)
        if btn:
          if (
              k_adi in st.session_state.global_users
              and st.session_state.global_users[k_adi] == sifre
          ):
            st.session_state.current_user = k_adi
            st.success("Giriş başarılı!")
            st.rerun()
          else:
            st.error("Kullanıcı adı veya şifre hatalı!")

    elif secim == "Şifremi Unuttum":
      with st.form("sifre_unuttum_form"):
        st.markdown("### Şifre Sıfırlama")
        k_adi = st.text_input("Kullanıcı Adı")
        yeni_sifre = st.text_input("Yeni Şifre", type="password")
        yeni_sifre_tekrar = st.text_input(
            "Yeni Şifre (Tekrar)", type="password"
        )
        sifre_sifirla_btn = st.form_submit_button(
            "Şifreyi Sıfırla", use_container_width=True
        )

        if sifre_sifirla_btn:
          if k_adi in st.session_state.global_users:
            if yeni_sifre and yeni_sifre == yeni_sifre_tekrar:
              st.session_state.global_users[k_adi] = yeni_sifre
              st.success(
                  "✅ Şifreniz başarıyla güncellendi. Giriş yapabilirsiniz."
              )
            else:
              st.error("❌ Yeni şifreler boş olamaz ve uyuşmalıdır!")
          else:
            st.error("❌ Bu kullanıcı adı sistemde bulunamadı!")

    elif secim == "Yeni Hesap Aç":
      with st.form("yeni_hesap_form"):
        st.markdown("### Yeni Kullanıcı Kaydı")
        y_kadi = st.text_input("Yeni Kullanıcı Adı")
        y_sifre = st.text_input("Şifre", type="password")
        y_sifre_tekrar = st.text_input("Şifre (Tekrar)", type="password")
        kayit_btn = st.form_submit_button(
            "Hesap Oluştur", use_container_width=True
        )

        if kayit_btn:
          if not y_kadi:
            st.error("❌ Kullanıcı adı boş olamaz!")
          elif y_kadi in st.session_state.global_users:
            st.error("❌ Bu kullanıcı adı zaten alınmış!")
          elif not y_sifre or y_sifre != y_sifre_tekrar:
            st.error("❌ Şifreler boş olamaz ve uyuşmalıdır!")
          else:
            st.session_state.global_users[y_kadi] = y_sifre
            st.success(
                "✅ Hesabınız başarıyla oluşturuldu! Şimdi giriş"
                " yapabilirsiniz."
            )


# Oturum Kontrolü
if st.session_state.current_user is None:
  auth_ekrani()
else:
  # Kenar Çubuğu Menüsü
  st.sidebar.title("🛋️ Hayal Mobilya ERP")
  st.sidebar.markdown(f"Kullanıcı: **{st.session_state.current_user}**")

  menu_secim = st.sidebar.selectbox(
      "Menü",
      [
          "🏠 Ana Sayfa",
          "📦 Stok Yönetimi",
          "📄 Satış & Faturalar",
          "👥 Cari Hesaplar & Borçlar",
          "🏦 Banka Hesapları",
          "➕ Yeni Ürün Kartı Aç",
          "💰 Kasa & Finans",
          "📊 Raporlar & Analiz",
          "🔑 Şifre Değiştir",
      ],
  )

  if st.sidebar.button("Çıkış Yap"):
    st.session_state.current_user = None
    st.rerun()

  # =========================================================
  # 1. ANA SAYFA (TÜM VERİLERİN LİSTELENDİĞİ GENEL PANEL)
  # =========================================================
  if menu_secim == "🏠 Ana Sayfa":
    st.markdown(
        '<div class="page-title">🏠 Hayal Mobilya Yönetim Paneli</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kurumsal ERP ve Operasyon Kontrol'
        " Merkezi - Tüm Veri Özeti.</div>",
        unsafe_allow_html=True,
    )

    # Üst Metrik Kartları
    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(
          "📦 Toplam Ürün Çeşidi", len(st.session_state.global_stok)
      )
    with col2:
      st.metric(
          "👥 Toplam Cari Hesap", len(st.session_state.global_cariler)
      )
    with col3:
      toplam_ciro = (
          sum([f["Toplam"] for f in st.session_state.global_faturalar])
          if len(st.session_state.global_faturalar) > 0
          else 0.0
      )
      st.metric("💰 Toplam Ciro / Satış", f"₺{toplam_ciro:,.2f}")
    with col4:
      st.metric(
          "🏦 Banka Hesap Sayısı",
          len(st.session_state.global_banka_hesaplari),
      )

    st.markdown("---")

    # Tüm Stok Listesi
    st.markdown("#### 📦 Tüm Stok ve Envanter Listesi")
    st.dataframe(
        st.session_state.global_stok, use_container_width=True, hide_index=True
    )

    st.markdown("---")

    # Tüm Cari Hesaplar Listesi
    st.markdown("#### 👥 Tüm Cari Hesaplar (Müşteri & Tedarikçiler)")
    st.dataframe(
        st.session_state.global_cariler,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # Tüm Banka Hesapları Listesi
    st.markdown("#### 🏦 Tüm Banka Hesapları ve IBAN Bilgileri")
    st.dataframe(
        st.session_state.global_banka_hesaplari,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # Tüm Faturalar Listesi
    st.markdown("#### 📄 Tüm Kesilen Satış Faturaları")
    if len(st.session_state.global_faturalar) > 0:
      st.dataframe(
          pd.DataFrame(st.session_state.global_faturalar),
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.info("Kayıtlı fatura bulunmuyor.")

  elif menu_secim == "📦 Stok Yönetimi":
    st.markdown(
        '<div class="page-title">📦 Stok & Envanter Yönetimi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kayıtlı mobilya bileşenleri ve hammadde stok'
        " durumu.</div>",
        unsafe_allow_html=True,
    )
    st.dataframe(
        st.session_state.global_stok, use_container_width=True, hide_index=True
    )

  elif menu_secim == "📄 Satış & Faturalar":
    st.markdown(
        '<div class="page-title">📄 Satış Faturaları & Siparişler</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kesilen faturalar ve ciro takibi.</div>',
        unsafe_allow_html=True,
    )
    if len(st.session_state.global_faturalar) > 0:
      st.dataframe(
          pd.DataFrame(st.session_state.global_faturalar),
          use_container_width=True,
          hide_index=True,
      )
    else:
      st.info("Kayıtlı fatura bulunmuyor.")

  elif menu_secim == "👥 Cari Hesaplar & Borçlar":
    st.markdown(
        '<div class="page-title">👥 Cari Hesaplar & Borç / Alacak Takibi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Müşteri ve tedarikçilerinizin finansal'
        " bakiye durumları.</div>",
        unsafe_allow_html=True,
    )

    arama_cari = st.text_input(
        "🔎 Cari Ara", placeholder="Müşteri veya tedarikçi adı girin..."
    )
    df_c = st.session_state.global_cariler.copy()
    if arama_cari:
      df_c = df_c[
          df_c["Cari Adı"].str.contains(arama_cari, case=False, na=False)
      ]

    st.dataframe(df_c, use_container_width=True, hide_index=True)

    st.markdown("#### Yeni Cari Hesap Ekle")
    with st.form("yeni_cari_form"):
      c_ad = st.text_input("Cari Adı / Firma Unvanı *")
      c_tel = st.text_input("Telefon Numarası")
      c_tur = st.selectbox("Cari Türü", ["Müşteri", "Tedarikçi"])
      c_bakiye = st.number_input(
          "Başlangıç Bakiyesi (TL) (Borç için -, Alacak için +)",
          value=0.0,
          step=100.0,
      )

      cari_kaydet = st.form_submit_button("Cari Hesabı Kaydet")
      if cari_kaydet:
        if c_ad:
          yeni_cari = pd.DataFrame([{
              "Cari Adı": c_ad,
              "Telefon": c_tel,
              "Tür": c_tur,
              "Bakiye (TL)": c_bakiye,
          }])
          st.session_state.global_cariler = pd.concat(
              [st.session_state.global_cariler, yeni_cari], ignore_index=True
          )
          st.success(f"✅ {c_ad} başarıyla cari hesaplara eklendi.")
          st.rerun()
        else:
          st.error("❌ Cari adı boş olamaz!")

  elif menu_secim == "🏦 Banka Hesapları":
    st.markdown(
        '<div class="page-title">🏦 Banka Hesapları & IBAN Yönetimi</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirketin ticari banka hesapları ve döviz'
        " varlıkları.</div>",
        unsafe_allow_html=True,
    )

    st.dataframe(
        st.session_state.global_banka_hesaplari,
        use_container_width=True,
        hide_index=True,
    )

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
              "Döviz": b_doviz,
          }])
          st.session_state.global_banka_hesaplari = pd.concat(
              [st.session_state.global_banka_hesaplari, yeni_b],
              ignore_index=True,
          )
          st.success("✅ Banka hesabı başarıyla eklendi.")
          st.rerun()
        else:
          st.error("❌ Banka adı ve IBAN alanları zorunludur!")

  elif menu_secim == "➕ Yeni Ürün Kartı Aç":
    st.markdown(
        '<div class="page-title">➕ Yeni Ürün & Model Tanımlama</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Kataloğa yeni bir mobilya kalemi veya'
        " hammadde ekleyin.</div>",
        unsafe_allow_html=True,
    )

    with st.form("yeni_urun_kart_form"):
      u_ad = st.text_input("Ürün / Model Adı *")
      u_barkod = st.text_input("Barkod (Boş bırakılırsa otomatik üretilir)")
      c1, c2 = st.columns(2)
      with c1:
        u_alis = st.number_input(
            "Alış / Maliyet Fiyatı (TL)", min_value=0.0, step=100.0
        )
        u_kritik = st.number_input(
            "Kritik Stok Sınırı", min_value=1, value=3, step=1
        )
      with c2:
        u_satis = st.number_input(
            "Satış Fiyatı (TL)", min_value=0.0, step=100.0
        )
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
          st.session_state.global_stok = pd.concat(
              [st.session_state.global_stok, yeni_satir], ignore_index=True
          )
          st.success(
              f"✅ '{u_ad}' başarıyla sisteme tanımlandı! (Barkod: {u_barkod})"
          )

  elif menu_secim == "💰 Kasa & Finans":
    st.markdown(
        '<div class="page-title">💰 Kasa & Genel Finansal Durum</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Şirket nakit akışı ve genel finansal'
        " özet.</div>",
        unsafe_allow_html=True,
    )

    toplam_satis_ciro = (
        sum([f["Toplam"] for f in st.session_state.global_faturalar])
        if len(st.session_state.global_faturalar) > 0
        else 0.0
    )

    col_k1, col_k2 = st.columns(2)
    with col_k1:
      st.metric("Toplam Tahsil Edilen / Ciro", f"₺{toplam_satis_ciro:,.2f}")
    with col_k2:
      toplam_borc_alacak = st.session_state.global_cariler["Bakiye (TL)"].sum()
      st.metric("Net Cari Bakiye Durumu", f"₺{toplam_borc_alacak:,.2f}")

    st.info(
        "💡 Detaylı gelir-gider ve kasa hareketleri modülü yakında eklenecektir."
    )

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

  elif menu_secim == "🔑 Şifre Değiştir":
    st.markdown(
        '<div class="page-title">🔑 Kullanıcı Şifre Değiştirme</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-subtitle">Oturum açan hesap için güvenli şifre'
        " güncelleme.</div>",
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

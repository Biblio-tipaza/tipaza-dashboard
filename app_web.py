import base64
import os
import streamlit as st

# إعداد صفحة الويب
st.set_page_config(
    page_title="لوحة التحكم المركزية - جامعة تيبازة",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# دالة لتضمين الشعار كخلفية بوضوح عالٍ
def set_bg_hack(image_file):
  if os.path.exists(image_file):
    with open(image_file, "rb") as f:
      data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
        <style>
        .stApp {{
            background-color: #225c68;
            background-image: linear-gradient(rgba(34, 92, 104, 0.45), rgba(34, 92, 104, 0.45)), url("data:image/png;base64,{encoded}");
            background-size: 55% auto;
            background-repeat: no-repeat;
            background-position: center;
            background-attachment: fixed;
        }}
        /* تخصيص إطار تسجيل الدخول ليصبح أصغر وأنيقاً في المنتصف */
        .stForm {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 25px !important;
            border-radius: 15px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            max-width: 380px !important;
            margin: 0 auto !important;
        }}
        .platform-card {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 15px;
            transition: transform 0.2s;
        }}
        .platform-card:hover {{
            transform: translateY(-5px);
        }}
        h1, h2, h3, p, label {{
            direction: rtl;
            text-align: right;
        }}
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)
  else:
    st.markdown(
        """
        <style>
        .stApp { background-color: #225c68; }
        </style>
        """,
        unsafe_allow_html=True,
    )


# تطبيق الخلفية
set_bg_hack("logo.png")

# إدارة حالة تسجيل الدخول
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

# شاشة تسجيل الدخول
if not st.session_state.logged_in:
  st.markdown("<br>", unsafe_allow_html=True)

  col1, col2, col3 = st.columns([1, 1.2, 1])
  with col2:
    with st.form("login_form"):
      # العناوين متواجدة الآن داخل الإطار تماماً لضمان التوسيط الدقيق
      st.markdown(
          """
                <div style="text-align: center; margin-bottom: 15px;">
                    <h2 style="color: #225c68; font-family: 'Cairo', sans-serif; font-size: 17px; font-weight: bold; margin-bottom: 4px;">لوحة التحكم المركزية للأنظمة والمنصات</h2>
                    <p style="color: #e67e22; font-size: 14px; font-weight: bold; margin: 0;">جامعة تيبازة</p>
                </div>
            """,
          unsafe_allow_html=True,
      )

      username = st.text_input("اسم المستخدم", placeholder="أدخل اسم المستخدم...")
      password = st.text_input(
          "كلمة المرور", type="password", placeholder="أدخل كلمة المرور..."
      )

      submit = st.form_submit_button("تسجيل الدخول", use_container_width=True)

      if submit:
        if username == "admin" and password == "12345":
          st.session_state.logged_in = True
          st.rerun()
        else:
          st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

    # مسافة بسيطة قبل زر الخروج
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 الخروج", use_container_width=True):
      st.warning("تم إغلاق التطبيق.")

# لوحة التحكم الرئيسية بعد تسجيل الدخول
else:
  st.markdown(
      """
        <div style="background-color: rgba(255, 255, 255, 0.92); padding: 15px; border-radius: 10px; margin-bottom: 25px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h2 style="color: #225c68; margin: 0;">لوحة التحكم المركزية للأنظمة والمنصات - جامعة تيبازة</h2>
        </div>
    """,
      unsafe_allow_html=True,
  )

  platforms = [
      ("OPAC بوابة البحث", "🔍"),
      ("CIRCULATION PMB", "📚"),
      ("بوابة البحث بالمكتبة المركزية", "🏛️"),
      ("PMB التحقق البصري لـ", "👁️"),
      ("PROGRES Compte", "💻"),
      ("SETS فضاء الموظفين", "👥"),
      ("OPU بوابة البحث", "🌐"),
      ("SNDL بوابة البحث", "🔎"),
      ("موقع المكتبة المركزية", "🌐"),
      ("SNDL واجهة تسجيل", "📝"),
      ("SNDL قاعدة طلبات", "🗂️"),
      ("نظام تسيير المكتبة", "⚙️"),
      ("Data Base قاعدة البيانات", "🗄️"),
      ("HPTAI نظام المساومة", "📊"),
      ("GitHub موقع قواعد الأنظمة", "📂"),
      ("SNDL استمارة التسجيل", "📋"),
  ]

  cols = st.columns(4)
  for index, (title, icon) in enumerate(platforms):
    with cols[index % 4]:
      st.markdown(
          f"""
                <div class="platform-card">
                    <div style="font-size: 28px; margin-bottom: 8px;">{icon}</div>
                    <div style="font-weight: bold; color: #2c3e50; font-size: 14px;">{title}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
      if st.button(f"فتح النظام", key=f"btn_{index}", use_container_width=True):
        st.toast(f"جاري الانتقال إلى: {title}")

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("تسجيل الخروج", type="primary"):
    st.session_state.logged_in = False
    st.rerun()

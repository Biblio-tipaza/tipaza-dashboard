import base64
import json
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
        /* تخصيص إطار تسجيل الدخول */
        .stForm {{
            background-color: rgba(255, 255, 255, 0.95);
            padding: 25px !important;
            border-radius: 15px !important;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
            max-width: 380px !important;
            margin: 0 auto !important;
        }}
        /* تخصيص البطاقة لتكون متناسقة تماماً في العرض */
        .platform-card {{
            background: linear-gradient(135deg, #ffffff, #f8f9fa);
            padding: 15px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            height: 100px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            border: 1px solid #e0e0e0;
            border-bottom: none;
        }}
        /* تخصيص وتلوين زر فتح النظام ليكون بنفس عرض ومقاس البطاقة تماماً */
        .system-link {{
            display: block;
            background: linear-gradient(135deg, #2980b9, #2c3e50);
            color: #ffffff !important;
            padding: 8px 10px;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 12px;
            text-align: center;
            text-decoration: none !important;
            font-weight: bold;
            font-size: 13px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
            border: 1px solid #2c3e50;
            border-top: none;
        }}
        .system-link:hover {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.2);
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
    st.markdown(
        """
            <div style="text-align: center; margin-bottom: 15px; transform: translateX(-30px);">
                <h2 style="color: #ffffff; font-family: 'Cairo', sans-serif; font-size: 18px; font-weight: bold; text-shadow: 0 2px 4px rgba(0,0,0,0.7); margin-bottom: 4px;">لوحة التحكم المركزية للأنظمة والمنصات</h2>
                <p style="color: #f1c40f; font-size: 15px; font-weight: bold; text-shadow: 0 1px 3px rgba(0,0,0,0.7); margin: 0;">جامعة تيبازة</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
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

  platforms = []
  if os.path.exists("systems.json"):
    with open("systems.json", "r", encoding="utf-8") as f:
      platforms = json.load(f)

  cols = st.columns(4)
  for index, item in enumerate(platforms):
    title = item.get("name", "")
    icon = item.get("icon", "🔗")
    url = item.get("url", "#")

    with cols[index % 4]:
      st.markdown(
          f"""
                <div class="platform-card">
                    <div style="font-size: 24px; margin-bottom: 4px;">{icon}</div>
                    <div style="font-weight: bold; color: #2c3e50; font-size: 12px;">{title}</div>
                </div>
            """,
          unsafe_allow_html=True,
      )
      st.markdown(
          f'<a href="{url}" target="_blank" class="system-link">فتح النظام</a>',
          unsafe_allow_html=True,
      )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("تسجيل الخروج", type="primary"):
    st.session_state.logged_in = False
    st.rerun()

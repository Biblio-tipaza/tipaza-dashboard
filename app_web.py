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
        
        /* تقليص المسافة بين الأعمدة إلى حوالي 1 سم */
        [data-testid="stHorizontalBlock"] {{
            gap: 12px !important;
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
        
        /* تصميم البطاقات المدمجة */
        .platform-card {{
            padding: 10px 15px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
            height: 90px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
            border: 1px solid rgba(255,255,255,0.3);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}
        .platform-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.25);
        }}
        
        /* تنسيق الأيقونة والنص داخل البطاقة المدمجة */
        .card-content {{
            display: flex;
            align-items: center;
            width: 100%;
            text-decoration: none !important;
        }}
        .card-icon {{
            font-size: 22px;
            margin-left: 10px;
            flex-shrink: 0;
        }}
        .card-title {{
            font-weight: bold;
            font-size: 13px;
            color: #ffffff;
            text-align: right;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            width: 100%;
            text-shadow: 0 1px 2px rgba(0,0,0,0.2);
        }}

        /* تلوين زر Popover (إضافة جديد) باللون الأحمر وتنسيقه */
        div[data-testid="stPopover"] button {{
            background: linear-gradient(135deg, #c0392b, #962d22) !important;
            color: #ffffff !important;
            font-weight: bold !important;
            border-radius: 8px !important;
            border: 1px solid #962d22 !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
            width: 100% !important;
        }}
        div[data-testid="stPopover"] button:hover {{
            background: linear-gradient(135deg, #e74c3c, #c0392b) !important;
            color: #ffffff !important;
            border: 1px solid #c0392b !important;
            transform: translateY(-1px);
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
        [data-testid="stHorizontalBlock"] { gap: 12px !important; }
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
  # توزيع الأعمدة للإطار العلوي (العنوان في المنتصف وزر الإضافة في اليسار)
  col_empty1, col_title, col_btn = st.columns([0.1, 4.5, 1.3])

  with col_btn:
    with st.popover("➕ إضافة جديد", use_container_width=True):
      st.markdown(
          "<h4 style='text-align: right; color: #c0392b;'>إضافة نظام جديد</h4>",
          unsafe_allow_html=True,
      )
      with st.form("add_system_form_popup"):
        new_name = st.text_input(
            "اسم النظام", placeholder="مثال: منصة الإشعارات"
        )
        new_url = st.text_input(
            "رابط النظام (URL)", placeholder="https://..."
        )
        new_icon = st.text_input("الأيقونة (Emoji)", placeholder="📌")

        submitted = st.form_submit_button("حفظ في القائمة")
        if submitted:
          if new_name and new_url:
            platforms = []
            if os.path.exists("systems.json"):
              with open("systems.json", "r", encoding="utf-8") as f:
                platforms = json.load(f)

            platforms.append({
                "name": new_name,
                "url": new_url,
                "icon": new_icon if new_icon else "🔗",
            })

            with open("systems.json", "w", encoding="utf-8") as f:
              json.dump(platforms, f, ensure_ascii=False, indent=2)

            st.success("تمت الإضافة بنجاح!")
            st.rerun()
          else:
            st.error("الرجاء ملء اسم النظام والرابط!")

  with col_title:
    st.markdown(
        """
        <div style="background-color: rgba(255, 255, 255, 0.95); padding: 12px 20px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.2); text-align: center;">
            <h2 style="color: #225c68; margin: 0; font-size: 21px;">لوحة التحكم المركزية للأنظمة والمنصات - جامعة تيبازة</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

  st.markdown("<div style='margin-top: 15px;'></div>", unsafe_allow_html=True)

  # قائمة من الألوان المتناسقة والجميلة لتوزيعها على البطاقات
  card_colors = [
      "linear-gradient(135deg, #2980b9, #2c3e50)",  # أزرق غامق
      "linear-gradient(135deg, #27ae60, #1e8449)",  # أخضر
      "linear-gradient(135deg, #8e44ad, #5b2c6f)",  # بنفسجي
      "linear-gradient(135deg, #d35400, #a04000)",  # برتقالي/قرميدي
      "linear-gradient(135deg, #16a085, #0e6655)",  # تركواز
      "linear-gradient(135deg, #c0392b, #962d22)",  # أحمر داكن
      "linear-gradient(135deg, #f39c12, #d68910)",  # أصفر ذهبي
      "linear-gradient(135deg, #34495e, #2c3e50)",  # رمادي فحمي
  ]

  # تحميل الأنظمة من ملف systems.json وعرضها
  platforms = []
  if os.path.exists("systems.json"):
    with open("systems.json", "r", encoding="utf-8") as f:
      platforms = json.load(f)

  cols = st.columns(4)
  for index, item in enumerate(platforms):
    title = item.get("name", "")
    icon = item.get("icon", "🔗")
    url = item.get("url", "#")
    bg_color = card_colors[index % len(card_colors)]

    with cols[index % 4]:
      st.markdown(
          f"""
                <div class="platform-card" style="background: {bg_color};">
                    <a href="{url}" target="_blank" class="card-content">
                        <span class="card-title">{title}</span>
                        <span class="card-icon">{icon}</span>
                    </a>
                </div>
            """,
          unsafe_allow_html=True,
      )

  st.markdown("<br>", unsafe_allow_html=True)
  if st.button("تسجيل الخروج", type="primary"):
    st.session_state.logged_in = False
    st.rerun()

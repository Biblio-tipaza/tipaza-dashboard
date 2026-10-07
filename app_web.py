import streamlit as st

# إعداد صفحة الويب وعنوانها
st.set_page_config(
    page_title="لوحة التحكم المركزية - جامعة تيبازة",
    page_icon="🎓",
    layout="wide"
)

# تخصيص التصميم بلغة CSS (دعم اللغة العربية والخطوط والألوان)
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        background-color: #27ae60;
        color: white;
        border-radius: 8px;
        width: 100%;
        height: 45px;
        font-weight: bold;
        font-size: 15px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #2ecc71;
        color: white;
    }
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border-top: 4px solid #225c68;
    }
    h1, h2, h3 {
        color: #225c68;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# إدارة جلسة تسجيل الدخول
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# --- 1. واجهة تسجيل الدخول ---
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.write("")
        st.write("")
        try:
            st.image("logo.png", width=110)
        except:
            pass
            
        st.markdown("<h1>لوحة التحكم المركزية للأنظمة والمنصات</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #7f8c8d; font-size: 15px; margin-bottom: 20px;'>جامعة تيبازة</h3>", unsafe_allow_html=True)
        
        username = st.text_input("👤 اسم المستخدم")
        password = st.text_input("🔒 كلمة المرور", type="password")
        
        st.write("")
        if st.button("تسجيل الدخول"):
            if username == "admin" and password == "12345":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة!")

# --- 2. لوحة التحكم الرئيسية بعد تسجيل الدخول ---
else:
    # الشريط الجانبي (Sidebar) للتنقل السريع
    with st.sidebar:
        st.image("logo.png" if "logo.png" else "", width=70)
        st.markdown("### المكتبة المركزية")
        st.markdown("---")
        if st.button("🏠 الرئيسية"):
            st.session_state.current_page = "home"
        if st.button("📚 إدارة منصة SNDL"):
            st.session_state.current_page = "sndl"
        if st.button("👥 أرشيف الطلبة"):
            st.session_state.current_page = "students"
        if st.button("📊 الإحصائيات والتقارير"):
            st.session_state.current_page = "stats"
        
        st.markdown("---")
        if st.button("🚪 تسجيل الخروج", type="primary"):
            st.session_state.logged_in = False
            st.session_state.current_page = "home"
            st.rerun()

    # محتوى الصفحات بناءً على اختيار المستخدم
    if st.session_state.current_page == "home":
        st.markdown("<h1>🎓 لوحة التحكم المركزية للأنظمة والمنصات</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #555; font-size: 16px;'>المكتبة المركزية - جامعة تيبازة</p>", unsafe_allow_html=True)
        st.write("---")
        
        # عرض بطاقات سريعة للخدمات
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="card">
                    <h3>📚 منصة SNDL</h3>
                    <p>إدارة وتفعيل حسابات الطلبة والباحثين للوصول إلى الوثائق الرقمية.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("إدارة SNDL"):
                st.session_state.current_page = "sndl"
                st.rerun()
                
        with col2:
            st.markdown("""
                <div class="card">
                    <h3>👥 أرشيف الطلبة</h3>
                    <p>متابعة إبراء الذمة، إيداع المذكرات، وتسجيلات الطلبة المتخرِّجين.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("فتح الأرشيف"):
                st.session_state.current_page = "students"
                st.rerun()
                
        with col3:
            st.markdown("""
                <div class="card">
                    <h3>📊 التقارير والإحصائيات</h3>
                    <p>عرض مؤشرات الاستخدام، إحصائيات التسجيل والتحكم بالمنصات.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("عرض التقارير"):
                st.session_state.current_page = "stats"
                st.rerun()

    elif st.session_state.current_page == "sndl":
        st.markdown("<h2>📚 إدارة منصة SNDL والوثائق الرقمية</h2>", unsafe_allow_html=True)
        st.write("هنا يمكنك متابعة طلبات الاشتراكات وتفعيل الحسابات الخاصة بالطلبة.")
        st.info("💡 جارٍ ربط النظام بقاعدة البيانات لاستعراض قائمة المشتركين...")
        if st.button("العودة للرئيسية"):
            st.session_state.current_page = "home"
            st.rerun()

    elif st.session_state.current_page == "students":
        st.markdown("<h2>👥 أرشيف وقاعدة بيانات الطلبة</h2>", unsafe_allow_html=True)
        st.write("إدارة إيداع مذكرات التخرج وإجراءات إبراء الذمة (ال clearance).")
        st.success("✅ النظام جاهز لاستقبال ملفات ومذكرات الطلبة.")
        if st.button("العودة للرئيسية"):
            st.session_state.current_page = "home"
            st.rerun()

    elif st.session_state.current_page == "stats":
        st.markdown("<h2>📊 لوحة الإحصائيات والتقارير العامة</h2>", unsafe_allow_html=True)
        st.metric(label="إجمالي الطلبة المسجلين هذا الموسم", value="1,420 طالب")
        st.metric(label="حسابات SNDL المفعلة", value="890 حساب")
        st.write("")
        if st.button("العودة للرئيسية"):
            st.session_state.current_page = "home"
            st.rerun()
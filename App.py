import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- הגדרות עיצוב ומדע ---
st.set_page_config(page_title="OCD ERP Tool - ILT Model", layout="centered")

# עיצוב מותאם למובייל (RTL)
st.markdown("""
    <style>
    body {direction: rtl; text-align: right; font-family: -apple-system, BlinkMacSystemFont, sans-serif;}
    .stTextInput, .stTextArea, .stSelectbox, .stSlider {direction: rtl;}
    div.stButton > button:first-child {background-color: #007AFF; color: white; border-radius: 12px; height: 50px; font-size: 18px;}
    .script-card {background-color: #F2F2F7; padding: 20px; border-radius: 15px; border-right: 6px solid #FF3B30; margin-bottom: 20px;}
    .scientific-note {font-size: 12px; color: gray; margin-top: -10px; margin-bottom: 10px;}
    </style>
    """, unsafe_allow_html=True)

# --- ניהול זיכרון ---
if 'scripts' not in st.session_state: st.session_state.scripts = []
if 'logs' not in st.session_state: st.session_state.logs = []

# --- לוגיקה מדעית: הפרת ציפיות ---
def calculate_learning(prediction, reality):
    gap = prediction - reality
    if gap > 0: return "✨ התרחשה למידה מעכבת: הציפייה הייתה גרועה מהמציאות."
    return "⚠️ שים לב: המוח עדיין נצמד לציפייה המפחידה."

# --- תפריט ראשי ---
st.title("🛡️ ERP Inhibitory Tool")
st.caption("כלי קליני לחשיפה ומניעת תגובה | מבוסס מחקר ILT")

mode = st.selectbox("בחר מצב עבודה:", ["📝 יצירת תסריט חשיפה", "⏱️ ביצוע חשיפה (בזמן אמת)", "📊 יומן מעקב ומסקנות"])

# --- מצב 1: יצירת תסריט ---
if mode == "📝 יצירת תסריט חשיפה":
    st.subheader("בניית תסריט מבוסס חוסר ודאות")
    st.markdown("על פי מודל ה-ERP, המטרה היא לא להרגיע, אלא לייצר תסריט שמעורר את 'הספק המקסימלי'.")
    
    with st.form("new_script"):
        title = st.text_input("שם התסריט (למשל: 'היא שותקת בסלון')")
        trigger = st.text_area("הטריגר (המציאות האובייקטיבית)")
        catastrophe = st.text_area("הקטסטרופה (מה ה-OCD טוען שיקרה?)")
        response_prevention = st.text_area("מניעת התגובה (מה אסור לי לעשות?)", value="לא לבדוק, לא לשאול, לא לנתח בראש.")
        
        submitted = st.form_submit_button("שמור תסריט למאגר")
        if submitted and title:
            script_content = f"""
            **המצב:** {trigger}
            **הפחד:** {catastrophe}
            ---
            **הצהרת חשיפה:**
            "זה נכון ש-{trigger}, ויכול להיות שזה אומר ש-{catastrophe}.
            אני מוכן להישאר עם האימה הזו ולא לדעת את האמת.
            אני בוחר שלא: {response_prevention}."
            """
            st.session_state.scripts.append({"title": title, "content": script_content, "prevention": response_prevention})
            st.success("התסריט נשמר.")

# --- מצב 2: חדר חשיפה ---
elif mode == "⏱️ ביצוע חשיפה (בזמן אמת)":
    if not st.session_state.scripts:
        st.warning("יש ליצור תסריט תחילה.")
    else:
        script = st.selectbox("בחר תסריט:", st.session_state.scripts, format_func=lambda x: x['title'])
        
        st.markdown("### שלב 1: ניבוי החרדה (Expectancy)")
        st.markdown("<p class='scientific-note'>מודל ILT: עלינו לבדוק עד כמה אתה מצפה שהתוצאה תהיה בלתי נסבלת.</p>", unsafe_allow_html=True)
        predicted_distress = st.slider("עד כמה זה יהיה נורא/בלתי נסבל? (0-100)", 0, 100, 80)
        
        st.markdown("---")
        st.markdown(f"<div class='script-card'>{script['content']}</div>", unsafe_allow_html=True)
        
        exposure_time = st.selectbox("זמן חשיפה בדקות:", [5, 10, 15, 20])
        
        if st.button("התחל טיימר חשיפה"):
            progress_bar = st.progress(0)
            status = st.empty()
            for i in range(exposure_time * 60):
                progress_bar.progress((i + 1) / (exposure_time * 60))
                status.markdown(f"**זמן נותר: {exposure_time*60 - i} שניות.**\n\n זכור: {script['prevention']}")
                time.sleep(1)
            status.success("החשיפה הסתיימה.")
            
            st.session_state.current_exposure = {"script": script['title'], "predicted": predicted_distress}

        # שלב העיבוד (Post-Exposure)
        if 'current_exposure' in st.session_state:
            st.markdown("### שלב 2: עיבוד והפרת ציפיות")
            actual_distress = st.slider("בפועל, כמה בלתי נסבל זה היה? (0-100)", 0, 100, 50, key="actual")
            
            if st.button("סיים ותעד ביומן"):
                learning_msg = calculate_learning(st.session_state.current_exposure['predicted'], actual_distress)
                st.session_state.logs.append({
                    "Date": datetime.now().strftime("%d/%m %H:%M"),
                    "Script": st.session_state.current_exposure['script'],
                    "Prediction": st.session_state.current_exposure['predicted'],
                    "Reality": actual_distress,
                    "Conclusion": learning_msg
                })
                st.info(learning_msg)

# --- מצב 3: יומן ---
elif mode == "📊 יומן מעקב ומסקנות":
    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)
        st.table(df)
    else:
        st.info("עדיין אין נתונים. בצע חשיפה ראשונה.")

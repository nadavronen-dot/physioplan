import streamlit as st
import pandas as pd
import os
import urllib.parse

# --- 1. הגדרות דף ---
st.set_page_config(page_title="נדב רונן פיזיותרפיה", layout="wide")

# הזרקת CSS ליישור לימין ותצוגה נקייה
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; }
    [data-testid="stSidebar"] { direction: rtl; }
    .stAlert { direction: rtl; text-align: right; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ניהול הזיכרון (Session State) ---
if 'exercise_cart' not in st.session_state:
    st.session_state.exercise_cart = {}


# --- 3. טעינת נתונים חסינה ---
@st.cache_data
def load_data():
    base_path = os.path.dirname(os.path.abspath(__file__))
    # מחפש את הקובץ גם בתוך תיקיית data וגם בתיקייה הראשית (למקרה של אי התאמה ב-GitHub)
    paths = [
        os.path.join(base_path, "data", "exercises.csv"),
        os.path.join(base_path, "exercises.csv")
    ]

    csv_path = None
    for p in paths:
        if os.path.exists(p):
            csv_path = p
            break

    if not csv_path:
        st.error("קובץ הנתונים exercises.csv לא נמצא.")
        return None

    encodings = ['utf-8-sig', 'windows-1255', 'utf-8']
    for enc in encodings:
        try:
            # בדיקה אם השורה הראשונה היא הכותרת המיותרת "exercises"
            test_df = pd.read_csv(csv_path, encoding=enc, nrows=1)
            skip = 1 if test_df.columns.size == 1 and test_df.columns[0] == 'exercises' else 0

            data = pd.read_csv(csv_path, encoding=enc, skiprows=skip)
            data.columns = data.columns.str.strip()
            data = data.fillna('')
            return data
        except:
            continue
    return None


df = load_data()


# פונקציית עזר למציאת עמודה (מונע KeyError)
def find_col(df, options):
    for opt in options:
        if opt in df.columns: return opt
    return df.columns[0] if not df.empty else None


if df is not None:
    COL_NAME = find_col(df, ['Exercise_Name_HE', 'name_he', 'Exercise_Name'])
    COL_INST = find_col(df, ['Instructions_HE', 'instructions_he', 'Instructions'])
    COL_TIPS = find_col(df, ['Clinical_Tips_HE', 'clinical_tips_he', 'Clinical_Tips'])
    COL_AREA = find_col(df, ['Body_Area_HE', 'body_area_he', 'Body_Area'])
else:
    st.stop()


# פונקציית עזר להצגת טקסט בעברית מיושר לימין
def rtl_markdown(text, size="p"):
    if size == "h3":
        st.markdown(f'<div style="direction: rtl; text-align: right;"><h3>{text}</h3></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="direction: rtl; text-align: right;">{text}</div>', unsafe_allow_html=True)


# --- 4. סרגל צד ---
with st.sidebar:
    st.markdown('<div style="direction: rtl; text-align: right;"><h1>נדב רונן</h1></div>', unsafe_allow_html=True)
    st.divider()

    rtl_markdown("סל תרגילים")
    if not st.session_state.exercise_cart:
        rtl_markdown("הסל ריק")
    else:
        for ex_id, details in list(st.session_state.exercise_cart.items()):
            col_ex, col_del = st.columns([4, 1])
            with col_ex:
                rtl_markdown(f"{details['name']} ({details['sets']}x{details['reps']})")
            if col_del.button("הסר", key=f"del_{ex_id}"):
                del st.session_state.exercise_cart[ex_id]
                st.rerun()

        st.divider()
        full_message = "*תוכנית תרגול - נדב רונן פיזיותרפיה*\n\n"
        for ex in st.session_state.exercise_cart.values():
            full_message += f"* {ex['name']}\n"
            full_message += f"מינון: {ex['sets']} סטים, {ex['reps']} חזרות\n"
            full_message += f"קושי נדרש (RPE): {ex['rpe']}/10\n"
            full_message += f"רף כאב מותר (VAS): {ex['vas']}/10\n"
            full_message += f"הנחיית ביצוע: {ex['status']}\n"
            if ex['instructions']: full_message += f"הוראות: {ex['instructions']}\n"
            if ex['link']: full_message += f"קישור: {ex['link']}\n"
            full_message += "----------------\n"

        wa_url = f"https://wa.me/?text={urllib.parse.quote(full_message)}"
        st.link_button("שלח תוכנית בוואטסאפ", wa_url, use_container_width=True)

    st.divider()
    rtl_markdown("### סינון")
    search_query = st.text_input("חיפוש חופשי", "")
    area_options = sorted(df[COL_AREA].unique()) if COL_AREA in df.columns else []
    selected_area = st.selectbox("אזור בגוף", ["הכל"] + area_options)

# --- 5. תצוגה מרכזית ---
st.markdown('<div style="direction: rtl; text-align: right;"><h1>מאגר תרגילים קליני</h1></div>', unsafe_allow_html=True)

filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df[COL_NAME].astype(str).str.contains(search_query, case=False)]
if selected_area != "הכל":
    filtered_df = filtered_df[filtered_df[COL_AREA] == selected_area]

for index, row in filtered_df.iterrows():
    with st.container(border=True):
        col_content, col_input = st.columns([2.2, 1])

        with col_content:
            rtl_markdown(row[COL_NAME], size="h3")

            if row[COL_INST]:
                rtl_markdown("**הוראות:**")
                rtl_markdown(row[COL_INST])

            if row[COL_TIPS]:
                st.info(f"דגש קליני: {row[COL_TIPS]}")

            if 'YouTube_Link' in row and row['YouTube_Link']:
                st.write("---")
                v_col, _ = st.columns([1.2, 1])
                with v_col:
                    st.video(row['YouTube_Link'])

        with col_input:
            st.write("**מינון והנחיות**")
            s = st.number_input("סטים", 1, 10, 3, key=f"s_{index}")
            r = st.text_input("חזרות", "10", key=f"r_{index}")
            rpe = st.select_slider("קושי (RPE)", options=list(range(1, 11)), value=5, key=f"rpe_{index}")
            vas = st.select_slider("רף כאב מותר (VAS)", options=list(range(11)), value=3, key=f"vas_{index}")
            status = st.selectbox(
                "הנחיית המשכיות",
                ["המשך כרגיל", "המשך בזהירות", "עצור אם הכאב עולה"],
                key=f"status_{index}"
            )

            if st.button("הוספה", key=f"btn_{index}", use_container_width=True):
                st.session_state.exercise_cart[index] = {
                    "name": row[COL_NAME],
                    "sets": s,
                    "reps": r,
                    "rpe": rpe,
                    "vas": vas,
                    "status": status,
                    "instructions": row[COL_INST],
                    "link": row.get('YouTube_Link', '')
                }
                st.rerun()
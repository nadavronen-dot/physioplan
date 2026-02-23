import streamlit as st
import pandas as pd
import os
import urllib.parse
from datetime import date

st.set_page_config(page_title="נדב רונן פיזיותרפיה", layout="centered")

st.markdown("""
<style>
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 16px;
    }
    .block-container { max-width: 520px !important; padding: 1.2rem 1rem !important; }
    div[data-baseweb="select"] > div { direction: rtl; text-align: right; }
    div[data-testid="stSlider"] { direction: ltr; }
    .stButton > button {
        width: 100%; font-size: 1rem; padding: 0.7rem;
        border-radius: 10px; margin-top: 6px; font-weight: bold;
    }
    .ex-card {
        background: #f0f6fb; border-right: 5px solid #2E86AB;
        padding: 14px 16px; border-radius: 10px; margin: 8px 0; direction: rtl;
    }
    .cart-item {
        background: #f8f9fa; border: 1px solid #dee2e6;
        border-right: 4px solid #27AE60; padding: 10px 14px;
        border-radius: 10px; margin: 6px 0; direction: rtl;
        font-size: 0.92rem; line-height: 1.7;
    }
    .info-box {
        padding: 12px 16px; border-radius: 10px; direction: rtl;
        margin: 8px 0; color: white; font-size: 0.95rem; line-height: 1.6;
    }
    .load-box {
        padding: 12px 8px; border-radius: 10px; direction: rtl;
        text-align: center; margin: 4px 0; color: white;
        font-weight: bold; font-size: 0.95rem; line-height: 1.5;
    }
    .divider { border: none; border-top: 1px solid #e0e0e0; margin: 18px 0; }
    .tag {
        display: inline-block; background: #e8f4f8; color: #2E86AB;
        border-radius: 6px; padding: 2px 8px; font-size: 0.8rem; margin-left: 4px;
    }
    .region-tag {
        display: inline-block; background: #2E86AB; color: white;
        border-radius: 6px; padding: 2px 8px; font-size: 0.8rem; margin-left: 4px;
    }
    .main-header {
        background: linear-gradient(135deg, #2E86AB, #1a5f7a);
        color: white; padding: 16px 20px; border-radius: 12px;
        direction: rtl; margin-bottom: 16px;
    }
    .en-text {
        direction: ltr; text-align: left;
        display: block; margin: 4px 0; color: #333; font-size: 0.93rem;
    }
    .en-text-green {
        direction: ltr; text-align: left;
        display: block; margin: 4px 0; color: #1a6b3a; font-size: 0.93rem;
    }
</style>
""", unsafe_allow_html=True)

if "exercise_cart" not in st.session_state:
    st.session_state.exercise_cart = {}

def rtl(text, tag="p", color="#111", size="1rem"):
    st.markdown(
        f'<{tag} style="direction:rtl;text-align:right;color:{color};'
        f'margin:4px 0;font-size:{size}">{text}</{tag}>',
        unsafe_allow_html=True
    )

def traffic_light(vas):
    if vas == 0:
        return "#27AE60", "ירוק - ללא כאב", "המשך את התרגיל לפי המינון שקיבלת."
    if vas <= 3:
        return "#27AE60", "ירוק - כאב קל (תקין)", "כאב קל במהלך שיקום הוא תקין. המשך כרגיל. אם הכאב גדל - עצור."
    if vas <= 6:
        return "#F39C12", "כתום - הפחת עצימות", "הפחת חזרות ב-50% ועבוד בטווח תנועה קטן יותר. אם הכאב לא פוחת תוך 24 שעות - צור קשר."
    return "#E74C3C", "אדום - עצור", "הפסק את התרגיל עכשיו. מנוחה מלאה. אם הכאב נמשך מעל שעה - פנה לטיפול."

def load_label(load):
    if load < 150:   return "#27AE60", "עומס נמוך - שיקום ראשוני"
    if load < 300:   return "#F39C12", "עומס בינוני - שלב חיזוק"
    if load < 450:   return "#E67E22", "עומס גבוה - וודא התאוששות"
    return "#E74C3C", "עומס גבוה מאוד - שקול הפחתה"

REGION_MAP = {
    "knee":               "Lower Limb",
    "hip":                "Lower Limb",
    "ankle":              "Lower Limb",
    "foot":               "Lower Limb",
    "legs":               "Lower Limb",
    "shoulder":           "Upper Limb",
    "shoulder / scapula": "Upper Limb",
    "shoulders":          "Upper Limb",
    "elbow":              "Upper Limb",
    "wrist":              "Upper Limb",
    "hand":               "Upper Limb",
    "lower back":         "Spine",
    "thoracic":           "Spine",
    "cervical":           "Spine",
    "core":               "Core",
    "shoulders , abs":    "Upper Limb / Core",
    "shoulders / core":   "Upper Limb / Core",
}

AREA_NORMALIZE = {
    "shoulders":          "Shoulder",
    "shoulder / scapula": "Shoulder",
    "shoulders , abs":    "Shoulder",
    "shoulders / core":   "Shoulder",
    "legs":               "Knee",
}

def get_region(area):
    return REGION_MAP.get(str(area).strip().lower(), "General")

def normalize_area(area):
    return AREA_NORMALIZE.get(str(area).strip().lower(), str(area).strip())

@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    search_paths = [
        os.path.join(base, "data", "exercises.csv"),
        os.path.join(base, "exercises.csv"),
        os.path.join(base, "data", "Exercises.csv"),
    ]
    for path in search_paths:
        if not os.path.exists(path):
            continue
        for enc in ["utf-8-sig", "utf-8", "windows-1255", "cp1255"]:
            try:
                df = pd.read_csv(path, encoding=enc)
                df.columns = df.columns.str.strip()
                df = df.fillna("")
                df["Type_EN"] = df["Type_EN"].str.strip().str.replace(
                    "stabillity", "stability", case=False, regex=False
                )
                df["Body_Area_EN"]   = df["Body_Area_EN"].apply(normalize_area)
                df["Body_Region_EN"] = df["Body_Area_EN"].apply(get_region)
                return df, None
            except UnicodeDecodeError:
                continue
            except Exception as e:
                return None, str(e)
    return None, "לא נמצא קובץ exercises.csv"

df, error = load_data()
if df is None or error:
    st.error(f"שגיאה בטעינת הנתונים: {error}")
    st.stop()

COL_NAME   = "Exercise_Name_EN"
COL_AREA   = "Body_Area_EN"
COL_REGION = "Body_Region_EN"
COL_TYPE   = "Type_EN"
COL_DIFF   = "Difficulty"
COL_EQUIP  = "Equipment_EN"
COL_INST   = "Instructions_EN"
COL_TIPS   = "Clinical_Tips_EN"
COL_YT     = "YouTube_Link"
COL_RPE    = "Default_RPE"

missing = [c for c in [COL_NAME, COL_AREA, COL_TYPE] if c not in df.columns]
if missing:
    st.error(f"עמודות חסרות: {missing}")
    st.stop()

today = date.today().strftime("%d.%m.%Y")
st.markdown(
    f'<div class="main-header">'
    f'<div style="font-size:1.3rem;font-weight:bold">נדב רונן | פיזיותרפיה</div>'
    f'<div style="font-size:0.85rem;opacity:0.85;margin-top:4px">{today}</div>'
    f'</div>',
    unsafe_allow_html=True
)

patient_name = st.text_input("שם המטופל", placeholder="לדוגמה: יוסי כהן")
phone        = st.text_input("טלפון", placeholder="972501234567")
st.markdown('<hr class="divider">', unsafe_allow_html=True)

rtl("בחירת תרגיל", tag="h4", color="#2E86AB")

regions = sorted([r for r in df[COL_REGION].unique() if r != ""])
selected_region = st.selectbox("אזור כללי", ["הכל"] + regions)

filtered = df.copy()
if selected_region != "הכל":
    filtered = filtered[filtered[COL_REGION] == selected_region]

areas = sorted([a for a in filtered[COL_AREA].unique() if a != ""])
selected_area = st.selectbox("אזור ספציפי", ["הכל"] + areas)
if selected_area != "הכל":
    filtered = filtered[filtered[COL_AREA] == selected_area]

types = sorted([t for t in filtered[COL_TYPE].unique() if t != ""])
selected_type = st.selectbox("סוג תרגיל", ["הכל"] + types)
if selected_type != "הכל":
    filtered = filtered[filtered[COL_TYPE] == selected_type]

if filtered.empty:
    st.warning("אין תרגילים בסינון זה.")
    st.stop()

exercise_list = sorted(filtered[COL_NAME].tolist())
selected = st.selectbox("בחר תרגיל", exercise_list)
row = filtered[filtered[COL_NAME] == selected].iloc[0]

diff  = str(row[COL_DIFF]) if row[COL_DIFF] != "" else "-"
equip = row[COL_EQUIP]     if row[COL_EQUIP] != "" else "ללא ציוד"
yt    = str(row.get(COL_YT, "")).strip()
inst  = str(row.get(COL_INST, "")).strip()
tips  = str(row.get(COL_TIPS, "")).strip()

st.markdown(
    f'<div class="ex-card">'
    f'<div style="font-size:1.05rem;font-weight:bold;margin-bottom:8px">'
    f'{selected} '
    f'<span class="region-tag">{row[COL_REGION]}</span>'
    f'<span class="tag">קושי {diff}/4</span>'
    f'<span class="tag">{equip}</span>'
    f'</div>',
    unsafe_allow_html=True
)
if inst:
    st.markdown(
        f'<span style="direction:rtl;color:#555;font-size:0.88rem">הוראות:</span>'
        f'<span class="en-text">{inst}</span>',
        unsafe_allow_html=True
    )
if tips:
    st.markdown(
        f'<span style="direction:rtl;color:#1a6b3a;font-size:0.88rem">טיפ קליני:</span>'
        f'<span class="en-text-green">{tips}</span>',
        unsafe_allow_html=True
    )
if yt:
    st.markdown(
        f'<a href="{yt}" target="_blank" style="color:#2E86AB;font-weight:bold;'
        f'text-decoration:none;display:block;margin-top:6px">סרטון הדגמה ב-YouTube</a>',
        unsafe_allow_html=True
    )
else:
    rtl("אין סרטון לתרגיל זה", color="#aaa", size="0.85rem")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
rtl("מינון", tag="h4", color="#2E86AB")

col1, col2, col3 = st.columns(3)
with col1: sets = st.number_input("סטים",         min_value=1, max_value=10,  value=3)
with col2: reps = st.number_input("חזרות",        min_value=1, max_value=60,  value=10)
with col3: hold = st.number_input("שמירה (שנ')", min_value=0, max_value=120, value=0)

try:
    default_rpe = int(float(row[COL_RPE])) if str(row[COL_RPE]).strip() not in ["", "nan"] else 5
except:
    default_rpe = 5

rtl("רמת מאמץ - RPE (1 = קל מאוד, 10 = מקסימום)")
rpe = st.slider("RPE", 1, 10, default_rpe, label_visibility="collapsed")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
rtl("רמת כאב - VAS", tag="h4", color="#2E86AB")
rtl("0 = ללא כאב | 10 = כאב קיצוני", color="#888", size="0.85rem")
vas = st.slider("VAS", 0, 10, 0, label_visibility="collapsed")
tl_color, tl_label, tl_msg = traffic_light(vas)
st.markdown(
    f'<div class="info-box" style="background:{tl_color}">'
    f'<strong>{tl_label}</strong><br>'
    f'<span style="font-size:0.9rem">{tl_msg}</span>'
    f'</div>',
    unsafe_allow_html=True
)

st.markdown('<hr class="divider">', unsafe_allow_html=True)
rtl("ניהול עומס", tag="h4", color="#2E86AB")

col1, col2 = st.columns(2)
with col1: duration    = st.number_input("משך אימון (דקות)", min_value=5, max_value=120, value=30)
with col2: sessions_pw = st.number_input("פעמים בשבוע",      min_value=1, max_value=7,   value=3)

session_load = rpe * duration
weekly_load  = session_load * sessions_pw
lc, ll = load_label(session_load)

col1, col2 = st.columns(2)
with col1:
    st.markdown(
        f'<div class="load-box" style="background:{lc}">'
        f'עומס יחידה<br><strong>{session_load} AU</strong></div>',
        unsafe_allow_html=True
    )
with col2:
    st.markdown(
        f'<div class="load-box" style="background:#2E86AB">'
        f'עומס שבועי<br><strong>{weekly_load} AU</strong></div>',
        unsafe_allow_html=True
    )
rtl(ll, color=lc, size="0.88rem")

st.markdown('<hr class="divider">', unsafe_allow_html=True)
if st.button("הוסף תרגיל לתוכנית", type="primary"):
    if len(st.session_state.exercise_cart) >= 8:
        st.warning("מקסימום 8 תרגילים בתוכנית אחת.")
    else:
        st.session_state.exercise_cart[selected] = {
            "שם": selected, "אזור": row[COL_AREA], "region": row[COL_REGION],
            "סוג": row[COL_TYPE], "סטים": sets, "חזרות": reps, "שמירה": hold,
            "RPE": rpe, "VAS": vas, "עומס": session_load,
            "yt": yt, "הוראות": inst, "טיפ": tips,
        }
        st.success(f"{selected} נוסף לתוכנית")

if st.session_state.exercise_cart:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    n          = len(st.session_state.exercise_cart)
    total_load = sum(d["עומס"] for d in st.session_state.exercise_cart.values())
    rtl(f"התוכנית - {n} תרגילים | עומס כולל: {total_load} AU", tag="h4", color="#2E86AB")

    for i, (name, d) in enumerate(st.session_state.exercise_cart.items(), 1):
        hold_str = f" | שמירה {d['שמירה']} שנ'" if d["שמירה"] > 0 else ""
        yt_link  = (
            f' | <a href="{d["yt"]}" target="_blank" style="color:#2E86AB">סרטון</a>'
            if d["yt"] else ""
        )
        st.markdown(
            f'<div class="cart-item">'
            f'<strong>{i}. {d["שם"]}</strong> '
            f'<span class="region-tag">{d["region"]}</span>'
            f'<span class="tag">{d["אזור"]}</span><br>'
            f'{d["סטים"]} סטים x {d["חזרות"]} חזרות{hold_str} | RPE: {d["RPE"]}'
            f'{yt_link}</div>',
            unsafe_allow_html=True
        )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    rtl("שליחה לוואטסאפ", tag="h4", color="#2E86AB")
    include_inst = st.checkbox("כלול הוראות ביצוע", value=False)

    if st.button("שלח תוכנית לוואטסאפ", type="primary"):
        if not patient_name or not phone:
            st.warning("נא למלא שם מטופל ומספר טלפון בראש הדף")
        else:
            lines = [f"שלום {patient_name},", f"תאריך: {today}", "", "התוכנית שלך:", ""]
            for i, (name, d) in enumerate(st.session_state.exercise_cart.items(), 1):
                hold_str = f", שמירה {åd['שמירה']} שנ'" if d["שמירה"] > 0 else ""
                lines.append(f"{i}. {d['שם']} ({d['אזור']})")
                lines.append(f"   {d['סטים']} סטים x {d['חזרות']} חזרות{hold_str} | RPE: {d['RPE']}")
                if include_inst and d["הוראות"]:
                    lines.append(f"   {d['הוראות']}")
                if d["yt"]:
                    lines.append(f"   {d['yt']}")
                lines.append("")
            lines += [
                "--- הנחיות כאב ---",
                "ירוק (VAS 0-3): המשך כרגיל",
                "כתום (VAS 4-6): הפחת חזרות ב-50%",
                "אדום (VAS 7+): עצור ופנה אלי",
                "",
                "--- צ'קליסט שבועי ---",
                "לאחר כל אימון שלח לי:",
            ]
            for i, (name, d) in enumerate(st.session_state.exercise_cart.items(), 1):
                lines.append(f"{i}. {d['שם']} - בוצע? כן / לא | כאב (0-10):")
            lines += ["", "בהצלחה!", "נדב רונן | פיזיותרפיה"]

            msg = "\n".join(lines)
            url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
            st.markdown(
                f'<a href="{url}" target="_blank">'
                f'<button style="background:#25D366;color:white;padding:14px;'
                f'border:none;border-radius:10px;width:100%;font-size:1.05rem;'
                f'font-weight:bold;cursor:pointer;margin-top:8px">'
                f'פתח בוואטסאפ</button></a>',
                unsafe_allow_html=True
            )

    if st.button("נקה תוכנית"):
        st.session_state.exercise_cart = {}
        st.rerun()

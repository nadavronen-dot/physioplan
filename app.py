import streamlit as st
import pandas as pd
import os
import base64
import urllib.parse
from datetime import date

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="נדב רונן פיזיותרפיה", layout="centered")

# ── Logo helper ───────────────────────────────────────────────────────────────
def get_logo_b64():
    base = os.path.dirname(os.path.abspath(__file__))
    for name in ["logo.jpg", "logo.png", "logo.jpeg"]:
        path = os.path.join(base, name)
        if os.path.exists(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
    return None

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --green-dark:  #1a5c2e;
    --green-mid:   #2d8a4e;
    --green-light: #e8f5ec;
    --green-wa:    #25D366;
    --border:      #e0e0e0;
}

.stApp { background-color: #f4f6f4; }
header[data-testid="stHeader"] { display: none !important; }

.app-header {
    background: linear-gradient(135deg, var(--green-dark) 0%, var(--green-mid) 100%);
    border-radius: 14px;
    padding: 20px 28px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 16px rgba(26,92,46,0.18);
}
.app-header img {
    height: 72px;
    width: 72px;
    object-fit: contain;
    border-radius: 10px;
    background: white;
    padding: 5px;
}
.app-header-text { flex: 1; text-align: center; }
.app-header-text h1 {
    color: white;
    font-size: 1.7rem;
    font-weight: 800;
    margin: 0 0 2px 0;
}
.app-header-text p {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    margin: 0;
}
.app-header-date {
    color: rgba(255,255,255,0.7);
    font-size: 0.8rem;
    margin-top: 6px;
}

div[data-testid="stSelectbox"] label {
    direction: rtl !important;
    text-align: center !important;
    color: var(--green-dark) !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    display: block;
    width: 100%;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
    direction: rtl !important;
    text-align: center !important;
    font-weight: 600 !important;
    display: block;
    width: 100%;
}

.section-title {
    direction: rtl;
    text-align: center;
    color: var(--green-dark);
    font-weight: 700;
    font-size: 1rem;
    margin: 18px 0 6px 0;
    padding-bottom: 4px;
    border-bottom: 2px solid var(--green-light);
}

.ex-card {
    background: #f8f9fa;
    border-radius: 12px;
    padding: 16px 20px;
    border-left: 4px solid var(--green-mid);
    margin: 14px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.ex-card h3 {
    color: var(--green-dark);
    font-size: 1.1rem;
    margin: 0 0 10px 0;
}

.tag {
    display: inline-block;
    background: var(--green-dark);
    color: white;
    border-radius: 20px;
    padding: 2px 11px;
    font-size: 0.78rem;
    margin: 2px 3px 2px 0;
    font-weight: 600;
}
.tag-gray {
    display: inline-block;
    background: #6c757d;
    color: white;
    border-radius: 20px;
    padding: 2px 11px;
    font-size: 0.78rem;
    margin: 2px 3px 2px 0;
}
.tag-outline {
    display: inline-block;
    border: 1.5px solid var(--green-mid);
    color: var(--green-dark);
    border-radius: 20px;
    padding: 2px 11px;
    font-size: 0.78rem;
    margin: 2px 3px 2px 0;
}

.inst-box {
    background: #f0f4ff;
    border-left: 4px solid #4a6fa5;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #2c3e50;
    direction: ltr;
    text-align: center;
}

.tip-box {
    background: var(--green-light);
    border-left: 4px solid var(--green-mid);
    border-radius: 8px;
    padding: 10px 14px;
    margin: 10px 0;
    color: var(--green-dark);
    font-size: 0.9rem;
}

.status-bar {
    border-radius: 10px;
    padding: 10px 16px;
    direction: rtl;
    text-align: center;
    font-weight: 700;
    margin-bottom: 6px;
    color: white;
}

/* ── Cart item text ── */
.cart-item {
    background: white;
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 8px;
    border: 1px solid var(--border);
    direction: rtl;
    text-align: right;
    color: #1a1a1a;
    font-size: 0.95rem;
    line-height: 1.6;
}
.cart-item strong {
    color: var(--green-dark);
    font-size: 1rem;
}

/* ── Checkbox ── */
div[data-testid="stCheckbox"] label p,
div[data-testid="stCheckbox"] label span,
div[data-testid="stCheckbox"] p {
    color: #1a1a1a !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

.wa-btn {
    display: block;
    background: var(--green-wa);
    color: white !important;
    text-decoration: none !important;
    border-radius: 24px;
    padding: 12px 28px;
    font-size: 1rem;
    font-weight: 700;
    text-align: center;
    box-shadow: 0 3px 10px rgba(37,211,102,0.35);
    margin-top: 8px;
}
.wa-btn:hover { background: #1da851; }

.stButton > button {
    border-radius: 20px !important;
    font-weight: 600 !important;
}

hr { border-color: var(--border); margin: 18px 0; }
/* ── Text input labels ── */
div[data-testid="stTextInput"] label {
    direction: rtl !important;
    text-align: center !important;
    color: #1a5c2e !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    display: block;
    width: 100%;
}

/* ── Remove extra spacing after header ── */
div[data-testid="stMarkdownContainer"] + div[data-testid="stVerticalBlock"] {
    margin-top: 0 !important;
}

/* ── All input labels visible ── */
.stTextInput label, .stSelectbox label,
.stNumberInput label, .stSlider label {
    color: #1a5c2e !important;
    font-weight: 700 !important;
    direction: rtl !important;
    text-align: center !important;
}
/* ── Cursor pointer on selectbox ── */
div[data-testid="stSelectbox"] > div,
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stSelectbox"] input,
div[data-testid="stSelectbox"] [role="listbox"],
div[data-testid="stSelectbox"] [role="option"] {
    cursor: pointer !important;
}
/* ══ RESPONSIVE ══════════════════════════════════════════════ */

/* ── Desktop (מעל 768px) ── */
@media (min-width: 768px) {
    .app-header {
        padding: 24px 36px;
    }
    .app-header img {
        height: 88px;
        width: 88px;
    }
    .app-header-text h1 {
        font-size: 2rem;
    }
    .app-header-text p {
        font-size: 1.05rem;
    }
    .ex-card {
        padding: 20px 28px;
    }
    .stButton > button {
        width: auto !important;
        min-width: 200px;
    }
}

/* ── Mobile (עד 768px) ── */
@media (max-width: 768px) {
    .app-header {
        padding: 14px 16px;
        gap: 12px;
        border-radius: 10px;
    }
    .app-header img {
        height: 52px;
        width: 52px;
    }
    .app-header-text h1 {
        font-size: 1.25rem;
    }
    .app-header-text p {
        font-size: 0.82rem;
    }
    .app-header-date {
        font-size: 0.72rem;
    }
    .ex-card {
        padding: 12px 14px;
        border-radius: 10px;
    }
    .inst-box, .tip-box {
        font-size: 0.85rem;
        padding: 8px 10px;
    }
    .tag, .tag-gray, .tag-outline {
        font-size: 0.72rem;
        padding: 2px 8px;
    }
    .cart-item {
        padding: 8px 12px;
        font-size: 0.9rem;
    }
    .wa-btn {
        padding: 14px 20px;
        font-size: 1.05rem;
    }
    .section-title {
        font-size: 0.95rem;
    }
    .status-bar {
        font-size: 0.92rem;
        padding: 8px 12px;
    }
    /* כפתורים — רוחב מלא במובייל */
    .stButton > button {
        width: 100% !important;
        border-radius: 14px !important;
    }
}
/* ── Checkbox label ── */
div[data-testid="stCheckbox"] label {
    color: #1a1a1a !important;
    font-weight: 600 !important;
}

</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "exercise_cart" not in st.session_state:
    st.session_state.exercise_cart = {}

# ── Helper functions ──────────────────────────────────────────────────────────
def section_title(text):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)

def rtl(text, tag="p", color="#111", size="1rem"):
    st.markdown(
        f'<{tag} style="direction:rtl;text-align:center;color:{color};'
        f'margin:4px 0;font-size:{size}">{text}</{tag}>',
        unsafe_allow_html=True
    )

def safe(row, col, fallback=""):
    if col in row.index:
        val = str(row[col]).strip()
        if val and val.lower() != "nan":
            return val
    return fallback

def traffic_light(vas):
    if vas == 0:
        return "#27AE60", "ירוק - ללא כאב", "המשך את התרגיל לפי המינון שקיבלת."
    if vas <= 3:
        return "#27AE60", "ירוק - כאב קל (תקין)", "כאב קל במהלך שיקום הוא תקין. המשך כרגיל. אם הכאב גדל - עצור."
    if vas <= 6:
        return "#F39C12", "כתום - הפחת עצימות", "הפחת חזרות ב-50% ועבוד בטווח תנועה קטן יותר. אם הכאב לא פוחת תוך 24 שעות - צור קשר."
    return "#E74C3C", "אדום - עצור", "הפסק את התרגיל עכשיו. מנוחה מלאה. אם הכאב נמשך מעל שעה - פנה לטיפול."

def load_label(au):
    if au < 150:
        return "#27AE60", "עומס נמוך - שיקום ראשוני"
    if au < 300:
        return "#F39C12", "עומס בינוני - שלב חיזוק"
    if au < 450:
        return "#E67E22", "עומס גבוה - וודא התאוששות"
    return "#E74C3C", "עומס גבוה מאוד - שקול הפחתה"

# ── Data maps ─────────────────────────────────────────────────────────────────
REGION_MAP = {
    "knee": "Lower Limb", "hip": "Lower Limb", "ankle": "Lower Limb",
    "foot": "Lower Limb", "legs": "Lower Limb",
    "shoulder": "Upper Limb", "shoulder / scapula": "Upper Limb",
    "shoulders": "Upper Limb", "elbow": "Upper Limb",
    "wrist": "Upper Limb", "hand": "Upper Limb",
    "lower back": "Spine", "thoracic": "Spine", "cervical": "Spine",
    "core": "Core",
    "shoulders , abs": "Upper Limb / Core",
    "shoulders / core": "Upper Limb / Core",
}
AREA_NORMALIZE = {
    "shoulders": "Shoulder", "shoulder / scapula": "Shoulder",
    "shoulders , abs": "Shoulder", "shoulders / core": "Shoulder",
    "legs": "Knee",
}

def get_region(area):
    return REGION_MAP.get(str(area).strip().lower(), "General")

def normalize_area(area):
    return AREA_NORMALIZE.get(str(area).strip().lower(), str(area).strip())

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    base = os.path.dirname(os.path.abspath(__file__))
    paths = [
        os.path.join(base, "data", "exercises.csv"),
        os.path.join(base, "exercises.csv"),
        os.path.join(base, "data", "Exercises.csv"),
    ]
    for path in paths:
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

# ── Column names ──────────────────────────────────────────────────────────────
C_NAME    = "Exercise_Name_EN"
C_NAME_HE = "Exercise_Name_HE"
C_AREA    = "Body_Area_EN"
C_REGION  = "Body_Region_EN"
C_TYPE    = "Type_EN"
C_DIFF    = "Difficulty"
C_EQUIP   = "Equipment_EN"
C_INST    = "Instructions_EN"
C_INST_HE = "Instructions_HE"
C_TIPS    = "Clinical_Tips_EN"
C_YT      = "YouTube_Link"
C_RPE     = "Default_RPE"

missing = [c for c in [C_NAME, C_AREA, C_TYPE] if c not in df.columns]
if missing:
    st.error(f"עמודות חסרות: {missing}")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────────
today = date.today().strftime("%d.%m.%Y")
logo_b64 = get_logo_b64()
logo_html = (
    f'<img src="data:image/jpeg;base64,{logo_b64}" alt="logo">'
    if logo_b64
    else '<div style="width:72px;height:72px;background:rgba(255,255,255,0.15);border-radius:10px;"></div>'
)

st.markdown(f"""
<div class="app-header">
    {logo_html}
    <div class="app-header-text">
        <h1>נדב רונן</h1>
        <p>פיזיותרפיה וספורט</p>
        <div class="app-header-date">{today}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Patient info ──────────────────────────────────────────────────────────────
patient_name = st.text_input("שם המטופל", placeholder="לדוגמה: יוסי כהן")
phone        = st.text_input("טלפון", placeholder="972501234567")

st.markdown("---")

# ── Filters — all shown at once ───────────────────────────────────────────────
regions = sorted([r for r in df[C_REGION].unique() if r])
selected_region = st.selectbox("אזור גוף", ["הכל"] + regions)

filtered = df.copy()
if selected_region != "הכל":
    filtered = filtered[filtered[C_REGION] == selected_region]

areas = sorted([a for a in filtered[C_AREA].unique() if a])
selected_area = st.selectbox("אזור ספציפי", ["הכל"] + areas)
if selected_area != "הכל":
    filtered = filtered[filtered[C_AREA] == selected_area]

types = sorted([t for t in filtered[C_TYPE].unique() if t])
selected_type = st.selectbox("סוג תרגיל", ["הכל"] + types)
if selected_type != "הכל":
    filtered = filtered[filtered[C_TYPE] == selected_type]

if filtered.empty:
    st.warning("אין תרגילים בסינון זה.")
    st.stop()

exercise_list = sorted(filtered[C_NAME].tolist())
selected_ex = st.selectbox("תרגיל", exercise_list)
row = filtered[filtered[C_NAME] == selected_ex].iloc[0]

# ── Exercise card ─────────────────────────────────────────────────────────────
st.markdown("---")
name_he  = safe(row, C_NAME_HE)
inst_en  = safe(row, C_INST)
inst_he  = safe(row, C_INST_HE)
tips_en  = safe(row, C_TIPS)
equip_en = safe(row, C_EQUIP)
yt_link  = safe(row, C_YT)
diff     = safe(row, C_DIFF)
rpe_def  = safe(row, C_RPE, "5")

display_name = selected_ex + (f" ({name_he})" if name_he else "")

st.markdown(f"""
<div class="ex-card">
    <h3>{display_name}</h3>
    <span class="tag">{safe(row, C_REGION)}</span>
    <span class="tag-gray">{safe(row, C_AREA)}</span>
    {'<span class="tag-outline">קושי: ' + diff + '</span>' if diff else ''}
    {'<span class="tag-outline">ציוד: ' + equip_en + '</span>' if equip_en else ''}
</div>
""", unsafe_allow_html=True)

if inst_en:
    st.markdown(f'<div class="inst-box">{inst_en}</div>', unsafe_allow_html=True)
if tips_en:
    st.markdown(f'<div class="tip-box"><strong>Clinical Tip:</strong> {tips_en}</div>', unsafe_allow_html=True)
if yt_link:
    st.markdown(f'[הדגמה ב-YouTube]({yt_link})')

# ── Dosage ────────────────────────────────────────────────────────────────────
st.markdown("---")
section_title("מינון")
default_rpe = int(float(rpe_def)) if rpe_def else 5
c1, c2, c3 = st.columns(3)
with c1: sets = st.number_input("סטים", 1, 10, 3)
with c2: reps = st.number_input("חזרות", 1, 60, 10)
with c3: hold = st.number_input("שמירה (שנ')", 0, 120, 0)
rpe = st.slider("רמת מאמץ - RPE", 1, 10, default_rpe)

# ── VAS ───────────────────────────────────────────────────────────────────────
st.markdown("---")
vas = st.slider("רמת כאב - VAS", 0, 10, 0)
tl_color, tl_label, tl_msg = traffic_light(vas)
st.markdown(f'<div class="status-bar" style="background:{tl_color};">{tl_label}</div>', unsafe_allow_html=True)
rtl(tl_msg, color="#444")

# ── Load management ───────────────────────────────────────────────────────────
st.markdown("---")
section_title("Load Management (Foster)")
c1, c2 = st.columns(2)
with c1: duration    = st.number_input("משך אימון (דקות)", 5, 120, 30)
with c2: sessions_pw = st.number_input("פעמים בשבוע", 1, 7, 3)

session_au = rpe * duration
weekly_au  = session_au * sessions_pw
lm_color, lm_label = load_label(session_au)

ca, cb = st.columns(2)
with ca:
    st.markdown(f'<div class="status-bar" style="background:{lm_color};">עומס יחידה: {session_au} AU<br><small>{lm_label}</small></div>', unsafe_allow_html=True)
with cb:
    st.markdown(f'<div class="status-bar" style="background:#2E86AB;">עומס שבועי: {weekly_au} AU</div>', unsafe_allow_html=True)

# ── Add to cart ───────────────────────────────────────────────────────────────
st.markdown("---")
if st.button("הוסף לתוכנית", use_container_width=True):
    if len(st.session_state.exercise_cart) >= 8:
        st.warning("מקסימום 8 תרגילים בתוכנית.")
    else:
        st.session_state.exercise_cart[selected_ex] = {
            "name_he":  name_he,
            "area":     safe(row, C_AREA),
            "region":   safe(row, C_REGION),
            "sets":     sets,
            "reps":     reps,
            "hold":     hold,
            "rpe":      rpe,
            "vas":      vas,
            "inst_he":  inst_he or inst_en,
            "yt":       yt_link,
            "au":       session_au,
        }
        st.success(f"{selected_ex} נוסף לתוכנית!")

# ── Cart ──────────────────────────────────────────────────────────────────────
cart = st.session_state.exercise_cart
if cart:
    st.markdown("---")
    total_au = sum(d["au"] for d in cart.values())
    section_title(f"תוכנית — {len(cart)} תרגילים | עומס כולל: {total_au} AU")

    for i, (ex_name, d) in enumerate(cart.items(), 1):
        he       = d.get("name_he", "")
        label    = ex_name + (f" ({he})" if he else "")
        hold_str = f", שמירה {d['hold']} שנ'" if d["hold"] > 0 else ""
        st.markdown(
            f'<div class="cart-item">'
            f'<strong>{i}. {label}</strong><br>'
            f'{d["sets"]} סטים x {d["reps"]} חזרות{hold_str} | RPE {d["rpe"]} | VAS {d["vas"]}'
            f'</div>',
            unsafe_allow_html=True
        )

    include_inst = st.checkbox("כלול הוראות ביצוע בהודעה", value=False)

    # בניית הודעת וואטסאפ
    lines = [f"*תוכנית תרגילים — {today}*", "_נדב רונן, פיזיותרפיה וספורט_", ""]
    if patient_name:
        lines.insert(0, f"שלום {patient_name},")

    for i, (ex_name, d) in enumerate(cart.items(), 1):
        he = d.get("name_he") or ex_name
        hold_str = f", שמירה {d['hold']} שנ'" if d["hold"] > 0 else ""
        lines.append(f"*{i}. {he}*")
        lines.append(f"   {d['sets']} סטים x {d['reps']} חזרות{hold_str} | RPE {d['rpe']}")
        if include_inst and d.get("inst_he"):
            lines.append(f"   {d['inst_he']}")
        if d.get("yt"):
            lines.append(f"   {d['yt']}")
        lines.append("")

    lines += [
        "━━━━━━━━━━━━━━",
        "*הנחיות כאב:*",
        "ירוק (0-3): המשך כרגיל",
        "כתום (4-6): הפחת חזרות ב-50%",
        "אדום (7+): עצור ופנה אלי",
        "",
        "━━━━━━━━━━━━━━",
        "*צ'קליסט שבועי:*",
        "יום א׳ [ ]  יום ג׳ [ ]  יום ה׳ [ ]",
        "",
        "_בהצלחה! נדב_"
    ]

    # כפתור נקה תוכנית
    col_clear, _ = st.columns([1, 2])
    with col_clear:
        if st.button("נקה תוכנית", use_container_width=True):
            st.session_state.exercise_cart = {}
            st.rerun()

    # כפתור וואטסאפ — שורה נפרדת ורוחב מלא
    msg = "\n".join(lines)
    encoded = urllib.parse.quote(msg)
    phone_clean = phone.strip() if phone else ""
    wa_url = f"https://wa.me/{phone_clean}?text={encoded}" if phone_clean else f"https://wa.me/?text={encoded}"
    st.markdown(
        f'<a href="{wa_url}" target="_blank" class="wa-btn">שלח בוואטסאפ</a>',
        unsafe_allow_html=True
    )

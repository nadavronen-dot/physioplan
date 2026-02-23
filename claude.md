# CLAUDE.md — PhysioPlan Coding Conventions

## Project
PhysioPlan — כלי HEP לפיזיותרפיסט. Streamlit + CSV. ללא DB, ללא login.
Owner: נדב רונן | פיזיותרפיה וספורט

## Project Structure
- `app.py` — Main entry point (single file)
- `data/exercises.csv` — מקור הנתונים
- `requirements.txt` — streamlit, pandas, openpyxl, deep-translator
- `.claude/PRD.md` — מסמך דרישות מלא

## Commands
- Run: `streamlit run app.py`
- Install: `pip install -r requirements.txt`
- CSV translate: `python3 translate_csv.py`

## Coding Rules
- Python 3.13, PEP 8
- Streamlit: `st.session_state` לשמירת בחירות בין re-runs
- `@st.cache_data` על load_data()
- Layout: `layout="centered"`, max-width 520px
- RTL: כל ה-CSS ברמת html/body
- LTR: class="en-text" / class="en-text-green" לטקסט אנגלי

## Language Rules (חשוב!)
| מיקום | שפה | יישור |
|---|---|---|
| ממשק כללי | עברית | RTL |
| הוראות + טיפ קליני (אפליקציה) | אנגלית _EN | LTR |
| הודעת וואטסאפ | עברית _HE, fallback → EN | RTL |

## CSV Column Names (exact)
Exercise_Name_EN, Exercise_Name_HE,
Body_Area_EN, Body_Area_HE,
Type_EN, Type_HE,
Difficulty, Equipment_EN, Equipment_HE,
Instructions_EN, Instructions_HE,
Clinical_Tips_EN, Clinical_Tips_HE,
YouTube_Link, Default_RPE

## Error Handling
- CSV לא נמצא → st.error() + st.stop()
- סינון ריק → st.warning() + st.stop()
- encoding fallback: utf-8-sig → utf-8 → windows-1255 → cp1255
## v1.3 — Design Update (23.02.2026)

### שינויים שבוצעו:
- Header: גרדיאנט ירוק + לוגו אוטומטי מ-logo.jpg
- CSS גלובלי: צבעי מותג ירוק, כרטיסי תרגיל עם shadow
- Responsive design: @media queries למובייל ודסקטופ
- Selectbox labels: RTL, מרכז, ירוק כהה
- Cursor pointer על selectbox
- Cart: מחיקת תרגיל בודד עם כפתור ✕
- כפתור וואטסאפ: שורה נפרדת, רוחב מלא
- Checkbox label: צבע נראה
- Cart item: טקסט כהה על רקע לבן, RTL
- אפס אימוג'ים בממשק

# PRD — PhysioPlan | נדב רונן פיזיותרפיה וספורט
**Version:** 1.2 | **Date:** 23.02.2026 | **Status:** Active

---

## 1. Executive Summary

כלי Prescription קליני לפיזיותרפיסט לבניית תוכנית תרגילים ביתית (HEP) ושליחתה למטופל בוואטסאפ תוך 3 דקות.
רץ על Streamlit Cloud, מחובר ל-GitHub, ללא צורך ב-login או DB.
ממשק דו-שפתי: עברית ראשית למטופל, אנגלית שניונית לפיזיותרפיסט.

---

## 2. Target Users

| משתמש | תפקיד |
|---|---|
| נדב רונן (PRIMARY) | פיזיותרפיסט — בונה ושולח תוכנית מהטלפון בקליניקה |
| המטופל (SECONDARY) | מקבל הודעת וואטסאפ בעברית — לא נכנס לאפליקציה |

---

## 3. Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.13 |
| UI | Streamlit (layout="centered") |
| Data | pandas + exercises.csv |
| Hosting | Streamlit Community Cloud |
| Messaging | WhatsApp wa.me deep link |
| Translation | deep-translator (GoogleTranslator, target='iw') |

---

## 4. Data Schema — exercises.csv

### עמודות קיימות (v1.2)

| עמודה | תיאור | דוגמה |
|---|---|---|
| Exercise_Name_EN | שם תרגיל — מזהה ראשי (LTR) | Wall Sit |
| Exercise_Name_HE | שם תרגיל בעברית — מוצג למטופל | ישיבת קיר |
| Body_Area_EN | אזור גוף (LTR) | Knee |
| Body_Area_HE | אזור גוף בעברית | ברך |
| Type_EN | סוג תרגיל (LTR) | strength |
| Type_HE | סוג תרגיל בעברית | כוח |
| Difficulty | קושי 1-4 | 2 |
| Equipment_EN | ציוד (LTR) | Wall |
| Equipment_HE | ציוד בעברית | קיר |
| Instructions_EN | הוראות ביצוע (LTR) — לפיזיותרפיסט | Lean against wall... |
| Instructions_HE | הוראות בעברית — למטופל | הישען על הקיר... |
| Clinical_Tips_EN | טיפ קליני (LTR) — לפיזיותרפיסט | Keep knees at 90 deg |
| Clinical_Tips_HE | טיפ קליני בעברית | שמור על ברכיים ב-90° |
| YouTube_Link | לינק הדגמה | https://youtu.be/... |
| Default_RPE | RPE ברירת מחדל | 3 |

### עמודות מחושבות (runtime, לא ב-CSV)

| עמודה | תיאור | לוגיקה |
|---|---|---|
| Body_Region_EN | אזור כללי | REGION_MAP dict בקוד |

---

## 5. כללי שפה ויישור (Language Rules)

| מיקום | שפה | יישור |
|---|---|---|
| ממשק כללי (כותרות, כפתורים, תוויות) | עברית | RTL — ימין |
| שם תרגיל באפליקציה | אנגלית ראשית + עברית בסוגריים | LTR |
| הוראות + טיפ קליני באפליקציה | אנגלית (EN) | LTR — שמאל |
| תגיות Body_Region / Body_Area | אנגלית | LTR |
| הודעת וואטסאפ — שם תרגיל | עברית (_HE) אם קיים, אחרת אנגלית | RTL |
| הודעת וואטסאפ — הוראות | עברית (_HE) אם קיים | RTL |
| הודעת וואטסאפ — כל השאר | עברית | RTL |

---

## 6. MVP Features (v1.2)

**F1 — טעינת נתונים יציבה**
- חיפוש CSV בנתיבים: root/ ו-data/
- ניסיון ב-4 encodings: utf-8-sig, utf-8, windows-1255, cp1255
- נרמול Body_Area_EN (shoulders→Shoulder, legs→Knee)
- מיפוי אוטומטי Body_Region_EN מ-REGION_MAP

**F2 — סינון היררכי (3 שלבים)**
- שלב 1: Body_Region_EN — Lower Limb / Upper Limb / Spine / Core / General
- שלב 2: Body_Area_EN — Knee / Hip / Shoulder...
- שלב 3: Type_EN — strength / mobility / stability...
- שלב 4: בחירת תרגיל

**F3 — כרטיס תרגיל**
- שם EN + שם HE בסוגריים
- תגיות: Body_Region (כחול), קושי, ציוד
- הוראות EN — LTR שמאל
- טיפ קליני EN — LTR שמאל, ירוק
- לינק YouTube אם קיים

**F4 — מינון:** סטים / חזרות / שמירה / RPE (ברירת מחדל מ-CSV)

**F5 — VAS + רמזור:** ירוק (0-3) / כתום (4-6) / אדום (7+)

**F6 — Load Management:** Foster Method — RPE × דקות = AU

**F7 — סל תרגילים:** הוספה + תצוגה + ניקוי (עד 8 תרגילים)

**F8 — כותרת ראשית (Header)**
- שם: נדב רונן
- תת-כותרת: פיזיותרפיה וספורט
- תאריך שוטף
- גרדיאנט כחול

**F9 — וואטסאפ**
- שם תרגיל: Exercise_Name_HE (fallback → EN)
- הוראות: Instructions_HE (fallback → EN)
- הנחיות כאב בעברית
- צ'קליסט שבועי בעברית

---

## 7. Out of Scope (v1.2)

- Google Sheets / API / Secrets
- היסטוריית מטופלים
- Authentication
- מצלמה / חיישנים
- כניסת מטופל לאפליקציה

---

## 8. Roadmap

| גרסה | פיצ'ר | סטטוס |
|---|---|---|
| v1.0 | MVP — Prescription Tool | ✅ הושלם |
| v1.1 | Body_Region_EN — סינון היררכי | ✅ הושלם |
| v1.2 | תרגום עברית + כללי שפה/יישור | **בפיתוח** |
| v1.3 | שיפור Header + עיצוב | מתוכנן |
| v2.0 | Google Sheets — עריכת תרגילים בענן | עתידי |
| v3.0 | היסטוריית מטופלים | עתידי |

---

## 9. File Structure

```
/Users/nadavronen/Documents/app/
├── app.py
├── requirements.txt
├── CLAUDE.md
├── data/
│   └── exercises.csv
└── .claude/
    └── PRD.md
```

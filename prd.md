{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;}
{\colortbl;\red255\green255\blue255;\red36\green36\blue36;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c18824\c18824\c18824;\cssrgb\c100000\c100000\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # Product Requirements Document (PRD) - PhysioPlan\
\
## 1. Executive Summary\
A simple Streamlit web application for Physical Therapists to quickly create personalized exercise plans from an existing CSV database and share them with patients via WhatsApp.\
\
## 2. Target Users\
Physical Therapists (PTs) who need an efficient way to assign homework exercises.\
\
## 3. Tech Stack\
- **Language:** Python 3.10+\
- **Frontend/UI:** Streamlit\
- **Data:** CSV file processing (Pandas)\
- **Deployment:** Local or Streamlit Cloud\
\
## 4. MVP Scope (Features)\
1. **Data Loading:**\
   - Load `data/exercises.csv`.\
   - Relevant Columns: `Exercise_Name`, `Body_Area`, `Difficulty`, `Equipment`, `YouTube_Link`, `Instructions`.\
2. **Filtering (Sidebar):**\
   - Filter by `Body_Area` (multiselect).\
   - Filter by `Difficulty` (1-4).\
   - Filter by `Equipment` (multiselect).\
3. **Selection Interface:**\
   - Display filtered exercises in a table or list.\
   - Allow users to select multiple exercises via checkboxes.\
4. **WhatsApp Export:**\
   - Generate a "Share to WhatsApp" link.\
   - Message format: A list of selected exercise names + their YouTube links + Instructions.\
}
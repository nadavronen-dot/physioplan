{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fmodern\fcharset0 Courier;\f1\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red36\green36\blue36;\red255\green255\blue255;}
{\*\expandedcolortbl;;\cssrgb\c18824\c18824\c18824;\cssrgb\c100000\c100000\c100000;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 # CLAUDE.md - Coding Conventions\
\
## Project Structure\
- `app.py`: Main entry point.\
- `data/`: Contains `exercises.csv`.\
- `utils/`: Helper functions.\
- `requirements.txt`: Dependencies.\
\
## Coding Style\
- **Python:** Follow PEP 8.\
- **Streamlit:** Use `st.session_state` to keep selections between re-runs.\
- **Data Handling:** Ensure column names match the CSV exactly (e.g., `Body_Area`, `YouTube_Link`).\
- **Error Handling:** Handle case where CSV is missing or filters return empty results.\
\
## Commands\
- Run: `streamlit run app.py`\
- Install: `pip install -r requirements.txt`\
\pard\pardeftab720\partightenfactor0

\f1 \cf2 \
}
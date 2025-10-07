import streamlit as st
import datetime as dt
import os
import io

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="My Notes App", page_icon="📝", layout="centered")

# ---------- CSS STYLING ----------
st.markdown("""
    <style>
    .stApp {
        background-color: #8C92AC;
    }

    .title {
        text-align: center;
        color: black;
    }

    .note-card {
        background-color: #fff;
        padding: 10px;
        border-radius: 8px;
        box-shadow: 1px 1px 6px rgba(0,0,0,0.15);
        margin-bottom: 10px;
        transition : all 0.2s ease;
    }

    .stTextArea textarea {
        border: 2px solid #2E4053 !important;
        border-radius: 8px !important;
        background-color: #FDFEFE !important;
        color: #17202A !important;
        font-size: 16px !important;
        padding: 8px !important;
    }

    .stTextArea textarea:focus {
        border-color: #3498DB !important;
        box-shadow: 0 0 6px #85C1E9 !important;
        outline: none !important;
        background-color : #ADD8E6 !important;
    }

    div.stButton > button:hover {
        background-color: #ADD8E6;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# ---------- FILE ----------
NOTES_FILE = "notes.txt"

# ---------- COMPATIBILITY RERUN HANDLER ----------
if hasattr(st, "rerun"):
    rerun = st.rerun
else:
    rerun = st.experimental_rerun

# ---------- HELPER FUNCTIONS ----------
def load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for n in notes:
            f.write(n + "\n")

def add_note(content, category, pinned):
    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {category} | {'Pinned' if pinned else 'Unpinned'} | {content}\n")

# ---------- HEADER ----------
st.markdown('<h1 class="title">📝 MY NOTES APP</h1>', unsafe_allow_html=True)

# ---------- INPUT AREA ----------
category = st.selectbox("🏷️ Choose a Category", ["Personal", "Work", "Study", "Ideas", "Other"])
new_note = st.text_area("ENTER THE NOTE HERE:")
pinned = st.checkbox("⭐ Pin this note to top")


col1, col2, col3 = st.columns([2, 2, 1])
with col2:
    if st.button("➕ Add Note"):
        if new_note.strip():
            add_note(new_note.strip(), category, pinned)
            st.success("NOTE ADDED!!")
            st.session_state["new_note"] = ""
            rerun()
        else:
            st.warning("PLEASE ENTER SOMETHING!!")

st.markdown("---")

# ---------- DOWNLOAD BUTTON ----------

notes = load_notes()
if notes:
    all_notes_text = "\n".join(notes)
    st.download_button("💾 Download All Notes", all_notes_text, file_name="my_notes.txt")
else:
    st.info("No notes to download yet.")

st.markdown("---")

# ---------- SEARCH AND DISPLAY ----------

st.subheader("📄 Saved Notes:")
search = st.text_input("🔍 Search notes:")
filtered = [n for n in notes if search.lower() in n.lower()] if search else notes

if filtered:

    # Show pinned notes first
    
    pinned_notes = [n for n in filtered if "Pinned" in n]
    unpinned_notes = [n for n in filtered if "Unpinned" in n]
    display_notes = pinned_notes + unpinned_notes

    for i, note in enumerate(display_notes, start=1):
        if " | " in note:
         try:
            timestamp, category, status, content = note.split(" | ", 3)
         except ValueError:
            continue  # Skip malformed lines
        else:
             if "." in note :
                 timestamp,content = note.split("." , 1)
                 category , status = "General" , "Unpinned"
             else:
                 timestamp,category,status,content="","General","Unpinned",note

        st.markdown(
            f"""
            <div class="note-card">
                <b>#{i}</b> — <b>{timestamp}</b> <span style='color:gray;'>[{category}]</span><br>
                {'⭐' if status == 'Pinned' else ''} {content}
            </div>
            """,
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Delete", key=f"del_{i}"):
                notes.remove(note)
                save_notes(notes)
                st.warning("Note deleted.")
                rerun()
else:
    st.info("🕮 No Notes Yet !!")

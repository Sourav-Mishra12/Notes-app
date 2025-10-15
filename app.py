import streamlit as st
import datetime as dt
import os
import uuid
import html

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="My Notes App", page_icon="📝", layout="centered")

# ---------- SIDEBAR NAVIGATION ----------
st.sidebar.title("🗂️ Notes App Menu")
menu = st.sidebar.radio(
    "Go to:",
    ["➕ Add Note", "📄 View Notes", "🔍 Search Notes"],
)

# ---------- CSS STYLING ----------
st.markdown("""
<style>
.stApp{
    background-color: #8C92AC;
    height: 100% !important;
    min-height: 100vh !important;
}

.title {
    text-align: center;
    color: black;
    font-weight: 700;
}

.note-card {
    background-color: #fff;
    padding: 12px;
    border-radius: 8px;
    box-shadow: 1px 1px 6px rgba(0,0,0,0.15);
    margin-bottom: 10px;
    transition: all 0.2s ease;
}
.note-card:hover {
    transform: scale(1.01);
    box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
}
.category-tag {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 8px;
    color: white;
    font-size: 0.8em;
}
.Work { background-color: #3498db; }
.Personal { background-color: #2ecc71; }
.Study { background-color: #f1c40f; }
.Ideas { background-color: #9b59b6; }
.Other { background-color: #95a5a6; }

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
    background-color: #EAF2F8 !important;
}

div.stButton > button:hover {
    background-color: #ADD8E6;
    transform: scale(1.05);
}
</style>
""", unsafe_allow_html=True)

# ---------- FILE ----------
NOTES_FILE = "notes.txt"

# ---------- RERUN HANDLER ----------
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
    note_id = str(uuid.uuid4())
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(f"{note_id} | {timestamp} | {category} | {'Pinned' if pinned else 'Unpinned'} | {content}\n")

# ---------- SESSION STATE ----------
if "edit_id" not in st.session_state:
    st.session_state["edit_id"] = None

# ---------- HEADER ----------
st.markdown('<h1 class="title">📝 MY NOTES APP</h1>', unsafe_allow_html=True)

# ---------- MENU NAVIGATION ----------
if menu == "➕ Add Note":
    # --- ADD NOTE PAGE ---
    st.subheader("✍️ Add a New Note")

    category = st.selectbox("🏷️ Choose a Category", ["Personal", "Work", "Study", "Ideas", "Other"])
    new_note = st.text_area("ENTER THE NOTE HERE:")
    pinned = st.checkbox("⭐ Pin this note to top")

    if st.button("➕ Add Note"):
        if new_note.strip():
            add_note(new_note.strip(), category, pinned)
            st.success("✅ Note Added Successfully!")
            st.session_state["new_note"] = ""
            rerun()
        else:
            st.warning("⚠️ Please enter something before saving.")

elif menu == "📄 View Notes":
    # --- VIEW NOTES PAGE ---
    st.subheader("📄 Saved Notes")

    notes = load_notes()
    if not notes:
        st.info("No notes available yet. Add one from the sidebar.")
    else:
        # --- CATEGORY FILTER ---
        categories = ["All", "Personal", "Work", "Study", "Ideas", "Other"]
        selected_category = st.selectbox("📂 Filter by Category", categories)

        pinned_notes = [n for n in notes if "Pinned" in n]
        unpinned_notes = [n for n in notes if "Unpinned" in n]
        display_notes = pinned_notes + unpinned_notes

        # Apply category filter
        if selected_category != "All":
            display_notes = [
                n for n in display_notes
                if f"| {selected_category} |" in n
            ]

        # Handle empty results
        if not display_notes:
            st.info(f"No notes found in '{selected_category}' category.")
        else:
            for i, note in enumerate(display_notes, start=1):
                try:
                    note_id, timestamp, category, status, content = note.split(" | ", 4)
                except ValueError:
                    continue

                # --- EDIT MODE ---
                if st.session_state.get("edit_id") == note_id:
                    st.markdown(f"### ✏️ Editing Note #{i}")
                    new_content = st.text_area("Edit your note:", content, key=f"edit_area_{note_id}")

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("💾 Save", key=f"save_{note_id}"):
                            updated_note = f"{note_id} | {timestamp} | {category} | {status} | {new_content.strip()}"
                            index = notes.index(note)
                            notes[index] = updated_note
                            save_notes(notes)
                            st.session_state["edit_id"] = None
                            st.success("✅ Note updated successfully!")
                            rerun()

                    with col2:
                        if st.button("❌ Cancel", key=f"cancel_{note_id}"):
                            st.session_state["edit_id"] = None
                            rerun()

                # --- NORMAL DISPLAY ---
                else:
                    escaped_content = html.escape(content.strip())
                    escaped_timestamp = html.escape(timestamp.strip())
                    st.markdown(
                        f"""
                        <div class="note-card">
                            <span class="category-tag {category}">{category}</span>
                            {'📌' if 'Pinned' in status else ''}
                            {escaped_timestamp} | {escaped_content}
                        </div>
                        """, unsafe_allow_html=True
                    )

                    col1, col2, col3 = st.columns([1, 1, 6])
                    with col1:
                        if st.button("🗑️ Delete", key=f"del_{note_id}"):
                            notes.remove(note)
                            save_notes(notes)
                            st.warning("Note deleted.")
                            rerun()
                    with col2:
                        if st.button("✏️ Edit", key=f"edit_{note_id}"):
                            st.session_state["edit_id"] = note_id
                            rerun()

elif menu == "🔍 Search Notes":
    # --- SEARCH NOTES PAGE ---
    st.subheader("🔍 Search Notes")

    search = st.text_input("Type a keyword to search:")
    notes = load_notes()

    # --- CATEGORY FILTER FOR SEARCH ---
    categories = ["All", "Personal", "Work", "Study", "Ideas", "Other"]
    selected_category = st.selectbox("📂 Search within Category", categories)

    if not notes:
        st.info("No notes yet. Add some from the sidebar.")
    elif search:
        filtered = [n for n in notes if search.lower() in n.lower()]

        # Apply category filter
        if selected_category != "All":
            filtered = [n for n in filtered if f"| {selected_category} |" in n]

        if filtered:
            st.success(f"Found {len(filtered)} matching note(s).")
            for note in filtered:
                try:
                    note_id, timestamp, category, status, content = note.split(" | ", 4)
                except ValueError:
                    continue

                st.markdown(
                    f"""
                    <div class="note-card">
                        <span class="category-tag {category}">{category}</span>
                        {'📌' if 'Pinned' in status else ''}
                        <b>{timestamp}</b>
                        <p>{content.strip()}</p>
                    </div>
                    """, unsafe_allow_html=True
                )
        else:
            st.warning("No matching notes found.")
    else:
        st.info("Enter a word or phrase to search your notes.")

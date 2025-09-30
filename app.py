
# NOTES APP streamlit version , trying to blend the notes app CLI version into a streamlit web app
# i am just a beginner starting off this project hope it turns out well.

import streamlit as st
import datetime as dt

st.markdown(
    """
    <style>
    .stApp{
         background-color : #AEC6CF;
    }

    .title{
         text-align : center;
         text-decoration : underline;
         color : black ;
    }

    div.stButton > button:hover{
            background-color : #ADD8E6;
            transform : scale(1.05)
    }

    </style>
""" , unsafe_allow_html= True
)



NOTES_FILE = "notes.txt"

def load_notes():
    try :
        with open(NOTES_FILE , "r") as f :
            return f.readlines()
        
    except FileNotFoundError :
        return []



def save_notes(notes):
    with open(NOTES_FILE , "w") as file:
        file.writelines(notes)


st.markdown('<h1 class = "title"> MY NOTES APP </h1>' , unsafe_allow_html= True)

new_note = st.text_area("WRITE A NEW NOTE :- ")

col1 , col2 , col3 = st.columns([2,2,1])  # this for creating the button

with col2 :
    if st.button("➕ Add Note"):
        if new_note.strip() :
            timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]")
            with open(NOTES_FILE, "a") as file:
                file.write(f"{timestamp} {new_note.strip() } \n")
            st.success("NOTE ADDED!! ")

        else :
            st.warning("PLEASE ENTER SOMETHING !! ")

# this chunk of code is for showing all the notes

st.markdown("----------------")
st.subheader("📄 Saved Notes:")

notes = load_notes()

if notes :
    for idx , note in enumerate(notes,1):
        st.write(f"{idx} . {note.strip()}")

else:
    st.info("No Notes Yet !!")
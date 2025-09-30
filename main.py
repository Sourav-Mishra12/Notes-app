
# NOTES APP 

# it is a notes app that will have basic operations like adding , viewing and deleting notes by entering the index number
# also i have learnt a little bit of streamlit so i will be adding its functionalities into it
# not using any kind of module like json,os,pathlib because i want to keep it simple and practice the concepts of file i/o
# do not judge me i am just a beginner :) 

import datetime as dt 


NOTES_FILE = "notes.txt"

def add_notes():             # creating a function to add notes by using the input function and apppending the files

    notes = input("Enter your notes here : ").strip()

    timestamp = dt.datetime.now().strftime("[%Y-%m-%d %H:%M]") 
    note_with_stamp = f"{timestamp} {notes}"

    with open (NOTES_FILE , "a" ) as file :
         file.write(note_with_stamp + "\n")
         print(" ✅ Your note has been added successfully ")




def view_notes():            # using this function to show the notes that are already present in the notes.txt file
     
        print("\n 📄 Your notes are below :- \n")

        try :
             notes  = load_notes()   # this will read all the lines in the file and we are storing it in a variable because in the next line we are checking if the notes exist or is it an empty file

             if not notes:
                    print("No notes found here \n")
                    return
                
             for num, note in enumerate(notes,1):     # this will give a counter starting from the number 1
                     print(f"{num} . {note.strip()}")

        except FileNotFoundError :
             print(" Unable to find the notes file !!!! \n")
             
        print()




def update_notes():          # writing this function in case if anyone want to update their notes 

    try : 
         notes = load_notes()

         if not notes :
            print("There is nothing to update !!")    # checking if the file is present or not
            return

         for num,note in enumerate(notes,1):
            print(f"{num} . {note.strip()}")
        
         index = int(input("Enter the note number you want to edit or update : ")) -1 

         if 0 <= index < len(notes):
            old_note = notes[index].strip()     # this will store the indexed note in a variable called old_note
            confirm = input(f"Do you want to update this note -> {old_note} (y/n) : ")  # confirmation is important

            if confirm.lower() == "y":
                new_note = input("Enter the new note content : ")
                notes[index] = f"{dt.datetime.now().strftime('[%Y-%m-%d %H:%M]')} {new_note}\n"     # taking the new note as input and overwriting on the old note
                with open (NOTES_FILE , "w") as file :
                    file.writelines(notes) 
                print("updation successful")
            else :
                print("updation cancelled !!!")
         else :
            print("invalid index number")

    except FileNotFoundError :
        print("file not found")

    except ValueError :
        print("entered an invalid input !!!!!")
                    

def load_notes():
    try :
        with open(NOTES_FILE , "r") as f :
            return f.readlines()
        
    except FileNotFoundError :
        return []


def save_file():

    notes = load_notes()

    if not notes :
        print("No file exists to save !!")
        return
    
    print ("\n💾 Do you want to save/export your notes?")
    print("\n 1) Enter '1' to save as txt file ")
    print("\n 2) Enter '2' to not save the notes ")

    choice = input("enter your choice : ").strip()

    if choice == "1" :
        filename = input("Enter the file name (without extension) : ").strip()

        if not filename :
            print("❌ Filename cannot be empty!")
            return

        if not filename.endswith(".txt"):
            filename += ".txt"
        
        try :
            with open(filename , "r"):    # this will check if the file already exists or not and ask do the user want to overwrite ??
                confirm = input(f"{filename} already exists , do you want to overwrite it?? (yes/no) : ").strip().lower()

                if confirm != "yes" :
                    print("🚫 Save cancelled.")
                    return
                
        except FileNotFoundError :
            pass


        with open (filename , "w") as file :
            file.writelines(notes)
        print(f"✅ Notes saved to {filename}")

    elif choice == "2":
        print("Exiting without saving and exporting the file ")

    else :
        print("Invalid choice !!! ")


def delete_notes():
     
     notes = load_notes()

     if not notes :
        print("There are no notes here !!! \n")
        return
     
     for num , note in enumerate(notes,1):
          print(f"{num}  . {note.strip()}")

     try :      

      index = int(input("Enter the number you want to delete : ")) -1 # used for the python's 0 based index

      if 0 <= index < len(notes):
          selected_note = notes[index].strip()
          confirm = input(f"ARE YOU SURE YOU WANT TO DELETE THIS NOTE ?? {selected_note}  , (y/n) : ")

          if confirm.lower() == "y":
              deleted_note = notes.pop(index)
              with open(NOTES_FILE , "w") as file:
                   file.writelines(notes)
          print(f" 🗑️ Deleted note : {deleted_note.strip()} \n")

      else :
          print("Please enter a valid number  ")

     except ValueError:
         print("enter a valid input !!!")

         

def main():

   while True:
    print(" \n ------ WELCOME TO THE NOTES APP ------ \n")
    print("1) ADD NOTES \n")
    print("2) VIEW NOTES \n")
    print("3) DELETE NOTES \n")
    print("4) UPDATE NOTES\n")
    print("5) EXIT \n")

    choice = input("Enter your choice (1-5) : ").strip()

    if choice == "1" :
        add_notes()

    elif choice == "2" :
        view_notes()

    elif choice == "3" :
        delete_notes()

    elif choice == "4" :
        update_notes() 

    elif choice == "5":
        save_file()
        print("👋 THANK YOU !! HAVE A NICE DAY")
        break



if __name__ == "__main__":
    main()
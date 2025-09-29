
# NOTES APP 

# it is a notes app that will have basic operations like adding , viewing and deleting notes by entering the index number
# also i have learnt a little bit of streamlit so i will be adding its functionalities into it
# not using any kind of module like json,os,pathlib because i want to keep it simple and practice the concepts of file i/o
# do not judge me i am just a beginner :) 

import datetime as dt 


NOTES_FILE = "notes.txt"

def add_notes():             # creating a function to add notes by using the input function and apppending the files

    notes = input("Enter your notes here : ")

    timestamp = dt.now().strftime("[%Y-%m-%d %H:%M]") 
    note_with_stamp = f"{timestamp} {notes}"

    with open (NOTES_FILE , "a" ) as file :
         file.write(note_with_stamp + "\n")
         print(" ✅ Your note has been added successfully ")




def view_notes():            # using this function to show the notes that are already present in the notes.txt file
     
        print("\n 📄 Your notes are below :- \n")

        try :
              with open (NOTES_FILE , "r" ) as file :
                notes = file.readlines()   # this will read all the lines in the file and we are storing it in a variable because in the next line we are checking if the notes exist or is it an empty file

                if not notes:
                    print("No notes found here \n")
                    return
                
                for num, note in enumerate(notes,1):     # this will give a counter starting from the number 1
                     print(f"{num} . {note.strip()}")

        except FileNotFoundError :
             print(" Unable to find the notes file !!!! \n")
             
        print()




def update_notes():

    try : 
        with open(NOTES_FILE , "r" ) as file:
           notes=  file.readlines()

        if not notes :
            print("There is nothing to update !!")
            return

        for num,note in enumerate(notes,1):
            print(f"{num} . {note.strip()}")
        
        index = int(input("Enter the note number you want to edit or update : ")) -1

        if 0 <= index < len(notes):
            old_note = notes[index].strip()
            confirm = input(f"Do you want to delete this note -> {old_note} (y/n) : ")

            if confirm.lower() == "y":
                new_note = input("Enter the new note content : ")
                note[index] = new_note + "\n"
                with open (NOTES_FILE , "w") as file :
                    file.writelines(new_note)
                print("updation successful")
            else :
                print("updation cancelled !!!")
        else :
            print("invalid index number")

    except FileNotFoundError :
        print("file not found")

    except ValueError :
        print("entered an invalid input !!!!!")
                    




def delete_notes():
     
     with open(NOTES_FILE , "r") as file:
        notes = file.readlines()

     if not notes :
        print("There are no notes here !!! \n")
        return
     
     for num , note in enumerate(notes,1):
          print(f"{num} : " , "{note}")

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
    print(" ------ WELCOME TO THE NOTES APP ------")
    print("1) ADD NOTES \n")
    print("2) VIEW NOTES \n")
    print("3) DELETE NOTES \n")
    print("4) EXIT \n")

    choice = input("Enter your choice (1-4) : ")

    if choice == "1" :
        add_notes()

    elif choice == "2" :
        view_notes()

    elif choice == "3" :
        delete_notes()

    elif choice == "4" :
        print("👋 THANK YOU !! HAVE A NICE DAY")
        break 
    else:
        print("Enter a valid choice ")



if __name__ == "__main__":
    main()
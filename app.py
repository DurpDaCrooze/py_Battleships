# Author: Luca Cassart 👍 

def displayTitle():
    # Fetch ASCII title element from file
    try:
        with open('ASCII_ART/titleScreen.txt', 'r') as file:
            title = file.read()
            print(title)
    except FileNotFoundError:
        print("Error: ASCII title file not found.")
        exit(1)

def main_menu():
    uIn = -1
    while not (uIn > 0 and uIn < 4):
        # Display the main menu
        print("---===Main Menu===---", 
            "\n1. | Enter User Info", 
            "\n2. | Start New Game",
            "\n3. | Quit",)
        uIn = int(input("Select a valid option:"))
    return uIn;    

displayTitle()
print(main_menu())
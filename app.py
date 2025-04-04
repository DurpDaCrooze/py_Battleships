def displayTitle():
    # Get the title element
    with open('ASCII_ART/titleScreen.txt', 'r') as file:
        title = file.read()
        print(title)

displayTitle()
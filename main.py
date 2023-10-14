from scrape import HTML_to_Lists
import os

def getHTMLFileInput () -> str:
    while True:
        file_path = input("Enter the file path: ")

        if os.path.exists(file_path) and os.path.isfile(file_path):
            return file_path
        else:
            print(f"File '{file_path}' does not exist. Please enter a valid file path.")

if __name__ == "__main__":
    file_path = getHTMLFileInput()
    data = HTML_to_Lists (file_path)
    for key, value in data.items():
        print(f"{key}: {value}")


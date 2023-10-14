from scrape import HTML_to_Lists
import os

def getHTMLFileInput () -> str:
    while True:
        try:
            file_path = input("Enter the file path (Ctrl-C to exit): ")
        except:
            return ""
        if file_path != "" and os.path.exists(file_path) and os.path.isfile(file_path):
            return file_path
        else:
            print(f"File '{file_path}' does not exist. Please enter a valid file path.")

if __name__ == "__main__":
    file_path = getHTMLFileInput()
    if file_path == "":
        exit()
    try:
        data = HTML_to_Lists (file_path)
    except ValueError:
        print (f"Could not find a matching html table tag from {file_path}.")
        exit()
    except FileNotFoundError:
        print (f"Could not find {file_path}.")

    for key, value in data.items():
        print(f"{key}: {value}")


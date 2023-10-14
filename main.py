from scrape import HTML_to_Lists
import os

def getHTMLFileInput () -> str:
    while True:
        try:
            file_path = input("Enter the file path (Ctrl-C to exit): ")
            if file_path == "":
                exit()
        except:
            exit()
        if file_path != "" and os.path.exists(file_path) and os.path.isfile(file_path):
            return file_path
        else:
            print(f"File '{file_path}' does not exist. Please enter a valid file path.")

def getDatafromInput (file_path):
    try:
        data = HTML_to_Lists (file_path)
    except ValueError:
        print (f"Could not find a matching html table tag from {file_path}.")
        exit()
    except FileNotFoundError:
        print (f"Could not find {file_path}.")
        exit()
    return data

def print_data (data):
    print("\n--- All Captured Data ---")
    for key, value in data.items():
        print(f"{key}: {value}")

def print_quiz_info (quizList):
    MAXQUIZ = 41
    A_MIN_QUIZ = 31
    e = quizList.count(3)
    m = quizList.count(2)
    r = quizList.count(1)
    n = quizList.count(0)
    total_score = e + m + min(e // 2, r)
    quiz_left = MAXQUIZ - (len(quizList))
    
    print ("\n---- Quizzies ----")
    print (f"Your score so far is {total_score}/{len(quizList)}.")
    print (f"You have {quiz_left} quizzies left.")
    print (f"Your highest possible score is {quiz_left + total_score}/{MAXQUIZ}.")
    if total_score < A_MIN_QUIZ:
        print (f"You only need {A_MIN_QUIZ - total_score} more Es or Ms to get an A!")
    else:
        print (f"You already got an A in the Quizzies Section!")



if __name__ == "__main__":
    file_path = getHTMLFileInput()
    data = getDatafromInput (file_path)

    print_quiz_info(data["Quiz"])
    print_data (data)

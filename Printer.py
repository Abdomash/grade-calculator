import Grader
from colorama import init, Fore, Style

# Initialize colorama to work with ANSI escape codes on Windows
init(autoreset=True)

def bb(text):
    return Style.BRIGHT + text + Style.RESET_ALL
    
def header(name, course, date):
    print(bb("\n------| File Information |-------\n"))
    print(bb("Name:"), name)
    print(bb("Course:"), course.replace('-', ' '))
    print(bb("File Created on:"), str(date).split(' ')[0])
    print()

def grade(grade: Grader):
    print(bb(f"------| Current Grade |-------\n"))

    print("Note:",
    '''
    This is your current grade and the max grade you can
    get given your current grade and how many assignments 
    are remaining. 

    It is shown in this format:
    ''', bb("current grade"), "--> max possible grade")
    print(bb(f"\nTotal Grade:\t{grade.finalGrade}"), end="")
    if grade.finalGrade != 'A':
        print(f" --> {grade.finalMaxGrade}", end="")
    print('\n')
    for key, value in grade.data.items():
        print(bb(f"\t{(key + ':').ljust(9)} {value['grade'].ljust(2)} "), end="")
        print(f"({value['score']}/{value['rubric']['MAX']})".ljust(7), end="")
        if value['grade'] == 'A':
            print()
            continue
        print(f" --> {value['max-grade'].ljust(2)} ", end="")
        print(f"({value['max-score']}/{value['rubric']['MAX']})")
    print()

def path_to_all_grades(grade: Grader):
    def toText(scores, use1s):
        maxScore = 3 if use1s else 2
        ch = "NRME"
        output = ""
        correct_range = [i for i in range(1, max(scores) + 1) if scores.count(i) > 0]
        for k, i in enumerate(correct_range):
            output += f"{scores.count(i)}x {ch[i]}"
            if k < len(correct_range) - 2:
                output += ", "
            elif k < len(correct_range) - 1:
                output += " and "
        return output
            
    if grade.finalGrade == 'A':
        return
    
    print(bb("\n------| Detailed path to higher grades |------\n"))
    print("Note:", 
    '''
    This is a detailed path on how to get to each of the 
    higher grades you can get to. For each grade, it shows
    you how many more assignments (and what scores) you 
    need in each category.
    ''')

    print("Remember:\n\tE = 3/3, M = 2/3, R = 1/3, N = 0/3\n")
    for key, value in grade.data.items():
        if value['grade'] == 'A':
            continue
        print(f"\t{(key + ':').ljust(9)} ")
        for letter, scores in value['path-to-all-grades'].items():
            print(f"\t  ↳ to get {('(' + letter + '),').ljust(5)}", end="")
            print(f" You need at least {toText(scores, value['use1s'])}.")
        print()

def captured_data(data: Grader):
    print(bb("\n------| Captured Data |------\n"))
    for key, value in data.items():
        print(f"{key.rjust(8)} {len(value):>2}: {value}")

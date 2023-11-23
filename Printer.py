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
            output += f"{scores.count(i)}x{bb(ch[i])}"
            if k < len(correct_range) - 2:
                output += ", "
            elif k < len(correct_range) - 1:
                output += " and "
        return output

    def aORAn(letter):
        return 'an ' if letter[0] == 'A' or letter[0] == 'F' else 'a '

    if grade.finalGrade == 'A':
        return
    
    print(bb("\n------| Detailed path to higher grades |------\n"))
    print("Note:", 
    '''
    This is a detailed path on how to get to each higher 
    grades you can get to. For each grade, it shows you
    how many additional assignments (and what scores) you 
    need for each category.
    ''')

    print(f"Remember:\n\t{bb('E')} = 3/3, {bb('M')} = 2/3, {bb('R')} = 1/3, {bb('N')} = 0/3\n")

    grades_order = [key for key in grade.data["Quiz"]["rubric"].keys() if key != 'MAX']

    for letter in grades_order:
        if letter == grade.finalGrade:
            break

        if letter in grade.paths.keys():
            print(f"To get {aORAn(letter)}{bb(letter)},")
            max_cat_len = max(len(category) for category in grade.paths[letter].keys() if grade.data[category]['grade'] != letter) + 1
            for category, scores in grade.paths[letter].items():
                if grade.data[category]['grade'] == letter:
                    continue
                print(f"  -> in {(category + ','):<{max_cat_len}}", end="")
                print(f" from {(grade.data[category]['rubric']['MAX'] - len(grade.data[category]['data'])):>2} assignments left, ", end='')
                print(f"you need {toText(scores, grade.data[category]['use1s'])}.")
            print()

def captured_data(data: Grader):
    print(bb("\n------| Captured Data |------\n"))
    for key, value in data.items():
        print(f"{key.rjust(8)} {len(value):>2}: {value}")

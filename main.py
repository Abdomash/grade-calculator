import sys
import scrape

def print_data (data):
    print("\n--- Captured Data ---")
    for key, value in data.items():
        print(f"{key.ljust(9)}: {value}")

def getDataAsList(data, function):

    blogScore     = function(data['Blog'])
    exerciseScore = function(data['Exercise'])
    paperScore    = function(data['Paper'])
    projectScore  = function(data['Project']) 
    quizScore     = function(data['Quiz'])

    return [
    blogScore,
    exerciseScore,
    paperScore,
    projectScore,
    quizScore
    ]

def computeGrade(rubric, scores):
    def indexToLetter(index):
        letters = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
        if index == -1:
            return 'F'
        return letters[index]
    
    gradeRow = [-1, -1, -1, -1, -1]
    for i, row in enumerate(rubric):
        for j in range(len(gradeRow)):
            if gradeRow[j] == -1 and scores[j] >= row[j]:
                gradeRow[j] = i
    
    finalGrade = indexToLetter(max(i for i in gradeRow))
    subGrades = [indexToLetter(i) for i in gradeRow]
    return (finalGrade, subGrades)

def computeMaxGrades(rubric, max_rubric, grades, scores):
    def indexToLetter(index):
        letters = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-']
        if index == -1:
            return 'F'
        return letters[index]
    
    for i in range(len(grades)):
        scores[i] += (max_rubric[i] - grades[i])
    
    gradeRow = [-1, -1, -1, -1, -1]
    for i, row in enumerate(rubric):
        for j in range(len(gradeRow)):
            if gradeRow[j] == -1 and scores[j] >= row[j]:
                gradeRow[j] = i
    
    finalGrade = indexToLetter(max(i for i in gradeRow))
    subGrades = [indexToLetter(i) for i in gradeRow]
    return (finalGrade, subGrades)



def print_all_info(full_name, date, currFinalGrade, currSubGrades, maxFinalGrade, maxSubGrades):
    print(f"\n------| {full_name} |-------")
    print(f"------| Captured at {str(date).split(' ')[0]} |-------\n")


    print(f"Format: (current grade -→ max grade)\n")
    print(f"Total Grade:\t   {currFinalGrade} -→ {maxFinalGrade.ljust(2)}")
    print(f"\tBlogs:     {currSubGrades[0].ljust(2)} -→ {maxSubGrades[0].ljust(2)}")
    print(f"\tExercises: {currSubGrades[1].ljust(2)} -→ {maxSubGrades[1].ljust(2)}")
    print(f"\tPapers:    {currSubGrades[2].ljust(2)} -→ {maxSubGrades[2].ljust(2)}")
    print(f"\tProjects:  {currSubGrades[3].ljust(2)} -→ {maxSubGrades[3].ljust(2)}")
    print(f"\tQuizzies:  {currSubGrades[4].ljust(2)} -→ {maxSubGrades[4].ljust(2)}") 
    print()


if __name__ == "__main__":
    file = scrape.readfilePath(sys.argv)
    full_name = scrape.getName(file)
    date_of_creation = scrape.getDateOfCreation(file)
    data = scrape.getData(file)
    
    rubric = [
    #   The Rubric is from https://www.cs.utexas.edu/users/downing/cs371p/index.html.
    #   Each row correspond to a letter grade and each column refers to a category 
    #   in the following format:
    #   [Blogs, Exercises, Papers, Projects, Quizzes] # letter grade
        [11,  8, 11, 5, 33],  # A
        [11,  8, 11, 5, 31],  # A-
        [10,  7, 10, 4, 30],  # B+
        [10,  7, 10, 4, 28],  # B
        [ 9,  7,  9, 4, 27],  # B-
        [ 9,  6,  9, 4, 26],  # C+
        [ 8,  6,  8, 4, 24],  # C
        [ 8,  5,  8, 4, 23],  # C-
        [ 7,  5,  7, 3, 21],  # D+
        [ 7,  5,  7, 3, 20],  # D
        [ 6,  4,  6, 3, 19]   # D-
    ]

    #   max number of assignments per category in the same format:
    #   Blogs|Exercises|Papers|Projects|Quizzes
    max_scores = [14, 12, 14, 5, 41]
    

    def accountFor1s(scores):
        return scores.count(3) + scores.count(2) + min(scores.count(3) // 2, scores.count(1))
    scores = getDataAsList(data, accountFor1s);
    grades = getDataAsList(data, len)

    currFinalGrade, currSubGrades = computeGrade(rubric, scores)
    maxFinalGrade, maxSubGrades = computeMaxGrades(rubric, max_scores, grades, scores)

    print_all_info(full_name, date_of_creation, currFinalGrade, currSubGrades, maxFinalGrade, maxSubGrades)

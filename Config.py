def convertToDictPerCategory(categories, full_rubric):
    rubric_dict = {}
    for i, category in enumerate(categories):
        rubric_dict[category] = {key: value[i] for key, value in full_rubric.items()}
    return rubric_dict

def getRubric():    
    """
        The Rubric is from https://www.cs.utexas.edu/users/downing/cs371p/index.html.
        Each column refers to a category in the following format:
        "Letter":[Blogs, Exercises, Papers, Projects, Quizzes].
        The first row is for the total amount of assignment per each category.
    """
    categories = ["Blog", "Exercise", "Paper", "Project", "Quiz"]
    rubric = {
        "MAX": [14, 12, 14, 5, 41],
         "A" : [11,  8, 11, 5, 33],
         "A-": [11,  8, 11, 5, 31],
         "B+": [10,  7, 10, 4, 30],
         "B" : [10,  7, 10, 4, 28],
         "B-": [ 9,  7,  9, 4, 27],
         "C+": [ 9,  6,  9, 4, 26],
         "C" : [ 8,  6,  8, 4, 24],
         "C-": [ 8,  5,  8, 4, 23],
         "D+": [ 7,  5,  7, 3, 21],
         "D" : [ 7,  5,  7, 3, 20],
         "D-": [ 6,  4,  6, 3, 19] 
    }
    return convertToDictPerCategory(categories, rubric)

def attachRubricToDataAsJSON(data, rubric):
    return {
        "Blog":{
            "use1s": False,
            "data": data["Blog"],
            "rubric": rubric["Blog"]
        },
        "Exercise":{
            "use1s": True,
            "data": data["Exercise"],
            "rubric": rubric["Exercise"]
        },
        "Paper":{
            "use1s": True,
            "data": data["Paper"],
            "rubric": rubric["Paper"]
        },
        "Project":{
            "use1s": False,
            "data": data["Project"],
            "rubric": rubric["Project"]
        },
        "Quiz":{
            "use1s": True,
            "data": data["Quiz"],
            "rubric": rubric["Quiz"]
        }
    }


from functools import reduce

class Grader:
    def __init__(self, data: dict[str, dict]):
        data = self.addScores(data)
        data = self.addMaxPossibleScores(data)
        data = self.addGrades(data)
        data = self.addMaxGrades(data)
        self.data: dict[str, dict] = data
        self.finalGrade = self.computeFinalGrade("grade")
        self.finalMaxGrade = self.computeFinalGrade("max-grade")
        data = self.addPathToAllNextGrades(data)

    def computeFinalGrade(self, tag: str):
        grades = [value[tag] for key, value in self.data.items()]
        rubric = list(self.data["Quiz"]["rubric"].keys());
        return reduce(lambda x, y: max(x, y, key=rubric.index), grades)

    def addScores(self, data: dict[str, dict]) -> dict[str, dict]:
        for key, value in data.items():
            value["score"] = self.computeScore(value["use1s"], value["data"])
        return data
    
    def addMaxPossibleScores(self, data: dict[str, dict]) -> dict[str, dict]:
        for key, value in data.items():
            value["max-score"] = self.computeMaxScore(
                value["use1s"], 
                value['rubric']['MAX'],
                value["data"]
            )
        return data
    
    def addGrades(self, data) -> dict[str, dict]:
        for key, value in data.items():
            value["grade"] = self.computeGrade(value["score"], value["rubric"])
        return data
    
    def addPathToAllNextGrades(self, data) -> dict[str, dict]:
        for key, value in data.items():
            value["path-to-all-grades"] = self.computeMinsToAllNextGrades(
                value["data"],
                value["rubric"],
                value["use1s"]
            )
        return data
    
    def addMaxGrades(self, data) -> dict[str, dict]:
        for key, value in data.items():
            value["max-grade"] = self.computeGrade(value["max-score"], value["rubric"])
        return data

    def computeScore(self, use1s: bool, scores: list[int]):
        score = scores.count(3) + scores.count(2)
        if use1s:
            score += min(scores.count(3) // 2, scores.count(1))
        return score
    
    def computeMaxScore(self, use1s: bool, amount: int, scores: list[int]):
        maxScore = 3 if use1s else 2
        additional = [maxScore] * (amount - len(scores))
        return self.computeScore(use1s, scores + additional)

    def computeGrade(self, score: int, rubric: dict[str, int]):
        for key, value in rubric.items():
            if key == 'MAX':
                continue
            if score >= value:
                return key
        return 'F'
    
    """
    This function finds the minimum amount of assignments to complete to get to
    all of the higher grades. This function will priorities lesser assignments 
    than lesser scores. For example, if you need one more 3 or two more 1s to 
    jump from C+ to B-, this function will return the 3 only because it used 
    less assignments.
    """
    def computeMinsToAllNextGrades(self, scores: list[int], rubric: dict[str, int], use1s: bool):
        maxSingleScore = 3 if use1s else 2
        added_values = [0] * (rubric["MAX"] - len(scores))
        min_values = {}
        currIndex = len(added_values) - 1

        while currIndex != -1:
            added_values[currIndex] += 1
            if added_values[currIndex] > maxSingleScore:
                added_values[currIndex] -= 1
                added_values[currIndex - 1] += 1
                currIndex -= 1
            
            current_score = self.computeScore(use1s, added_values + scores)
            current_grade = self.computeGrade(current_score, rubric)
            if current_grade != self.finalGrade and current_grade not in min_values:
                min_values[current_grade] = [x for x in added_values if x != 0]

        return min_values
        
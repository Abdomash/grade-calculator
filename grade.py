from functools import reduce

class Grade:
    def __init__(self, data: dict[str, dict]):
        data = self.addScores(data)
        data = self.addMaxPossibleScores(data)
        data = self.addGrades(data)
        data = self.addMaxGrades(data)
        self.data: dict[str, dict] = data
        self.finalGrade = self.computeFinalGrade("grade")
        self.finalMaxGrade = self.computeFinalGrade("max-grade")
        data = self.addMinToAllNextGrades(data)

    def print_grade(self):
        print(f"Total Grade:\t{self.finalGrade}", end="")
        if self.finalGrade != 'A':
            print(f" --> {self.finalMaxGrade}", end="")
        print('\n')
        for key, value in self.data.items():
            print(f"\t{(key + ':').ljust(9)} {value['grade'].ljust(2)} ", end="")
            print(f"({value['score']}/{value['rubric']['MAX']})".ljust(7), end="")
            if value['grade'] == 'A':
                print()
                continue
            print(f" --> {value['max-grade'].ljust(2)} ", end="")
            print(f"({value['max-score']}/{value['rubric']['MAX']})")
        print()

    def print_path_to_all_next_grades(self):
        def toText(scores, use1s):
            maxScore = 3 if use1s else 2
            ch = "NRME"
            output = ""
            correct_range = [i for i in range(1, max(scores) + 1) if scores.count(i) > 0]
            for k, i in enumerate(correct_range):
                addS = "s" if scores.count(i) > 1 else ""
                output += f"({scores.count(i)}x{ch[i]}{addS})"
                if k < len(correct_range) - 2:
                    output += ", "
                elif k < len(correct_range) - 1:
                    output += " and "
            return output
                
        if self.finalGrade == 'A':
            return
        
        print("\n------| Detailed path to next grades |------")
        print("Notes: E = 3/3    M = 2/3    R = 1/3    N = 0/3\n")
        for key, value in self.data.items():
            if value['grade'] == 'A':
                continue
            print(f"\t{(key + ':').ljust(9)} ")
            for letter, scores in value['path-to-all-grades'].items():
                print(f"\t  ↳ to get {('(' + letter + '),').ljust(5)}", end="")
                print(f" You need at least {toText(scores, value['use1s'])}.")
            print()


    def print_captured_data(self):
        print("\n------| Captured Data |------\n")
        for key, value in self.data.items():
            print(f"{key.rjust(8)} {len(value['data']):>2}: {value['data']}")

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
    
    def addMinToAllNextGrades(self, data) -> dict[str, dict]:
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
        
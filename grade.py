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

    def print_grade(self):
        print(f"Total Grade:\t{self.finalGrade}", end="")
        if self.finalGrade != 'A':
            print(f" --> {self.finalMaxGrade}", end="")
        print('\n')
        for key, value in self.data.items():
            print(f"   {key.rjust(8)}: {value['grade'].ljust(2)} ", end="")
            print(f"({value['score']}/{value['rubric']['MAX']})".ljust(7), end="")
            if value['grade'] == 'A':
                print()
                continue
            print(f" --> {value['max-grade'].ljust(2)} ", end="")
            print(f"({value['max-score']}/{value['rubric']['MAX']})")
        print()

    def print_captured_data(self):
        print("\n------| Captured Data |------")
        for key, value in self.data.items():
            print(f"{key.rjust(8)}: {len(value['data']):>2} {value['data']}")

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
        
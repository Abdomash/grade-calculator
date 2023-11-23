import sys
import Scraper
import Grader
import Printer
import Config

if __name__ == "__main__":

    # -----| Scraping Data |-----
    file_path = Scraper.readfilePath(sys.argv)
    name, course = Scraper.getNameAndCourseName(file_path)
    date_of_creation = Scraper.getDateOfCreation(file_path)
    data = Scraper.getData(file_path)

    # -----| Rubric Config |-----
    rubric = Config.getRubric()
    dataJSON = Config.attachRubricToDataAsJSON(data, rubric)

    # -----| Computing Grades |-----
    grade = Grader.Grader(dataJSON)

    # -----| Printing Grades |-----
    Printer.header(name, course, date_of_creation)
    Printer.grade(grade)
    Printer.path_to_all_grades(grade)
    Printer.captured_data(data)

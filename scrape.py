from bs4 import BeautifulSoup
from collections import defaultdict

def HTML_to_Lists (html_file_path):
    # read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    grade_attrs = {
    'id': 'grades_summary',
    'class': ['editable', 'ic-Table', 'ic-Table--hover-row', 'ic-Table--grades-summary-table']
    }

    # Find the table with id="grades_summary"
    grades_table = soup.find('table', grade_attrs)

    if grades_table == None:
        raise ValueError(f"No table with id='grades_summary' found in {html_file_path}.")
    
    data = defaultdict(list)

    # Find the tbody tag within the table
    tbody = grades_table.find('tbody')

    # Find all entries of the grades_table
    rows = tbody.find_all('tr', {'class': 'student_assignment assignment_graded editable'})

    for row in rows:
        th_tag = row.find('th')
        grade_span = row.find('span', {'class': 'grade'})
        title_tag = row.find('th', {'class': 'title', 'scope': 'row'})

        # We found an entry inside the grades table
        if th_tag and grade_span:
            
            # Remove text under <div class="context">
            for span in title_tag.find_all('div', {'class': 'context'}):
                span.decompose()
            
            th_text = ((th_tag.get_text(strip=True)).split(":")[0]).strip()
            if "#" not in th_text:
                continue
            name = (th_text.split("#")[0].strip())

            # Remove text under <span class="screenreader-only" role="button">
            for span in grade_span.find_all('span', {'class': 'screenreader-only', 'role': 'button'}):
                span.decompose()
            
            # Remove text under <span class="tooltip_wrap right" aria-hidden="true">
            for span in grade_span.find_all('span', {'class': 'tooltip_wrap right', 'aria-hidden': 'true'}):
                span.decompose()

            grade = grade_span.get_text(strip=True)
            
            data[name].append(int(float(grade)))
    return data

def getCourseFromTitle(html_file_path):
    # read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')

    name = soup.find("title").text
    course_name = name.split(':')[1].strip().upper()
    first_name, second_name = (name.split(' ')[2].strip(), name.split(' ')[3].removesuffix(":").strip())
    return (f"{first_name} {second_name} {course_name}")


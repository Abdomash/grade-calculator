from bs4 import BeautifulSoup
from collections import defaultdict

def HTML_to_Lists (html_file_path):
    # read the HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the table with id="grades_summary"
    grades_table = soup.find('table', {'id': 'grades_summary'})

    if not grades_table:
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
            
            data[name].append(int(grade))
    return data
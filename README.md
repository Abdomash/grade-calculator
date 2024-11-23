# Grade Calculator 🧮
A Canvas page scraper that calculates your current grade and provides strategies to improve it.

> ### **NOTE**
>This project was designed for the UT Austin Canvas page for the following courses only: 
>- CS373: Software Engineering, taught by Prof. Downing, Fall 2023.
>- CS371p: Object Oriented Programming, taught by Prof. Downing, Fall 2023.
>
>Running the code on other courses or in the far future will likely break the script, as the scraping format is hardcoded to what the Canvas page looked like in Feb 2024. Additionally, the grade & rubric processing is only compatible with the two above classes. If you want to use it with other classes, you need to modify the script to use your class's rubric. Your class should have a clear rubric if you want to implement it in an easy way, like:
>- *How many assignments do you need to complete to get an A?*
>- *How many assignments are remaining?*
>- *Does the professor post grades regularly to Canvas?*
>- *etc.*

## Features
- Scrapes Canvas grade page for the relevant class.
- Computes your current grade based on available data.
- Predicts the highest possible future grade you can achieve.
- Provides actionable steps to improve and reach the highest possible grade.

## Requirements
- Python 3.x
- Libraries:  `beautifulsoup4`, `colorama`

## Setup
1. Clone the repository: `git clone <repo-url>`
2. Navigate to the project directory: `cd grade-calculator`
3. Install required libraries: `pip install beautifulsoup4 colorama`
4. Configure the `config.py` file with the class's Rubric.

## Usage
1. Go to your Canvas Grade page for your class.
2. Save the page as an `html` file
3. Run the script: `python main.py <your-html-filepath>` (Or you could run the compiled binary `gradeCalculator <your-html-filepath>`)
2. View the results in a vim-like viewer.

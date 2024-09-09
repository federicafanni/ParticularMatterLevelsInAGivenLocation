# Daily Particular Matter (PM10) Levels in Dublin

## Description
This Python program retrieves the current day's PM10 (Particulate Matter 10) levels in Dublin, Ireland, from a public API and provides visualizations, CSV storage, and database logging for historical data.

## Features
- **API data retrieval**: The program retrieves the hourly PM10 air quality levels for Dublin via the [Open-Meteo API](https://open-meteo.com/). Specifically, the PM10 level at midday is extracted for tracking air quality trends.
- **Data display**: The PM10 levels for midday are displayed in a tabular format on the console using the tabulate library.
- **CSV storage**: The program appends the PM10 levels along with the date to a CSV file (dailyPM10levelsInDublin.csv), which can be updated daily.
- **SQLite database**: The daily PM10 data is stored in an SQLite database (dailyPM10levelsInDublin.db). A table called dailyPM10levels is created to store the date and PM10 level, if it doesn't already exist.
- **Data visualization**:
  - *Line plot*: The program generates a line plot of the daily PM10 levels over time using matplotlib. The plot is saved as an SVG file (dailyPM10levelsInDublin.svg).
  - *Bar chart*: A bar chart of PM10 levels over time is created using plotly, displayed in a web browser, and saved as a PNG file (dailyPM10levelsInDublin.png).
- **Automation**: The program can be automated to run daily by using a batch script and Task Scheduler on Windows (or cron jobs on Unix-based systems).

## Installation and usage
To run this project locally, you will need Python and the following libraries installed on your system:
- Python 3.x
- `requests` library to make API calls.
- `json` library (usually included in standard Python distribution) to parse the JSON data returned by the API.
- `tabulate` to format and display the data in a table.
- `csv` to write and append data to a CSV file.
- `sqlite3` to store the data in an SQLite database.
- `matplotlib` To generate line plots.
- `pandas` to handle data manipulation for plotting.
- `plotly.graph_objects`: To create and display interactive bar charts.

To run the project, roceed as follows:
1. Clone the repository to your local machine.
2. Run `dailyPM10levelsInDublin.py` in the terminal or using an interpreter.
3. The program will:
   - 3.1 Fetch the current day's PM10 data.
   - 3.2 Display the PM10 levels in a table.
   - 3.3 Append the data to dailyPM10levelsInDublin.csv.
   - 3.4 Store the data in the SQLite database dailyPM10levelsInDublin.db.
   - 3.5 Generate and save visualizations as SVG and PNG files.

## Automating the script (Windows)
1. Create a batch file (like the one provided in this repository).
2. Open Task Scheduler and create a new task:
   - 2.1 Set the trigger to run daily at your preferred time.
   - 2.2 Add the batch file as the program to be executed.

## Contributing
Contributions to this project are welcome. Please fork the repository and submit a pull request with your changes.

## License
[MIT License](LICENSE.md) - feel free to use and modify this code for your own projects.

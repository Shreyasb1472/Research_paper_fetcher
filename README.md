

Clone the Repository :

git clone https://github.com/Shreyasb1472/research-paper-fetcher.git
cd research-paper-fetcher


Install Dependencies:
poetry install

Command:
poetry run python src/cli.py "your query here" -f results.csv

    Example
        Fetch papers on "COVID-19 vaccine" and save results to results.csv:
        poetry run python src/cli.py "COVID-19 vaccine" -f results.csv

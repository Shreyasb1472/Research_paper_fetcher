import typer
from paper_fetcher.fetch import fetch_papers
from paper_fetcher.filter import filter_non_academic_authors
from paper_fetcher.save import save_to_csv

app = typer.Typer()

@app.command()
def get_papers_list(query: str, filename: str = typer.Option(None, "-f", "--file"), debug: bool = False):
    """Fetch research papers from PubMed, filter non-academic authors, and save results as CSV."""
    print("=== CLI script is running! ===")  # Debugging print

    try:
        print(f"Query received: {query}")  # Debugging print

        papers = fetch_papers(query)  #  This should return a dictionary
        print("Fetched Papers (Raw Output):", papers)  #  Print full output

        if isinstance(papers, list):  #  Check if it's returning a list
            print(" ERROR: fetch_papers() is returning a LIST instead of a DICTIONARY!")
        elif isinstance(papers, dict):
            print(" fetch_papers() is returning a DICTIONARY as expected.")

        filtered_papers = filter_non_academic_authors(papers)  #  Pass full paper details
        print("Filtered papers:", filtered_papers)  #  Debugging print


        if filename:
            save_to_csv(filtered_papers, filename)
        else:
            print(filtered_papers)

    except Exception as e:
        print("An error occurred:", e)  #  Print any errors

if __name__ == "__main__":
    app()

from typing import List, Dict
import requests
import xml.etree.ElementTree as ET

PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
DETAILS_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"  #  Use efetch.fcgi instead of esummary.fcgi

def fetch_details(paper_ids: List[str]) -> Dict[str, Dict]:
    """Fetch detailed information of papers, including author affiliations, using efetch."""
    if not paper_ids:
        print("No paper IDs found.")
        return {}

    params = {
        "db": "pubmed",
        "id": ",".join(paper_ids),
        "retmode": "xml",  #  Get full XML data
        "rettype": "abstract"
    }
    response = requests.get(DETAILS_API_URL, params=params)
    
    print(" Fetching full details for Paper IDs:", paper_ids)  # Debug print
    print(" Raw API Response (First 500 chars):", response.text[:500])  # Debug print
    
    if response.status_code != 200:
        raise Exception("Failed to fetch detailed paper data")

    print("Fetched XML Data:", response.text[:500])  #  Print first 500 chars for debugging

    return parse_pubmed_xml(response.text)  #  Convert XML to structured data

import xml.etree.ElementTree as ET

def parse_pubmed_xml(xml_data: str) -> Dict[str, Dict]:
    """Parse PubMed XML response and extract relevant details."""
    root = ET.fromstring(xml_data)
    papers = {}

    for article in root.findall(".//PubmedArticle"):
        paper_id = article.find(".//PMID").text if article.find(".//PMID") is not None else "Unknown"
        title = article.find(".//ArticleTitle").text if article.find(".//ArticleTitle") is not None else "No Title"
        pub_date = article.find(".//PubDate").text if article.find(".//PubDate") is not None else "No Date"

        authors = []
        for author in article.findall(".//Author"):
            name = author.find(".//LastName").text if author.find(".//LastName") is not None else "Unknown"
            affiliation = author.find(".//Affiliation").text if author.find(".//Affiliation") is not None else "No Affiliation"
            authors.append({"name": name, "affiliation": affiliation})

        papers[paper_id] = {
            "title": title,
            "pubdate": pub_date,
            "authors": authors
        }

    print(" Parsed Paper Details:", papers)  # Debugging print
    return papers

def fetch_papers(query: str, max_results: int = 10) -> Dict[str, Dict]:
    """Fetch research papers from PubMed based on a query and return full details."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": max_results
    }
    response = requests.get(PUBMED_API_URL, params=params)

    print(f" PubMed API Status Code: {response.status_code}")  #  Debugging print

    if response.status_code != 200:
        raise Exception(f" Failed to fetch data from PubMed. Status Code: {response.status_code}")

    data = response.json()
    print(f" PubMed API Response JSON: {data}")  # Print entire response

    paper_ids = data.get("esearchresult", {}).get("idlist", [])
    print(f"Fetched Paper IDs: {paper_ids}")  #  Debugging print

    if not paper_ids:
        print(" No paper IDs found!")  # Debugging print 
        return {}  # No papers found

    return fetch_details(paper_ids)  #  Fetch and return full paper details

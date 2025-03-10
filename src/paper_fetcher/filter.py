from typing import List, Dict

def filter_non_academic_authors(papers: Dict[str, Dict]) -> List[Dict]:
    """Find papers where at least one author is from a pharmaceutical or biotech company."""
    print("Raw Paper Data Before Filtering:", papers)  # Debugging print

    filtered_papers = []
    
    for paper_id, paper in papers.items():
        if isinstance(paper, dict) and "authors" in paper:
            print(f"Checking Paper: {paper.get('title', 'No Title')}")
            
            authors = paper.get("authors", [])
            print("Authors:", authors)  # Debug print

            non_academic_authors = [
                author for author in authors
                if any(kw in author.get("affiliation", "").lower() for kw in ["pharma", "biotech", "inc", "ltd"])
            ]
            
            if non_academic_authors:
                print(f"Paper {paper_id} has non-academic authors!")  # Debug print
                filtered_papers.append({
                    "PubmedID": paper_id,
                    "Title": paper.get("title", "N/A"),
                    "Publication Date": paper.get("pubdate", "N/A"),
                    "Non-academic Authors": [author["name"] for author in non_academic_authors],
                    "Company Affiliations": [author["affiliation"] for author in non_academic_authors]
                })
    
    print("Filtered Papers:", filtered_papers)  # Debugging print
    return filtered_papers

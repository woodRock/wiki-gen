from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Backpropagation Applied to Handwritten Zip Code Recognition LeCun 1989")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

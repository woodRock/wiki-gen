from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Gradient-Based Learning Applied to Document Recognition LeCun 1998")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

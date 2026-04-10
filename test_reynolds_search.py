from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Flocks, Herds, and Schools Craig Reynolds 1987")
for paper in results[:5]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

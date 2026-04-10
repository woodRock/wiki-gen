from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Learning representations by back-propagating errors Rumelhart Hinton Williams 1986")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

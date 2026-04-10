from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Acoustic fish species identification using deep learning and machine learning algorithms: A systematic review Yassir 2023")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

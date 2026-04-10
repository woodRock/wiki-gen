from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("Dropout: A Simple Way to Prevent Neural Networks from Overfitting Srivastava 2014")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

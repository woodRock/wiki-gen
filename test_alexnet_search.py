from semanticscholar import SemanticScholar
sch = SemanticScholar()
results = sch.search_paper("ImageNet Classification with Deep Convolutional Neural Networks Krizhevsky 2012")
for paper in results[:3]:
    print(f"Title: {paper.title}")
    print(f"Paper ID: {paper.paperId}")
    print(f"Year: {paper.year}")
    print("-" * 20)

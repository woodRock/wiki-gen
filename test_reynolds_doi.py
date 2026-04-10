from semanticscholar import SemanticScholar
sch = SemanticScholar()
paper = sch.get_paper("10.1145/37402.37406")
print(f"Title: {paper.title}")
print(f"Paper ID: {paper.paperId}")

from semanticscholar import SemanticScholar
sch = SemanticScholar()
paper = sch.get_paper("10.1121/1.395298")
print(f"Title: {paper.title}")
print(f"References count: {len(paper.references) if paper.references else 0}")
if paper.references:
    for ref in paper.references[:5]:
        print(f" - {ref.title}")

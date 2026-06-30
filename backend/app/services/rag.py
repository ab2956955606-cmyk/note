import re
from collections import Counter

from ..schemas import RagRequest


def tokenize(text: str) -> list[str]:
    return re.findall(r"[\w\u4e00-\u9fff]+", text.lower())


class RagIndex:
    def query(self, req: RagRequest):
        chunks = [c.strip() for c in re.split(r"\n{2,}|[。.!?]", req.context or "") if c.strip()]
        if not chunks:
            chunks = ["No material provided. Paste a JD, course note, or resume to enable retrieval."]
        query_terms = Counter(tokenize(req.goal + " " + req.date))
        scored = []
        for idx, chunk in enumerate(chunks):
            terms = Counter(tokenize(chunk))
            score = sum((query_terms & terms).values()) or (1 if idx == 0 else 0)
            scored.append((score, idx, chunk))
        top = sorted(scored, reverse=True)[:3]
        return {
            "mode": "rag-lite",
            "answer": "Retrieved the most relevant material snippets for planning.",
            "sources": [
                {"title": f"Chunk {idx + 1}", "quote": chunk[:220]}
                for _, idx, chunk in top
            ],
        }

"""
DuckDuckGo quick search.
"""

from duckduckgo_search import DDGS

class WebSearcher:
    def search(self, query: str, max_results: int = 4) -> list[str]:
        with DDGS() as ddgs:
            return [
                f"{r['title']} – {r['href']}"
                for r in ddgs.text(query, max_results=max_results)
            ]

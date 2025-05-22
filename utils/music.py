"""
Plays first YouTube result for a track query (no Premium needed).
"""

import webbrowser
from utils.search import WebSearcher

class MusicPlayer:
    def play(self, track_query: str) -> str | None:
        res = WebSearcher().search(f"site:youtube.com {track_query}", max_results=1)
        if res:
            url = res[0].split(" – ")[-1]
            webbrowser.open(url)
            return url
        return None

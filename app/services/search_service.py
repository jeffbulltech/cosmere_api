from elasticsearch import AsyncElasticsearch
from typing import List, Dict, Any, Optional
from app.core.config import settings

class SearchService:
    def __init__(self):
        self.es = AsyncElasticsearch([settings.elasticsearch_url])

    async def search_characters(self, query: str, filters: Optional[Dict[str, Any]] = None, size: int = 20) -> Dict[str, Any]:
        search_body = {
            "query": {
                "bool": {
                    "must": [
                        {"multi_match": {
                            "query": query,
                            "fields": ["name^2", "aliases", "biography"]
                        }}
                    ]
                }
            },
            "size": size,
            "sort": [{"_score": {"order": "desc"}}]
        }
        if filters:
            search_body["query"]["bool"]["filter"] = [
                {"term": {k: v}} for k, v in filters.items()
            ]
        return await self.es.search(index="characters", body=search_body)

    async def global_search(self, query: str, size: int = 20) -> Dict[str, Any]:
        # Search across multiple indices (characters, books, worlds, etc.)
        search_body = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": [
                        "name^3", "aliases^2", "biography", "title^2", "summary", "system", "intent"
                    ],
                    "type": "best_fields",
                    "fuzziness": "AUTO"
                }
            },
            "size": size,
            "sort": [{"_score": {"order": "desc"}}]
        }
        return await self.es.search(index=["characters", "books", "worlds", "magic_systems", "shards"], body=search_body) 
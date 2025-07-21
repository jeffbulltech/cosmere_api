# backend/scripts/fetch_coppermind_data.py
import aiohttp
import asyncio
import json
from typing import Dict, List

class CoppermindFetcher:
    def __init__(self):
        self.base_url = "https://coppermind.net/api.php"
        self.session = None
    
    async def fetch_page_content(self, page_title: str) -> Dict:
        """Fetch content for a specific page"""
        params = {
            'action': 'query',
            'format': 'json',
            'titles': page_title,
            'prop': 'extracts|categories|pageprops',
            'exintro': True,
            'explaintext': True
        }
        headers = {'User-Agent': 'CosmereAPI/1.0 (contact: your-email@example.com)'}
        async with self.session.get(self.base_url, params=params, headers=headers) as response:
            data = await response.json()
            return data
    
    async def search_characters(self) -> List[str]:
        """Get list of character pages"""
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'categorymembers',
            'cmtitle': 'Category:Characters',
            'cmlimit': 100
        }
        headers = {'User-Agent': 'CosmereAPI/1.0 (contact: your-email@example.com)'}
        async with self.session.get(self.base_url, params=params, headers=headers) as response:
            data = await response.json()
            return [page['title'] for page in data['query']['categorymembers']]
    
    async def enhance_character_data(self, character_name: str) -> Dict:
        """Fetch detailed character information"""
        content = await self.fetch_page_content(character_name)
        
        # Extract relevant information
        pages = content.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if page_id != '-1':  # Page exists
                return {
                    'name': character_name,
                    'summary': page_data.get('extract', ''),
                    'categories': [cat['title'] for cat in page_data.get('categories', [])]
                }
        
        return {'name': character_name, 'summary': '', 'categories': []}
    
    async def run_collection(self):
        """Main collection process"""
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            print("🔍 Fetching character data from Coppermind...")
            characters = await self.search_characters()
            
            enhanced_data = []
            for char in characters[:20]:  # Limit for testing
                try:
                    data = await self.enhance_character_data(char)
                    enhanced_data.append(data)
                    print(f"✅ Fetched: {char}")
                    await asyncio.sleep(1)  # Be respectful to the API
                except Exception as e:
                    print(f"❌ Error fetching {char}: {e}")
            
            # Save to file
            with open('backend/data/coppermind_characters.json', 'w') as f:
                json.dump(enhanced_data, f, indent=2)
            
            print(f"💾 Saved {len(enhanced_data)} character records")

if __name__ == "__main__":
    fetcher = CoppermindFetcher()
    asyncio.run(fetcher.run_collection())
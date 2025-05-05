# main.py
import os
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_clutch

app = FastAPI()

class ScrapeRequest(BaseModel):
    base_url: str
    pages: int = 3

@app.post('/scrape')
async def scrape_endpoint(req: ScrapeRequest):
    all_rows = []
    for page_num in range(1, req.pages + 1):
        url = f"{req.base_url}?page={page_num}"
        ua = random.choice(os.getenv('USER_AGENTS').split(',')) if os.getenv('USE_AGENT')=='True' else None
        proxy_list = os.getenv('PROXIES', '').split(',')
        proxy = random.choice(proxy_list) if proxy_list and proxy_list[0] else None
        names, websites, locations = await scrape_clutch(
            url,
            os.getenv('HEADLESS') == 'True',
            ua,
            proxy
        )
        for i, name in enumerate(names):
            raw_url = websites[i]['destination_url'] if i < len(websites) else None
            website = f"{urlparse(raw_url).scheme}://{urlparse(raw_url).netloc}" if raw_url else None
            location = locations[i] if i < len(locations) else None
            all_rows.append({
                'S.No': len(all_rows)+1,
                'Company Name': name,
                'Website': website,
                'Location': location
            })
    if not all_rows:
        raise HTTPException(status_code=404, detail='No data scraped')
    return {'results': all_rows}

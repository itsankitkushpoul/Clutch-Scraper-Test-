import os
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_clutch
import asyncio

app = FastAPI()

class ScrapeRequest(BaseModel):
    base_url: str
    pages: int = 3

@app.post('/scrape')
async def scrape_endpoint(req: ScrapeRequest):
    all_rows = []
    for i in range(1, req.pages + 1):
        url = f"{req.base_url}?page={i}"
        ua = random.choice(os.getenv('USER_AGENTS').split(','))
        proxy = random.choice(os.getenv('PROXIES').split(','))
        names, data, locations = await scrape_clutch(url, os.getenv('HEADLESS')=='True', ua, proxy)
        # assemble rows ...
    if not all_rows:
        raise HTTPException(status_code=404, detail="No data scraped")
    return {'results': all_rows}

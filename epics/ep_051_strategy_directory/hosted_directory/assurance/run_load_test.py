"""Bounded local load acceptance for public intelligence read paths."""
from __future__ import annotations

import asyncio
from datetime import datetime,timezone
import json
from pathlib import Path
import statistics
import time

import httpx

ROOT=Path(__file__).resolve().parents[1]
URLS=(
    "/api/dna/strategies?page=1&page_size=25&sort=total_net_return&direction=desc",
    "/api/intelligence/strategies/DNA_102001",
    "/api/intelligence/strategies/DNA_102001/score",
    "/api/intelligence/compare?strategy_ids=DNA_102001,DNA_101001",
)


async def run(base_url="http://127.0.0.1:8012",requests=400,concurrency=20):
    semaphore=asyncio.Semaphore(concurrency);latencies=[];statuses=[]
    async with httpx.AsyncClient(base_url=base_url,timeout=10) as client:
        async def one(index):
            async with semaphore:
                started=time.perf_counter();response=await client.get(URLS[index%len(URLS)]);latencies.append((time.perf_counter()-started)*1000);statuses.append(response.status_code)
        await asyncio.gather(*(one(index) for index in range(requests)))
    ordered=sorted(latencies);p95=ordered[max(0,int(len(ordered)*.95)-1)];failures=sum(status>=500 for status in statuses)
    return {"generated_at":datetime.now(timezone.utc).isoformat(),"base_url":base_url,"requests":requests,"concurrency":concurrency,"p50_ms":round(statistics.median(ordered),3),"p95_ms":round(p95,3),"max_ms":round(max(ordered),3),"server_failures":failures,"slo":{"p95_ms":500,"server_failures":0},"passed":p95<=500 and failures==0}


if __name__=="__main__":
    report=asyncio.run(run());target=ROOT/"evidence"/"intelligence_load_report.json";target.write_text(json.dumps(report,indent=2),encoding="utf-8");print(json.dumps(report))

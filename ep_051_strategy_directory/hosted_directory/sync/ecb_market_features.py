"""Build point-in-time FX regime features from official ECB daily EXR observations."""
from __future__ import annotations

import argparse,asyncio,csv,hashlib,io,json,math,statistics
from datetime import date,datetime,timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx

CURRENCIES=("USD","GBP","JPY","CHF","AUD","CAD","NZD")
SOURCE_VERSION="ecb-exr-daily-v1"
API="https://data-api.ecb.europa.eu/service/data/EXR/D.{currencies}.EUR.SP00.A"
ROOT=Path(__file__).resolve().parents[1]


def load_csv(text):
    rows={currency:{} for currency in CURRENCIES}
    for row in csv.DictReader(io.StringIO(text)):
        currency=row.get("CURRENCY") or row.get("KEY_VALUE") or row.get("Currency")
        period=row.get("TIME_PERIOD") or row.get("Period");value=row.get("OBS_VALUE") or row.get("Observation Value")
        if currency in rows and period and value not in (None,""):rows[currency][date.fromisoformat(period)]=float(value)
    return rows


def build_features(rates):
    common=sorted(set.intersection(*(set(values) for values in rates.values())));output=[];daily=[];cumulative=0.0
    for index in range(1,len(common)):
        today,yesterday=common[index],common[index-1];value=statistics.mean(math.log(rates[c][today]/rates[c][yesterday]) for c in CURRENCIES);cumulative+=value;daily.append((today,value,cumulative))
        if index<260:continue
        trailing=[item[1] for item in daily[-252:]];current_vol=statistics.stdev(item[1] for item in daily[-20:])*math.sqrt(252)
        historical_vol=[statistics.stdev(item[1] for item in daily[end-20:end])*math.sqrt(252) for end in range(max(20,len(daily)-120),len(daily))]
        vol_mean=statistics.mean(historical_vol);vol_sd=statistics.pstdev(historical_vol);vol_z=(current_vol-vol_mean)/vol_sd if vol_sd else 0.0
        trend=statistics.mean(math.log(rates[c][today]/rates[c][common[index-20]]) for c in CURRENCIES)
        peak=max(item[2] for item in daily[-252:]);drawdown=math.exp(cumulative-peak)-1;breadth=sum(rates[c][today]>rates[c][common[index-20]] for c in CURRENCIES)/len(CURRENCIES)
        as_of=datetime(today.year,today.month,today.day,16,tzinfo=ZoneInfo("Europe/Paris")).astimezone(timezone.utc)
        output.append({"market":"FX","as_of":as_of.isoformat(),"features":{"trend":trend,"volatility_z":vol_z,"drawdown":drawdown,"breadth":breadth,"realized_volatility":current_vol},"source_version":SOURCE_VERSION})
    return output


async def fetch(start,end):
    url=API.format(currencies="+".join(CURRENCIES));params={"format":"csvdata","startPeriod":start,"endPeriod":end,"detail":"dataonly"}
    async with httpx.AsyncClient(timeout=60,follow_redirects=True) as client:
        response=await client.get(url,params=params,headers={"Accept":"text/csv","User-Agent":"EP051-DNA-Strategy-Directory/1.0"});response.raise_for_status();return response.text,str(response.url)


async def publish(features,url,token):
    async with httpx.AsyncClient(timeout=30) as client:
        for feature in features:
            response=await client.post(url.rstrip("/")+"/internal/intelligence/market-features",headers={"Authorization":f"Bearer {token}"},json=feature);response.raise_for_status()


def main():
    parser=argparse.ArgumentParser();parser.add_argument("--start",default="2000-01-01");parser.add_argument("--end",default=date.today().isoformat());parser.add_argument("--output",default="runtime/market_features.json");parser.add_argument("--publish-url");parser.add_argument("--token");args=parser.parse_args()
    text,source_url=asyncio.run(fetch(args.start,args.end));features=build_features(load_csv(text));payload={"schema_version":"1.0.0","generated_at":datetime.now(timezone.utc).isoformat(),"market":"FX","source":"European Central Bank EXR daily reference rates","source_url":source_url,"source_version":SOURCE_VERSION,"features":features};payload["sha256"]=hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    target=Path(args.output);target=target if target.is_absolute() else ROOT/target;target.parent.mkdir(parents=True,exist_ok=True);temporary=target.with_suffix(".tmp");temporary.write_text(json.dumps(payload,separators=(",",":")),encoding="utf-8");temporary.replace(target)
    if args.publish_url:
        if not args.token:raise SystemExit("--token is required with --publish-url")
        asyncio.run(publish(features,args.publish_url,args.token))
    print(json.dumps({"output":str(target),"features":len(features),"first":features[0]["as_of"] if features else None,"last":features[-1]["as_of"] if features else None,"sha256":payload["sha256"]}))


if __name__=="__main__":main()

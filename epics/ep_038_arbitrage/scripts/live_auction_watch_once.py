from pathlib import Path
from datetime import datetime
import csv, json, urllib.request

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

WATCH = {
    "watch_id": "WATCH-LIVE-001",
    "spread_id": "SPRD-LIVE-001",
    "item_name": "namedigital.com",
    "asset_type": "domain",
    "marketplace": "Sav domain auctions",
    "marketplace_url": "https://v2.sav.com/domains/auctions",
    "auction_type": "domain auction",
    "current_bid_usd": "355.00",
    "auction_fee_usd": "9.65",
    "total_current_cost_usd": "364.65",
    "bidders": "5",
    "bids": "14",
    "auction_end_date": "2026-06-28",
    "time_left_observed": "1h 33m",
    "hours_to_expiry": "1.55",
    "reference_market": "Sedo public search endpoint",
    "reference_url": "https://sedo.com/search/?language=us&keyword=namedigital",
    "reference_result": "pending",
    "spread_status": "sought_not_quantified",
    "gross_spread_amount_usd": "",
    "gross_spread_pct": "",
    "state": "WATCHING",
    "confidence_score": "42",
    "risk_score": "high",
    "notes": "Script records the selected live-auction proof row. No bid/buy/contact action is performed.",
}

def sedo_reference_check():
    url = "https://sedo.com/search/service/service.php?safe_search=2&synonyms=true&listing_type%5B%5D=1&listing_type%5B%5D=2&listing_type%5B%5D=3&listing_type%5B%5D=5&auction_group%5B%5D=62&auction_event=&price_start=0&price_end=0&price_currency=3&traffic_start=0&traffic_end=0&number_of_words_min=1&number_of_words_max=0&len_min=1&len_max=0&special_characters%5B%5D=3&special_characters%5B%5D=1&special_characters%5B%5D=2&cat%5B%5D=0&cat%5B%5D=0&cat%5B%5D=0&type=0&special_inventory=4&kws=contains&age_min=0&age_max=0&keyword=namedigital&page=1&rel=6&orderdirection=2&domainIds=&cc=&member=&v=0.1&o=json&m=whois&f=getDataBulk"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    try:
        raw = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
        payload = json.loads(raw)
        domains = payload.get("b", {}).get("domainList", [])
        return "Sedo related domains: " + ", ".join(domains) if domains else "No related domains returned"
    except Exception as exc:
        return f"Sedo reference check failed: {type(exc).__name__}: {exc}"

def main():
    DATA.mkdir(exist_ok=True)
    row = dict(WATCH)
    row["observed_at"] = datetime.now().isoformat(timespec="seconds")
    row["reference_result"] = sedo_reference_check()
    watch_path = DATA / "live_auction_watch.csv"
    obs_path = DATA / "live_auction_observations.csv"
    with watch_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        w.writeheader(); w.writerow(row)
    obs = {"observation_id": "OBS-LIVE-001", **row}
    with obs_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(obs.keys()))
        w.writeheader(); w.writerow(obs)
    print(f"Captured live auction watch: {row['item_name']} current bid ${row['current_bid_usd']} time left {row['time_left_observed']} status {row['spread_status']}")

if __name__ == "__main__":
    main()

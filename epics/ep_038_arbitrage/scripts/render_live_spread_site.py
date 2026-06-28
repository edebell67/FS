from pathlib import Path
import csv
import html

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "live_spread_board.csv"
OUT = ROOT / "site_mvp"
OUT.mkdir(exist_ok=True)

COLORS = {
    "LIVE": "#1fed9c",
    "WATCHING": "#ffd166",
    "DISCOVERED": "#7cc7ff",
    "COOLING": "#ff9f43",
    "EXPIRED": "#8a8f98",
    "AVOID": "#ff4d6d",
}


def e(value):
    return html.escape(str(value or ""))


def load_rows():
    with DATA.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def spread_card(row):
    state = e(row["state"])
    color = COLORS.get(row["state"], "#9aa4b2")
    return f"""
<article class="card">
  <div class="topline"><span class="badge" style="--badge:{color}">{state}</span><span>{e(row['category'])}</span></div>
  <h3>{e(row['item_name'])}</h3>
  <p class="variant">{e(row['variant'])}</p>
  <div class="prices">
    <div><small>Marketplace</small><strong>{e(row['marketplace_price'])} {e(row['currency'])}</strong></div>
    <div><small>Source</small><strong>{e(row['source_price'])} {e(row['currency'])}</strong></div>
    <div><small>Gross spread</small><strong>{e(row['gross_spread_pct'])}%</strong></div>
  </div>
  <p class="summary">{e(row['public_card_summary'])}</p>
  <div class="urgency"><b>Time pressure:</b> {e(row.get('urgency_level', 'low'))} · {e(row.get('expiry_type', '') or 'not time-sensitive')} · {e(row.get('hours_to_expiry', '') or 'no countdown')}h</div>
  <dl>
    <div><dt>Confidence</dt><dd>{e(row['confidence_score'])}/100</dd></div>
    <div><dt>Risk</dt><dd>{e(row['risk_score'])}</dd></div>
    <div><dt>Last checked</dt><dd>{e(row['last_checked'])}</dd></div>
    <div><dt>Availability</dt><dd>{e(row['source_availability'])}</dd></div>
  </dl>
  <p class="risk"><b>Risk note:</b> {e(row['risk_notes'])}</p>
  <div class="links"><a href="{e(row['marketplace_url'])}">Marketplace</a><a href="{e(row['source_url'])}">Source/check</a></div>
</article>"""


def layout(title, body, active):
    def nav(name):
        return "active" if active == name else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <header class="nav">
    <a class="logo" href="index.html">EP038</a>
    <nav>
      <a class="{nav('home')}" href="index.html">Home</a>
      <a class="{nav('board')}" href="live-spreads.html">Live board</a>
      <a class="{nav('method')}" href="methodology.html">Methodology</a>
      <a class="{nav('preferences')}" href="preferences.html">Preferences</a>
    </nav>
  </header>
  {body}
  <footer><b>Information product only.</b> EP038 provides pricing-spread research and market information. It does not guarantee profit and does not instruct users to buy, sell, list, or transact.</footer>
</body>
</html>"""


def write_css():
    (OUT / "styles.css").write_text("""
:root{color-scheme:dark;--bg:#070b12;--panel:#101722;--muted:#9aa4b2;--text:#eef3ff;--line:#223044;--accent:#7cf7d4;--gold:#ffd166}*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at top left,#16213b,#070b12 45%,#05070b);font-family:Inter,ui-sans-serif,system-ui,Segoe UI,Arial,sans-serif;color:var(--text)}a{color:var(--accent);text-decoration:none}.nav{position:sticky;top:0;z-index:3;display:flex;justify-content:space-between;align-items:center;padding:18px 5vw;background:rgba(7,11,18,.84);backdrop-filter:blur(14px);border-bottom:1px solid var(--line)}.logo{font-weight:900;letter-spacing:.12em;color:#fff}.nav nav{display:flex;gap:18px}.active{color:#fff;border-bottom:2px solid var(--accent)}.hero{padding:80px 5vw 40px;display:grid;grid-template-columns:1.1fr .9fr;gap:36px;align-items:center}.eyebrow{color:var(--accent);text-transform:uppercase;letter-spacing:.16em;font-size:13px}h1{font-size:clamp(40px,7vw,82px);line-height:.95;margin:12px 0}h2{font-size:clamp(28px,4vw,48px)}.lead{font-size:clamp(18px,2.4vw,25px);color:#cad4e6;max-width:920px}.cta{display:flex;gap:14px;flex-wrap:wrap;margin-top:28px}.button{padding:14px 20px;border-radius:999px;background:var(--accent);color:#03110d;font-weight:800}.button.secondary{background:#172234;color:#fff;border:1px solid var(--line)}.mock,.panel{border:1px solid var(--line);background:linear-gradient(145deg,#111b2d,#0b111d);border-radius:28px;padding:18px}.metric{display:grid;grid-template-columns:1fr 1fr;gap:12px}.metric div{border:1px solid var(--line);background:rgba(255,255,255,.035);border-radius:20px;padding:18px}.metric strong{display:block;font-size:34px}.section{padding:42px 5vw}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(290px,1fr));gap:18px}.card{border:1px solid var(--line);border-radius:24px;padding:20px;background:linear-gradient(180deg,rgba(255,255,255,.055),rgba(255,255,255,.025));box-shadow:0 20px 60px rgba(0,0,0,.22)}.topline{display:flex;align-items:center;justify-content:space-between;color:var(--muted);font-size:13px}.badge{background:color-mix(in srgb,var(--badge) 18%, transparent);color:var(--badge);border:1px solid var(--badge);padding:6px 10px;border-radius:999px;font-weight:900;font-size:12px}.card h3{font-size:23px;margin:16px 0 2px}.variant,.summary,.risk,footer{color:#b7c2d4}.urgency{margin:12px 0;padding:10px 12px;border:1px solid rgba(255,209,102,.45);background:rgba(255,209,102,.08);border-radius:14px;color:#ffe29a;font-size:13px}.prices{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:18px 0}.prices div{background:#0b111d;border:1px solid var(--line);border-radius:14px;padding:10px}.prices small{display:block;color:var(--muted);font-size:11px}.prices strong{font-size:18px}dl{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:14px 0}dl div{background:rgba(255,255,255,.035);border-radius:12px;padding:9px}dt{color:var(--muted);font-size:11px}dd{margin:0;font-size:13px}.links{display:flex;gap:10px;margin-top:16px}.links a{border:1px solid var(--line);border-radius:999px;padding:9px 12px;background:#0b111d}.notice{border-left:4px solid var(--gold);padding:18px;background:rgba(255,209,102,.08);border-radius:14px}.step{padding:18px}footer{padding:30px 5vw;border-top:1px solid var(--line);margin-top:40px}@media(max-width:800px){.hero{grid-template-columns:1fr;padding-top:48px}.nav{align-items:flex-start;gap:12px;flex-direction:column}.prices,dl{grid-template-columns:1fr}.metric{grid-template-columns:1fr}}
""", encoding="utf-8")


def main():
    rows = load_rows()
    live = sum(1 for row in rows if row["state"] == "LIVE")
    watching = sum(1 for row in rows if row["state"] == "WATCHING")
    active_states = {"DISCOVERED", "WATCHING", "LIVE", "COOLING"}
    active_rows = [row for row in rows if row["state"] in active_states]
    active_spread_value = sum(float(row["gross_spread_amount"]) for row in active_rows if row.get("gross_spread_amount"))
    all_time_spread_value = sum(float(row["gross_spread_amount"]) for row in rows if row.get("gross_spread_amount"))
    time_sensitive_rows = [row for row in active_rows if row.get("time_sensitive") == "yes" and row.get("expiry_value_status") != "expired"]
    time_sensitive_value = sum(float(row["gross_spread_amount"]) for row in time_sensitive_rows if row.get("gross_spread_amount"))
    expiring_24h_rows = [row for row in time_sensitive_rows if row.get("hours_to_expiry") and float(row["hours_to_expiry"]) <= 24]
    expiring_24h_value = sum(float(row["gross_spread_amount"]) for row in expiring_24h_rows if row.get("gross_spread_amount"))
    next_expiry = min([float(row["hours_to_expiry"]) for row in expiring_24h_rows if row.get("hours_to_expiry")], default=None)
    avg = round(sum(int(row["confidence_score"]) for row in rows if row["confidence_score"].isdigit()) / len(rows))

    home_body = f"""
<main>
  <section class="hero">
    <div>
      <p class="eyebrow">Digital information product</p>
      <h1>£{active_spread_value:,.0f} gross spread value currently active.</h1>
      <p class="lead">£{expiring_24h_value:,.0f} of that active spread value is time-sensitive and marked as expiring within 24h. EP038 publishes the spread, the count, and the time pressure behind each opportunity signal.</p>
      <div class="cta"><a class="button" href="live-spreads.html">View sample board</a><a class="button secondary" href="preferences.html">Set alert preferences</a></div>
    </div>
    <aside class="mock"><div class="metric"><div><small>Active gross spread value</small><strong>£{active_spread_value:,.0f}</strong></div><div><small>Active spread count</small><strong>{len(active_rows)}</strong></div><div><small>Expiring within 24h</small><strong>£{expiring_24h_value:,.0f}</strong></div><div><small>Time-sensitive count</small><strong>{len(time_sensitive_rows)}</strong></div></div></aside>
  </section>
  <section class="section"><div class="notice"><b>Research information only.</b> No profit is guaranteed. Prices, stock, fees, delivery, resale rights and platform rules must be verified before acting.</div></section>
  <section class="section"><h2>Sample spread products</h2><div class="grid">{''.join(spread_card(row) for row in rows[:3])}</div></section>
</main>"""
    board_body = f"""<main><section class="section"><p class="eyebrow">Sample MVP board</p><h1>Live Spread Board</h1><p class="lead">Currently tracking {len(active_rows)} active spread candidates with £{active_spread_value:,.0f} gross spread value identified. £{expiring_24h_value:,.0f} is marked as expiring within 24h across {len(expiring_24h_rows)} time-sensitive records.</p><div class="notice"><b>Value means observed gross spread, not profit.</b> Figures are before fees, stock, delivery, rights, authenticity and platform checks. Time pressure indicates expiry risk, not an instruction to trade.</div><div class="grid">{''.join(spread_card(row) for row in rows)}</div></section></main>"""
    method_body = """<main><section class="section"><p class="eyebrow">How EP038 works</p><h1>Methodology</h1><p class="lead">The product is information provision: repeatable discovery, scoring, freshness, source memory and risk filtering.</p><div class="grid"><article class="panel step"><h3>Find spreads</h3><p>Compare observed marketplace prices against lower-cost acquisition sources.</p></article><article class="panel step"><h3>Score confidence</h3><p>Balance spread size, demand evidence, source reliability, policy status and risk.</p></article><article class="panel step"><h3>Track state</h3><p>Every spread moves through DISCOVERED, WATCHING, LIVE, COOLING, EXPIRED or AVOID.</p></article><article class="panel step"><h3>Publish information</h3><p>Customers receive research leads and must verify prices, stock, fees and rules before action.</p></article></div><section class="notice" style="margin-top:28px"><b>Preferred spread alerts.</b> Subscribers choose categories, marketplaces, minimum spread value, confidence, risk and expiry window. EP038 then notifies them when matching spread candidates appear or are about to expire.</section><section class="notice" style="margin-top:28px"><b>Not trading execution.</b> EP038 does not trade for users, guarantee outcomes, or instruct transactions. Internal test trading may later be used only to validate signal quality.</section></section></main>"""


    preferences_body = f"""<main><section class="section"><p class="eyebrow">Subscriber alerts</p><h1>Tell EP038 what spreads you want.</h1><p class="lead">Subscribers will be notified when preferred spread candidates become available, cross a threshold, or approach expiry.</p><div class="grid"><article class="panel"><h3>Preference controls</h3><ul><li>Categories: trainers, domains, digital products, electronics, collectibles</li><li>Minimum spread value and percentage</li><li>Minimum confidence / maximum risk</li><li>Time-sensitive only or expiry window</li><li>Marketplaces and source types</li></ul></article><article class="panel"><h3>Example alert</h3><p><b>Trainer spread matched:</b> £31 gross spread · 25.8% · auction closes in 6h · confidence 67/100.</p><p class="risk">Research information only. Verify price, stock, fees, delivery, authenticity, rights and platform rules before acting. No profit is guaranteed.</p></article><article class="panel"><h3>MVP capture fields</h3><p>Email/channel, category filters, marketplace filters, min spread %, min spread value, confidence threshold, risk ceiling, expiry window, frequency.</p></article></div><div class="notice" style="margin-top:28px"><b>Current build:</b> preferences are modelled in <code>data/subscriber_preferences.csv</code>. The local matcher writes would-send events to <code>data/alert_events.csv</code>; no real notifications are sent yet.</div></section></main>"""

    (OUT / "index.html").write_text(layout("EP038 — Live Spread Intelligence", home_body, "home"), encoding="utf-8")
    (OUT / "live-spreads.html").write_text(layout("EP038 — Live Spread Board", board_body, "board"), encoding="utf-8")
    (OUT / "methodology.html").write_text(layout("EP038 — Methodology", method_body, "method"), encoding="utf-8")
    (OUT / "preferences.html").write_text(layout("EP038 — Alert Preferences", preferences_body, "preferences"), encoding="utf-8")
    write_css()
    print(f"Generated {OUT} with {len(rows)} spread records")


if __name__ == "__main__":
    main()

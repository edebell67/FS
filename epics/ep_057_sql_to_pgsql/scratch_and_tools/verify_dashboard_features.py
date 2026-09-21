from bs4 import BeautifulSoup
import json

path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

print("1. Criteria buttons:", bool(soup.find(id='criteriaNetBtn')), bool(soup.find(id='criteriaWinBtn')))
print("2. Date tabs container:", bool(soup.find(id='dateTabsContainer')))
print("3. Directional split buttons:", bool(soup.find(id='metricAll')), bool(soup.find(id='metricBuy')), bool(soup.find(id='metricSell')), bool(soup.find(id='metricTriSplit')))
print("4. Delta toggle buttons:", bool(soup.find(id='toggleNetDeltaBtn')), bool(soup.find(id='toggleBuyDeltaBtn')), bool(soup.find(id='toggleSellDeltaBtn')))
print("5. Replay controls:", bool(soup.find(id='playBtn')), bool(soup.find(id='stepBackBtn')), bool(soup.find(id='stepFwdBtn')), bool(soup.find(id='restartBtn')))
print("6. Scrubber & Baseline:", bool(soup.find(id='scrubberTrack')), bool(soup.find(id='baselineMarker')), bool(soup.find(id='setBaseAtHeadBtn')))
print("7. Win rate slider:", bool(soup.find(id='winRateSlider')))
print("8. Model cards container:", bool(soup.find(id='modelCardsContainer')))
print("9. Canvas element:", bool(soup.find(id='top10Canvas')))
print("10. File size bytes:", len(content))

# Verify that ALL_CRITERIA_DATA exists in script
assert "const ALL_CRITERIA_DATA =" in content
assert "const ALL_DATE_DATA =" in content
assert "function setRankingCriteria(" in content
assert "function startReplay(" in content
print("11. Script validation: All functions, variables and data blocks confirmed present!")

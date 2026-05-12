import psycopg2
from datetime import datetime
import json

# Database Configuration
DB_CONFIG = {
    'dbname': 'bizpa',
    'user': 'postgres',
    'password': 'admin6093',
    'host': 'localhost',
    'port': '5432'
}

def get_analytics():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        # Query counts per page_id
        query = """
        SELECT page_id, COUNT(*) as count, MIN(captured_at) as first_lead, MAX(captured_at) as last_lead
        FROM leads_pain_points
        GROUP BY page_id
        ORDER BY count DESC;
        """
        
        cur.execute(query)
        rows = cur.fetchall()
        
        print("\n" + "="*80)
        print(f" EP017 LEAD CAPTURE ANALYTICS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print(f"{'Page ID':<30} | {'Leads':<10} | {'First Lead':<20} | {'Last Lead':<20}")
        print("-" * 80)
        
        total_leads = 0
        for row in rows:
            page_id, count, first, last = row
            first_str = first.strftime('%Y-%m-%d %H:%M') if first else 'N/A'
            last_str = last.strftime('%Y-%m-%d %H:%M') if last else 'N/A'
            print(f"{page_id:<30} | {count:<10} | {first_str:<20} | {last_str:<20}")
            total_leads += count
            
        print("-" * 80)
        print(f"{'TOTAL':<30} | {total_leads:<10}")
        print("="*80 + "\n")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error fetching analytics: {e}")

if __name__ == "__main__":
    get_analytics()

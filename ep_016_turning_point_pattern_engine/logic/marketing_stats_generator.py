import json
import os
import sys
from datetime import datetime, timedelta

import psycopg2
from psycopg2.extras import RealDictCursor

# ---------------------------------------------------
# Configuration
# ---------------------------------------------------
DB_CONFIG = {
    "dbname": "pattern_engine",
    "user": "postgres",
    "password": "admin6093",
    "host": "localhost",
    "port": "5432",
}

OUTPUT_DIR = r"C:\Users\edebe\eds\epics\ep_016_turning_point_pattern_engine\outputs"
STATS_PACK_FILENAME = "ep016_marketing_stats_pack.json"


class StatsGenerator:
    """Generates strictly LIVE-ONLY marketing statistics for Epic 016."""
    
    def __init__(self):
        self.conn = psycopg2.connect(**DB_CONFIG, cursor_factory=RealDictCursor)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def __del__(self):
        if hasattr(self, "conn") and self.conn:
            self.conn.close()

    def get_core_stats(self):
        cur = self.conn.cursor()
        
        # 1. Last LIVE Snapshot
        cur.execute("""
            SELECT snapshot_time, created_at 
            FROM frequency_snapshots 
            WHERE market_mode = 'LIVE'
            ORDER BY snapshot_time DESC LIMIT 1
        """)
        latest = cur.fetchone()
        
        # 2. Volume Counts (Live Only)
        cur.execute("SELECT COUNT(*) as total FROM frequency_snapshots WHERE market_mode = 'LIVE'")
        total_snapshots = cur.fetchone()["total"]
        
        cur.execute("""
            SELECT COUNT(DISTINCT product_id) as active 
            FROM frequency_snapshots 
            WHERE market_mode = 'LIVE' AND snapshot_time > NOW() - INTERVAL '15 minutes'
        """)
        active_products = cur.fetchone()["active"]
        
        # 3. Latency
        freshness_sec = 0
        db_latency_sec = 0
        if latest:
            freshness_sec = (datetime.now() - latest["snapshot_time"]).total_seconds()
            db_latency_sec = (latest["created_at"] - latest["snapshot_time"]).total_seconds()

        return {
            "run_mode": "LIVE",
            "engine_status": "Active" if freshness_sec < 600 else "Stale",
            "last_snapshot_time": latest["snapshot_time"].isoformat() if latest else None,
            "active_monitored_products": active_products,
            "total_live_snapshots": total_snapshots,
            "data_freshness_seconds": round(max(0, freshness_sec), 1),
            "db_write_latency_seconds": round(db_latency_sec, 1)
        }

    def get_coverage_stats(self):
        cur = self.conn.cursor()
        
        cur.execute("SELECT COUNT(*) as total FROM products WHERE is_active = TRUE")
        monitored = cur.fetchone()["total"]
        
        cur.execute("""
            SELECT COUNT(DISTINCT t.product_id) as turn_active 
            FROM turning_points t
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
            WHERE s.market_mode = 'LIVE'
        """)
        turn_active = cur.fetchone()["turn_active"]
        
        return {
            "products_under_monitoring": monitored,
            "products_with_live_patterns": turn_active,
            "market_coverage_pct": round((turn_active / monitored * 100), 1) if monitored > 0 else 0
        }

    def get_detection_stats(self):
        cur = self.conn.cursor()
        
        # Join with snapshots to ensure we only count turns created in LIVE mode
        cur.execute("""
            SELECT COUNT(*) as total 
            FROM turning_points t 
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time 
            WHERE s.market_mode = 'LIVE'
        """)
        total = cur.fetchone()["total"]
        
        cur.execute("""
            SELECT COUNT(*) as tops 
            FROM turning_points t 
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time 
            WHERE s.market_mode = 'LIVE' AND t.turn_type = 'TOP'
        """)
        tops = cur.fetchone()["tops"]
        
        cur.execute("""
            SELECT COUNT(*) as bottoms 
            FROM turning_points t 
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time 
            WHERE s.market_mode = 'LIVE' AND t.turn_type = 'BOTTOM'
        """)
        bottoms = cur.fetchone()["bottoms"]
        
        return {
            "total_live_turns_detected": total,
            "live_tops_identified": tops,
            "live_bottoms_identified": bottoms,
            "directional_balance_ratio": round(tops / bottoms, 2) if bottoms > 0 else 1.0
        }

    def get_performance_stats(self):
        """Calculates authentic live outcomes only."""
        cur = self.conn.cursor()
        
        cur.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(*) filter (WHERE outcome_5m_pips > 0 AND turn_type = 'BOTTOM' OR outcome_5m_pips < 0 AND turn_type = 'TOP') as hold_5m,
                COUNT(*) filter (WHERE outcome_10m_pips > 0 AND turn_type = 'BOTTOM' OR outcome_10m_pips < 0 AND turn_type = 'TOP') as hold_10m,
                AVG(ABS(outcome_10m_pips)) as avg_move_10m
            FROM turning_points t
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
            WHERE s.market_mode = 'LIVE' AND outcome_5m_pips IS NOT NULL
        """)
        res = cur.fetchone()
        
        total = res["total"] or 0
        hold_5m_pct = (res["hold_5m"] / total * 100) if total > 0 else 0
        hold_10m_pct = (res["hold_10m"] / total * 100) if total > 0 else 0
        
        return {
            "verified_sample_size": total,
            "structural_stability_5m_pct": round(hold_5m_pct, 1),
            "structural_stability_10m_pct": round(hold_10m_pct, 1),
            "avg_move_captured_pips": round(float(res["avg_move_10m"] or 0), 2)
        }

    def get_quality_stats(self):
        cur = self.conn.cursor()
        
        cur.execute("""
            SELECT AVG(t.confirmation_delay_minutes) as avg_delay 
            FROM turning_points t 
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time 
            WHERE s.market_mode = 'LIVE'
        """)
        avg_delay = cur.fetchone()["avg_delay"]
        
        # Quality score from features
        cur.execute("""
            SELECT AVG(f.pattern_quality_score) as avg_quality 
            FROM pattern_features f
            JOIN turning_points t ON t.turn_id = f.turn_id
            JOIN frequency_snapshots s ON s.product_id = t.product_id AND s.snapshot_time = t.turn_time
            WHERE s.market_mode = 'LIVE'
        """)
        avg_quality = cur.fetchone()["avg_quality"]
        
        return {
            "avg_confirm_delay_minutes": round(float(avg_delay or 0), 1),
            "avg_structural_quality_score": round(float(avg_quality or 0), 3)
        }

    def generate_full_pack(self):
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Generating Epic 016 LIVE-ONLY Marketing Stat Pack...")
        
        pack = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "report_type": "LIVE_ONLY",
                "engine_version": "EP016_V1"
            },
            "engine_health": self.get_core_stats(),
            "live_coverage": self.get_coverage_stats(),
            "live_detection": self.get_detection_stats(),
            "live_quality": self.get_quality_stats(),
            "live_performance_claims": self.get_performance_stats()
        }
        
        output_path = os.path.join(OUTPUT_DIR, STATS_PACK_FILENAME)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(pack, f, indent=2)
            
        print(f"LIVE Stat pack saved to: {output_path}")
        return pack


if __name__ == "__main__":
    gen = StatsGenerator()
    gen.generate_full_pack()

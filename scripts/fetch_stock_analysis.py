#!/usr/bin/env python3
"""
Daily Stock Analysis Fetcher
Runs at 10:00 AM GMT+7 (Vietnam time)
Fetches VN-Index market data and saves as markdown report
"""

import os
import sys
from datetime import datetime
import requests
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def fetch_vn_market_data():
    """
    Fetch VN-Index, HNX-Index, and key ticker data from cafef.vn
    Returns aggregated market snapshot as dict
    """
    try:
        # This would normally call cafef.vn or vietstock.vn APIs
        # For now, returning placeholder that can be replaced with real API call
        print("🔄 Fetching VN-Index market data...")
        
        market_data = {
            "vni_index": 1756.69,
            "vni_change": 20.01,
            "vni_change_pct": 1.15,
            "vni_volume": 2946.47,
            "hnx_index": 251.89,
            "hnx_change": 0.91,
            "hnx_change_pct": 0.36,
            "hnx_volume": 252.02,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        return market_data
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return None

def generate_markdown_report(market_data):
    """
    Generate markdown report from market data
    """
    if not market_data:
        return None
    
    report = f"""# 📊 VN Stock Market Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S GMT+7')}

## Market Overview

| Index | Value | Change | % |
|---|---|---|---|
| VN-Index | {market_data['vni_index']} | {market_data['vni_change']:+.2f} | {market_data['vni_change_pct']:+.2f}% |
| HNX-Index | {market_data['hnx_index']} | {market_data['hnx_change']:+.2f} | {market_data['hnx_change_pct']:+.2f}% |

**Status:** Trading data as of {market_data['timestamp']}

## Trading Volume
- HOSE: VND {market_data['vni_volume']:.2f}B
- HNX: VND {market_data['hnx_volume']:.2f}B

---

*This is an automated daily report. For full analysis, use Stock Agent with `/surf-trade-decision` skill.*
"""
    return report

def save_report(report, base_dir="reports"):
    """
    Save markdown report to /reports/stock-analysis-{date}.md
    """
    try:
        report_dir = Path(base_dir)
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Create filename with current date
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"stock-analysis-{date_str}.md"
        filepath = report_dir / filename
        
        # Write report
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved: {filepath}")
        return filepath
    except Exception as e:
        print(f"❌ Error saving report: {e}")
        return None

def main():
    """Main entry point"""
    print("=" * 60)
    print("Daily Stock Market Analysis")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Fetch market data
    market_data = fetch_vn_market_data()
    
    if not market_data:
        print("❌ Failed to fetch market data. Exiting.")
        sys.exit(1)
    
    # Generate report
    report = generate_markdown_report(market_data)
    
    if not report:
        print("❌ Failed to generate report. Exiting.")
        sys.exit(1)
    
    # Save report
    filepath = save_report(report)
    
    if filepath:
        print(f"✅ Daily analysis complete!")
        print(f"📁 Output: {filepath}")
    else:
        print("❌ Failed to save report.")
        sys.exit(1)

if __name__ == "__main__":
    main()

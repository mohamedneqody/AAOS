import logging
from typing import Dict, Any

logger = logging.getLogger("KPIEngine")

class KPIEngineCapability:
    def execute(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        logger.info("KPIEngineCapability executing")
        metrics = payload.get("normalized_metrics", {})
        
        views = metrics.get("views", 0)
        clicks = metrics.get("clicks", 0)
        conversions = metrics.get("conversions", 0)
        revenue = metrics.get("revenue", 0.0)
        cost = metrics.get("cost", 0.0)
        total_assets = metrics.get("assets_produced", 1)
        
        ctr = (clicks / views * 100) if views > 0 else 0.0
        roi = ((revenue - cost) / cost * 100) if cost > 0 else 0.0
        epc = (revenue / clicks) if clicks > 0 else 0.0
        conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0.0
        cpa = (cost / total_assets) if total_assets > 0 else 0.0
        
        logger.info(f"KPIs - ROI: {roi:.2f}%, CTR: {ctr:.2f}%, EPC: ${epc:.2f}, Conv: {conversion_rate:.2f}%, Cost/Asset: ${cpa:.2f}")
        
        return {
            "status": "SUCCESS", 
            "derived_kpis": {
                "roi_percentage": roi,
                "ctr_percentage": ctr,
                "epc_dollars": epc,
                "conversion_rate_percentage": conversion_rate,
                "cost_per_asset": cpa,
                "net_profit": revenue - cost
            }
        }

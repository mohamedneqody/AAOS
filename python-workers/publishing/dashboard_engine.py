import uuid
from shared_libs.core.contracts.publishing import PublishingContext, DashboardModel, DashboardLayout

class DashboardEngine:
    def generate(self, context: PublishingContext) -> DashboardModel:
        """
        Pure Python. Generates structural DashboardModel.
        Never calculates metrics, never generates UI code.
        Dynamically applies LocalizationConfig and BrandingConfig.
        """
        cards = []
        for dec in context.decision_package.business_decisions:
            cards.append({
                "card_id": str(uuid.uuid4()),
                "title": f"Decision: {dec.decision_type}",
                "value": dec.status,
                "color": context.branding.primary_color,
                "currency": context.localization.currency
            })
            
        tables = []
        # Create a table summarizing approved recommendations
        row_data = []
        for rec in context.decision_package.approved_recommendations:
            row_data.append({
                "id": rec.recommendation_id,
                "title": rec.title,
                "priority": str(round(rec.priority, 2)),
                "effort": rec.effort
            })
            
        tables.append({
            "table_id": str(uuid.uuid4()),
            "columns": ["ID", "Title", "Priority", "Effort"],
            "rows": row_data
        })
        
        risk_panels = []
        for risk in context.decision_package.risk_assessments:
            risk_panels.append({
                "panel_id": str(uuid.uuid4()),
                "category": risk.category,
                "severity": risk.severity,
                "description": risk.description
            })
            
        opportunity_panels = []
        for opp in context.decision_package.opportunity_assessments:
            opportunity_panels.append({
                "panel_id": str(uuid.uuid4()),
                "description": opp.description,
                "value": opp.potential_value
            })

        # Layout mapping
        layout = DashboardLayout(
            pages=["Executive Overview", "Detailed Analysis", "Actions"],
            sections=["Top KPIs", "Risk Register", "Opportunity Log"],
            widgets=[c["card_id"] for c in cards],
            panels=[p["panel_id"] for p in risk_panels],
            filters=["Date Range", "Category"],
            navigation=["Home", "Reports", "Settings"]
        )
        
        return DashboardModel(
            dashboard_id=str(uuid.uuid4()),
            cards=cards,
            tables=tables,
            risk_panels=risk_panels,
            opportunity_panels=opportunity_panels,
            recommendation_panels=[],
            trend_panels=[],
            layout=layout,
            charts=[] # Charts are attached later in domain by ChartEngine
        )

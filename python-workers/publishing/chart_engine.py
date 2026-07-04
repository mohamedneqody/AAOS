import uuid
from typing import List
from shared_libs.core.contracts.publishing import PublishingContext, ChartModel

class ChartEngine:
    def generate(self, context: PublishingContext) -> List[ChartModel]:
        """
        Pure Python. Generates structural Chart specifications ONLY.
        NO matplotlib, NO Plotly, NO UI Rendering.
        """
        charts = []
        
        # Aggregate priority data across all insights for a basic Bar Chart visualization
        priorities = context.decision_package.priority_scores
        if priorities:
            charts.append(ChartModel(
                chart_id=str(uuid.uuid4()),
                title="Priority Distribution",
                chart_type="Bar",
                series=[{
                    "name": "Final Score",
                    "data": [p.final_score for p in priorities]
                }],
                x_axis={"categories": [p.insight_id[:8] for p in priorities], "title": "Insights"},
                y_axis={"title": "Priority Score"},
                legend={"enabled": True, "position": "bottom"},
                tooltip={"enabled": True},
                filters={},
                theme=context.branding.theme,
                locale=context.localization.locale
            ))
            
        # Aggregate action execution phases
        phases = {}
        for action in context.decision_package.business_actions:
            phases[action.execution_group] = phases.get(action.execution_group, 0) + 1
            
        if phases:
            charts.append(ChartModel(
                chart_id=str(uuid.uuid4()),
                title="Execution Phases",
                chart_type="Pie",
                series=[{
                    "name": "Actions",
                    "data": [{"name": k, "y": v} for k, v in phases.items()]
                }],
                x_axis={},
                y_axis={},
                legend={"enabled": True},
                tooltip={"enabled": True},
                filters={},
                theme=context.branding.theme,
                locale=context.localization.locale
            ))
            
        return charts

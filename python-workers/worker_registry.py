from workers.data_worker import DataWorker
from workers.analytics_worker import AnalyticsWorker
from workers.document_worker import DocumentWorker
from workers.strategy_worker import StrategyWorker
from workers.planning_worker import PlanningWorker
from workers.revenue_worker import RevenueWorker
from workers.production_worker import ProductionWorker
from workers.quality_worker import QualityWorker
from workers.publisher_worker import PublisherWorker
from workers.kpi_worker import KpiWorker

worker_registry = {
    "data": DataWorker(),
    "analytics": AnalyticsWorker(),
    "document": DocumentWorker(),
    "strategy": StrategyWorker(),
    "planning": PlanningWorker(),
    "revenue": RevenueWorker(),
    "production": ProductionWorker(),
    "quality": QualityWorker(),
    "publisher": PublisherWorker(),
    "kpi": KpiWorker()
}

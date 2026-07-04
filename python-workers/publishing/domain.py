import uuid
import time
from datetime import datetime, timezone
from shared_libs.core.contracts.decision import DecisionPackage
from shared_libs.core.contracts.publishing import (
    PublishingPackage, PublishingContext, BrandingConfig, LocalizationConfig, PublishingMetadata, PublishingAudit
)

from publishing.dashboard_engine import DashboardEngine
from publishing.chart_engine import ChartEngine
from publishing.summary_engine import SummaryEngine
from publishing.pdf_engine import PDFEngine
from publishing.presentation_engine import PresentationEngine
from publishing.notification_engine import NotificationEngine
from publishing.export_engine import ExportEngine
from publishing.registries import RendererRegistry, TemplateRegistry

class PublishingDomain:
    def __init__(self):
        self.dashboard_engine = DashboardEngine()
        self.chart_engine = ChartEngine()
        self.summary_engine = SummaryEngine()
        self.pdf_engine = PDFEngine()
        self.presentation_engine = PresentationEngine()
        self.notification_engine = NotificationEngine()
        self.renderer_registry = RendererRegistry()
        self.template_registry = TemplateRegistry()
        self.export_engine = ExportEngine(self.renderer_registry)

    def process(self, decision_package: DecisionPackage, branding: BrandingConfig, localization: LocalizationConfig) -> PublishingPackage:
        start_ms = time.time() * 1000
        
        # 1. Validation of Template
        template_name = branding.theme
        if not self.template_registry.is_supported(template_name):
            # Fallback securely or flag. For strictness we could reject, but to not break existing backward compatibility we just pass it
            # The prompt requested validation, but also not to break existing APIs.
            # We'll default to WhiteLabel if it's completely missing, though ConfigDict forbids extra.
            if template_name not in ["Dark", "Light"]:
                template_name = "WhiteLabel" # Default fallback for custom names not strictly in registry to prevent breakage

        # 2. Context Creation
        metadata = PublishingMetadata(
            publish_id=str(uuid.uuid4()),
            published_at=datetime.now(timezone.utc).isoformat(),
            template_used=template_name
        )
        context = PublishingContext(
            decision_package=decision_package,
            branding=branding,
            localization=localization,
            metadata=metadata
        )
        
        # 2. Pipeline Execution
        dashboard = self.dashboard_engine.generate(context)
        charts = self.chart_engine.generate(context)
        dashboard.charts = charts # Attach charts to dashboard
        
        summary = self.summary_engine.generate(context)
        
        pdf = self.pdf_engine.generate(context, summary)
        presentation = self.presentation_engine.generate(context)
        notifications = self.notification_engine.generate(context)
        artifacts, manifests = self.export_engine.generate(context)
        
        # 3. Audit Logging
        end_ms = time.time() * 1000
        audit = PublishingAudit(
            request_id=str(uuid.uuid4()),
            trace_id=decision_package.package_id, # Link back to decision
            rendered_by="AAOS_Publishing_Domain",
            generated_at=datetime.now(timezone.utc).isoformat(),
            duration_ms=round(end_ms - start_ms, 2)
        )
        
        # 4. Package Assembly
        return PublishingPackage(
            package_id=str(uuid.uuid4()),
            planning_id=context.decision_package.planning_id,
            dashboard=dashboard,
            executive_summary=summary,
            pdf_report=pdf,
            presentation=presentation,
            notifications=notifications,
            export_artifacts=artifacts,
            export_manifests=manifests,
            audit=audit
        )

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ConfigDict, Field
from shared_libs.core.contracts.decision import DecisionPackage

class PublishingBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: str = "1.0"

# Multi-Tenant & Branding Context
class BrandingConfig(PublishingBase):
    tenant_id: str
    organization_id: str
    workspace_id: str
    user_id: str
    subscription_plan: str
    company_name: str
    logo_url: str
    primary_color: str
    secondary_color: str
    theme: str
    typography: str
    brand_assets: Dict[str, Any]

class LocalizationConfig(PublishingBase):
    locale: str
    language: str
    currency: str
    timezone: str
    rtl: bool
    number_format: str
    date_format: str

class PublishingVersion(PublishingBase):
    schema_version: str = "1.0"
    template_version: str = "1.0"
    renderer_version: str = "1.0"
    generation_version: str = "1.0"

class PublishingMetadata(PublishingBase):
    publish_id: str
    published_at: str
    template_used: str
    versions: PublishingVersion = Field(default_factory=PublishingVersion)

class PublishingContext(PublishingBase):
    decision_package: DecisionPackage
    branding: BrandingConfig
    localization: LocalizationConfig
    metadata: PublishingMetadata

# Chart Models
class ChartModel(PublishingBase):
    chart_id: str
    title: str
    chart_type: str # Bar, Line, Area, Pie, Scatter, Heatmap, Waterfall, Treemap, Radar
    series: List[Dict[str, Any]]
    x_axis: Dict[str, Any]
    y_axis: Dict[str, Any]
    legend: Dict[str, Any]
    tooltip: Dict[str, Any]
    filters: Dict[str, Any]
    theme: str
    locale: str

# Dashboard Models
class DashboardLayout(PublishingBase):
    pages: List[str]
    sections: List[str]
    widgets: List[str]
    panels: List[str]
    filters: List[str]
    navigation: List[str]

class DashboardModel(PublishingBase):
    dashboard_id: str
    cards: List[Dict[str, Any]]
    tables: List[Dict[str, Any]]
    risk_panels: List[Dict[str, Any]]
    opportunity_panels: List[Dict[str, Any]]
    recommendation_panels: List[Dict[str, Any]]
    trend_panels: List[Dict[str, Any]]
    layout: DashboardLayout
    charts: List[ChartModel]

# Document Models
class ExecutiveSummary(PublishingBase):
    summary_id: str
    title: str
    content: str
    key_highlights: List[str]

class ReportSection(PublishingBase):
    section_id: str
    title: str
    content: str
    charts: List[str] # References to ChartModel IDs

class PDFDocumentModel(PublishingBase):
    document_id: str
    title: str
    author: str
    summary: ExecutiveSummary
    sections: List[ReportSection]
    tables: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]
    appendix: str

# Presentation Models
class PresentationSlide(PublishingBase):
    slide_id: str
    slide_type: str # Overview, KPIs, Risks, Recommendations, Actions, Roadmap
    title: str
    content: Dict[str, Any]

class PresentationModel(PublishingBase):
    presentation_id: str
    title: str
    slides: List[PresentationSlide]

# Notification Models
class NotificationMessage(PublishingBase):
    message_id: str
    channel: str # Telegram, Slack, Teams, Discord, Email
    verbosity: str # Executive, Manager, Technical
    subject: str
    body: str
    decision_ids: List[str]

# Asset and Export Models
class AssetReference(PublishingBase):
    asset_id: str
    asset_type: str
    uri: str
    mime_type: str
    checksum: str

class ExportArtifact(PublishingBase):
    artifact_id: str
    artifact_type: str
    payload: Dict[str, Any] # Structured JSON ready for renderer

class ExportManifest(PublishingBase):
    manifest_id: str
    artifact_id: str
    artifact_type: str
    mime_type: str
    renderer: str
    template: str
    checksum: str
    generated_at: str
    version: str

# Audit Model
class PublishingAudit(PublishingBase):
    request_id: str
    trace_id: str
    rendered_by: str
    generated_at: str
    duration_ms: float

# Final Package
class PublishingPackage(PublishingBase):
    package_id: str
    planning_id: str
    dashboard: DashboardModel
    executive_summary: ExecutiveSummary
    pdf_report: PDFDocumentModel
    presentation: PresentationModel
    notifications: List[NotificationMessage]
    export_artifacts: List[ExportArtifact]
    export_manifests: List[ExportManifest]
    audit: PublishingAudit

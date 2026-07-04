import uuid
from shared_libs.core.contracts.publishing import PublishingContext, PresentationModel, PresentationSlide

class PresentationEngine:
    def generate(self, context: PublishingContext) -> PresentationModel:
        """
        Pure Python. Generates structural Presentation models.
        DOES NOT render PPTX files natively.
        """
        slides = []
        
        # Overview Slide
        slides.append(PresentationSlide(
            slide_id=str(uuid.uuid4()),
            slide_type="Overview",
            title=f"{context.branding.company_name} Strategy",
            content={"theme": context.branding.theme, "message": "Executive Board Presentation"}
        ))
        
        # Risks Slide
        if context.decision_package.risk_assessments:
            slides.append(PresentationSlide(
                slide_id=str(uuid.uuid4()),
                slide_type="Risks",
                title="Risk Register",
                content={"risks": [{"cat": r.category, "sev": r.severity} for r in context.decision_package.risk_assessments]}
            ))
            
        # Roadmap Slide
        if context.decision_package.business_actions:
            slides.append(PresentationSlide(
                slide_id=str(uuid.uuid4()),
                slide_type="Roadmap",
                title="Action Plan Phases",
                content={"actions": [{"phase": a.execution_group, "owner": a.owner} for a in context.decision_package.business_actions]}
            ))
            
        return PresentationModel(
            presentation_id=str(uuid.uuid4()),
            title=f"{context.branding.company_name} Presentation",
            slides=slides
        )

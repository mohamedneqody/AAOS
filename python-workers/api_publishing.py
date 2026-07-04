from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ValidationError
from shared_libs.core.contracts.decision import DecisionPackage
from shared_libs.core.contracts.publishing import PublishingPackage, BrandingConfig, LocalizationConfig
from publishing.domain import PublishingDomain

router = APIRouter()
publishing_domain = PublishingDomain()

class PublishingRequest(BaseModel):
    decision_package: DecisionPackage
    branding: BrandingConfig
    localization: LocalizationConfig

@router.post("/api/publishing/generate", response_model=PublishingPackage)
def generate_publishing(request: PublishingRequest):
    try:
        package = publishing_domain.process(request.decision_package, request.branding, request.localization)
        return package
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PublishingEngine failure: {str(e)}")

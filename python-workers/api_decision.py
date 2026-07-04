from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from shared_libs.core.contracts.intelligence import InsightPackage
from shared_libs.core.contracts.decision import DecisionPackage
from decision.domain import DecisionDomain

router = APIRouter()
decision_domain = DecisionDomain()

@router.post("/api/decision/analyze", response_model=DecisionPackage)
def analyze_decision(package: InsightPackage):
    try:
        decision_package = decision_domain.process(package)
        return decision_package
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DecisionEngine failure: {str(e)}")

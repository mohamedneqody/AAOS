import os
import json
import urllib.request
import uuid
from datetime import datetime, timezone
import google.auth
from google.auth.transport.requests import Request

from shared_libs.core.contracts.intelligence import CandidateInsights, Insight

class InsightEngine:
    def __init__(self):
        self.project_id = "gen-lang-client-0319131014"
        self.location = "us-central1"
        self.model = "gemini-2.5-pro"

    def _call_vertex(self, prompt: str) -> str:
        credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
        credentials.refresh(Request())
        access_token = credentials.token
        
        url = f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/publishers/google/models/{self.model}:generateContent"
        
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.1,
                "responseMimeType": "application/json"
            }
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        
        res = urllib.request.urlopen(req)
        data = json.loads(res.read())
        return data['candidates'][0]['content']['parts'][0]['text']

    def generate(self, context_str: str) -> CandidateInsights:
        prompt = f"""
        You are the Insight Engine of the AAOS Intelligence Domain.
        You are receiving a strict ExecutionResult context.
        You MUST NEVER calculate KPIs, statistics, or revenue.
        You may ONLY interpret the deterministic summaries provided below.
        Generate business observations, trends, anomalies, opportunities, risks, and recommendations.
        Every finding, risk, opportunity, and recommendation MUST reference an available `evidence_id` exactly as listed in the available_evidence_ids.
        
        Context:
        {context_str}
        
        Output MUST be a valid JSON matching this schema exactly without markdown wrapping:
        {{
            "insights": [
                {{
                    "insight_id": "string",
                    "category": "string",
                    "summary": "string",
                    "findings": [ {{"finding_id": "string", "title": "string", "description": "string", "severity": "string", "evidence_links": [{{"evidence_id": "string", "relevance": 1.0, "description": "string"}}]}} ],
                    "recommendations": [ {{"recommendation_id": "string", "action": "string", "expected_impact": "string", "evidence_links": [{{"evidence_id": "string", "relevance": 1.0, "description": "string"}}]}} ],
                    "risks": [ {{"risk_id": "string", "description": "string", "probability": "string", "impact": "string", "evidence_links": [{{"evidence_id": "string", "relevance": 1.0, "description": "string"}}]}} ],
                    "opportunities": [ {{"opportunity_id": "string", "description": "string", "potential_value": "string", "evidence_links": [{{"evidence_id": "string", "relevance": 1.0, "description": "string"}}]}} ]
                }}
            ]
        }}
        """
        
        try:
            text = self._call_vertex(prompt)
            # Clean markdown if vertex AI mistakenly wraps it despite responseMimeType
            if text.startswith("```json"):
                text = text[7:-3]
            parsed = json.loads(text)
            
            insights = []
            for i in parsed.get("insights", []):
                insights.append(Insight(**i))
                
            return CandidateInsights(
                package_id=str(uuid.uuid4()),
                generated_at=datetime.now(timezone.utc).isoformat(),
                insights=insights
            )
        except Exception as e:
            raise RuntimeError(f"InsightEngine Vertex AI failure: {e}")

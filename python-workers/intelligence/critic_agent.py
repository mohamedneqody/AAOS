import os
import json
import urllib.request
import uuid
from datetime import datetime, timezone
import google.auth
from google.auth.transport.requests import Request

from shared_libs.core.contracts.intelligence import CriticReport, InsightCriticism, CandidateInsights

class CriticAgent:
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
                "temperature": 0.0,
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

    def evaluate(self, candidates: CandidateInsights, context_str: str) -> CriticReport:
        prompt = f"""
        You are the Critic Agent.
        Your job is to challenge every Insight.
        Detect contradictions, hallucinated metrics, and unsupported conclusions.
        You MUST NEVER generate new insights.
        Only approve, reject, or request clarification.
        
        Context: {context_str}
        
        Insights to Evaluate:
        {candidates.model_dump_json()}
        
        Output MUST be a valid JSON matching this schema exactly without markdown wrapping:
        {{
            "criticisms": [
                {{
                    "insight_id": "string",
                    "status": "approved", // or "rejected", "clarification_requested"
                    "reason": "string",
                    "contradictions": ["string"],
                    "hallucinations": ["string"]
                }}
            ]
        }}
        """
        
        try:
            text = self._call_vertex(prompt)
            if text.startswith("```json"):
                text = text[7:-3]
            parsed = json.loads(text)
            
            criticisms = []
            approved = 0
            rejected = 0
            for c in parsed.get("criticisms", []):
                crit = InsightCriticism(**c)
                criticisms.append(crit)
                if crit.status == "approved":
                    approved += 1
                else:
                    rejected += 1
                
            return CriticReport(
                report_id=str(uuid.uuid4()),
                evaluated_at=datetime.now(timezone.utc).isoformat(),
                criticisms=criticisms,
                total_approved=approved,
                total_rejected=rejected
            )
        except Exception as e:
            raise RuntimeError(f"CriticAgent Vertex AI failure: {e}")

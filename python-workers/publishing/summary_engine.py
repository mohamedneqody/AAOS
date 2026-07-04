import json
import uuid
import google.auth
from google.auth.transport.requests import Request
import urllib.request
from typing import Dict, Any

from shared_libs.core.contracts.publishing import PublishingContext, ExecutiveSummary

class SummaryEngine:
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
            "generationConfig": {"temperature": 0.0}
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
        
        try:
            res = urllib.request.urlopen(req)
            response_data = json.loads(res.read().decode())
            text = response_data['candidates'][0]['content']['parts'][0]['text']
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"SummaryEngine Vertex AI failure: {e.read().decode()}")

    def generate(self, context: PublishingContext) -> ExecutiveSummary:
        """
        Uses Gemini 2.5 Pro ONLY to rewrite existing executive data into a narrative summary.
        MUST enforce locale language. MUST NOT calculate KPIs.
        """
        raw_data = {
            "decisions": [d.decision_type for d in context.decision_package.business_decisions],
            "recommendations": [r.title for r in context.decision_package.approved_recommendations],
            "actions": [a.category for a in context.decision_package.business_actions]
        }
        
        prompt = f"""
        You are an executive assistant rewriting raw decision data into an Executive Summary.
        
        RAW DATA:
        {json.dumps(raw_data, indent=2)}
        
        STRICT RULES:
        1. DO NOT calculate KPIs.
        2. DO NOT invent metrics, risks, or priorities.
        3. DO NOT invent recommendations.
        4. You ONLY format the provided content.
        5. The output MUST be entirely written in this language/locale: {context.localization.language} ({context.localization.locale}).
        
        Output MUST be a valid JSON matching this schema exactly without markdown wrapping:
        {{
            "title": "string (Executive Title)",
            "content": "string (Narrative paragraph summary)",
            "key_highlights": ["string", "string", "string"]
        }}
        """
        
        response_json = self._call_vertex(prompt)
        try:
            parsed = json.loads(response_json)
        except Exception as e:
            raise RuntimeError(f"Failed to parse LLM response: {response_json}") from e
            
        return ExecutiveSummary(
            summary_id=str(uuid.uuid4()),
            title=parsed.get("title", "Executive Summary"),
            content=parsed.get("content", ""),
            key_highlights=parsed.get("key_highlights", [])
        )

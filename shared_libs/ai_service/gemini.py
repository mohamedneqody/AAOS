import os
import requests
import json
import logging
from typing import Type, TypeVar
from pydantic import BaseModel, ValidationError
from google.oauth2 import service_account
from google.auth.transport.requests import Request

from shared_libs.core.exceptions import (
    LLMValidationException,
    LLMAuthenticationException,
    LLMTransportException
)
from shared_libs.ai_service.providers.base import BaseLLMProvider

logger = logging.getLogger("GeminiProvider")

T = TypeVar("T", bound=BaseModel)

def pydantic_to_gemini_schema(schema, defs=None):
    if defs is None:
        defs = schema.pop("$defs", {})
    if "$ref" in schema:
        ref_key = schema["$ref"].split("/")[-1]
        schema.pop("$ref")
        schema.update(defs.get(ref_key, {}))
    schema.pop("additionalProperties", None)
    schema.pop("title", None)
    schema.pop("default", None)
    
    if "type" in schema:
        t = schema["type"]
        if t == "string": schema["type"] = "STRING"
        elif t == "integer": schema["type"] = "INTEGER"
        elif t == "number": schema["type"] = "NUMBER"
        elif t == "boolean": schema["type"] = "BOOLEAN"
        elif t == "array": schema["type"] = "ARRAY"
        elif t == "object": schema["type"] = "OBJECT"
        elif t == "null": schema["type"] = "STRING" # workaround
    
    if "properties" in schema:
        for k, v in schema["properties"].items():
            schema["properties"][k] = pydantic_to_gemini_schema(v, defs)
    if "items" in schema:
        schema["items"] = pydantic_to_gemini_schema(schema["items"], defs)
    if schema.get("type") == "ARRAY" and "items" not in schema:
        schema["items"] = {"type": "STRING"}
        
    # Gemini requires nested objects to explicitly have type: OBJECT if properties exist
    if "properties" in schema and "type" not in schema:
        schema["type"] = "OBJECT"
        
    # Remove unsupported keys
    schema.pop("anyOf", None)
    schema.pop("allOf", None)
    schema.pop("oneOf", None)
    return schema

class GeminiProvider(BaseLLMProvider):
    def get_token(self):
        sa_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'python-workers', 'sa.json')
        if not os.path.exists(sa_path):
            sa_path = '/app/sa.json' # fallback for container execution
        if os.path.exists(sa_path):
            try:
                creds = service_account.Credentials.from_service_account_file(
                    sa_path,
                    scopes=['https://www.googleapis.com/auth/generative-language']
                )
                request = Request()
                creds.refresh(request)
                return creds.token
            except Exception as e:
                raise LLMAuthenticationException(f"Failed to authenticate with Service Account: {e}")
        return None

    def generate_structured(self, prompt: str, response_model: Type[T], model_name: str = "gemini-flash-latest", temperature: float = 0.7, max_tokens: int = 8192) -> T:
        if "1.5" in model_name:
            # model_name = "gemini-2.5-flash" # REMOVED to avoid 20 requests per day limit!
            pass
            
        token = self.get_token()
        from shared_libs.core.config import ConfigService
        api_key = ConfigService.get_gemini_api_key()
        
        headers = {"Content-Type": "application/json"}
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        
        if token:
            headers["Authorization"] = f"Bearer {token}"
        elif api_key and api_key != "your_gemini_api_key_here":
            url += f"?key={api_key}"
        else:
            raise LLMAuthenticationException("GEMINI_API_KEY is not set or invalid. Cannot execute real AI call.")

        schema = response_model.model_json_schema()
        gemini_schema = pydantic_to_gemini_schema(schema)
        
        # Gemini specific structured output payload
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens,
                "responseMimeType": "application/json",
                "responseSchema": gemini_schema
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            err_msg = str(e)
            if hasattr(e, 'response') and getattr(e, 'response') is not None:
                err_msg += f"\nResponse: {e.response.text}"
            raise LLMTransportException(f"Network error calling Gemini API: {err_msg}")
            
        try:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            raise LLMTransportException(f"Malformed response format from Gemini API: {e}")
            
        try:
            # Layer 2 Validation: Pydantic Validation (no text manipulation, just pure validation)
            validated_obj = response_model.model_validate_json(text)
            return validated_obj
        except ValidationError as e:
            raise LLMValidationException(f"Failed to validate LLM output against {response_model.__name__}: {e}\nRaw output: {text}")

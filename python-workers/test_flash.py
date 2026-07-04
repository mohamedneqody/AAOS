import urllib.request, json
import sys
sys.path.append('/app')
from shared_libs.ai_service.gemini import GeminiProvider
import pydantic

class Dummy(pydantic.BaseModel):
    test: str

provider = GeminiProvider()
try:
    res = provider.generate_structured(prompt='Test', response_model=Dummy, model_name='gemini-flash-latest')
    print('SUCCESS!', res)
except Exception as e:
    print('FAILED:', e)

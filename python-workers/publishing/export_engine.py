import uuid
import json
import hashlib
from typing import Tuple, List
from datetime import datetime, timezone
from shared_libs.core.contracts.publishing import PublishingContext, ExportManifest, ExportArtifact
from publishing.registries import RendererRegistry

class ExportEngine:
    def __init__(self, registry: RendererRegistry):
        self.registry = registry

    def _compute_checksum(self, payload: dict) -> str:
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode('utf-8')).hexdigest()

    def generate(self, context: PublishingContext) -> Tuple[List[ExportArtifact], List[ExportManifest]]:
        """
        Pure Python. Configures ExportArtifact and ExportManifest metadata list.
        Does not physically write files to disk.
        """
        artifacts = []
        manifests = []
        
        # JSON Export (Full Package)
        art_id_json = str(uuid.uuid4())
        json_payload = context.decision_package.model_dump()
        artifacts.append(ExportArtifact(
            artifact_id=art_id_json,
            artifact_type="JSON_DUMP",
            payload=json_payload
        ))
        
        renderer_api = "APIRenderer" if self.registry.is_supported("APIRenderer") else "FallbackJSON"
        
        manifests.append(ExportManifest(
            manifest_id=str(uuid.uuid4()),
            artifact_id=art_id_json,
            artifact_type="JSON_DUMP",
            mime_type="application/json",
            renderer=renderer_api,
            template="None",
            checksum=self._compute_checksum(json_payload),
            generated_at=datetime.now(timezone.utc).isoformat(),
            version="1.0"
        ))
        
        # Example PDF Metadata
        art_id_pdf = str(uuid.uuid4())
        pdf_payload = {"report": "PDFDocumentModel_reference_here"}
        artifacts.append(ExportArtifact(
            artifact_id=art_id_pdf,
            artifact_type="PDF_REPORT",
            payload=pdf_payload
        ))
        
        renderer_pdf = "PDFRenderer" if self.registry.is_supported("PDFRenderer") else "FallbackPDF"
        
        manifests.append(ExportManifest(
            manifest_id=str(uuid.uuid4()),
            artifact_id=art_id_pdf,
            artifact_type="PDF_REPORT",
            mime_type="application/pdf",
            renderer=renderer_pdf,
            template=context.branding.theme,
            checksum=self._compute_checksum(pdf_payload),
            generated_at=datetime.now(timezone.utc).isoformat(),
            version="1.0"
        ))
        
        return artifacts, manifests

from fastapi import APIRouter
import uuid
import base64

from app.models.manifest_models import (
    CreateManifestRequest, CreateManifestResponse,
    PrintManifestRequest, PrintManifestResponse
)
from app.classes.authorization_config import AuthorizationConfig
from app.resources import test_resources

router = APIRouter()

@router.post("/CreateManifest", response_model=CreateManifestResponse)
async def create_manifest(request: CreateManifestRequest):
    # Authenticate user
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return CreateManifestResponse(error_message=f"Authorization failed for token {request.authorization_token}")

    # In a real implementation, you would contact the carrier API to create a manifest
    # Here we'll just generate a random manifest reference
    manifest_reference = uuid.uuid4().hex[:10].upper()
    
    return CreateManifestResponse(manifest_reference=manifest_reference)

@router.post("/PrintManifest", response_model=PrintManifestResponse)
async def print_manifest(request: PrintManifestRequest):
    # Authenticate user
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return PrintManifestResponse(error_message=f"Authorization failed for token {request.authorization_token}")

    # In a real implementation, you would generate or retrieve a PDF manifest document
    # Here we'll just return a sample PDF document
    return PrintManifestResponse(
        pdf_base64=base64.b64encode(test_resources.SAMPLE_MANIFEST).decode('utf-8')
    )
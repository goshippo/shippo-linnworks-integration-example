from typing import Optional, List
from pydantic import BaseModel
from app.models.base_models import BaseRequest, BaseResponse

class CreateManifestRequest(BaseRequest):
    order_ids: List[str]

class CreateManifestResponse(BaseResponse):
    manifest_reference: Optional[str] = None

class PrintManifestRequest(BaseRequest):
    manifest_reference: str

class PrintManifestResponse(BaseResponse):
    pdf_base64: Optional[str] = None
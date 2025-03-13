from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from app.models.base_models import BaseRequest, BaseResponse

class ConsignmentAddress(BaseModel):
    address_id: Optional[str] = None
    full_name: str
    company_name: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    address_line3: Optional[str] = None
    city: str
    region: Optional[str] = None
    postal_code: str
    country_code: str
    telephone: Optional[str] = None
    email: Optional[str] = None

class ConsignmentPackage(BaseModel):
    package_reference: str
    weight: float
    length: float
    width: float
    height: float
    description: str
    value: float
    currency_code: str
    ext_properties: Optional[Dict[str, str]] = None

class GenerateLabelRequest(BaseRequest):
    service_id: str
    reference1: str
    reference2: Optional[str] = None
    reference3: Optional[str] = None
    sender: ConsignmentAddress
    recipient: ConsignmentAddress
    packages: List[ConsignmentPackage]
    shipping_date: str
    ext_properties: Optional[Dict[str, str]] = None

class LabelResponse(BaseModel):
    tracking_number: str
    package_reference: str
    image_base64: str
    format: str

class GenerateLabelResponse(BaseResponse):
    consignment_reference: Optional[str] = None
    labels: List[LabelResponse] = []

class CancelLabelRequest(BaseRequest):
    consignment_reference: str

class CancelLabelResponse(BaseResponse):
    pass
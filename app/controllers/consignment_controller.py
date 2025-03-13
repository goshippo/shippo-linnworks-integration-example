from fastapi import APIRouter, HTTPException
import base64
import uuid
from PIL import Image
from io import BytesIO

from app.models.consignment_models import (
    GenerateLabelRequest, GenerateLabelResponse,
    CancelLabelRequest, CancelLabelResponse,
    LabelResponse
)
from app.classes.authorization_config import AuthorizationConfig
from app.services.courier_service import get_services
from app.resources import test_resources

router = APIRouter()

@router.post("/GenerateLabel", response_model=GenerateLabelResponse)
async def generate_label(request: GenerateLabelRequest):
    try:
        # Authenticate user
        auth = AuthorizationConfig.load(request.authorization_token)
        if not auth:
            return GenerateLabelResponse(error_message=f"Authorization failed for token {request.authorization_token}")

        # Get available services
        services = get_services()
        
        # Find the requested service
        selected_service = next((s for s in services if s.service_unique_id == request.service_id), None)
        if not selected_service:
            return GenerateLabelResponse(error_message=f"Service Id {request.service_id} is not available")

        # Get service details
        service_code = selected_service.service_code
        vendor_code = selected_service.service_group
        
        # Create response
        response = GenerateLabelResponse()
        response.consignment_reference = str(uuid.uuid4())
        
        # Generate a label for each package
        for package in request.packages:
            # Create a label for this package
            label = LabelResponse(
                tracking_number=f"TRK{uuid.uuid4().hex[:10].upper()}",
                package_reference=package.package_reference,
                image_base64=base64.b64encode(test_resources.SAMPLE_LABEL).decode('utf-8'),
                format="PDF"
            )
            response.labels.append(label)
        
        return response
    
    except Exception as ex:
        return GenerateLabelResponse(error_message=f"Error generating label: {str(ex)}")

def image_to_byte_array(image):
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

@router.post("/CancelLabel", response_model=CancelLabelResponse)
async def cancel_label(request: CancelLabelRequest):
    try:
        # Authenticate user
        auth = AuthorizationConfig.load(request.authorization_token)
        if not auth:
            return CancelLabelResponse(error_message=f"Authorization failed for token {request.authorization_token}")

        # In a real implementation, you would contact the carrier API to cancel the label
        # Here we'll just return a success response
        return CancelLabelResponse()
    
    except Exception as ex:
        return CancelLabelResponse(error_message=f"Error cancelling label: {str(ex)}")
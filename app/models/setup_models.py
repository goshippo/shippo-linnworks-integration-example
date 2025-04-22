from typing import Optional, List, Any
from pydantic import BaseModel
from app.models.base_models import BaseRequest, BaseResponse

class ConfigItem(BaseModel):
    config_item_id: str
    selected_value: str

class AddNewUserRequest(BaseRequest):
    email: str
    linnworks_unique_identifier: str
    account_name: str

class AddNewUserResponse(BaseResponse):
    authorization_token: Optional[str]

class UserConfigRequest(BaseRequest):
    pass

class UserConfigStage(BaseModel):
    config_items: List[Any] = []
    name: str
    title: str
    
class UserConfigResponse(BaseResponse):
    config_stage: Optional[UserConfigStage]
    is_config_active: bool = False
    config_status: Optional[str]

class UpdateConfigRequest(BaseRequest):
    config_status: str
    config_items: List[ConfigItem]

class UpdateConfigResponse(BaseResponse):
    pass

class ConfigDeleteRequest(BaseRequest):
    pass

class ConfigDeleteResponse(BaseResponse):
    pass

class UserAvailableServicesRequest(BaseRequest):
    pass

class CourierServiceModel(BaseModel):
    service_unique_id: str
    service_name: str
    service_code: str
    service_group: str
    service_description: str

class UserAvailableServicesResponse(BaseResponse):
    services: List[CourierServiceModel] = []

class ExtendedPropertyMapping(BaseModel):
    property_name: str
    property_title: str
    property_type: str
    property_description: str

class ExtendedPropertyMappingRequest(BaseRequest):
    pass

class ExtendedPropertyMappingResponse(BaseResponse):
    items: List[ExtendedPropertyMapping] = []
from fastapi import APIRouter, HTTPException
import uuid

from app.models.setup_models import (
    AddNewUserRequest, AddNewUserResponse,
    UserConfigRequest, UserConfigResponse, 
    UpdateConfigRequest, UpdateConfigResponse,
    ConfigDeleteRequest, ConfigDeleteResponse,
    UserAvailableServicesRequest, UserAvailableServicesResponse,
    ExtendedPropertyMappingRequest, ExtendedPropertyMappingResponse,
    ExtendedPropertyMapping
)
from app.classes.authorization_config import AuthorizationConfig
from app.classes.config_stages import ConfigStageFactory
from app.services.courier_service import get_services

router = APIRouter()

@router.post("/AddNewUser", response_model=AddNewUserResponse)
async def add_new_user(request: AddNewUserRequest):
    try:
        new_config = AuthorizationConfig.create_new(
            request.email, 
            request.linnworks_unique_identifier, 
            request.account_name
        )
        return AddNewUserResponse(authorization_token=str(new_config.authorization_token))
    except Exception as ex:
        return AddNewUserResponse(error_message=f"AddNewUser error: {str(ex)}")

@router.post("/UserConfig", response_model=UserConfigResponse)
async def user_config(request: UserConfigRequest):
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return UserConfigResponse(error_message=f"Authorization failed for token {request.authorization_token}")

    if not auth.is_config_active:
        if auth.config_status == "":
            auth.config_status = "ContactStage"
            auth.save()

        # Get the appropriate config stage handler
        config_stage = ConfigStageFactory.get_config_stage(auth.config_status)
        if config_stage:
            return UserConfigResponse(
                config_stage=config_stage.get_user_config_stage(auth),
                is_config_active=False,
                config_status=auth.config_status
            )
        else:
            return UserConfigResponse(error_message=f"Config stage is not handled: {auth.config_status}")
    else:
        # Config is in completed stage (active config)
        user_config_stage = ConfigStageFactory.get_user_config_stage(auth)
        return UserConfigResponse(
            config_stage=user_config_stage,
            is_config_active=True,
            config_status="CONFIG"
        )

@router.post("/UpdateConfig", response_model=UpdateConfigResponse)
async def update_config(request: UpdateConfigRequest):
    try:
        auth = AuthorizationConfig.load(request.authorization_token)
        if not auth:
            return UpdateConfigResponse(error_message=f"Authorization failed for token {request.authorization_token}")

        # Ensure config stage is consistent
        if auth.config_status != request.config_status:
            return UpdateConfigResponse(error_message="Current config stage is not what is sent in the Update")

        # Handle specific stages
        if auth.config_status == "ContactStage":
            # Handle contact stage
            auth.account_name = next((item.selected_value for item in request.config_items if item.config_item_id == "NAME"), "")
            auth.address_line1 = next((item.selected_value for item in request.config_items if item.config_item_id == "ADDRESS1"), "")
            auth.config_status = "ValuesStage"
            auth.save()
            return UpdateConfigResponse()
            
        elif auth.config_status == "ValuesStage":
            # Validate int value
            int_value_str = next((item.selected_value for item in request.config_items if item.config_item_id == "INTVALUE"), "0")
            try:
                int_value = int(int_value_str)
                if int_value < 10:
                    return UpdateConfigResponse(error_message="Some Int Value must be greater than 10. This is just some validation on the integration side;")
            except ValueError:
                return UpdateConfigResponse(error_message="Some Int Value is not an int. WTF?")
                
            auth.config_status = "DescriptionStage"
            auth.save()
            return UpdateConfigResponse()
            
        elif auth.config_status == "DescriptionStage":
            # Final step - activate config
            auth.is_config_active = True
            auth.config_status = "CONFIG"
            auth.save()
            return UpdateConfigResponse()
            
        elif auth.config_status == "CONFIG" or auth.is_config_active:
            # Update config properties for active config
            auth.account_name = next((item.selected_value for item in request.config_items if item.config_item_id == "NAME"), auth.account_name)
            auth.address_line1 = next((item.selected_value for item in request.config_items if item.config_item_id == "ADDRESS1"), auth.address_line1)
            auth.save()
            return UpdateConfigResponse()
            
        else:
            return UpdateConfigResponse(error_message=f"{auth.config_status} is not handled")
            
    except Exception as ex:
        return UpdateConfigResponse(error_message=f"Unhandled exception saving user config: {str(ex)}")

@router.post("/ConfigDelete", response_model=ConfigDeleteResponse)
async def config_delete(request: ConfigDeleteRequest):
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return ConfigDeleteResponse(error_message=f"Authorization failed for token {request.authorization_token}")
    
    AuthorizationConfig.delete(request.authorization_token)
    return ConfigDeleteResponse()

@router.post("/UserAvailableServices", response_model=UserAvailableServicesResponse)
async def user_available_services(request: UserAvailableServicesRequest):
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return UserAvailableServicesResponse(error_message=f"Authorization failed for token {request.authorization_token}")
    
    return UserAvailableServicesResponse(services=get_services())

@router.post("/ExtendedPropertyMapping", response_model=ExtendedPropertyMappingResponse)
async def extended_property_mapping(request: ExtendedPropertyMappingRequest):
    auth = AuthorizationConfig.load(request.authorization_token)
    if not auth:
        return ExtendedPropertyMappingResponse(error_message=f"Authorization failed for token {request.authorization_token}")
    
    # Return predefined extended property mappings
    return ExtendedPropertyMappingResponse(
        items=[
            ExtendedPropertyMapping(
                property_name="SafePlace1",
                property_title="Safe Place note",
                property_type="ORDER",
                property_description="Safe place note for delivery"
            ),
            ExtendedPropertyMapping(
                property_name="ExtendedCover",
                property_title="Extended Cover flag",
                property_type="ITEM",
                property_description="Identifies whether the item requires Extended Cover. Set to 1 if required."
            )
        ]
    )
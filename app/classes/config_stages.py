from typing import Dict, Any, Optional, List
from app.models.setup_models import UserConfigStage, ConfigItem

class ConfigStageBase:
    @staticmethod
    def get_user_config_stage(auth) -> UserConfigStage:
        raise NotImplementedError("Subclasses must implement this method")

class ContactStage(ConfigStageBase):
    @staticmethod
    def get_user_config_stage(auth) -> UserConfigStage:
        return UserConfigStage(
            name="ContactStage",
            title="Contact Information",
            config_items=[
                {
                    "configItemId": "NAME",
                    "title": "Account Name",
                    "type": "TEXT",
                    "description": "The name of your account",
                    "selectedValue": auth.account_name if hasattr(auth, 'account_name') else ""
                },
                {
                    "configItemId": "ADDRESS1",
                    "title": "Address Line 1",
                    "type": "TEXT",
                    "description": "Your primary address",
                    "selectedValue": auth.address_line1 if hasattr(auth, 'address_line1') else ""
                }
            ]
        )

class ValuesStage(ConfigStageBase):
    @staticmethod
    def get_user_config_stage(auth) -> UserConfigStage:
        return UserConfigStage(
            name="ValuesStage",
            title="Configuration Values",
            config_items=[
                {
                    "configItemId": "INTVALUE",
                    "title": "Some Int Value",
                    "type": "TEXT",
                    "description": "Enter a number greater than 10",
                    "selectedValue": "15"
                }
            ]
        )

class DescriptionStage(ConfigStageBase):
    @staticmethod
    def get_user_config_stage(auth) -> UserConfigStage:
        return UserConfigStage(
            name="DescriptionStage",
            title="Final Step",
            config_items=[
                {
                    "configItemId": "DESCRIPTION",
                    "title": "Configuration Description",
                    "type": "TEXT",
                    "description": "A description of this configuration",
                    "selectedValue": ""
                }
            ]
        )

class ConfigStageFactory:
    _stages = {
        "ContactStage": ContactStage,
        "ValuesStage": ValuesStage,
        "DescriptionStage": DescriptionStage,
    }
    
    @classmethod
    def get_config_stage(cls, stage_name: str) -> Optional[ConfigStageBase]:
        return cls._stages.get(stage_name)
    
    @classmethod
    def get_user_config_stage(cls, auth) -> UserConfigStage:
        # For active configurations, return a combined view of all settings
        return UserConfigStage(
            name="CONFIG",
            title="Shipping Configuration",
            config_items=[
                {
                    "configItemId": "NAME",
                    "title": "Account Name",
                    "type": "TEXT",
                    "description": "The name of your account",
                    "selectedValue": auth.account_name if hasattr(auth, 'account_name') else ""
                },
                {
                    "configItemId": "ADDRESS1",
                    "title": "Address Line 1",
                    "type": "TEXT",
                    "description": "Your primary address",
                    "selectedValue": auth.address_line1 if hasattr(auth, 'address_line1') else ""
                }
            ]
        )
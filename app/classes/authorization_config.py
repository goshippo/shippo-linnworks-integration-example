import os
import json
import uuid
from typing import Optional
import datetime

from app.config import settings

class AuthorizationConfig:
    def __init__(self):
        self.authorization_token = str(uuid.uuid4())
        self.email = ""
        self.linnworks_unique_identifier = ""
        self.account_name = ""
        self.address_line1 = ""
        self.config_status = ""
        self.is_config_active = False
        self.created_date = datetime.datetime.now().isoformat()

    @classmethod
    def create_new(cls, email: str, linnworks_unique_identifier: str, account_name: str) -> 'AuthorizationConfig':
        config = cls()
        config.email = email
        config.linnworks_unique_identifier = linnworks_unique_identifier
        config.account_name = account_name
        config.save()
        return config

    def save(self):
        # Create config directory if it doesn't exist
        os.makedirs(settings.CONFIG_STORAGE_PATH, exist_ok=True)
        
        # Save config to file
        config_file = os.path.join(settings.CONFIG_STORAGE_PATH, f"{self.authorization_token}.json")
        with open(config_file, 'w') as f:
            json.dump(self.__dict__, f)

    @classmethod
    def load(cls, token: str) -> Optional['AuthorizationConfig']:
        if not token:
            return None
            
        config_file = os.path.join(settings.CONFIG_STORAGE_PATH, f"{token}.json")
        
        if not os.path.exists(config_file):
            return None
            
        try:
            with open(config_file, 'r') as f:
                data = json.load(f)
                
            config = cls()
            for key, value in data.items():
                setattr(config, key, value)
                
            return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return None

    @classmethod
    def delete(cls, token: str) -> bool:
        config_file = os.path.join(settings.CONFIG_STORAGE_PATH, f"{token}.json")
        
        if os.path.exists(config_file):
            os.remove(config_file)
            return True
        
        return False
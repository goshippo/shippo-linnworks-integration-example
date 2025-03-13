from typing import List
from app.models.setup_models import CourierServiceModel

def get_services() -> List[CourierServiceModel]:
    """
    Returns a list of available courier services
    """
    return [
        CourierServiceModel(
            service_unique_id="PS-STD",
            service_name="Standard Delivery",
            service_code="STD",
            service_group="PARCELSTATION",
            service_description="Standard 3-5 day delivery service"
        ),
        CourierServiceModel(
            service_unique_id="PS-EXP", 
            service_name="Express Delivery",
            service_code="EXP",
            service_group="PARCELSTATION",
            service_description="Express next day delivery"
        ),
        CourierServiceModel(
            service_unique_id="PS-INT",
            service_name="International Delivery",
            service_code="INT",
            service_group="PARCELSTATION",
            service_description="International 5-7 day delivery"
        )
    ]
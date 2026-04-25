"""
Pydantic data models for request/response validation.
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Order(BaseModel):
    order_id: str
    customer_name: str
    customer_phone: str
    order_details: str
    service_type: str = "all"   # medical / restaurant / business / all
    language: str = "en"        # en / hi / kn / mr / te


class CallLog(BaseModel):
    order_id: str
    call_sid: Optional[str] = None
    speech_result: Optional[str] = None
    intent: Optional[str] = None
    status: str = "pending"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SessionCreate(BaseModel):
    browser_type: str = "chromium"
    headless: bool = True
    user_data_dir: Optional[str] = None

class TabCreate(BaseModel):
    url: Optional[str] = "about:blank"

class SessionResponse(BaseModel):
    session_id: str
    status: str
    tabs: Dict[str, Any] = Field(default_factory=dict)

class TabResponse(BaseModel):
    tab_id: str
    session_id: str
    url: str
    status: str

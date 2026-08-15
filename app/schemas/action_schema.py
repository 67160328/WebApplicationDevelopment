from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class ActionType(str, Enum):
    MOUSE_CLICK = "mouse_click"
    KEY_BINDING = "key_binding"
    DELAY = "delay"

class AutomationStep(BaseModel):
    action_type: ActionType = Field(..., description="Type of action (mouse_click, key_binding, delay)")
    x: Optional[int] = Field(None, description="X coordinate for mouse click")
    y: Optional[int] = Field(None, description="Y coordinate for mouse click")
    key: Optional[str] = Field(None, description="Key identifier for keypress (e.g., 'a', 'enter', 'ctrl+c')")
    duration_ms: Optional[int] = Field(None, description="Delay duration in milliseconds")
    
    # Advanced mouse click fields
    click_count: Optional[int] = Field(1, description="Number of clicks to perform")
    click_interval: Optional[str] = Field("0.0", description="Seconds or range (e.g. 0.5-5) to wait between clicks")
    delay_after: Optional[str] = Field("0.0", description="Seconds or range (e.g. 0.5-5) to wait after click action completes")

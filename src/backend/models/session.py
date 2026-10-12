"""Pydantic models for browserclaw sessions."""
import base64
from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class AgentRole(str, Enum):
    """Roles used in the cognitive loop."""
    OBSERVE = "observe"
    THINK = "think"
    ACT = "act"
    VERIFY = "verify"


class ActionType(str, Enum):
    """Types of actions the agent can perform."""
    CLICK = "click"
    TYPE = "type"
    SCROLL = "scroll"
    WAIT = "wait"
    NAVIGATE = "navigate"
    SCREAMSHOT = "screenshot"


class AgentThought(BaseModel):
    """A single thought/message from the cognitive agent."""
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    id: str
    session_id: str
    role: AgentRole
    content: str
    timestamp: datetime
    element_id: Optional[str] = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ActionStep(BaseModel):
    """A recorded action step within a session."""
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    id: str
    session_id: str
    step_number: int
    action_type: ActionType
    target: Optional[str] = None
    element_id: Optional[str] = None
    description: Optional[str] = None
    status: str = "pending"
    result: Optional[str] = None
    duration_ms: Optional[float] = None
    timestamp: datetime
    screenshot: Optional[str] = None
    error: Optional[str] = None


class Artifact(BaseModel):
    """An artifact (screenshot, document, etc.) produced during a session."""
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    id: str
    session_id: str
    artifact_type: str
    name: str
    data: Optional[str] = None  # base64 for images, text otherwise
    file_path: Optional[str] = None
    mime_type: Optional[str] = None
    created_at: datetime


class Element(BaseModel):
    """An interactive DOM element with its position and attributes."""
    
    id: str
    tag: str
    tag_name: str
    text: str
    label: Optional[str] = None
    role: Optional[str] = None
    attributes: dict[str, str] = Field(default_factory=dict)
    bounds: dict[str, int]  # x, y, width, height
    is_visible: bool
    is_interactive: bool
    parent_id: Optional[str] = None
    children: list["Element"] = Field(default_factory=list)
    xpath: Optional[str] = None
    a11y: dict[str, Any] = Field(default_factory=dict)


class DOMSnapshot(BaseModel):
    """A snapshot of the current DOM state."""
    
    model_config = ConfigDict(from_attributes=True)
    
    url: str
    title: str
    viewport: dict[str, int]
    timestamp: datetime
    elements: list[Element]
    element_count: int
    screenshot: Optional[str] = None


class BrowserState(BaseModel):
    """The current state of the browser."""
    
    model_config = ConfigDict(from_attributes=True)
    
    url: str
    title: str
    viewport: dict[str, int]
    screenshot: Optional[str] = None
    dom_snapshot: Optional[DOMSnapshot] = None


class SessionStatus(str, Enum):
    """Status of a session."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class Session(BaseModel):
    """A browser session."""
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    id: str
    name: str
    task: str
    status: SessionStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    last_activity: datetime
    user_id: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""
    
    model_config = ConfigDict(from_attributes=True)
    
    name: str
    task: str
    user_id: Optional[str] = None
    config: dict[str, Any] = Field(default_factory=dict)


class CreateSessionResponse(BaseModel):
    """Response after creating a session."""
    
    model_config = ConfigDict(from_attributes=True)
    
    session: Session


class DeleteSessionResponse(BaseModel):
    """Response after deleting a session."""
    
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    message: str


class RunRequest(BaseModel):
    """Request to start an agent run within a session."""
    
    model_config = ConfigDict(from_attributes=True)
    
    session_id: str
    task: Optional[str] = None
    target_url: Optional[str] = None
    max_steps: int = 50
    timeout_seconds: int = 300


class StartRunResponse(BaseModel):
    """Response after starting a run."""
    
    model_config = ConfigDict(from_attributes=True)
    
    success: bool
    run_id: Optional[str] = None
    message: str


class LiveMessage(BaseModel):
    """A message streamed over the WebSocket."""
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    
    type: str
    session_id: str
    timestamp: datetime
    data: dict[str, Any] = Field(default_factory=dict)
    screenshot: Optional[str] = None
    thought: Optional[AgentThought] = None
    action_step: Optional[ActionStep] = None
    browser_state: Optional[BrowserState] = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    
    error: str
    detail: Optional[str] = None
    status_code: int

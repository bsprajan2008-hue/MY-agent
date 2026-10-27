from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

# Auth Models
class LoginRequest(BaseModel):
    email: str
    password: str

class SwitchUserRequest(BaseModel):
    user_id: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "teacher"  # teacher, manager, coordinator
    department_id: Optional[str] = None
    weekly_target_hours: float = 35.0
    contracted_teaching_periods: int = 22
    preferred_language: str = "en"

class UserResponse(BaseModel):
    id: str
    org_id: str
    department_id: Optional[str] = None
    department_name: Optional[str] = None
    name: str
    email: str
    role: str
    avatar_url: Optional[str] = None
    weekly_target_hours: float
    contracted_teaching_periods: int
    preferred_language: str
    created_at: Optional[str] = None

# Task Models
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=200)
    description: Optional[str] = ""
    category: str = "teaching"
    assigned_to_id: Optional[str] = None
    collaborators: Optional[List[str]] = []
    estimated_duration_hours: float = Field(..., ge=0.1, le=100.0)
    actual_duration_hours: Optional[float] = 0.0
    due_date: str
    priority: str = "normal"  # critical, high, normal, deferrable
    status: str = "pending"  # pending, in_progress, completed, delegated, cancelled
    is_recurring: bool = False
    assignment_type: str = "formally_assigned"  # formally_assigned, voluntarily_taken, emergency_work, unclear_owner
    completed_within_scheduled_hours: bool = True
    extra_work_reason: Optional[str] = "none"
    private_note: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    assigned_to_id: Optional[str] = None
    collaborators: Optional[List[str]] = None
    estimated_duration_hours: Optional[float] = None
    actual_duration_hours: Optional[float] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    is_recurring: Optional[bool] = None
    assignment_type: Optional[str] = None
    completed_within_scheduled_hours: Optional[bool] = None
    extra_work_reason: Optional[str] = None
    private_note: Optional[str] = None

# Time Log Models
class TimeLogCreate(BaseModel):
    task_id: Optional[str] = None
    log_date: str
    duration_hours: float = Field(..., ge=0.1, le=24.0)
    is_after_hours: bool = False
    reason: str = "routine"
    notes: Optional[str] = None

# Workload Request Models
class WorkloadRequestCreate(BaseModel):
    request_type: str  # clarification, assistance, reassignment, recurring_imbalance, confidential_concern
    assigned_to_manager_id: Optional[str] = None
    task_a_id: Optional[str] = None
    task_b_id: Optional[str] = None
    available_time_hours: Optional[float] = None
    message: str = Field(..., min_length=5)
    access_scope: str = "manager_only"

class WorkloadRequestRespond(BaseModel):
    status: str  # under_review, resolved, reassigned
    manager_response: str

# Reassignment Action Model
class ReassignTaskRequest(BaseModel):
    task_id: str
    new_user_id: str
    reason: str = Field(..., min_length=3)

# 5-Day Experiment Models
class ExperimentEntryCreate(BaseModel):
    day_number: int = Field(..., ge=1, le=5)
    task_title: str
    category: str
    hours_spent: float = Field(..., ge=0.1, le=24.0)
    extra_work_cause: str
    perceived_consequence: Optional[str] = None
    actual_outcome: Optional[str] = None
    candidate_action: str = "keep"  # delegate, reschedule, streamline, keep

# AI Request Models
class AIPromptRequest(BaseModel):
    mode: str = "summarize_workload"  # summarize_workload, draft_request, suggest_questions, propose_rebalancing
    task_id: Optional[str] = None
    target_user_id: Optional[str] = None
    include_private_notes: bool = False  # requires explicit consent!
    user_context: Optional[str] = None

# Organisation Settings Model
class OrgSettingsUpdate(BaseModel):
    standard_weekly_hours: Optional[float] = None
    enable_anonymous_feedback_threshold: Optional[int] = None
    default_language: Optional[str] = None
    working_days: Optional[List[str]] = None

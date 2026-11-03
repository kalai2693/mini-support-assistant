from pydantic import BaseModel, Field


class TicketInfo(BaseModel):
    customer_name: str
    product: str
    issue_type: str
    urgency: int = Field(ge=1, le=5)
    summary: str
from typing import Literal

from model.poi_owner_registration_model import PoiOwnerRegistrationStatus
from pydantic import BaseModel, model_validator


class UpdatePoiPOwnerRegistration(BaseModel):
    status: Literal[
        PoiOwnerRegistrationStatus.APPROVED,
        PoiOwnerRegistrationStatus.REJECTED
    ]
    admin_note: str | None = None

    @model_validator(mode="after")
    def require_rejection_reason(self):
        if (
            self.status == PoiOwnerRegistrationStatus.REJECTED
            and not (self.admin_note or "").strip()
        ):
            raise ValueError("Yêu cầu có lý do từ chối")

        if self.admin_note is not None:
            self.admin_note = self.admin_note.strip()

        return self

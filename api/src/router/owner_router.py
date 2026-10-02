from fastapi import APIRouter

router = APIRouter(prefix="/owner", tags=["Owner Controller"])


@router.get("/registration-status")
async def get_registration_status():
    pass


@router.get("/dashboard")
async def get_owner_dashboard():
    pass


@router.get("/pois")
async def get_owner_pois():
    pass


@router.get("/pois/{poi_id}")
async def get_owner_poi(poi_id: str):
    pass


@router.put("/pois/{poi_id}")
async def update_owner_poi(poi_id: str):
    pass


@router.get("/submissions")
async def get_owner_submissions():
    pass


@router.post("/submissions")
async def create_owner_submission():
    pass


@router.get("/submissions/{submission_id}")
async def get_owner_submission(submission_id: str):
    pass


@router.get("/notifications")
async def get_owner_notifications():
    pass


@router.get("/notifications/unread-count")
async def get_unread_notification_count():
    pass


@router.get("/notifications/{notification_id}")
async def get_owner_notification(notification_id: str):
    pass


@router.patch("/notifications/{notification_id}/read")
async def mark_owner_notification_as_read(notification_id: str):
    pass

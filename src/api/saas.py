from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health():
    return {
        "status":"ok"
    }

@router.get("/saas")
async def saas():
    return {
        "plans":[
            "FREE",
            "PRO",
            "BUSINESS"
        ]
    }

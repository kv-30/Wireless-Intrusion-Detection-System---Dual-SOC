# backend/app/api/routes.py
from fastapi import APIRouter, Query

router = APIRouter()

# Core logic removed for IP protection.
# API endpoints have been stubbed for public release.

@router.get("/bronze")
def get_bronze(
    seconds: int = Query(60),
    start: str | None = Query(None),
    end: str | None = Query(None),
):
    """Fetch raw packets from Bronze layer (stubbed)"""
    return []


@router.get("/silver")
def get_silver(
    seconds: int = Query(60),
    start: str | None = Query(None),
    end: str | None = Query(None),
):
    """Fetch features from Silver layer (stubbed)"""
    return []


@router.get("/gold")
def get_gold(
    seconds: int = Query(300),
    start: str | None = Query(None),
    end: str | None = Query(None),
):
    """Fetch aggregated metrics from Gold layer (stubbed)"""
    return []


@router.get("/debug/ml-check")
def debug_ml_check(seconds: int = Query(300), sample_size: int = Query(20)):
    """ML debug endpoint (stubbed)"""
    return {
        "status": "stubbed",
        "message": "ML debug functionality removed for IP protection",
        "silver": None,
        "ml_response": None,
    }
                "attack_detected": attack_detected,
                "state": "ATTACK" if attack_detected else "NORMAL",
                "confidence": prob_attack,
            },
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
        }
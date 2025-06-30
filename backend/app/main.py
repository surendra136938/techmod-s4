from fastapi import FastAPI, HTTPException, Request
import logging
import json
from app.services.moveservice import MoveService
from app.spamfilters.spamfilterfactory import SpamFilterFactory
from app.spamfilters.spamfilterinterface import SpamFilterInterface
from app.spamfilters.farspamfilter import FARSpamFilter
from app.services.lcsservice import LCSService
from app.routes import include_routers

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Include all routers
include_routers(app)

# --------------------
# Endpoint: /detect_spam
# --------------------
@app.post("/detect_spam")
async def detect_spam(request: Request):
    """
    Receives payloads and processes spam detection logic.
    """
    try:
        post_body = await request.body()
        post_body = post_body.decode("utf-8")
        MoveService.log_info(f"Client is sending post body {post_body}")

        post_body_dict = json.loads(post_body)

        lead_type = post_body_dict.get("lead", {}).get("type", SpamFilterInterface.LEAD_TYPE_CO_BROKE)
        request_guid = post_body_dict.get("request_guid", "")

        spam_filter = SpamFilterFactory.get_spam_filter(lead_type)

        detection_result = spam_filter.filter(post_body_dict['lead'])

        MoveService.log_info(f"detection_result for {lead_type} lead={detection_result['detection_result']}")

        response = {
            "meta": {"build": "1.0.0"},
            "detection_result": detection_result["detection_result"],
        }

        if detection_result["detection_result"] != SpamFilterInterface.NOT_SPAM:
            response["spam_reason"] = detection_result.get("spam_reason", "")

        if "data" in detection_result and detection_result["data"]:
            response["data"] = detection_result["data"]

        if request_guid:
            response["request_guid"] = request_guid

        return response

    except Exception as e:
        logging.error(f"Error during spam detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Endpoint: /detect_far_spam
# --------------------
@app.post("/detect_far_spam")
async def detect_far_spam(request: Request):
    """
    Receives payloads and processes FAR spam detection logic.
    """
    try:
        post_body = await request.body()
        post_body = post_body.decode("utf-8")
        MoveService.log_info(f"FAR client is sending post body {post_body}")

        post_body_dict = json.loads(post_body)

        lead_type = post_body_dict.get("lead", {}).get("type", SpamFilterInterface.LEAD_TYPE_CO_BROKE)
        request_guid = post_body_dict.get("request_guid", "")

        spam_filter = FARSpamFilter(lead_type)
        detection_result = spam_filter.filter(post_body_dict)
        MoveService.log_info(f"FAR detection_result for {lead_type} lead={detection_result}")

        response = {
            "meta": {"build": "1.0.0"},
            "detection_result": detection_result,
        }

        # # Add spam reason if the result is spam
        # if detection_result["detection_result"] != SpamFilterInterface.NOT_SPAM:
        #     response["spam_reason"] = detection_result.get("spam_reason", "")

        # # Add additional data if present
        # if "data" in detection_result and detection_result["data"]:
        #     response["data"] = detection_result["data"]

        if request_guid:
            response["request_guid"] = request_guid

        return response

    except Exception as e:
        logging.error(f"Error during FAR spam detection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
# --------------------
# Endpoint: /resubmit_lead
# --------------------
@app.post("/resubmit_lead")
async def resubmit_lead(request: Request):
    """
    Endpoint to re-submit lead events using LCSService.
    """
    try:
        post_body = await request.body()
        post_body = post_body.decode("utf-8")
        post_body_dict = json.loads(post_body)

        lcs_service = LCSService(post_body_dict)
        connection = lcs_service.connect()

        response = lcs_service.set_response()

        return response

    except Exception as e:
        logging.error(f"Error during lead resubmission: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


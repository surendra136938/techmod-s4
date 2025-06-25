import json
from app.services.moveservice import MoveService
from app.spamfilters.spamfilterfactory import SpamFilterFactory
from app.spamfilters.spamfilterinterface import SpamFilterInterface


class SimpleStopSpamService:
    """
    Service to detect spam using the appropriate spam filter.
    """

    def __init__(self, post_body: str):
        """
        Initialize the SimpleStopSpamService with the given post body.
        """
        MoveService.log_info(f"Client is sending post body {post_body}")
        self.post_body = json.loads(post_body)
        self.request_guid = ""
        self.response = {}
        self.spam_filter = None
        self.spam_detection = None
        self.detection_result = SpamFilterInterface.NOT_SPAM
        self.lead_type = SpamFilterInterface.LEAD_TYPE_CO_BROKE

        # Set lead type if provided in the post body
        if "lead" in self.post_body and "type" in self.post_body["lead"]:
            self.lead_type = self.post_body["lead"]["type"]

        # Get the appropriate spam filter based on the lead type
        self.spam_filter = SpamFilterFactory.get_spam_filter(self.lead_type)

        # Set request GUID if provided in the post body
        if "request_guid" in self.post_body:
            self.request_guid = self.post_body["request_guid"]

    def detect_spam(self):
        """
        Detect spam using the spam filter and set the response.
        """
        # Perform spam detection
        self.detection_result = self.spam_filter.filter(self.post_body)
        self.set_response()

        # Return the response as JSON
        return json.dumps(self.response)

    def set_response(self):
        """
        Set the response based on the detection result.
        """
        MoveService.log_info(
            f"detection_result for {self.lead_type} lead={self.detection_result['detection_result']}"
        )

        # Build the response
        if self.detection_result["detection_result"] == "not_spam":
            self.response = {
                "meta": {"build": "1.0.0"},
                "detection_result": self.detection_result["detection_result"],
            }
        else:
            self.response = {
                "meta": {"build": "1.0.0"},
                "detection_result": self.detection_result["detection_result"],
                "spam_reason": self.detection_result.get("spam_reason", ""),
            }

        # Add additional data if present
        if "data" in self.detection_result and self.detection_result["data"]:
            self.response["data"] = self.detection_result["data"]

        # Add request GUID if present
        if self.request_guid:
            self.response["request_guid"] = self.request_guid
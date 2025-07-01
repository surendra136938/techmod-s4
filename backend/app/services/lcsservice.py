import json
from typing import Dict, Any
from app.services.moveservice import MoveService


class LCSService(MoveService):
    """
    Lead Capture Service for re-submitting lead events.
    """
    def __init__(self, post_body: Dict[str, Any]) -> None:
        """
        Initializes LCSService with lead payload for resubmission.
        """
        super().__init__()  # Call the parent's constructor
        self.post_body = post_body

    def connect(self) -> Dict[str, Any]:
        """
        Connects to Lead Capture Service without authentication.
        """
        return self.connect_without_token()

    def set_response(self) -> Dict[str, Any]:
        """
        Processes and logs the service response.
        """
        super().set_response()

        if isinstance(self.response, dict):
            serialized_response = json.dumps(self.response)
        else:
            serialized_response = self.response

        MoveService.log_info(serialized_response)

        return self.response

    def get_service(self) -> str:
        """
        Returns Lead Capture Service base URL.
        """
        from ..config import host_lead_capture_service  # Import the host configuration
        return f"http://{host_lead_capture_service}"

    def get_path(self) -> str:
        """
        Returns API endpoint path for lead resubmission.
        """
        return "/leads/resubmit"

    def get_query(self) -> str:
        """
        Returns query parameters for the request.
        """
        query = super().get_query()
        return query

    def get_post(self) -> str:
        """
        Returns JSON-serialized POST body for lead resubmission.
        """
        return json.dumps(self.post_body)

    def get_operation_name(self) -> str:
        """
        Returns the operation name for this service.
        """
        return "LCSService"

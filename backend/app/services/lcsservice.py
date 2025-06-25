import json
from app.services.moveservice import MoveService


class LCSService(MoveService):
    """
    Service that calls Lead Capture Service to re-submit lead events.
    """
    def __init__(self, post_body: dict):
        """
        Initialize the LCSService with the given post body.
        """
        super().__init__()  # Call the parent's constructor
        self.post_body = post_body

    def connect(self):
        """
        Connect to the service without a token.
        """
        return self.connect_without_token()

    def set_response(self):
        # import pdb; pdb.set_trace()
        """
        Set the response for the service.
        """
        super().set_response()

        if isinstance(self.response, dict):
            serialized_response = json.dumps(self.response)
        else:
            serialized_response = self.response

        MoveService.log_info(serialized_response)

        return self.response

    def get_service(self):
        """
        Get the service URL.
        """
        from ..config import host_lead_capture_service  # Import the host configuration
        return f"http://{host_lead_capture_service}"

    def get_path(self):
        """
        Get the API path for the service.
        """
        return "/leads/resubmit"

    def get_query(self):
        """
        Get the query parameters for the service.
        """
        query = super().get_query()
        return query

    def get_post(self):
        """
        Get the POST body for the service.
        """
        return json.dumps(self.post_body)

    def get_operation_name(self):
        """
        Get the operation name for the service.
        """
        return "LCSService"
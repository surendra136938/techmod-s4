import logging
import json
import time
import os
from urllib.parse import parse_qs, urlencode, urlparse
from requests.exceptions import RequestException
import requests

class MoveService:
    """
    Base class for Move services; implements common features for all services.
    """

    ErrorType = {
        "MoveServiceErrorNone": {"mesg": "OK", "desc": "OK"},
        "MoveServiceErrorConnect": {"mesg": "", "desc": ""},
        "MoveServiceErrorNotSupported": {"mesg": "Request is not supported", "desc": "Request is not supported"},
        "MoveServiceErrorParms": {"mesg": "Parameters were bad or missing", "desc": "Parameters were bad or missing"},
        "MoveServiceErrorNotFound": {"mesg": "Item was not found", "desc": "Item was not found"},
        "MoveServiceErrorFormat": {"mesg": "Incorrectly formatted response", "desc": "Incorrectly formatted response"},
        "MoveServiceErrorNoData": {"mesg": "Response contained no data", "desc": "Response contained no data"},
        "MoveServiceErrorUnknown": {"mesg": "No details are available", "desc": "No details are available"},
        "MoveServiceErrorExceedMaxSavedResources": {
            "mesg": "You have exceeded the max # of saved resources limit (100)",
            "desc": "You have exceeded the max # of saved resources limit (100)",
        },
        "MoveServiceErrorDuplicatedSavedResourceItems": {
            "mesg": "Duplicated saved resources item",
            "desc": "Duplicated saved resources item",
        },
        "MoveServiceErrorExceedMaxSavedSearches": {
            "mesg": "You have exceeded the max # of saved searches limit (100)",
            "desc": "You have exceeded the max # of saved searches limit (100)",
        },
        "MoveServiceErrorMortgagerRateService": {
            "mesg": "An error occurred while calling MortgagerRateService",
            "desc": "An error occurred while calling MortgagerRateService",
        },
        "MoveServiceErrorInvalidAdminPassword": {
            "mesg": "Invalid MAPI administrator password",
            "desc": "Invalid MAPI administrator user password",
        },
        "MoveServiceErrorInvalidMemberEmail": {
            "mesg": "Invalid member email address",
            "desc": "Invalid member email address",
        },
        "MoveServiceErrorInvalidMemberPhone": {
            "mesg": "Invalid member phone number",
            "desc": "Invalid member phone number",
        },
        "MoveServiceErrorNoLocationQueryParamsFound": {
            "mesg": "No location query parameters in saved searches request",
            "desc": "No location query parameters in saved searches request",
        },
        "MemberServiceErrorMemberNotFound": {"mesg": "Member not found", "desc": "Member not found"},
        "MemberServiceErrorDuplicateEmail": {"mesg": "Member email existed", "desc": "Member email existed"},
        "MoveServiceErrorPolygonTooLarge": {"mesg": "Polygon size too large", "desc": "Polygon size too large"},
    }

    def __init__(self):
        """
        Initialize the MoveService class.
        """
        # Initialize attributes
        self.request = ""
        self.post = ""
        self.post_type = "json"
        self.response = ""

        self.error_code = "MoveServiceErrorNone"
        self.curl_error = ""
        self.curl_http_ret_code = 0

        self.trace_info = False

        # Connection timeout settings
        self.connection_timeout = 10
        self.curl_exec_timeout = 25

        self.error_message = ""
        self.error_description = ""



        query_string = os.getenv("QUERY_STRING", "")  # Get query string from environment
        query_params = parse_qs(query_string)

        if query_params.get("mapi_trace", ["0"])[0] == "1":
            self.trace_info = []
        else:
            self.trace_info = False

    def connect(self):
        """
        Connect to the service.
        """
        return self.connect_without_token()

    def send_response(self):
        """
        Just before sending, log any errors found in the standard structure.
        """
        # Log any errors found in the response
        if (
            isinstance(self.response, dict)
            and "meta" in self.response
            and "errors" in self.response["meta"]
            and len(self.response["meta"]["errors"]) > 0
        ):
            self.log_error(self.response["meta"]["errors"][0])

        # Simulate HTTP headers (in a real web framework, use the framework's response object)
        print("Content-Type: application/json")
        print("Expires: 0")

        # Print the JSON response
        print(json.dumps(self.response))

    @staticmethod
    def is_error(response):
        """
        By the time this method is called, errors should be all normalized.
        """
        return (
            isinstance(response, dict)
            and "meta" in response
            and "errors" in response["meta"]
            and len(response["meta"]["errors"]) > 0
        )

    @staticmethod
    def append_to_query(query, parm, value):
        """
        Append a parameter and value to the query string.
        """
        if len(query) > 0:
            query += "&"
        else:
            query += "?"

        query += f"{parm}={urlencode({'': value})[1:]}"  # Encode the value
        return query

    @staticmethod
    def append_to_path(path, comp):
        """
        Append a component to the path.
        """
        return f"{path}/{comp}"

    @staticmethod
    def append_to_list(lst, item):
        """
        Append an item to a comma-separated list.
        """
        if len(lst) > 0:
            lst += f",{item}"
        else:
            lst += item
        return lst

    @staticmethod
    def string_for_point(lat, lon):
        """
        Return a string representation of a point.
        """
        return f"({lat},{lon})"

    @staticmethod
    def string_for_points(points):
        """
        Return a string representation of a list of points.
        """
        s = ""

        for p in points:
            if "lat" in p and "lon" in p and p["lat"] and p["lon"]:
                point_str = MoveService.string_for_point(p["lat"], p["lon"])
                s = MoveService.append_to_list(s, point_str)

        # Close the polygon if necessary
        if len(points) >= 2:
            if (
                points[-1]["lat"] != points[0]["lat"]
                or points[-1]["lon"] != points[0]["lon"]
            ):
                closing_point = MoveService.string_for_point(
                    points[0]["lat"], points[0]["lon"]
                )
                s = MoveService.append_to_list(s, closing_point)

        # Wrap the entire set of points with enclosing parentheses
        if s:
            s = f"({s})"

        return s

    @staticmethod
    def log_error(error):
        """
        Log an error message.
        """
        code = error.get("code", "UnknownError")
        message = error.get("message", "No details available")
        print(f"ERROR: {code} - {message}")
    
    @staticmethod
    def titlecase(s: str) -> str:
        """
        Convert a string to title case, skipping certain words.
        """
        # Convert to lowercase and handle special characters
        t = s.lower()
        t = t.replace("-", "- ")
        t = t.replace("'", "' ")

        # List of words to skip capitalization
        skip_words = [
            "a", "au", "aux", "an", "and", "at", "but", "by", "d", "d'", "da", "dal",
            "dalla", "de", "des", "di", "du", "else", "for", "from", "gli", "if", "in",
            "into", "is", "l'", "la", "le", "les", "nor", "of", "off", "on", "or",
            "out", "over", "the", "then", "to", "when", "with"
        ]

        words = t.split(" ")
        for i, word in enumerate(words):
            if i == 0 or (word.rstrip("-") not in skip_words):
                words[i] = word.capitalize()

        # Rejoin the words and restore special characters
        t = " ".join(words)
        t = t.replace("- ", "-")
        t = t.replace("' ", "'")
        return t

    @staticmethod
    def log(message: str, context: str = "", log_type: str = "I"):
        """
        Log a message with context and type information.
        """
        log_type = log_type.upper()
        if log_type not in ["I", "W", "E"]:
            log_type = "I"

        context = f" {context}:" if context else ""
        logging.log(
            {"I": logging.INFO, "W": logging.WARNING, "E": logging.ERROR}[log_type],
            f"({log_type}){context} {message}"
        )

    @staticmethod
    def log_error(error):
        """
        Log an error message.
        """
        code = "MoveServiceErrorUnknown"
        mesg = MoveService.ErrorType.get(code, {}).get("mesg", "Unknown error occurred")

        if isinstance(error, dict) and "code" in error:
            code = error.get("code", code)
            mesg = error.get("message", mesg)
        elif isinstance(error, str):
            MoveService.log(f"{error}. pid={os.getpid()}", "", "E")
            return

        MoveService.log(f"{code} ({mesg}), pid={os.getpid()}", "", "E")

    @staticmethod
    def log_info(message: str):
        """
        Log an informational message.
        """
        MoveService.log(f"{message}, pid={os.getpid()}", __name__, "I")

    def connect_without_token(self):
        """
        Connect to the service without a token.
        """
        self.set_request()
        self.curl()
        self.set_response()
        self.create_trace_info()
        return self.response
    def curl(self):
        """
        Perform the HTTP request using the `requests` library.
        """
        self.response = ""
        self.error_code = "MoveServiceErrorNone"
        self.curl_error = ""
        self.curl_http_ret_code = 0

        # Set client_id if available
        self.set_client_id()

        headers = {}
        if self.post:
            # Default to JSON, but XML is implied when the post begins with "<"
            if self.post.strip().startswith("<"):
                headers = {
                    "Content-Type": "text/xml",
                    "Content-Length": str(len(self.post)),
                    "Expect": "",
                }
            else:
                headers = {
                    "Content-Type": "application/json",
                    "Content-Length": str(len(self.post)),
                    "Expect": "",
                }

        msg = self.request
        if self.post:
            clean_post = self.post.replace('\\n', ' ')
            msg += f", POST={clean_post}" 

        # Perform the request
        start_time = time.time()
        try:
            if self.post:
                response = requests.post(
                    self.request,
                    data=self.post,
                    headers=headers,
                    timeout=(self.connection_timeout, self.curl_exec_timeout),
                )
            else:
                response = requests.get(
                    self.request,
                    headers=headers,
                    timeout=(self.connection_timeout, self.curl_exec_timeout),
                )

            self.response = response.text
            self.curl_http_ret_code = response.status_code
        except requests.RequestException as e:
            self.error_code = f"MoveServiceErrorConnect:{e.errno}"
            self.curl_error = str(e)
        finally:
            end_time = time.time()
            runtime = f"t={end_time - start_time:.4f} sec"
            logging.info(f"{msg}, pid={os.getpid()}, {runtime}")

            if self.trace_info is not False:
                self.trace_info.append(
                    {
                        "request": msg,
                        "response": self.response,
                        "time": runtime,
                    }
                )

    def set_request(self):
        """
        Set the request details.
        """
        self.post = self.get_post()
        self.request = self.get_service() + self.get_path() + self.get_query()

    def set_client_id(self):
        """
        Automatically append client_id to the request if not already set.
        """
        parsed_url = urlparse(self.request)
        query_params = parse_qs(parsed_url.query)

        if "client_id" not in query_params:
            client_id = os.getenv("CLIENT_ID", None)
            if client_id:
                query_params["client_id"] = client_id
                self.request = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?{urlencode(query_params, doseq=True)}"

    def set_response(self):
        """
        Set the response details.
        """
        if self.error_code == "MoveServiceErrorNone":
            try:
                self.response = json.loads(self.response)
            except json.JSONDecodeError:
                self.response = self.create_error("MoveServiceErrorNoData")
        else:
            if self.error_code.startswith("MoveServiceErrorConnect"):
                self.response = self.create_error(
                    self.error_code, self.curl_error, self.curl_error
                )
            else:
                self.response = self.create_error(
                    self.error_code, self.error_message, self.error_description
                )

    
    def create_trace_info(self):
        """
        Add trace information to the response if trace_info is enabled.
        """
        if self.trace_info is False:
            return

        if "meta" not in self.response:
            self.response["meta"] = {}

        self.response["meta"]["mapi_trace"] = self.trace_info

    def create_error(self, code, mesg="", desc=""):
        """
        Standardize on the same error structure as used by the Move API.
        """
        # Look up the error message and description if not provided
        if not mesg:
            mesg = self.ErrorType.get(code, {}).get("mesg", "No details are available")
        if not desc:
            desc = self.ErrorType.get(code, {}).get("desc", "No details are available")

        # Create the standardized error structure
        return {
            "meta": {
                "errors": [
                    {
                        "code": code,
                        "message": mesg,
                        "description": desc,
                    }
                ]
            }
        }

    def get_service(self):
        """
        Placeholder for getting the service URL.
        """
        return ""

    def get_path(self):
        """
        Placeholder for getting the service path.
        """
        return ""

    def get_query(self):
        """
        Placeholder for getting the query string.
        """
        return ""

    def get_post(self):
        """
        Placeholder for getting the POST data.
        """
        return ""

    def get_operation_name(self):
        """
        Get the operation name.
        """
        return "MoveService"

    @staticmethod
    def get_saved_resources_backend():
        """
        Get the saved resources backend.
        """
        return os.getenv("SAVED_RESOURCES_BACKEND", "SRS")

    @staticmethod
    def get_saved_searches_backend():
        """
        Get the saved searches backend.
        """
        return os.getenv("SAVED_SEARCHES_BACKEND", "SRS")

    @staticmethod
    def get_nsi_api_key():
        """
        Get the NSI API key.
        """
        return os.getenv("NSI_API_KEY", "")

    @staticmethod
    def get_srs_api_key():
        """
        Get the SRS API key.
        """
        return os.getenv("SRS_API_KEY", "")



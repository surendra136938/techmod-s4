import logging
from app.spamfilters.spamfilterinterface import SpamFilterInterface
from app.spamfilters.normalize_email import NormalizeEmail


class SimpleSpamFilter:
    def __init__(self, lead_type):
        """
        Initialize the SimpleSpamFilter with the given lead type.
        """
        logging.info("Calling SimpleSpamFilter()")
        self.lead_type = lead_type
        self.sender_email = ""
        self.normalized_sender_email = ""
        self.sender_ip = ""
        self.sender_phone = ""
        self.session_id = ""
        self.member_id = ""
        self.visitor_id = ""
        self.whiteEmailList = ["test@example.com, test@gmail.com"]
        self.blackEmailList = []
        self.suspeciousEmailList = []
        self.whiteIpList = []
        self.blackIpList = []
        self.suspeciousIpList = []
        self.whitePhoneList = []
        self.blackPhoneList = []
        self.suspeciousPhoneList = []
        self.suspecious_spam_score = 0
        self.spamsDAO = None

    def parse_lead_payload(self, lead_payload):
        """
        Parse the lead payload to extract sender details.
        """
        self.sender_email = lead_payload.get("sender_email", "").strip().lower()
        self.normalized_sender_email = NormalizeEmail.normalize_email(self.sender_email)
        self.sender_ip = lead_payload.get("sender_ip", "").strip().lower()
        self.sender_phone = lead_payload.get("sender_phone", "").strip()
        self.session_id = lead_payload.get("session_id", "").strip()
        self.member_id = lead_payload.get("member_id", "").strip()
        self.visitor_id = lead_payload.get("visitor_id", "").strip()

    def formatted_data(self, block_status, list_type, context_attrs, triggered_data):
        """
        Format the data for spam detection response.
        """
        return {
            "block_status": block_status,
            "list_type": list_type,
            "context_attrs": context_attrs,
            "triggered_data": triggered_data,
        }

    def check_member_session_visitor_id(self):
        """
        Check if the member, session, or visitor ID is blocked.
        """
        # Placeholder for logic to check member/session/visitor ID
        return {}

    def check_email_domain(self, email):
        """
        Check the email domain for spam detection.
        """
        # Placeholder for email domain check logic
        return SpamFilterInterface.NOT_SPAM

    def check_email_pattern(self):
        """
        Check the email pattern for spam detection.
        """
        # Placeholder for email pattern check logic
        return SpamFilterInterface.NOT_SPAM

    def check_lead_sender(self):
        """
        Check the lead sender for spam detection.
        """
        # Placeholder for lead sender check logic
        return SpamFilterInterface.NOT_SPAM

    def check_ip_sender(self):
        """
        Check the IP sender for spam detection.
        """
        # Placeholder for IP sender check logic
        return SpamFilterInterface.NOT_SPAM

    def check_phone_sender(self):
        """
        Check the phone sender for spam detection.
        """
        # Placeholder for phone sender check logic
        return SpamFilterInterface.NOT_SPAM

    def check_phone_format(self, phone):
        """
        Check the phone format for spam detection.
        """
        # Placeholder for phone format check logic
        return SpamFilterInterface.NOT_SPAM

    def check_message_body(self):
        """
        Check the message body for spam detection.
        """
        # Placeholder for message body check logic
        return SpamFilterInterface.NOT_SPAM

    def calculate_suspecious_score(self):
        """
        Calculate the suspicious spam score.
        """
        # Placeholder for suspicious score calculation
        return 0

    def add_lead_sender(self):
        """
        Add the current lead sender to the sender list table.
        """
        # Placeholder for adding lead sender logic
        pass

    def filter(self, lead_payload):
        """
        Perform spam filtering on the given lead payload.
        """
        detection_result = SpamFilterInterface.NOT_SPAM
        detection_result_email = SpamFilterInterface.NOT_SPAM
        detection_result_phone = SpamFilterInterface.NOT_SPAM
        detection_result_ip = SpamFilterInterface.NOT_SPAM
        spam_detection = None

        self.parse_lead_payload(lead_payload)
        original_sender_email_address = self.sender_email
        sender_email_address = self.normalized_sender_email
        sender_ip_address = self.sender_ip
        black_phone = self.sender_phone

        if sender_ip_address:
            logging.info("IP Address Set")
        if black_phone:
            logging.info("Phone Number Set")
        if sender_email_address:
            logging.info("Email Address Set")

        member_session_visitor_block = self.check_member_session_visitor_id()
        if member_session_visitor_block:
            spam_detection = {
                "detection_result": SpamFilterInterface.IS_SPAM,
                "spam_reason": "Member / Session / Visitor ID Blocked",
                "data": self.formatted_data(
                    SpamFilterInterface.BLOCKED,
                    SpamFilterInterface.BLACKLIST,
                    list(member_session_visitor_block.keys()),
                    member_session_visitor_block,
                ),
            }
            return spam_detection

        try:
            # Check email
            if sender_email_address:
                if sender_email_address in self.whiteEmailList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["email"],
                            {"email": sender_email_address, "sender_email": original_sender_email_address},
                        ),
                    }
                elif self.check_email_domain(sender_email_address) == SpamFilterInterface.IS_SPAM:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"email_domain": sender_email_address, "sender_email": original_sender_email_address},
                        ),
                    }
                elif sender_email_address in self.blackEmailList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"confirmed_email": sender_email_address, "sender_email": original_sender_email_address},
                        ),
                    }
                elif sender_email_address in self.suspeciousEmailList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"suspected_email": sender_email_address, "sender_email": original_sender_email_address},
                        ),
                    }
                else:
                    if sender_ip_address not in self.whiteIpList:
                        email_pattern = self.check_email_pattern()
                        if email_pattern == SpamFilterInterface.IS_SPAM:
                            spam_detection = {
                                "detection_result": email_pattern,
                                "spam_reason": "partially_matched_email",
                                "data": self.formatted_data(
                                    SpamFilterInterface.BLOCKED,
                                    SpamFilterInterface.PATTERN_MATCH,
                                    ["email"],
                                    {"partially_matched_email": sender_email_address, "sender_email": original_sender_email_address},
                                ),
                            }
                            return spam_detection
                        else:
                            detection_result_email = self.check_lead_sender()
                            if detection_result_email == SpamFilterInterface.MAYBE_SPAM:
                                self.suspecious_spam_score = self.calculate_suspecious_score()

          # IP checks
            if sender_ip_address:
                logging.info("Checking IP address...")
                if sender_ip_address in self.whiteIpList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["ip_address"],
                            {"ip_address": sender_ip_address},
                        ),
                    }
                elif sender_ip_address in self.blackIpList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_ip",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["ip_address"],
                            {"confirmed_ip": sender_ip_address},
                        ),
                    }
                elif sender_ip_address in self.suspeciousIpList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_ip",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["ip_address"],
                            {"suspected_ip": sender_ip_address},
                        ),
                    }
                else:
                    detection_result_ip = self.check_ip_sender()
                    if detection_result_ip == SpamFilterInterface.MAYBE_SPAM:
                        self.suspecious_spam_score = self.calculate_suspecious_score()

            # Phone checks
            if black_phone:
                logging.info("Checking phone number...")
                if black_phone in self.whitePhoneList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["phone"],
                            {"phone": black_phone},
                        ),
                    }
                elif self.check_phone_format(black_phone) == SpamFilterInterface.IS_SPAM:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"phone": black_phone},
                        ),
                    }
                elif black_phone in self.blackPhoneList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"confirmed_phone": black_phone},
                        ),
                    }
                elif black_phone in self.suspeciousPhoneList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"suspected_phone": black_phone},
                        ),
                    }
                else:
                    detection_result_phone = self.check_phone_sender()
                    if detection_result_phone == SpamFilterInterface.MAYBE_SPAM:
                        self.suspecious_spam_score = self.calculate_suspecious_score()

            # Final spam detection result
            if detection_result in [SpamFilterInterface.IS_SPAM, SpamFilterInterface.MAYBE_SPAM]:
                return spam_detection

        except Exception as e:
            logging.error(f"Exception occurred when filtering spam: {str(e)}")

        return spam_detection

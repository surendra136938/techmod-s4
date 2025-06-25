from app.spamfilters.spamfilterinterface import SpamFilterInterface
import logging


class FARSpamFilter:
    def __init__(self, lead_type):
        """
        Initialize the FARSpamFilter with the given lead type.
        """
        logging.info("Calling FARSpamFilter()")
        self.lead_type = lead_type
        self.sender_email = ""
        self.sender_phone = ""
        self.blackEmailList = []
        self.suspeciousEmailList = []
        self.blackPhoneList = []
        self.suspeciousPhoneList = []
        self.spamsDAO = None

    def parse_lead_payload(self, lead_payload):
        """
        Parse the lead payload to extract sender email and phone.
        """
        self.sender_email = lead_payload.get("sender_email", "").strip().lower()
        self.sender_phone = lead_payload.get("sender_phone", "").strip()

    def check_email_domain(self, email):
        """
        Check the email domain for spam detection.
        """
        # Placeholder for email domain check logic
        return SpamFilterInterface.NOT_SPAM

    def check_phone_format(self, phone):
        """
        Check the phone format for spam detection.
        """
        # Placeholder for phone format check logic
        return SpamFilterInterface.NOT_SPAM

    def check_lead_sender(self):
        """
        Check the lead sender for spam detection.
        """
        # Placeholder for lead sender check logic
        return SpamFilterInterface.NOT_SPAM

    def check_phone_sender(self):
        """
        Check the phone sender for spam detection.
        """
        # Placeholder for phone sender check logic
        return SpamFilterInterface.NOT_SPAM

    def check_message_body(self):
        """
        Check the message body for spam detection.
        """
        # Placeholder for message body check logic
        return SpamFilterInterface.NOT_SPAM

    def add_lead_sender(self):
        """
        Add the current lead sender to the sender list table.
        """
        # Placeholder for adding lead sender logic
        pass

    def calculate_suspecious_score(self):
        """
        Calculate the suspicious spam score.
        """
        # Placeholder for suspicious score calculation
        return 0

    def filter(self, lead_payload):
        """
        Perform spam filtering on the given lead payload.
        """
        detection_result = SpamFilterInterface.NOT_SPAM

        self.parse_lead_payload(lead_payload)

        sender_email_address = self.sender_email
        black_phone = self.sender_phone

        try:
            # 1. Check email domain
            email_result = self.check_email_domain(sender_email_address)
            if email_result and email_result != SpamFilterInterface.NOT_SPAM:
                detection_result = email_result

            # 2. Check confirmed spammer email list
            elif sender_email_address in self.blackEmailList:
                detection_result = SpamFilterInterface.IS_SPAM

            # 3. Check suspected email list
            elif sender_email_address in self.suspeciousEmailList:
                detection_result = SpamFilterInterface.IS_SPAM

            # 4. Check phone format
            elif self.check_phone_format(black_phone) == SpamFilterInterface.IS_SPAM:
                detection_result = SpamFilterInterface.IS_SPAM

            # 5. Check confirmed spammer phone list
            elif black_phone in self.blackPhoneList:
                detection_result = SpamFilterInterface.IS_SPAM

            # 6. Check suspected phone list
            elif black_phone in self.suspeciousPhoneList:
                detection_result = SpamFilterInterface.IS_SPAM

            # 7. Calculate suspicious spam score
            elif detection_result == SpamFilterInterface.MAYBE_SPAM:
                self.suspecious_spam_score = self.calculate_suspecious_score()

            else:
                # Check against 15/5-6/1 rules
                detection_result_email = ""
                detection_result_phone = ""

                if black_phone:
                    detection_result_phone = self.check_phone_sender()

                if sender_email_address:
                    detection_result_email = self.check_lead_sender()

                if (
                    detection_result_phone == SpamFilterInterface.MAYBE_SPAM
                    or detection_result_email == SpamFilterInterface.MAYBE_SPAM
                ):
                    detection_result = SpamFilterInterface.MAYBE_SPAM
                elif (
                    detection_result_phone == SpamFilterInterface.IS_SPAM
                    or detection_result_email == SpamFilterInterface.IS_SPAM
                ):
                    detection_result = SpamFilterInterface.IS_SPAM

                if detection_result == SpamFilterInterface.NOT_SPAM:
                    # Check bad words
                    detection_result = self.check_message_body()
                    if detection_result == SpamFilterInterface.MAYBE_SPAM:
                        detection_result = SpamFilterInterface.IS_SPAM

            # Add current lead timestamp to sender list table
            if sender_email_address:
                self.add_lead_sender()

        except Exception as e:
            error = {
                "code": "MoveServiceErrorS4FilteringException",
                "message": f"Exception occurred when filtering email spam, exception error message={str(e)}",
            }
            logging.error(error)

        self.spamsDAO = None

        return detection_result
from typing import Dict, Any
from app.spamfilters.spamfilter import SpamFilter
from app.spamfilters.spamfilterinterface import SpamFilterInterface
import logging

class FARSpamFilter(SpamFilter):
    def __init__(self, lead_type: str) -> None:
        """
        Initializes FAR (Find A Realtor) spam filter with specified lead type.
        """
        logging.info("calling FARSpamFilter()")
        super().__init__(lead_type)

    def filter(self, lead_payload: Dict[str, Any]) -> str:
        """
        Filters FAR lead payload using simplified spam detection rules.
        """
        detection_result = SpamFilterInterface.NOT_SPAM

        self.parse_lead_payload(lead_payload)

        sender_email_address = str(self.sender_email).strip().lower()
        black_phone = str(self.sender_phone).strip()

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
                # self.suspecious_spam_score = 10
            # 1. Check 10 digit phone number format
            elif self.check_phone_format(black_phone) == SpamFilterInterface.IS_SPAM:
                detection_result = SpamFilterInterface.IS_SPAM
            # 2. Check confirmed spammer phone list
            elif black_phone in self.blackPhoneList:
                detection_result = SpamFilterInterface.IS_SPAM
            # 3. Check suspected phone list
            elif black_phone in self.suspeciousPhoneList:
                detection_result = SpamFilterInterface.IS_SPAM
            elif detection_result == SpamFilterInterface.MAYBE_SPAM:
                self.suspecious_spam_score = self.caculate_suspecious_score()
            else:
                # check against 15/5-6/1 rules
                detection_result_email = ""
                detection_result_phone = ""
                if black_phone != "":
                    detection_result_phone = self.check_phone_sender()
                if sender_email_address != "":
                    detection_result_email = self.check_lead_sender()
                if (detection_result_phone == SpamFilterInterface.MAYBE_SPAM or
                    detection_result_email == SpamFilterInterface.MAYBE_SPAM):
                    detection_result = SpamFilterInterface.MAYBE_SPAM
                elif (detection_result_phone == SpamFilterInterface.IS_SPAM or
                      detection_result_email == SpamFilterInterface.IS_SPAM):
                    detection_result = SpamFilterInterface.IS_SPAM
                if detection_result == SpamFilterInterface.NOT_SPAM:
                    # 3. Check bad words
                    detection_result = self.check_message_body()
                    if detection_result == SpamFilterInterface.MAYBE_SPAM:
                        detection_result = SpamFilterInterface.IS_SPAM

            # add current lead timestamp to sender_list table
            if sender_email_address != "":
                self.add_lead_sender()
            # if black_phone != "":
            #     self.add_lead_phone_sender()

        except Exception as e:
            error = {
                "code": "MoveServiceErroS4FilteringExceotion",
                "message": "Exception occured when filtering email spame, exception errir message=" + str(e)
            }
            logging.error(error)

        self.spamsDAO = None

        return detection_result

from app.spamfilters.spamfilter import SpamFilter
from app.spamfilters.spamfilterinterface import SpamFilterInterface
from app.dao.spamdao import SpamDAO
from app.spamfilters.normalize_email import NormalizeEmail
import logging
import json

class SimpleSpamFilter(SpamFilter):

    def __init__(self, lead_type):
        logging.info("calling SimpleSpamFilter()")
        super().__init__(lead_type)

    def filter(self, lead_payload):
        import pdb; pdb.set_trace()
        detection_result = SpamFilterInterface.NOT_SPAM
        detection_result_email = SpamFilterInterface.NOT_SPAM
        detection_result_phone = SpamFilterInterface.NOT_SPAM
        detection_result_ip = SpamFilterInterface.NOT_SPAM
        spam_detection = None
        self.parse_lead_payload(lead_payload)
        original_sender_email_address = self.sender_email
        sender_email_address = self.normalized_sender_email
        sender_ip_address = str(self.sender_ip).strip().lower()
        black_phone = str(self.sender_phone).strip()
        session_id = str(self.session_id).strip()
        member_id = str(self.member_id).strip()
        visitor_id = str(self.visitor_id).strip()
        default_data = self.default_data()

        if sender_ip_address:
            logging.info("IP Address Set")
        if black_phone:
            logging.info("Phone Number Set")
        if sender_email_address:
            logging.info("Email Address Set")
        import pdb; pdb.set_trace()
        member_session_visitor_block = self.check_member_session_visitor_id()
        if len(member_session_visitor_block) > 0:
            spam_detection = {
                "detection_result": SpamFilterInterface.IS_SPAM,
                "spam_reason": "Member / Session / Visitor ID Blocked",
                "data": self.formatted_data(
                    SpamFilterInterface.BLOCKED,
                    SpamFilterInterface.BLACKLIST,
                    list(member_session_visitor_block.keys()),
                    member_session_visitor_block
                )
            }
            return spam_detection

        '''
        # Code to return ML model response to LCS/CLCS

        formatted_msg = self.format_message_body()
        # logging.info(formatted_msg)

        api_call = f"https://6wy0otisih.execute-api.us-west-2.amazonaws.com/test/sentiment-analysis/?msg-body={formatted_msg}"

        response = requests.get(api_call).text
        resp1 = json.loads(response)
        # logging.info(resp1)
        # logging.info(resp1[0]["label"][0])
        # logging.info(resp1[0]["prob"][0])

        ml_label = resp1[0]["label"][0]
        ml_prob = resp1[0]["prob"][0]
        # for key, value in resp1.items():
        #     for c_name, c_value in value.items():
        #         logging.info(c_value)
        '''

        try:
            # 0. Check confirmed white email list

            if sender_email_address:
                logging.info("IF Statement: Email")

                if sender_email_address in self.whiteEmailList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["email"],
                            {"email": sender_email_address, "sender_email": original_sender_email_address}
                        )
                    }
                # 1. Check email domain
                elif self.check_email_domain(sender_email_address) == SpamFilterInterface.IS_SPAM:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"email_domain": sender_email_address, "sender_email": original_sender_email_address}
                        )
                    }
                # 2. Check confirmed spammer email list
                elif sender_email_address in self.blackEmailList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"confirmed_email": sender_email_address, "sender_email": original_sender_email_address}
                        )
                    }
                # 3. Check suspected email list
                elif sender_email_address in self.suspeciousEmailList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_email",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["email"],
                            {"suspected_email": sender_email_address, "sender_email": original_sender_email_address}
                        )
                    }
                else:
                    # check against 15/5-6/1 rules
                    if sender_ip_address not in self.whiteIpList:
                        logging.info("calling whiteIpList")
                        email_pattern = self.check_email_pattern()
                        if email_pattern == SpamFilterInterface.IS_SPAM:
                            spam_detection = {
                                "detection_result": email_pattern,
                                "spam_reason": "partially_matched_email",
                                "data": self.formatted_data(
                                    SpamFilterInterface.BLOCKED,
                                    SpamFilterInterface.PATTERN_MATCH,
                                    ["email"],
                                    {"partially_matched_email": sender_email_address, "sender_email": original_sender_email_address}
                                )
                            }
                            return spam_detection
                        else:
                            logging.info("Checking Email Sender")
                            detection_result_email = self.check_lead_sender()
                            if detection_result_email == SpamFilterInterface.MAYBE_SPAM:
                                self.suspecious_spam_score = self.caculate_suspecious_score()

            if sender_ip_address:
                logging.info("IF Statement: IPs")

                # for IP_address
                if sender_ip_address in self.whiteIpList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["ip_address"],
                            {"ip_address": sender_ip_address}
                        )
                    }
                # 2. Check confirmed spammer ip list
                elif sender_ip_address in self.blackIpList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_ip",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["ip_address"],
                            {"confirmed_ip": sender_ip_address}
                        )
                    }
                # 3. Check suspected ip list
                elif sender_ip_address in self.suspeciousIpList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_ip",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["ip_address"],
                            {"suspected_ip": sender_ip_address}
                        )
                    }
                else:
                    if sender_email_address not in self.whiteEmailList:
                        logging.info("calling whiteEmailList")
                        # check against 15/5-6/1 rules
                        logging.info("Checking IP Sender")
                        detection_result_ip = self.check_ip_sender()
                        if detection_result_ip == SpamFilterInterface.MAYBE_SPAM:
                            self.suspecious_spam_score = self.caculate_suspecious_score()

            if black_phone:
                logging.info("IF Statement: Phone")

                # 1. Check whether in whitelist
                if black_phone in self.whitePhoneList:
                    detection_result = SpamFilterInterface.NOT_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "",
                        "data": self.formatted_data(
                            SpamFilterInterface.NOT_BLOCKED,
                            SpamFilterInterface.WHITELIST,
                            ["phone"],
                            {"phone": black_phone}
                        )
                    }
                # 2. Check 10 digit phone number format
                elif self.check_phone_format(black_phone) == SpamFilterInterface.IS_SPAM:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"phone": black_phone}
                        )
                    }
                # 3. Check confirmed spammer phone list
                elif black_phone in self.blackPhoneList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "confirmed_phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"confirmed_phone": black_phone}
                        )
                    }
                # 4. Check suspected phone list
                elif black_phone in self.suspeciousPhoneList:
                    detection_result = SpamFilterInterface.IS_SPAM
                    spam_detection = {
                        "detection_result": detection_result,
                        "spam_reason": "suspected_phone",
                        "data": self.formatted_data(
                            SpamFilterInterface.BLOCKED,
                            SpamFilterInterface.BLACKLIST,
                            ["phone"],
                            {"suspected_phone": black_phone}
                        )
                    }
                else:
                    # check against 15/5-6/1 rules
                    logging.info("Checking Phone Sender")
                    detection_result_phone = self.check_phone_sender()
                    if detection_result_phone == SpamFilterInterface.MAYBE_SPAM:
                        self.suspecious_spam_score = self.caculate_suspecious_score()

            # array_push($spam_detection, "ml_label"=>$ml_label);
            '''
            # Code to return ML model response to LCS/CLCS
            spam_detection["ml_label"] = ml_label
            spam_detection["ml_prob"] = ml_prob
            '''

            self.add_lead_sender()

            if (detection_result == SpamFilterInterface.IS_SPAM or
                detection_result_email == SpamFilterInterface.IS_SPAM or
                detection_result_phone == SpamFilterInterface.IS_SPAM or
                detection_result_ip == SpamFilterInterface.IS_SPAM):
                return spam_detection

            if (detection_result_phone == SpamFilterInterface.MAYBE_SPAM or
                detection_result_email == SpamFilterInterface.MAYBE_SPAM or
                detection_result_ip == SpamFilterInterface.MAYBE_SPAM):
                logging.info("Maybe Spam IF Statement 1")
                detection_result = SpamFilterInterface.MAYBE_SPAM
                '''
                # Code to return ML model response to LCS/CLCS
                spam_detection["ml_label"] = ml_label
                spam_detection["ml_prob"] = ml_prob
                '''
                spam_reason = "Rules Violated"
                contextAttrs = ["email"]
                # To display valid response for algotiyhm_match
                if detection_result_email == SpamFilterInterface.MAYBE_SPAM:
                    spam_reason = "email rule violated"
                    spam_triggered_data = {"email": sender_email_address, "sender_email": original_sender_email_address}
                elif detection_result_phone == SpamFilterInterface.MAYBE_SPAM:
                    spam_reason = "phone rule violated"
                    spam_triggered_data = {"phone": black_phone}
                    contextAttrs = ["phone"]
                spam_detection = {
                    "detection_result": detection_result,
                    "spam_reason": spam_reason,
                    "data": self.formatted_data(
                        SpamFilterInterface.MAYBE_BLOCKED,
                        SpamFilterInterface.ALGORITHM_MATCH,
                        contextAttrs,
                        spam_triggered_data
                    )
                }
                return spam_detection

            # add current lead timestamp to incoming_leads table
            # self.add_lead_phone_sender()
            detection_result = self.check_message_body()
            if (detection_result == SpamFilterInterface.IS_SPAM or
                detection_result == SpamFilterInterface.MAYBE_SPAM or
                (isinstance(detection_result, dict) and (
                    detection_result.get("detection_result") == SpamFilterInterface.IS_SPAM or
                    detection_result.get("detection_result") == SpamFilterInterface.MAYBE_SPAM
                ))):
                if getattr(self, "lcs_id", None):
                    self.spamsDAO.add_to_review_queue(self.lcs_id, json.dumps(lead_payload))

            if (detection_result_email != SpamFilterInterface.MAYBE_SPAM and
                detection_result == SpamFilterInterface.MAYBE_SPAM):
                # TODO:
                # 1. Caculate suspicious score
                self.suspecious_spam_score = self.caculate_suspecious_score()
                # 2. Save current email lead to review queue

            if (detection_result_email == SpamFilterInterface.MAYBE_SPAM or
                detection_result_ip == SpamFilterInterface.MAYBE_SPAM or
                detection_result == SpamFilterInterface.MAYBE_SPAM or
                detection_result_phone == SpamFilterInterface.MAYBE_SPAM):
                logging.info("Maybe Spam IF Statement 2")
                detection_result = SpamFilterInterface.MAYBE_SPAM
                '''
                # Code to return ML model response to LCS/CLCS
                spam_detection["ml_label"] = ml_label
                spam_detection["ml_prob"] = ml_prob
                '''
                spam_reason = "Rules Violated"
                contextAttrs = ["email"]
                ruleName = SpamFilterInterface.ALGORITHM_MATCH
                # To display valid response for algotiyhm_match
                if detection_result_email == SpamFilterInterface.MAYBE_SPAM:
                    spam_reason = "email rule violated"
                    spam_triggered_data = {"email": sender_email_address, "sender_email": original_sender_email_address}
                elif detection_result_phone == SpamFilterInterface.MAYBE_SPAM:
                    spam_reason = "phone rule violated"
                    spam_triggered_data = {"phone": black_phone}
                    contextAttrs = ["phone"]

                if detection_result == SpamFilterInterface.MAYBE_SPAM:
                    ruleName = SpamFilterInterface.BLACKLIST
                spam_detection = {
                    "detection_result": detection_result,
                    "spam_reason": spam_reason,
                    "data": self.formatted_data(
                        SpamFilterInterface.MAYBE_BLOCKED,
                        SpamFilterInterface.BLACKLIST,
                        contextAttrs,
                        spam_triggered_data
                    )
                }
        except Exception as e:
            error = {
                "code": "MoveServiceErroS4FilteringException",
                "message": f"Exception occured when filtering email spame, exception error message={str(e)}"
            }
            logging.error(error)

        self.spamsDAO = None
        spam_reason = detection_result["spam_reason"] if isinstance(detection_result, dict) and "spam_reason" in detection_result else ''
        data = (detection_result["data"] if isinstance(detection_result, dict) and detection_result.get("detection_result") != SpamFilterInterface.NOT_SPAM
                else spam_detection["data"] if spam_detection and "data" in spam_detection else default_data)
        detection_result_val = detection_result["detection_result"] if isinstance(detection_result, dict) and "detection_result" in detection_result else detection_result

        spam_detection = {
            "detection_result": detection_result_val,
            "spam_reason": spam_reason,
            "data": data if data else default_data
        }

        '''
        # Code to return ML model response to LCS/CLCS
        spam_detection["ml_label"] = ml_label
        spam_detection["ml_prob"] = ml_prob
        '''
        return spam_detection
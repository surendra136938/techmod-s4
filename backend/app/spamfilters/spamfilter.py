from abc import ABC, abstractmethod
from app.spamfilters.spamfilterinterface import SpamFilterInterface
from app.dao.spamdao import SpamDAO
# from app.services.cacheservice import CacheService
from app.spamfilters.normalize_email import NormalizeEmail
from datetime import datetime, timezone, timedelta
import logging
from app import config

class SpamFilter(SpamFilterInterface, ABC):
    def __init__(self, lead_type=SpamFilterInterface.LEAD_TYPE_CO_BROKE):
        self.spamsDAO = SpamDAO(
            db_host=config.db_host,
            db_user=config.db_user, 
            db_password=config.db_password,
            s4_database_name=config.s4_database_name,
            cache_enabled=config.cache_enabled,
            cache_host=config.cache_host,
            cache_host_port=config.cache_host_port
        )
        self.badWordMap = {}
        self.blackEmailList = []
        self.blackIpList = []
        self.whiteUrlList = []
        self.whiteIpList = []
        self.whitePhoneList = []
        self.whiteEmailList = []
        self.blackPhoneList = []
        self.suspeciousEmailList = []
        self.suspeciousIpList = []
        self.suspeciousPhoneList = []
        self.lcs_id = ""
        self.request_guid = ""
        self.sender_email = ""
        self.normalized_sender_email = ""
        self.session_id = ""
        self.member_id = ""
        self.visitor_id = ""
        self.lead_method = ""
        self.sender_ip = ""
        self.message_body = ""
        self.message_subject = ""
        self.sender_first_name = ""
        self.sender_last_name = ""
        self.lead_submitted_time = ""
        self.sender_phone = ""
        self.suspecious_spam_score = 0
        self.total_text_word_count = 0
        self.suspecious_text_word_count = 0
        self.suspecious_phone_count = 0
        self.sender_lead_count = 0
        self.sender_leads_time_stamp_keep_list = []
        self.sender_leads_time_stamp_to_be_removed_list = []
        self.lead_count_short_limit = None
        self.lead_count_long_limit = None
        self.time_treshold_short = None
        self.time_treshold_long = None
        self.email_time_treshold_long = None

        # self.lead_count_short_phone_limit = None

        # get a list of bad words first
        import pdb; pdb.set_trace()
        bad_words_result = self.spamsDAO.get_bad_words_list()
        if bad_words_result is not None:
            for value in bad_words_result:
                id = text = type = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'id':
                        id = c_val
                    elif c_name.lower() == 'text':
                        text = c_val
                    elif c_name.lower() == 'type':
                        type = c_val
                if text is not None and id is not None and type is not None:
                    self.badWordMap[str(text).strip().lower()] = f"{id}|{str(type).strip()}"

        black_phone_list_result = self.spamsDAO.get_black_phone_list()
        import pdb; pdb.set_trace()
        if black_phone_list_result is not None:
            for value in black_phone_list_result:
                phone = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'phone':
                        phone = c_val
                if phone is not None:
                    self.blackPhoneList.append(str(phone).strip().lower())

        suspected_phone_list_result = self.spamsDAO.get_suspected_phone_list()
        import pdb; pdb.set_trace()
        if suspected_phone_list_result is not None:
            for value in suspected_phone_list_result:
                phone = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'phone':
                        phone = c_val
                if phone is not None:
                    self.suspeciousPhoneList.append(str(phone).strip().lower())

        black_email_list_result = self.spamsDAO.get_black_email_list()
        import pdb; pdb.set_trace()
        if black_email_list_result is not None:
            for value in black_email_list_result:
                email = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'email':
                        email = c_val
                if email is not None:
                    self.blackEmailList.append(str(email).strip().lower())

        black_ip_list_result = self.spamsDAO.get_blacklist_ip()
        if black_ip_list_result is not None:
            for value in black_ip_list_result:
                ip = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'ip_address':
                        ip = c_val
                if ip is not None:
                    self.blackIpList.append(str(ip).strip().lower())

        whitelisted_url_list_result = self.spamsDAO.get_whitelisted_url_list()
        import pdb; pdb.set_trace()
        if whitelisted_url_list_result is not None:
            for value in whitelisted_url_list_result:
                url = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'url':
                        url = c_val
                if url is not None:
                    self.whiteUrlList.append(str(url).strip().lower())

        white_email_list_result = self.spamsDAO.get_white_email_list()
        import pdb; pdb.set_trace()
        if white_email_list_result is not None:
            for value in white_email_list_result:
                email = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'email':
                        email = c_val
                if email is not None:
                    self.whiteEmailList.append(str(email).strip().lower())

        white_ip_list_result = self.spamsDAO.get_whitelisted_ip()
        import pdb; pdb.set_trace()
        if white_ip_list_result is not None:
            for value in white_ip_list_result:
                ip = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'ip_address':
                        ip = c_val
                if ip is not None:
                    self.whiteIpList.append(str(ip).strip().lower())

        white_phone_list_result = self.spamsDAO.get_whitelisted_phone()
        import pdb; pdb.set_trace()
        if white_phone_list_result is not None:
            for value in white_phone_list_result:
                phone = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'phone':
                        phone = c_val
                if phone is not None:
                    self.whitePhoneList.append(str(phone).strip().lower())

        suspecious_email_list_result = self.spamsDAO.get_suspected_email_list()
        import pdb; pdb.set_trace()
        if suspecious_email_list_result is not None:
            for value in suspecious_email_list_result:
                email = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'email':
                        email = c_val
                if email is not None:
                    self.suspeciousEmailList.append(str(email).strip().lower())

        suspecious_ip_list_result = self.spamsDAO.get_suspected_ip_list()
        import pdb; pdb.set_trace()
        if suspecious_ip_list_result is not None:
            for value in suspecious_ip_list_result:
                ip = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'ip_address':
                        ip = c_val
                if ip is not None:
                    self.suspeciousIpList.append(str(ip).strip().lower())

        # $filter_config = new FilterConfig();
        # $this->lead_count_short_limit = $filter_config->get_leadcount_limit_short($lead_type);
        # $this->lead_count_long_limit =  $filter_config->get_leadcount_limit_long($lead_type);
        # $this->time_treshold_short = $filter_config->get_time_treshold_short($lead_type);
        # $this->time_treshold_long = $filter_config->get_time_treshold_long($lead_type);
        # $this->lead_count_short_phone_limit = $filter_config->get_leadcount_limit_phone_short($lead_type);

    def filter(self, lead_payload):
        self.spamsDAO = None
        return SpamFilterInterface.NOT_SPAM

    def parse_lead_payload(self, post_body):
        import pdb; pdb.set_trace()
        if "lead" in post_body and "id" in post_body["lead"] and post_body["lead"]["id"]:
            self.lcs_id = post_body["lead"]["id"]

        self.request_guid = post_body.get("request_guid", "")

        if "lead" in post_body and "lead_data" in post_body["lead"] and "phone" in post_body["lead"]["lead_data"]:
            post_phone = str(post_body["lead"]["lead_data"]["phone"]).strip()
            self.sender_phone = ''.join(filter(str.isdigit, post_phone))

        if "lead" in post_body and "lead_data" in post_body["lead"] and "email" in post_body["lead"]["lead_data"]:
            self.sender_email = str(post_body["lead"]["lead_data"]["email"]).strip().lower()
            self.normalized_sender_email = NormalizeEmail.normalize_email(self.sender_email)

        if "lead" in post_body and "user" in post_body["lead"] and "session_id" in post_body["lead"]["user"]:
            self.session_id = str(post_body["lead"]["user"]["session_id"]).strip()

        if "lead" in post_body and "user" in post_body["lead"] and "member_id" in post_body["lead"]["user"]:
            self.member_id = str(post_body["lead"]["user"]["member_id"]).strip()

        if "lead" in post_body and "user" in post_body["lead"] and "visitor_id" in post_body["lead"]["user"]:
            self.visitor_id = str(post_body["lead"]["user"]["visitor_id"]).strip()

        if "lead" in post_body and "client" in post_body["lead"] and "ip_address" in post_body["lead"]["client"]:
            self.sender_ip = str(post_body["lead"]["client"]["ip_address"]).strip()

        if "lead" in post_body and "lead_data" in post_body["lead"] and "message" in post_body["lead"]["lead_data"] and "body" in post_body["lead"]["lead_data"]["message"]:
            self.message_body = post_body["lead"]["lead_data"]["message"]["body"]

        if "lead" in post_body and "lead_data" in post_body["lead"] and "message" in post_body["lead"]["lead_data"] and "subject" in post_body["lead"]["lead_data"]["message"]:
            self.message_subject = post_body["lead"]["lead_data"]["message"]["subject"]

        if "lead" in post_body and "created_date" in post_body["lead"]:
            self.lead_submitted_time = str(post_body["lead"]["created_date"]).strip()

        if "lead" in post_body and "lead_data" in post_body["lead"] and "first_name" in post_body["lead"]["lead_data"]:
            self.sender_first_name = str(post_body["lead"]["lead_data"]["first_name"]).strip()

        if "lead" in post_body and "lead_data" in post_body["lead"] and "last_name" in post_body["lead"]["lead_data"]:
            self.sender_last_name = str(post_body["lead"]["lead_data"]["last_name"]).strip()

        post_lead_method = post_body["lead"].get("method", "email") if "lead" in post_body else "email"
        post_form_variant = post_body["lead"].get("form", {}).get("variant", "") if "lead" in post_body else ""
        post_form_name = post_body["lead"].get("form", {}).get("name", "") if "lead" in post_body else ""
        post_form_page_name = post_body["lead"].get("form", {}).get("page_name", "") if "lead" in post_body else ""

        is_srp = post_form_page_name.find('srp')
        if is_srp == -1:
            srp_flag_for_ldp = True
            srp_flag_for_srp = False
        else:
            srp_flag_for_ldp = False
            srp_flag_for_srp = True

        is_variant_srp = post_form_variant.find('srp')
        if is_variant_srp == -1:
            srp_variant_flag_for_ldp = True
            srp_variant_flag_for_srp = False
        else:
            srp_variant_flag_for_ldp = False
            srp_variant_flag_for_srp = True

        if ((post_lead_method != "call") and (post_lead_method != "tpn_call")) and srp_flag_for_ldp and srp_variant_flag_for_ldp and (post_form_name != "might_also_like"):
            self.lead_method = "email_ldp"
        elif ((post_lead_method != "call") and (post_lead_method != "tpn_call")) and (srp_flag_for_srp or srp_variant_flag_for_srp) and (post_form_name != "might_also_like"):
            self.lead_method = "email_srp_non_mal"
        elif ((post_lead_method != "call") and (post_lead_method != "tpn_call")) and ((post_form_name == "might_also_like") and srp_flag_for_ldp and srp_variant_flag_for_ldp):
            self.lead_method = "email_mal_ldp"
        elif ((post_lead_method != "call") and (post_lead_method != "tpn_call")) and ((post_form_name == "might_also_like") and (srp_flag_for_srp or srp_variant_flag_for_srp)):
            self.lead_method = "email_mal_srp"
        elif post_lead_method == "call":
            self.lead_method = "call"
        elif post_lead_method == "tpn_call":
            self.lead_method = "tpn_call"

    def default_data(self):
        return {
            "rule": [],
            "action": SpamFilterInterface.NOT_BLOCKED,
            "context": {
                "inquiry_id": self.lcs_id
            }
        }

    def formatted_data(self, ruleAction, ruleName, spamReason, data):
        ruleDesc = {
            "blacklist": "it could be blocked due to confirmed or suspected lead attribute(s)",
            "whitelist": "it could be allowed due to whitelisted lead attribute(s)",
            "pattern_match": "it could be blocked due to pattern matching lead attribute(s)",
            "algorithm_match": "it could be blocked due to algorithm matching lead attribute(s)"
        }
        return {
            "rule": {
                "name": ruleName,
                "description": ruleDesc[ruleName],
                "context_attributes": spamReason,
                "triggered_data": data
            },
            "action": ruleAction,
            "context": {
                "inquiry_id": self.lcs_id
            }
        }

    def getHost(self, Address):
        import re
        return re.sub(r'(?:https?:\/\/)?(?:www\.)?(.*)\/?$', r'\1', Address)

    def check_member_session_visitor_id(self):
        import pdb; pdb.set_trace()
        id_array = {
            "member_id": self.member_id,
            "session_id": self.session_id,
            "visitor_id": self.visitor_id
        }
        result_array = {}
        for key, value in id_array.items():
            val = str(value).strip().lower()
            if val in self.badWordMap:
                id_type = self.badWordMap[val]
                temp_array = id_type.split("|")
                type = temp_array[1]
                if type.lower() == SpamFilterInterface.BAD_WORD_TYPE_BANNED.lower():
                    result_array[key] = val
                    return result_array
        return result_array

    '''
    # Code to return ML model response to LCS/CLCS
    def format_message_body(self):
        import re
        formatted_message = re.sub(r'\s+', '%20', self.message_body)
        return formatted_message
    '''

    def check_message_body(self):
        detection_result = SpamFilterInterface.NOT_SPAM
        spam_detection = {"detection_result": detection_result, "data": self.default_data()}
        checked_message_body = self.cleanup_message_body(self.message_body)
        message_text_array = checked_message_body.split(" ")
        import re
        pattern = r'[^A-Za-z0-9@.\s\s+]'
        sender_email = re.sub(pattern, "", self.sender_email)
        email_tokens = sender_email.split(" ")
        for email in email_tokens:
            email_word_tokens = email.split("@")
            for e_token in email_word_tokens:
                final_email_word_token = e_token.split(".")
                for f_token in final_email_word_token:
                    message_text_array.append(f_token)
        sender_first_name = self.cleanup_message_body(self.sender_first_name)
        first_name_tokens = sender_first_name.split(" ")
        sender_last_name = self.cleanup_message_body(self.sender_last_name)
        last_name_tokens = sender_last_name.split(" ")
        for first_name in first_name_tokens:
            message_text_array.append(first_name)
        for last_name in last_name_tokens:
            message_text_array.append(last_name)
        self.total_text_word_count = len(message_text_array)
        second_sanitize = True

        def compare_with_badwords():
            nonlocal detection_result, spam_detection
            for text in message_text_array:
                key = str(text).strip().lower()
                if key in self.badWordMap:
                    id_type = self.badWordMap[key]
                    temp_array = id_type.split("|")
                    type = temp_array[1]
                    if type.lower() == SpamFilterInterface.BAD_WORD_TYPE_BANNED.lower():
                        detection_result = SpamFilterInterface.MAYBE_SPAM
                        bad_words = [key]
                        spam_detection = {
                            "detection_result": detection_result,
                            "spam_reason": "suspected_word",
                            "data": self.formatted_data(
                                SpamFilterInterface.MAYBE_BLOCKED,
                                SpamFilterInterface.PATTERN_MATCH,
                                ["message_body"],
                                {"bad_words": bad_words}
                            )
                        }
                        return True
                    elif type.lower() == SpamFilterInterface.BAD_WORD_TYPE_SUSPICIOUS.lower():
                        detection_result = SpamFilterInterface.MAYBE_SPAM
                        self.suspecious_text_word_count += 1
            return False

        if compare_with_badwords():
            return spam_detection

        if (detection_result != SpamFilterInterface.MAYBE_SPAM or detection_result != SpamFilterInterface.IS_SPAM) and second_sanitize:
            checked_message_body = self.cleanup_message_body(self.message_body, True)
            message_text_array = checked_message_body.split(" ")
            second_sanitize = False
            if compare_with_badwords():
                return spam_detection

        return detection_result

    def caculate_suspecious_score(self):
        score = 0.0
        if self.suspecious_spam_score > 0:
            return self.suspecious_spam_score
        else:
            if self.total_text_word_count > 0:
                score = (self.suspecious_text_word_count / self.total_text_word_count) * 100
            if score > 0 and score <= 10:
                score = 1
            elif score > 10 and score <= 20:
                score = 2
            elif score > 20 and score <= 30:
                score = 3
            elif score > 30 and score <= 40:
                score = 4
            elif score > 40 and score <= 50:
                score = 5
            elif score > 50 and score <= 60:
                score = 6
            elif score > 0 and score <= 70:
                score = 7
            elif score > 0 and score <= 80:
                score = 8
            elif score > 0 and score <= 90:
                score = 9
            elif score > 0 and score <= 100:
                score = 10
        return score

    def cleanup_message_body(self, message_body, is_second_sanitize=False):
        import re
        if is_second_sanitize:
            pattern = [r'[^A-Za-z0-9\s\s+]', r'[+,Š,Å]']
            clean_message_body = re.sub(pattern[0], "", message_body)
            clean_message_body = re.sub(pattern[1], "", clean_message_body)
        else:
            pattern = r'[^A-Za-z0-9\s\s+]'
            clean_message_body = re.sub(pattern, " ", message_body)
        clean_message_body = " ".join(list(dict.fromkeys(clean_message_body.split(" "))))
        return clean_message_body

    def default_config(self):
        config = []
        config1 = {}
        config2 = {}
        config1['lead_count'] = 6
        config1['minute'] = 1
        config2['lead_count'] = 15
        config2['minute'] = 15
        config.append(config1)
        config.append(config2)
        return config

    def check_email_pattern(self):
        pattern_result = SpamFilterInterface.NOT_SPAM
        pattern_list = self.spamsDAO.get_pattern_email_list()
        if pattern_list is not None:
            for value in pattern_list:
                email = None
                for c_name, c_val in value.items():
                    if c_name.lower() == 'email':
                        email = c_val
                        suspected_email_pattern = self.sender_email.find(email)
                        if suspected_email_pattern == -1:
                            pattern_result = SpamFilterInterface.NOT_SPAM
                        else:
                            self.add_sender_to_suspected_email_lsit()
                            pattern_result = SpamFilterInterface.IS_SPAM
                            return pattern_result
        return pattern_result

    def check_lead_sender(self):
        logging.info("Lead type is =%s", self.lead_method)
        detection_result = SpamFilterInterface.NOT_SPAM
        rule_type = 'email'
        email_algorithm_config = self.spamsDAO.get_rule_type_config(rule_type)
        if not email_algorithm_config:
            email_algorithm_config = self.default_config()
        lead_weights = self.spamsDAO.get_lead_weights()
        email_ldp_weight = email_srp_non_mal_weight = email_mal_ldp_weight = email_mal_srp_weight = 0
        for lead_weight in lead_weights:
            if lead_weight['lead_type'] == 'email_ldp':
                email_ldp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_srp_non_mal':
                email_srp_non_mal_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_ldp':
                email_mal_ldp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_srp':
                email_mal_srp_weight = lead_weight['weights']
        if email_algorithm_config:
            for email_config in email_algorithm_config:
                minute = email_config['minute']
                in_sec = minute * 60
                lead_count = email_config['lead_count']
                current_utc_time = int(datetime.now(timezone(timedelta(hours=-8))).timestamp())
                email_ldp_count = self.spamsDAO.get_lead_email_type_count(self.sender_email, 'email_ldp', current_utc_time, in_sec)
                email_srp_non_mal_count = email_mal_ldp_count = email_mal_srp_count = 0
                if email_srp_non_mal_weight > 0:
                    email_srp_non_mal_count = self.spamsDAO.get_lead_email_type_count(self.sender_email, 'email_srp_non_mal', current_utc_time, in_sec)
                if email_mal_ldp_weight > 0:
                    email_mal_ldp_count = self.spamsDAO.get_lead_email_type_count(self.sender_email, 'email_mal_ldp', current_utc_time, in_sec)
                if email_mal_srp_weight > 0:
                    email_mal_srp_count = self.spamsDAO.get_lead_email_type_count(self.sender_email, 'email_mal_srp', current_utc_time, in_sec)
                if email_srp_non_mal_count > 0:
                    email_srp_non_mal_count *= email_srp_non_mal_weight
                if email_mal_ldp_count > 0:
                    email_mal_ldp_count *= email_mal_ldp_weight
                if email_mal_srp_count > 0:
                    email_mal_srp_count *= email_mal_srp_weight
                min_leads_count = email_ldp_count + email_srp_non_mal_count + email_mal_ldp_count + email_mal_srp_count
                if self.lead_method == 'email_ldp':
                    min_leads_count += email_ldp_weight
                elif self.lead_method == 'email_srp_non_mal':
                    min_leads_count += email_srp_non_mal_weight
                elif self.lead_method == 'email_mal_ldp':
                    min_leads_count += email_mal_ldp_weight
                elif self.lead_method == 'email_mal_srp':
                    min_leads_count += email_mal_srp_weight
                if ((self.lead_method == 'email_srp_non_mal' and email_srp_non_mal_weight == 0) or
                    (self.lead_method == 'email_mal_ldp' and email_mal_ldp_weight == 0) or
                    (self.lead_method == 'email_mal_srp' and email_mal_srp_weight == 0)):
                    detection_result = SpamFilterInterface.NOT_SPAM
                else:
                    if min_leads_count >= lead_count:
                        detection_result = SpamFilterInterface.MAYBE_SPAM
                        self.add_sender_to_suspected_email_lsit()
                        break
        return detection_result

    def check_ip_sender(self):
        detection_result = SpamFilterInterface.NOT_SPAM
        rule_type_ip = 'ip_address'
        ip_algorithm_config = self.spamsDAO.get_rule_type_config(rule_type_ip)
        lead_weights = self.spamsDAO.get_lead_weights()
        email_ldp_weight = email_srp_non_mal_weight = email_mal_ldp_weight = email_mal_srp_weight = call_weight = tpn_call_weight = 0
        for lead_weight in lead_weights:
            if lead_weight['lead_type'] == 'email_ldp':
                email_ldp_weight = int(1 / lead_weight['weights'])
            elif lead_weight['lead_type'] == 'email_srp_non_mal':
                email_srp_non_mal_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_ldp':
                email_mal_ldp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_srp':
                email_mal_srp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'call':
                call_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'tpn_call':
                tpn_call_weight = lead_weight['weights']
        if isinstance(ip_algorithm_config, (list, dict)):
            for ip_config in ip_algorithm_config:
                minute = ip_config['minute']
                in_sec = minute * 60
                lead_count = ip_config['lead_count']
                current_utc_time = int(datetime.now(timezone(timedelta(hours=-8))).timestamp())
                email_ldp_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'email_ldp', current_utc_time, in_sec)
                email_srp_non_mal_count = email_mal_ldp_count = email_mal_srp_count = call_count = tpn_call_count = 0
                if email_srp_non_mal_weight > 0:
                    email_srp_non_mal_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'email_srp_non_mal', current_utc_time, in_sec)
                if email_mal_ldp_weight > 0:
                    email_mal_ldp_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'email_mal_ldp', current_utc_time, in_sec)
                if email_mal_srp_weight > 0:
                    email_mal_srp_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'email_mal_srp', current_utc_time, in_sec)
                if call_weight > 0:
                    call_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'call', current_utc_time, in_sec)
                if tpn_call_weight > 0:
                    tpn_call_count = self.spamsDAO.get_lead_ip_type_count(self.sender_ip, 'tpn_call', current_utc_time, in_sec)
                if email_srp_non_mal_count > 0:
                    email_srp_non_mal_count *= email_srp_non_mal_weight
                if email_mal_ldp_count > 0:
                    email_mal_ldp_count *= email_mal_ldp_weight
                if email_mal_srp_count > 0:
                    email_mal_srp_count *= email_mal_srp_weight
                if call_count > 0:
                    call_count *= call_weight
                if tpn_call_count > 0:
                    tpn_call_count = email_mal_srp_count * tpn_call_weight
                min_leads_count = email_ldp_count + email_srp_non_mal_count + email_mal_ldp_count + email_mal_srp_count + call_count + tpn_call_count
                if self.lead_method == 'email_ldp':
                    min_leads_count += email_ldp_weight
                elif self.lead_method == 'email_srp_non_mal':
                    min_leads_count += email_srp_non_mal_weight
                elif self.lead_method == 'email_mal_ldp':
                    min_leads_count += email_mal_ldp_weight
                elif self.lead_method == 'email_mal_srp':
                    min_leads_count += email_mal_srp_weight
                elif self.lead_method == 'call':
                    min_leads_count += call_weight
                elif self.lead_method == 'tpn_call':
                    min_leads_count += tpn_call_weight
                if ((self.lead_method == 'email_srp_non_mal' and email_srp_non_mal_weight == 0) or
                    (self.lead_method == 'email_mal_ldp' and email_mal_ldp_weight == 0) or
                    (self.lead_method == 'email_mal_srp' and email_mal_srp_weight == 0) or
                    (self.lead_method == 'call' and call_weight == 0) or
                    (self.lead_method == 'tpn_call' and tpn_call_weight == 0)):
                    detection_result = SpamFilterInterface.NOT_SPAM
                else:
                    if min_leads_count >= lead_count:
                        detection_result = SpamFilterInterface.MAYBE_SPAM
                        self.add_sender_to_suspected_ip_list()
                        break
        return detection_result

    def check_phone_sender(self):
        detection_result = SpamFilterInterface.NOT_SPAM
        rule_type_phone = 'phone'
        phone_algorithm_config = self.spamsDAO.get_rule_type_config(rule_type_phone)
        lead_weights = self.spamsDAO.get_lead_weights()
        email_ldp_weight = email_srp_non_mal_weight = email_mal_ldp_weight = email_mal_srp_weight = call_weight = tpn_call_weight = 0
        for lead_weight in lead_weights:
            if lead_weight['lead_type'] == 'email_ldp':
                email_ldp_weight = int(1 / lead_weight['weights'])
            elif lead_weight['lead_type'] == 'email_srp_non_mal':
                email_srp_non_mal_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_ldp':
                email_mal_ldp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'email_mal_srp':
                email_mal_srp_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'call':
                call_weight = lead_weight['weights']
            elif lead_weight['lead_type'] == 'tpn_call':
                tpn_call_weight = lead_weight['weights']
        if phone_algorithm_config:
            for phone_config in phone_algorithm_config:
                minute = phone_config['minute']
                in_sec = minute * 60
                lead_count = phone_config['lead_count']
                current_utc_time = int(datetime.now(timezone(timedelta(hours=-8))).timestamp())
                email_ldp_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'email_ldp', current_utc_time, in_sec)
                email_srp_non_mal_count = email_mal_ldp_count = email_mal_srp_count = call_count = tpn_call_count = 0
                if email_srp_non_mal_weight > 0:
                    email_srp_non_mal_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'email_srp_non_mal', current_utc_time, in_sec)
                if email_mal_ldp_weight > 0:
                    email_mal_ldp_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'email_mal_ldp', current_utc_time, in_sec)
                if email_mal_srp_weight > 0:
                    email_mal_srp_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'email_mal_srp', current_utc_time, in_sec)
                if call_weight > 0:
                    call_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'call', current_utc_time, in_sec)
                if tpn_call_weight > 0:
                    tpn_call_count = self.spamsDAO.get_lead_phone_type_count(self.sender_phone, 'tpn_call', current_utc_time, in_sec)
                if email_srp_non_mal_count > 0:
                    email_srp_non_mal_count *= email_srp_non_mal_weight
                if email_mal_ldp_count > 0:
                    email_mal_ldp_count *= email_mal_ldp_weight
                if email_mal_srp_count > 0:
                    email_mal_srp_count *= email_mal_srp_weight
                if call_count > 0:
                    call_count *= call_weight
                if tpn_call_count > 0:
                    tpn_call_count = email_mal_srp_count * tpn_call_weight
                min_leads_count = email_ldp_count + email_srp_non_mal_count + email_mal_ldp_count + email_mal_srp_count + call_count + tpn_call_count
                if self.lead_method == 'email_ldp':
                    min_leads_count += email_ldp_weight
                elif self.lead_method == 'email_srp_non_mal':
                    min_leads_count += email_srp_non_mal_weight
                elif self.lead_method == 'email_mal_ldp':
                    min_leads_count += email_mal_ldp_weight
                elif self.lead_method == 'email_mal_srp':
                    min_leads_count += email_mal_srp_weight
                elif self.lead_method == 'call':
                    min_leads_count += call_weight
                elif self.lead_method == 'tpn_call':
                    min_leads_count += tpn_call_weight
                if ((self.lead_method == 'email_srp_non_mal' and email_srp_non_mal_weight == 0) or
                    (self.lead_method == 'email_mal_ldp' and email_mal_ldp_weight == 0) or
                    (self.lead_method == 'email_mal_srp' and email_mal_srp_weight == 0) or
                    (self.lead_method == 'call' and call_weight == 0) or
                    (self.lead_method == 'tpn_call' and tpn_call_weight == 0)):
                    detection_result = SpamFilterInterface.NOT_SPAM
                else:
                    if min_leads_count >= lead_count:
                        detection_result = SpamFilterInterface.MAYBE_SPAM
                        self.add_sender_to_suspected_phone_list()
                        break
        return detection_result

    def add_lead_sender(self):
        current_utc_time = int(datetime.now(timezone(timedelta(hours=-8))).timestamp())
        lead_submitted_time = current_utc_time
        self.spamsDAO.save_or_update_sender(self.sender_email, self.sender_ip, self.lead_method, lead_submitted_time, False, self.sender_phone)

    def add_lead_phone_sender(self):
        lead_submitted_time = self.convert_to_UTC_phone_time(self.lead_submitted_time)
        self.spamsDAO.save_or_update_phone_sender(self.sender_phone, lead_submitted_time, False)

    def convert_to_UTC_time(self, time_stamp):
        utc_time = 0
        utc_time = int(datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
        return utc_time

    def convert_to_UTC_phone_time(self, time_stamp):
        utc_time = 0
        utc_time = int(datetime.strptime(time_stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
        return utc_time

    def add_sender_to_black_email_lsit(self):
        self.spamsDAO.add_to_black_email_lsit(self.sender_email)

    def check_phone_format(self, phone_format):
        phone = ''.join(filter(str.isdigit, phone_format))
        num_digits = len(phone)
        if num_digits == 0 or (num_digits >= 10 and num_digits <= 13):
            detection_result = SpamFilterInterface.NOT_SPAM
        else:
            detection_result = SpamFilterInterface.IS_SPAM
        return detection_result

    def add_sender_to_black_phone_lsit(self):
        self.spamsDAO.add_to_black_phone_list(self.sender_phone)

    def add_sender_to_suspected_email_lsit(self):
        self.spamsDAO.add_to_suspected_email_lsit(self.sender_email)
        self.invalidate_cache(SpamDAO.SPAM_SUSPECTED_EMAIL_LIST_CACHE_KEY)

    def add_sender_to_suspected_ip_list(self):
        self.spamsDAO.add_to_suspected_ip_list(self.sender_ip)
        self.invalidate_cache(SpamDAO.SPAM_SUSPECTED_IP_LIST_CACHE_KEY)

    def add_sender_to_suspected_phone_list(self):
        self.spamsDAO.add_to_suspected_phone_list(self.sender_phone)
        self.invalidate_cache(SpamDAO.SPAM_SUSPECTED_PHONE_LIST_CACHE_KEY)

    def check_email_domain(self, sender_email_address):
        detection_result = SpamFilterInterface.NOT_SPAM
        if sender_email_address == "":
            return detection_result
        if "@" not in sender_email_address:
            return SpamFilterInterface.BAD_EMAIL
        email_array = sender_email_address.split("@")
        domain = '@' + email_array[1]
        if domain in self.blackEmailList:
            detection_result = SpamFilterInterface.IS_SPAM
        return detection_result

    def invalidate_cache(self, cache_key):
        cacheService = CacheService()
        cacheService.invalidate_cache_on_all_node(cache_key)
        cacheService = None
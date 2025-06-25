import logging
from abc import ABC, abstractmethod
from app.spamfilters.spamfilterinterface import SpamFilterInterface
from app.db.spams_dao import SpamsDAO
from app.spamfilters.normalize_email import NormalizeEmail


class SpamFilter(SpamFilterInterface, ABC):
    def __init__(self, lead_type=SpamFilterInterface.LEAD_TYPE_CO_BROKE):
        """
        Initialize the SpamFilter with the given lead type.
        """
        self.spamsDAO = SpamsDAO()
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

        # Load bad words
        bad_words_result = self.spamsDAO.get_bad_words_list()
        if bad_words_result:
            for entry in bad_words_result:
                text = entry.get("text", "").strip().lower()
                word_id = entry.get("id", "")
                word_type = entry.get("type", "").strip()
                self.badWordMap[text] = f"{word_id}|{word_type}"

        # Load blacklisted and whitelisted data
        self.blackPhoneList = self._load_list(self.spamsDAO.get_black_phone_list(), "phone")
        self.suspeciousPhoneList = self._load_list(self.spamsDAO.get_suspected_phone_list(), "phone")
        self.blackEmailList = self._load_list(self.spamsDAO.get_black_email_list(), "email")
        self.blackIpList = self._load_list(self.spamsDAO.get_blacklist_ip(), "ip_address")
        self.whiteUrlList = self._load_list(self.spamsDAO.get_whitelisted_url_list(), "url")
        self.whiteEmailList = self._load_list(self.spamsDAO.get_white_email_list(), "email")
        self.whiteIpList = self._load_list(self.spamsDAO.get_whitelisted_ip(), "ip_address")
        self.whitePhoneList = self._load_list(self.spamsDAO.get_whitelisted_phone(), "phone")
        self.suspeciousEmailList = self._load_list(self.spamsDAO.get_suspected_email_list(), "email")
        self.suspeciousIpList = self._load_list(self.spamsDAO.get_suspected_ip_list(), "ip_address")

    def _load_list(self, result, key):
        """
        Helper method to load data from DAO results into a list.
        """
        data_list = []
        if result:
            for entry in result:
                value = entry.get(key, "").strip().lower()
                data_list.append(value)
        return data_list

    @abstractmethod
    def filter(self, lead_payload):
        """
        Abstract method to be implemented by subclasses for spam filtering.
        """
        pass

    def parse_lead_payload(self, post_body):
        """
        Parse the lead payload to extract sender details.
        """
        self.lcs_id = post_body.get("lead", {}).get("id", "").strip()
        self.request_guid = post_body.get("request_guid", "").strip()
        self.sender_phone = post_body.get("lead", {}).get("lead_data", {}).get("phone", "").strip()
        self.sender_email = post_body.get("lead", {}).get("lead_data", {}).get("email", "").strip().lower()
        self.normalized_sender_email = NormalizeEmail.normalize_email(self.sender_email)
        self.session_id = post_body.get("lead", {}).get("user", {}).get("session_id", "").strip()
        self.member_id = post_body.get("lead", {}).get("user", {}).get("member_id", "").strip()
        self.visitor_id = post_body.get("lead", {}).get("user", {}).get("visitor_id", "").strip()
        self.sender_ip = post_body.get("lead", {}).get("client", {}).get("ip_address", "").strip()
        self.message_body = post_body.get("lead", {}).get("lead_data", {}).get("message", {}).get("body", "").strip()
        self.message_subject = post_body.get("lead", {}).get("lead_data", {}).get("message", {}).get("subject", "").strip()
        self.sender_first_name = post_body.get("lead", {}).get("lead_data", {}).get("first_name", "").strip()
        self.sender_last_name = post_body.get("lead", {}).get("lead_data", {}).get("last_name", "").strip()
        self.lead_submitted_time = post_body.get("lead", {}).get("created_date", "").strip()

    def default_data(self):
        """
        Return default data for spam detection response.
        """
        return {
            "rule": [],
            "action": SpamFilterInterface.NOT_BLOCKED,
            "context": {"inquiry_id": self.lcs_id},
        }

    def formatted_data(self, rule_action, rule_name, spam_reason, data):
        """
        Format the data for spam detection response.
        """
        rule_desc = {
            "blacklist": "it could be blocked due to confirmed or suspected lead attribute(s)",
            "whitelist": "it could be allowed due to whitelisted lead attribute(s)",
            "pattern_match": "it could be blocked due to pattern matching lead attribute(s)",
            "algorithm_match": "it could be blocked due to algorithm matching lead attribute(s)",
        }
        return {
            "rule": {
                "name": rule_name,
                "description": rule_desc.get(rule_name, ""),
                "context_attributes": spam_reason,
                "triggered_data": data,
            },
            "action": rule_action,
            "context": {"inquiry_id": self.lcs_id},
        }

    def check_email_domain(self, sender_email_address):
        """
        Check the email domain for spam detection.
        """
        detection_result = SpamFilterInterface.NOT_SPAM
        if not sender_email_address or "@" not in sender_email_address:
            return SpamFilterInterface.BAD_EMAIL

        domain = f"@{sender_email_address.split('@')[1]}"
        if domain in self.blackEmailList:
            detection_result = SpamFilterInterface.IS_SPAM

        return detection_result

    def invalidate_cache(self, cache_key):
        """
        Invalidate the cache for the given cache key.
        """
        # Placeholder for cache invalidation logic
        logging.info(f"Invalidating cache for key: {cache_key}")
import json
from app.dao.spamdao import SpamDAO
from app.spamfilters.spamfilter import SpamFilter
from app.services.lcsservice import LCSService
from app import config
# from services.cacheservice import CacheService
from fastapi.responses import JSONResponse

class Administration:
    def __init__(self):
        self.spamDAO = SpamDAO(
            db_host=config.db_host,
            db_user=config.db_user, 
            db_password=config.db_password,
            s4_database_name=config.s4_database_name,
            cache_enabled=config.cache_enabled,
            cache_host=config.cache_host,
            cache_host_port=config.cache_host_port
        )

    # Add Algorithm Config
    def add_algorithm_config(self, post_body):
        data = json.loads(post_body)
        rule_type = data.get("rule_type", "").strip()
        lead_count = data.get("lead_count", 0)
        minute = data.get("minute", 0)

        if (rule_type or lead_count or minute):
            self.spamDAO.add_to_algorithm_config(rule_type, lead_count, minute)

        # # Invalidate cache
        # self.invalidate_cache(SpamDAO.SPAM_SUSPECTED_IP_LIST_CACHE_KEY)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "algorithm config added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Single Algorithm Config
    def get_single_algorithm_config(self, post_body):
        data = json.loads(post_body)
        id_ = data.get("id", 0)
        algorithm_config_result = None
        if id_:
            algorithm_config_result =  self.spamDAO.get_single_algorithm_config(id_)

        response = {
            "meta": {"build": "1.0.0"},
            "algorithm_config_detail": algorithm_config_result
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Update Algorithm Config
    def update_algorithm_config(self, post_body):
        data = json.loads(post_body)
        id_ = data.get("id", 0)
        rule_type = data.get("rule_type", "").strip()
        lead_count = data.get("lead_count", 0)
        minute = data.get("minute", 0)

        if id_ or rule_type or lead_count or minute:
            self.spamDAO.update_algorithm_config(id_, rule_type, lead_count, minute)

        # self.invalidate_cache(SpamDAO.SPAM_ALGORITHM_CONFIG_CACHE_KEY)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "Algorithm Config updated successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Algorithm Config
    def get_algorithm_config(self):
        algorithm_config_result = self.spamDAO.get_algorithm_config("false")

        response = {
            "meta": {"build": "1.0.0"},
            "result": algorithm_config_result
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Algorithm Config
    def delete_algorithm_config(self, post_body):
        data = json.loads(post_body)
        id_ = data.get("id",0)
        if id_:
            self.spamDAO.delete_algorithm_config(id_)

        # self.invalidate_cache(SpamDAO.SPAM_ALGORITHM_CONFIG_CACHE_KEY)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "algorithm config deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Bad Words List
    def get_bad_words_list(self):
        bad_word_list = []
        bad_words_result = self.spamDAO.get_bad_words_list(False)

        if bad_words_result:
            for row in bad_words_result:
                id_ = row.get('id')
                text = row.get('text')
                type_ = row.get('type')
                bad_word = {"id": id_, "text": text}
                if type_ and type_.lower() == "banned":
                    bad_word["type"] = "dirty"
                elif type_ and type_.lower() == "suspicious":
                    bad_word["type"] = "indicator"
                bad_word_list.append(bad_word)

        response = {
            "meta": {"build": "1.0.0"},
            "bad_word_list": bad_word_list
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Add Bad Word
    def add_bad_word(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        text = data.get("text","").strip()
        type_ = data.get("type","").strip()

        # Map type for DB
        if type_ and type_.lower() == "dirty":
            type_db = "banned"
        elif type_ and type_.lower() == "indicator":
            type_db = "suspicious"
        else:
            type_db = "banned"

        if text and type_db:
            self.spamDAO.add_to_bad_words_list(text, type_db)

        # # Invalidate cache
        # self.invalidate_cache(SpamDAO.SPAM_BAD_WORDS_CACHE_KEY)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "bad_word added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Bad Word
    def delete_bad_word(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        id_list = data.get("ids", [])

        if id_list:
            for id_ in id_list:
                self.spamDAO.delete_bad_word(id_)

        # # Invalidate cache
        # self.invalidate_cache(SpamDAO.SPAM_BAD_WORDS_CACHE_KEY)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "bad_words deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Add Black Email
    def add_black_email(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        email = data.get("email", "").strip()
        # if email:
        #     spamsDAO = SpamDAO()
        #     spamsDAO.add_to_black_email_list(email)
        # Invalidate cache
        # self.invalidate_cache(SpamDAO.SPAM_BLACK_EMAIL_LIST_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "black email added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Black Email
    def delete_black_email(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        email_list = data.get("email_list", [])
        # if email_list:
        #     spamsDAO = SpamDAO()
        #     for email in email_list:
        #         spamsDAO.delete_black_email(email.strip())
        # Invalidate cache
        # self.invalidate_cache(SpamDAO.SPAM_BLACK_EMAIL_LIST_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "black emails deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Black Email List
    def get_black_email_list(self):
        black_email_list = []
        # spamsDAO = SpamDAO()
        # black_email_list_result = spamsDAO.get_black_email_list(False)
        # if black_email_list_result:
        #     for row in black_email_list_result:
        #         email = row.get("email")
        #         if email:
        #             black_email_list.append(email)
        response = {
            "meta": {"build": "1.0.0"},
            "black_email_list": black_email_list
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Add Black IP
    def add_black_ip(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        ip_address = data.get("ip_address", "").strip()
        # if ip_address:
        #     spamsDAO = SpamDAO()
        #     spamsDAO.add_to_black_ip_list(ip_address)
        #     spamsDAO = None
        # self.invalidate_cache(SpamDAO.SPAM_BLACKLIST_IP_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "black ip address added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Black IP
    def delete_black_ip(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        ip_list = data.get("ip_list", [])
        # if ip_list:
        #     spamsDAO = SpamDAO()
        #     for ip in ip_list:
        #         spamsDAO.delete_black_ip(ip.strip())
        #     spamsDAO = None
        # self.invalidate_cache(SpamDAO.SPAM_BLACKLIST_IP_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "black ips deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Black IP List
    def get_blacklist_ip(self):
        black_ip_list = []
        # spamsDAO = SpamDAO()
        # blacklist_ip_result = spamsDAO.get_blacklist_ip(False)
        # if blacklist_ip_result:
        #     for row in blacklist_ip_result:
        #         ip_address = row.get("ip_address")
        #         if ip_address:
        #             black_ip_list.append(ip_address)
        response = {
            "meta": {"build": "1.0.0"},
            "black_ip_list": black_ip_list
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Add Black Phone
    def add_black_phone(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        phone = data.get("phone", "").strip()
        # if phone:
        #     spamsDAO = SpamDAO()
        #     spamsDAO.add_to_black_phone_list(phone)
        #     spamsDAO = None
        # self.invalidate_cache(SpamDAO.SPAM_BLACK_PHONE_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": phone
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Black Phone(s)
    def delete_black_phone(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        phone_list = data.get("phone_list", [])
        # if phone_list:
        #     spamsDAO = SpamDAO()
        #     for phone in phone_list:
        #         spamsDAO.delete_black_phone_list(phone.strip())
        #     spamsDAO = None
        # self.invalidate_cache(SpamDAO.SPAM_BLACK_PHONE_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": phone_list
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Black Phone List
    def get_black_phone_list(self):
        black_phone_list = []
        # spamsDAO = SpamDAO()
        # black_phone_list_result = spamsDAO.get_black_phone_list(False)
        # if black_phone_list_result:
        #     for row in black_phone_list_result:
        #         phone = row.get("phone")
        #         if phone:
        #             black_phone_list.append(phone)
        response = {
            "meta": {"build": "1.0.0"},
            "black_phone_list": black_phone_list
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Lead Weights
    def get_lead_weights(self):
        lead_weights_result = [] 
        lead_weights_result = self.spamDAO.get_lead_weights(False)
      # Replace with actual DAO call
        response = {
            "meta": {"build": "1.0.0"},
            "lead_weights": lead_weights_result
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Update Lead Weight
    def update_weight(self, post_body):
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        lead_type = data.get("lead_type", "").strip()
        weight = data.get("weight", 0)
        if lead_type and weight:
            self.spamDAO.update_weight(weight, lead_type)
            spamsDAO = None
        # self.invalidate_cache(SpamDAO.SPAM_LEAD_WEIGHTS_CACHE_KEY)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "Lead weight updated successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})
  
    # def invalidate_cache(self, cache_key):
    #     cacheService = CacheService()
    #     cacheService.invalidate_cache_on_all_node(cache_key)
    #     cacheService = None


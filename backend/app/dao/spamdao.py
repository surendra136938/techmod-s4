from app.dao.pgsqldao import PgSqlDAO
from app.services.moveservice import MoveService
from app.spamfilters.spamfilter import SpamFilter

class SpamDAO:
    def __init__(self, db_host=None, db_user=None, db_password=None, s4_database_name=None, db_port=5432, cache_enabled=False, cache_host=None, cache_host_port=None):
        self.pgsqlDao = PgSqlDAO(db_host, db_user, db_password, s4_database_name, db_port)
        self.cacheInstance = None

        if cache_enabled:
            try:
                self.cacheInstance = redis.Redis(
                    host=cache_host,
                    port=int(cache_host_port),
                    socket_connect_timeout=2.5,
                    socket_keepalive=True,
                    socket_keepalive_options={},
                    retry_on_timeout=True
                )
                # Test connection
                self.cacheInstance.ping()
            except Exception as e:
                self.cacheInstance = None
                error = {"code": "S4RedisError", "message": "Could not connect to redis server."}
                MoveService.log_error(error)


    GET_BAD_WORDS_LIST = "SELECT id, text, type FROM bad_words"
    GET_BLACK_EMAIL_LIST = "SELECT email FROM black_email_list"
    GET_BLACKLIST_IP = "SELECT ip_address FROM black_ip_list"
    GET_WHITELISTED_URL_LIST = "SELECT url FROM whitelist_urls"
    GET_WHITE_EMAIL_LIST = "SELECT email FROM whitelist_emails"
    GET_WHITELISTED_IP = "SELECT ip_address FROM whitelist_ip"
    GET_WHITELISTED_PHONE = "SELECT phone FROM whitelist_phone"
    GET_PENDING_REVIEW = "SELECT id FROM review_queue where status = 'pending'"
    GET_BLACK_PHONE_LIST = "SELECT phone FROM black_phone_list"
    GET_RULE_TYPE_LIST = "SELECT types FROM rule_types"
    GET_PATTERN_EMAIL_LIST = "SELECT email FROM pattern_email_list"
    GET_SUSPECTED_PHONE_LIST = "SELECT phone FROM suspected_phone_list"
    GET_LEAD_EMAIL_TYPE_COUNT = "SELECT count(*) as count FROM incoming_leads where email = %s and lead_method = %s and (%s -last_lead_submited_time_stamp) < %s"
    GET_LEAD_IP_TYPE_COUNT = "SELECT count(*) as count FROM incoming_leads where ip_address = %s and lead_method = %s and (%s -last_lead_submited_time_stamp) < %s"
    GET_LEAD_PHONE_TYPE_COUNT = "SELECT count(*) as count FROM incoming_leads where phone = %s and lead_method = %s and (%s -last_lead_submited_time_stamp) < %s"
    GET_SUSPECTED_EMAIL_LIST = "SELECT email FROM suspected_email_list"
    GET_SUSPECTED_IP_LIST = "SELECT ip_address FROM suspected_ip_list"
    GET_SENDER = "SELECT email, last_lead_submited_time_stamp FROM incoming_leads where email = %s"
    GET_SENDER_IP = "SELECT ip_address, last_lead_submited_time_stamp FROM incoming_leads where ip_address = %s"
    GET_SENDER_PHONE = "SELECT phone, last_lead_submited_time_stamp FROM incoming_leads where phone = %s"
    GET_WEIGHTS = "SELECT lead_type, weights FROM lead_weights"
    GET_ALGORITHM_CONFIG = "SELECT * FROM algorithm_config"
    GET_SINGLE_ALGORITHM_CONFIG = "SELECT * FROM algorithm_config where id = %s"
    GET_DOMAIN_ID = "SELECT id FROM domain_names where name = %s"
    INSERT_SENDER = "INSERT INTO incoming_leads (email, ip_address, lead_method, last_lead_submited_time_stamp, phone) VALUES (%s, %s, %s, %s, %s)"
    INSERT_ALGORITHM_CONFIG = "INSERT INTO algorithm_config (rule_type, lead_count, minute) VALUES (%s, %s, %s)"
    UPDATE_SENDER = "UPDATE incoming_leads set last_lead_submited_time_stamp = %s where email = %s"
    UPDATE_WEIGHT = "UPDATE lead_weights set weights = %s where lead_type = %s"
    UPDATE_ALGORITHM_CONFIG = "UPDATE algorithm_config set rule_type = %s, lead_count = %s, minute = %s where id = %s"
    DELETE_SENDER = "DELETE FROM incoming_leads where email = %s and last_lead_submited_time_stamp < %s"
    DELETE_SENDER_IP = "DELETE FROM incoming_leads where ip_address = %s and last_lead_submited_time_stamp < %s"
    DELETE_SENDER_PHONE = "DELETE FROM incoming_leads where phone = %s and last_lead_submited_time_stamp < %s"
    INSERT_SENDER_TO_PATTERN_EMAIL_LIST = "INSERT INTO pattern_email_list (email) VALUES (%s)"
    INSERT_SENDER_TO_BLACK_EMAIL_LIST = "INSERT INTO black_email_list (email) VALUES (%s)"
    INSERT_SENDER_TO_WHITE_EMAIL_LIST = "INSERT INTO whitelist_emails (email) VALUES (%s)"
    INSERT_SENDER_TO_WHITELISTED_IP = "INSERT INTO whitelist_ip (ip_address) VALUES (%s)"
    INSERT_SENDER_TO_WHITELISTED_PHONE = "INSERT INTO whitelist_phone (phone) VALUES (%s)"
    INSERT_SENDER_TO_BLACKLIST_IP = "INSERT INTO black_ip_list (ip_address) VALUES (%s)"
    INSERT_TO_LEAD_WEIGHT_LIST = "INSERT INTO lead_weights (lead_type,weight) VALUES (%s, %s)"
    INSERT_SENDER_TO_WHITELISTED_URL_LIST = "INSERT INTO whitelist_urls (url) VALUES (%s)"
    INSERT_BLACK_PHONE_LIST = "INSERT INTO black_phone_list (phone) VALUES (%s)"
    INSERT_SENDER_TO_SUSPECTED_EMAIL_LIST = "INSERT INTO suspected_email_list (email) VALUES (%s)"
    INSERT_SENDER_TO_SUSPECTED_IP_LIST = "INSERT INTO suspected_ip_list (ip_address) VALUES (%s)"
    INSERT_SENDER_TO_SUSPECTED_PHONE_LIST = "INSERT INTO suspected_phone_list (phone) VALUES (%s)"
    INSERT_BAD_WORD_TO_BAD_WORD_LIST = "INSERT INTO bad_words (text, type) VALUES (%s, %s)"
    DELETE_BAD_WORD = "DELETE FROM bad_words where id = %s"
    DELETE_LEAD_WEIGHT = "DELETE FROM lead_weights (lead_type,weight) VALUES (%s, %s)"
    DELETE_BLACK_PHONE = "DELETE FROM black_phone_list where phone = %s"
    INSERT_LEAD_TO_REVIEW_QUEUE = "INSERT INTO review_queue (id, payload, status, date_added) VALUES (%s, %s, %s, %s)"
    GET_LEAD_FROM_REVIEW_QUEUE = "SELECT id, payload FROM review_queue where status = %s order by date_added desc limit 4000"
    GET_LEAD_FROM_REVIEW_QUEUE_BY_ID = "SELECT id, payload FROM review_queue where id = %s"
    DELETE_PATTERN_EMAIL = "DELETE FROM pattern_email_list where email = %s"
    DELETE_BLACK_EMAIL = "DELETE FROM black_email_list where email = %s"
    DELETE_BLACKLISTED_IP = "DELETE FROM black_ip_list where ip_address = %s"
    DELETE_ALGORITHM_CONFIG = "DELETE FROM algorithm_config where id = %s"
    DELETE_WHITE_EMAIL = "DELETE FROM whitelist_emails where email = %s"
    DELETE_WHITE_IP = "DELETE FROM whitelist_ip where ip_address = %s"
    DELETE_WHITE_PHONE = "DELETE FROM whitelist_phone where phone = %s"
    DELETE_WHITELISTED_URL = "DELETE FROM whitelist_urls where url = %s"
    DELETE_SUSPECTED_EMAIL = "DELETE FROM suspected_email_list where email = %s"
    DELETE_SUSPECTED_IP = "DELETE FROM suspected_ip_list where ip_address = %s"
    DELETE_SUSPECTED_PHONE = "DELETE FROM suspected_phone_list where phone = %s"
    UPDATE_PENDING_LEAD = "UPDATE review_queue set status = %s, date_updated = %s, block_reason = %s where id = %s"
    UPDATE_PENDING_LEAD_NO_REASON = "UPDATE review_queue set status = %s, date_updated = %s where id = %s"
    GET_SENDER_TO_PURAGE = "SELECT email, last_lead_submited_time_stamp FROM incoming_leads where last_lead_submited_time_stamp < %s"
    PURGE_SENDERS = "DELETE FROM incoming_leads where email in %s and last_lead_submited_time_stamp in %s"
    GET_S4_CONFIG = "SELECT value FROM s4_config where name = %s AND lead_type = %s"
    GET_RULE_TYPE_ALGORITHM_CONFIG = "SELECT * FROM algorithm_config where rule_type = %s"
    GET_MAX_MINUTE_ALGORITHM_CONFIG = "SELECT MAX(minute) as max_minute FROM algorithm_config where rule_type = %s"

    SPAM_BAD_WORDS_CACHE_KEY = "spam_bad_words"
    SPAM_BLACK_PHONE_CACHE_KEY = "black_phone_list"
    SPAM_PATTERN_EMAIL_LIST_CACHE_KEY = "pattern_email_list"
    SPAM_SUSPECTED_PHONE_LIST_CACHE_KEY = "suspected_phone_list"
    SPAM_BLACK_EMAIL_LIST_CACHE_KEY = "black_email_list"
    SPAM_ALGORITHM_CONFIG_CACHE_KEY = "algorithm_spam_list"
    SPAM_RULE_TYPE_CACHE_KEY = "rule_type_list"
    SPAM_BLACKLIST_IP_CACHE_KEY = "black_ip_list"
    SPAM_LEAD_WEIGHTS_CACHE_KEY = "lead_weight_list"
    SPAM_WHITELISTED_URL_LIST_CACHE_KEY = "whitelisted_url_list"
    SPAM_WHITE_EMAIL_LIST_CACHE_KEY = "white_email_list"
    SPAM_WHITELISTED_IP_CACHE_KEY = "whitelisted_ip"
    SPAM_WHITELISTED_PHONE_CACHE_KEY = "whitelisted_phone"
    SPAM_SUSPECTED_EMAIL_LIST_CACHE_KEY = "suspected_email_list"
    ALGORITHM_EMAIL_CONFIG_CACHE_KEY = "algorithm_email_config"
    ALGORITHM_IP_CONFIG_CACHE_KEY = "algorithm_ip_config"
    ALGORITHM_PHONE_CONFIG_CACHE_KEY = "algorithm_phone_config"
    SPAM_SUSPECTED_IP_LIST_CACHE_KEY = "suspected_ip_list"
    CACHE_TTL = 300
    SUSPECTED_PHONE_CACHE_TTL = 300
    SUSPECTED_EMAIL_CACHE_TTL = 300
    S4_CONFIG_CACHE_TTL = 3600
    def get_bad_words_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_BAD_WORDS_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_BAD_WORDS_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write bad words to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_BAD_WORDS_LIST)
        return result

    def add_to_bad_words_list(self, text, type_):
        params = (text, type_)
        self.pgsqlDao.insert(self.INSERT_BAD_WORD_TO_BAD_WORD_LIST, params)

    def delete_bad_word(self, id_):
        params = (id_,)
        result = self.pgsqlDao.delete(self.DELETE_BAD_WORD, params)
        return result

    def get_black_phone_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_BLACK_PHONE_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_BLACK_PHONE_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write black phone to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_BLACK_PHONE_LIST)
        return result
    def get_rule_type_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_RULE_TYPE_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_RULE_TYPE_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write rule type to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_RULE_TYPE_LIST)
        return result

    def add_to_black_phone_list(self, black_phone):
        params = (black_phone,)
        self.pgsqlDao.insert(self.INSERT_BLACK_PHONE_LIST, params)

    def delete_black_phone_list(self, phone):
        params = (phone,)
        result = self.pgsqlDao.delete(self.DELETE_BLACK_PHONE, params)
        return result

    def get_suspected_phone_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_SUSPECTED_PHONE_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_SUSPECTED_PHONE_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.SUSPECTED_PHONE_CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write black phone to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_SUSPECTED_PHONE_LIST)
        return result
    # def add_to_suspected_phone_list(self, black_phone):
    #     params = (black_phone,)
    #     self.pgsqlDao.insert(self.INSERT_SUSPECTED_PHONE_LIST, params)

    # def delete_suspected_phone_list(self, phone):
    #     params = (phone,)
    #     result = self.pgsqlDao.delete(self.DELETE_SUSPECTED_PHONE, params)
    #     return result

    def get_pattern_email_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_PATTERN_EMAIL_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_PATTERN_EMAIL_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write pattern email to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_PATTERN_EMAIL_LIST)
        return result

    def get_black_email_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_BLACK_EMAIL_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_BLACK_EMAIL_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write black email to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_BLACK_EMAIL_LIST)
        return result
    def get_blacklist_ip(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_BLACKLIST_IP_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_BLACKLIST_IP)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write blacklisted ip to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_BLACKLIST_IP)
        return result

    def get_whitelisted_url_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_WHITELISTED_URL_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_WHITELISTED_URL_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write whitelisted url to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_WHITELISTED_URL_LIST)
        return result

    def get_lead_weights(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_LEAD_WEIGHTS_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_WEIGHTS)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write lead weights to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_WEIGHTS)
        return result
    def get_algorithm_config(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_ALGORITHM_CONFIG_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_ALGORITHM_CONFIG)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write algorithm config to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_ALGORITHM_CONFIG)
        return result

    def get_single_algorithm_config(self, id_):
        params = (id_,)
        result = self.pgsqlDao.get(self.GET_SINGLE_ALGORITHM_CONFIG, params)
        return result

    def get_domain_id(self, name):
        params = (name,)
        result = self.pgsqlDao.get(self.GET_DOMAIN_ID, params)
        result = result[0]['id']
        return result

    def get_pending_review(self):
        pending_id = self.pgsqlDao.get(self.GET_PENDING_REVIEW)
        pending_id_list = [row['id'] for row in pending_id]
        return pending_id_list

    def get_whitelisted_ip(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_WHITELISTED_IP_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_WHITELISTED_IP)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write whitelisted ip to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_WHITELISTED_IP)
        return result
    def get_whitelisted_phone(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_WHITELISTED_PHONE_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_WHITELISTED_PHONE)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write whitelisted phone to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_WHITELISTED_PHONE)
        return result

    def get_white_email_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_WHITE_EMAIL_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_WHITE_EMAIL_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write black email to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_WHITE_EMAIL_LIST)
        return result

    def add_to_pattern_email_list(self, sender_email):
        params = (sender_email,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_PATTERN_EMAIL_LIST, params)

    def add_to_black_email_lsit(self, sender_email):
        params = (sender_email,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_BLACK_EMAIL_LIST, params)

    def add_to_black_ip_list(self, sender_ip):
        params = (sender_ip,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_BLACKLIST_IP, params)
    # def add_to_lead_weight_list(self, lead_type, weight):
    #     params = (lead_type, weight)
    #     self.pgsqlDao.insert(self.INSERT_TO_LEAD_WEIGHT_LIST, params)

    def delete_algorithm_config(self, id_):
        params = (id_,)
        result = self.pgsqlDao.delete(self.DELETE_ALGORITHM_CONFIG, params)
        return result

    def delete_black_ip(self, ip):
        params = (ip,)
        result = self.pgsqlDao.delete(self.DELETE_BLACKLISTED_IP, params)
        return result

    def delete_pattern_email(self, email):
        params = (email,)
        result = self.pgsqlDao.delete(self.DELETE_PATTERN_EMAIL, params)
        return result

    def delete_black_email(self, email):
        params = (email,)
        result = self.pgsqlDao.delete(self.DELETE_BLACK_EMAIL, params)
        return result

    def add_to_white_email_lsit(self, sender_email):
        params = (sender_email,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_WHITE_EMAIL_LIST, params)

    def add_to_whitelisted_ip(self, sender_ip):
        params = (sender_ip,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_WHITELISTED_IP, params)

    def add_to_whitelisted_phone(self, sender_phone):
        params = (sender_phone,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_WHITELISTED_PHONE, params)

    def delete_whitelisted_ip(self, ip):
        params = (ip,)
        result = self.pgsqlDao.delete(self.DELETE_WHITE_IP, params)
        return result

    def delete_whitelisted_phone(self, phone):
        params = (phone,)
        result = self.pgsqlDao.delete(self.DELETE_WHITE_PHONE, params)
        return result

    def delete_white_email(self, email):
        params = (email,)
        result = self.pgsqlDao.delete(self.DELETE_WHITE_EMAIL, params)
        return result

    def add_to_whitelisted_url_list(self, sender_url):
        params = (sender_url,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_WHITELISTED_URL_LIST, params)

    def delete_whitelisted_url(self, url):
        params = (url,)
        result = self.pgsqlDao.delete(self.DELETE_WHITELISTED_URL, params)
        return result
    def get_suspected_email_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_SUSPECTED_EMAIL_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_SUSPECTED_EMAIL_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.SUSPECTED_EMAIL_CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write suspected email to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_SUSPECTED_EMAIL_LIST)
        return result

    def get_suspected_ip_list(self, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = self.SPAM_SUSPECTED_IP_LIST_CACHE_KEY

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_SUSPECTED_IP_LIST)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.SUSPECTED_EMAIL_CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write suspected email to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_SUSPECTED_IP_LIST)
        return result
    def add_to_suspected_email_lsit(self, sender_email):
        params = (sender_email,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_SUSPECTED_EMAIL_LIST, params)

    def add_to_suspected_ip_list(self, sender_ip):
        params = (sender_ip,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_SUSPECTED_IP_LIST, params)

    def add_to_suspected_phone_list(self, sender_phone):
        params = (sender_phone,)
        self.pgsqlDao.insert(self.INSERT_SENDER_TO_SUSPECTED_PHONE_LIST, params)

    def delete_suspected_email(self, email):
        params = (email,)
        result = self.pgsqlDao.delete(self.DELETE_SUSPECTED_EMAIL, params)
        return result

    def delete_suspected_ip(self, ip):
        params = (ip,)
        result = self.pgsqlDao.delete(self.DELETE_SUSPECTED_IP, params)
        return result

    def delete_suspected_phone_list(self, ip):
        params = (ip,)
        result = self.pgsqlDao.delete(self.DELETE_SUSPECTED_PHONE, params)
        return result

    def add_to_review_queue(self, id_, payload):
        from datetime import datetime, timezone, timedelta
        # America/Los_Angeles is UTC-8 or UTC-7 (with DST); using pytz is more accurate, but for now:
        import pytz
        la = pytz.timezone('America/Los_Angeles')
        current_utc_time = int(datetime.now(la).timestamp())
        params = (id_, payload, SpamFilter.SPAM_REVIEW_PENDING, current_utc_time)
        self.pgsqlDao.insert(self.INSERT_LEAD_TO_REVIEW_QUEUE, params)

    def get_lead_from_review_queue(self, status):
        params = (status,)
        result = self.pgsqlDao.get(self.GET_LEAD_FROM_REVIEW_QUEUE, params)
        return result

    def get_lead_from_review_queue_by_id(self, id_):
        params = (id_,)
        result = self.pgsqlDao.get(self.GET_LEAD_FROM_REVIEW_QUEUE_BY_ID, params)
        return result

    def update_pending_lead(self, id_, status, reason=None):
        from datetime import datetime
        import pytz
        la = pytz.timezone('America/Los_Angeles')
        current_utc_time = int(datetime.now(la).timestamp())
        if reason is None:
            params = (status, current_utc_time, id_)
            self.pgsqlDao.update(self.UPDATE_PENDING_LEAD_NO_REASON, params)
        else:
            params = (status, current_utc_time, reason, id_)
            self.pgsqlDao.update(self.UPDATE_PENDING_LEAD, params)

    def get_sender(self, sender_email):
        params = (sender_email,)
        result = self.pgsqlDao.get(self.GET_SENDER, params)
        return result

    def get_rule_type_config(self, rule_type, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None
        params = (rule_type,)
        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        if use_cache and self.cacheInstance is not None:
            if rule_type == 'email':
                cacheKey = self.ALGORITHM_EMAIL_CONFIG_CACHE_KEY
            elif rule_type == 'ip_address':
                cacheKey = self.ALGORITHM_IP_CONFIG_CACHE_KEY
            elif rule_type == 'phone':
                cacheKey = self.ALGORITHM_PHONE_CONFIG_CACHE_KEY
            else:
                cacheKey = None

            if cacheKey and self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                MoveService.log_info(f"Redis cache missed for key={cacheKey}")
                result = self.pgsqlDao.get(self.GET_RULE_TYPE_ALGORITHM_CONFIG, params)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": "Failed to write algorithm config to Redis cache"}
                    MoveService.log_error(error)
        else:
            result = self.pgsqlDao.get(self.GET_RULE_TYPE_ALGORITHM_CONFIG, params)
        return result
    def get_sender_ip(self, sender_ip):
        params = (sender_ip,)
        result = self.pgsqlDao.get(self.GET_SENDER_IP, params)
        return result

    def get_sender_phone(self, sender_phone):
        params = (sender_phone,)
        result = self.pgsqlDao.get(self.GET_SENDER_PHONE, params)
        return result

    def save_or_update_sender(self, sender_email, sender_ip, lead_method, last_lead_submited_time_stamp, sender_exist, sender_phone):
        if not sender_exist:
            params = (sender_email, sender_ip, lead_method, last_lead_submited_time_stamp, sender_phone)
            self.pgsqlDao.insert(self.INSERT_SENDER, params)
        else:
            params = (last_lead_submited_time_stamp, sender_email)
            self.pgsqlDao.update(self.UPDATE_SENDER, params)

    def add_to_algorithm_config(self, rule_type, lead_count, minute):
        params = (rule_type, lead_count, minute)
        self.pgsqlDao.insert(self.INSERT_ALGORITHM_CONFIG, params)

    def update_weight(self, weight, lead_type):
        params = (weight, lead_type)
        self.pgsqlDao.update(self.UPDATE_WEIGHT, params)

    def update_algorithm_config(self, id_, rule_type, lead_count, minute):
        params = (rule_type, lead_count, minute, id_)
        self.pgsqlDao.update(self.UPDATE_ALGORITHM_CONFIG, params)

    def delete_sender(self, sender_email, time):
        params = (sender_email, time)
        result = self.pgsqlDao.delete(self.DELETE_SENDER, params)
        return result

    def delete_sender_ip(self, sender_ip, time):
        params = (sender_ip, time)
        result = self.pgsqlDao.delete(self.DELETE_SENDER_IP, params)
        return result

    def delete_sender_phone(self, sender_phone, time):
        params = (sender_phone, time)
        result = self.pgsqlDao.delete(self.DELETE_SENDER_PHONE, params)
        return result

    # def get_phone_sender(self, black_phone):
    #     params = (black_phone,)
    #     result = self.pgsqlDao.get(self.GET_PHONE_SENDER, params)
    #     return result

    # def save_or_update_phone_sender(self, black_phone, last_lead_submited_time_stamp, sender_exist):
    #     if not sender_exist:
    #         params = (black_phone, last_lead_submited_time_stamp)
    #         self.pgsqlDao.insert(self.INSERT_PHONE_SENDER, params)
    #     else:
    #         params = (last_lead_submited_time_stamp, black_phone)
    #         self.pgsqlDao.update(self.UPDATE_PHONE_SENDER, params)

    # def delete_phone_sender(self, black_phone, time):
    #     params = (black_phone, time)
    #     result = self.pgsqlDao.delete(self.DELETE_PHONE_SENDER, params)
    #     return result

    def get_senders_to_purage(self, purage_threshold_time):
        params = (purage_threshold_time,)
        result = self.pgsqlDao.get(self.GET_SENDER_TO_PURAGE, params)
        return result
    def purge_sender_lists(self, purge_sql, email_list_str, last_lead_submited_time_stamp_list_str):
        email_list_str_token = email_list_str.split(',')
        time_stamp_list_str_token = last_lead_submited_time_stamp_list_str.split(',')

        param_types = ""
        param_types += 's' * len(email_list_str_token)
        param_types += 'i' * len(time_stamp_list_str_token)

        params = []
        params.extend(email_list_str_token)
        params.extend([int(ts) for ts in time_stamp_list_str_token])

        result = self.pgsqlDao.delete(purge_sql, tuple(params))
        return result

    def get_s4_confg(self, name, lead_type, use_cache=None):
        result = None
        cache_enabled = self.cacheInstance is not None

        if use_cache is None:
            use_cache = cache_enabled
        else:
            use_cache = True if str(use_cache).lower() == "true" else False

        cacheKey = name.strip().lower()

        if use_cache and self.cacheInstance:
            if self.cacheInstance.exists(cacheKey):
                MoveService.log_info(f"Redis cache hit for key={cacheKey}")
                value = self.cacheInstance.get(cacheKey)
                result = pickle.loads(value)
            else:
                params = (name, lead_type)
                result = self.pgsqlDao.get(self.GET_S4_CONFIG, params)
                try:
                    if result is not None:
                        self.cacheInstance.setex(cacheKey, self.S4_CONFIG_CACHE_TTL, pickle.dumps(result))
                except Exception as e:
                    error = {"code": "MoveServiceErroRedisWriteCacheFailed", "message": f"Failed to write S4 config: {cacheKey} to Redis cache"}
                    MoveService.log_error(error)
        else:
            params = (name, lead_type)
            result = self.pgsqlDao.get(self.GET_S4_CONFIG, params)
        return result

    def get_max_minute(self, rule_type):
        params = (rule_type,)
        result = self.pgsqlDao.get(self.GET_MAX_MINUTE_ALGORITHM_CONFIG, params)
        return result

    def get_lead_email_type_count(self, email, lead_method, current_time, time_in_sec):
        params = (email, lead_method, current_time, time_in_sec)
        result = self.pgsqlDao.get(self.GET_LEAD_EMAIL_TYPE_COUNT, params)
        value = 0
        if result:
            for row in result:
                for c_name, c_val in row.items():
                    if c_name.lower() == 'count':
                        value = c_val
                        break
        return int(value)

    def get_lead_ip_type_count(self, ip, lead_method, current_time, time_in_sec):
        params = (ip, lead_method, current_time, time_in_sec)
        result = self.pgsqlDao.get(self.GET_LEAD_IP_TYPE_COUNT, params)
        value = 0
        if result:
            for row in result:
                for c_name, c_val in row.items():
                    if c_name.lower() == 'count':
                        value = c_val
                        break
        return int(value)

    def get_lead_phone_type_count(self, phone, lead_method, current_time, time_in_sec):
        params = (phone, lead_method, current_time, time_in_sec)
        result = self.pgsqlDao.get(self.GET_LEAD_PHONE_TYPE_COUNT, params)
        value = 0
        if result:
            for row in result:
                for c_name, c_val in row.items():
                    if c_name.lower() == 'count':
                        value = c_val
                        break
        return int(value)

    def close(self):
        self.pgsqlDao.close()

    def __del__(self):
        self.pgsqlDao.close()
        if self.cacheInstance is not None:
            self.cacheInstance.close()

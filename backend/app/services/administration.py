import json
from typing import Union, List, Dict, Any
from app.dao.spamdao import SpamDAO
from app import config
from fastapi.responses import JSONResponse

class Administration:
    def __init__(self) -> None:
        """
        Initializes Administration service with spam detection database connection.
        """
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
    def add_algorithm_config(self, post_body: str) -> JSONResponse:
        """
        Adds new algorithm configuration for spam detection rules.
        """
        data = json.loads(post_body)
        rule_type = data.get("rule_type", "").strip()
        lead_count = data.get("lead_count", 0)
        minute = data.get("minute", 0)

        if (rule_type or lead_count or minute):
            self.spamDAO.add_to_algorithm_config(rule_type, lead_count, minute)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "algorithm config added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Single Algorithm Config
    def get_single_algorithm_config(self, post_body: str) -> JSONResponse:
        """
        Retrieves specific algorithm configuration by ID.
        """
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
    def update_algorithm_config(self, post_body: str) -> JSONResponse:
        """
        Updates existing algorithm configuration with new parameters.
        """
        data = json.loads(post_body)
        id_ = data.get("id", 0)
        rule_type = data.get("rule_type", "").strip()
        lead_count = data.get("lead_count", 0)
        minute = data.get("minute", 0)

        if id_ or rule_type or lead_count or minute:
            self.spamDAO.update_algorithm_config(id_, rule_type, lead_count, minute)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "Algorithm Config updated successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Algorithm Config
    def get_algorithm_config(self) -> JSONResponse:
        """
        Retrieves all algorithm configurations for spam detection.
        """
        algorithm_config_result = self.spamDAO.get_algorithm_config("false")

        response = {
            "meta": {"build": "1.0.0"},
            "result": algorithm_config_result
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Algorithm Config
    def delete_algorithm_config(self, post_body: str) -> JSONResponse:
        """
        Deletes algorithm configuration by ID.
        """
        data = json.loads(post_body)
        id_ = data.get("id",0)
        if id_:
            self.spamDAO.delete_algorithm_config(id_)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "algorithm config deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Bad Words List
    def get_bad_words_list(self) -> JSONResponse:
        """
        Retrieves list of bad words used for spam filtering.
        """
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
    def add_bad_word(self, post_body: bytes) -> JSONResponse:
        """
        Adds new bad word to spam filtering dictionary.
        """
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

        response = {
            "meta": {"build": "1.0.0"},
            "result": "bad_word added successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Delete Bad Word
    def delete_bad_word(self, post_body: bytes) -> JSONResponse:
        """
        Deletes bad words from spam filtering dictionary by IDs.
        """
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        id_list = data.get("ids", [])

        if id_list:
            for id_ in id_list:
                self.spamDAO.delete_bad_word(id_)

        response = {
            "meta": {"build": "1.0.0"},
            "result": "bad_words deleted successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Get Lead Weights
    def get_lead_weights(self) -> JSONResponse:
        """
        Retrieves lead type weights used in spam detection algorithms.
        """
        lead_weights_result = [] 
        lead_weights_result = self.spamDAO.get_lead_weights(False)
        response = {
            "meta": {"build": "1.0.0"},
            "lead_weights": lead_weights_result
        }
        return JSONResponse(content=response, headers={"Expires": "0"})

    # Update Lead Weight
    def update_weight(self, post_body: bytes) -> JSONResponse:
        """
        Updates weight value for specific lead type in spam detection.
        """
        post_body = post_body.decode("utf-8")
        data = json.loads(post_body)
        lead_type = data.get("lead_type", "").strip()
        weight = data.get("weight", 0)
        if lead_type and weight:
            self.spamDAO.update_weight(weight, lead_type)
        response = {
            "meta": {"build": "1.0.0"},
            "result": "Lead weight updated successfully"
        }
        return JSONResponse(content=response, headers={"Expires": "0"})



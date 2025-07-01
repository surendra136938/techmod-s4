from abc import ABC, abstractmethod


class SpamFilterInterface(ABC):
    """
    Abstract base class for spam filters.
    """

    # Constants
    NOT_SPAM = "not_spam"
    IS_SPAM = "is_spam"
    MAYBE_SPAM = "maybe_spam"
    BAD_EMAIL = "malformed-email"
    BAD_WORD_TYPE_BANNED = "banned"
    BAD_WORD_TYPE_SUSPICIOUS = "suspicious"
    SPAM_REVIEW_PENDING = "pending"
    LEAD_TYPE_CO_BROKE = "co_broke"
    LEAD_TYPE_FAR = "find_a_realtor"
    BLOCKED = "is_blocked"
    NOT_BLOCKED = "not_blocked"
    MAYBE_BLOCKED = "maybe_blocked"
    BLACKLIST = "blacklist"
    WHITELIST = "whitelist"
    PATTERN_MATCH = "pattern_match"
    ALGORITHM_MATCH = "algorithm_match"

    @abstractmethod
    def filter(self, lead_payload: dict) -> dict:
        """
        Abstract method to filter spam based on the lead payload.

        Args:
            lead_payload (dict): The lead payload to be analyzed.

        Returns:
            dict: The result of the spam detection.
        """
        pass

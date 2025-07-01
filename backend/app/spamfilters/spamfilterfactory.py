from app.spamfilters.simplespamfilter import SimpleSpamFilter
from app.spamfilters.farspamfilter import FARSpamFilter
from app.spamfilters.spamfilterinterface import SpamFilterInterface


class SpamFilterFactory:
    """
    Factory class to create instances of spam filters based on lead type.
    """

    @staticmethod
    def get_spam_filter(lead_type: str):
        """
        Get the appropriate spam filter instance based on the lead type.

        Args:
            lead_type (str): The type of lead.

        Returns:
            SpamFilter: An instance of the appropriate spam filter.
        """
        if lead_type == SpamFilterInterface.LEAD_TYPE_CO_BROKE:
            return SimpleSpamFilter(lead_type)
        elif lead_type == SpamFilterInterface.LEAD_TYPE_FAR:
            return FARSpamFilter(lead_type)
        else:
            return SimpleSpamFilter(lead_type)

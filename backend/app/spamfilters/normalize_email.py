import re
import logging

class NormalizeEmail:
    """
    Normalizes email addresses based on provider-specific rules.
    """

    # Patterns for normalization
    PLUS_ONLY = r'\+.*$'
    PLUS_AND_DOT = r'\.|\+.*$'

    # Normalizable providers and their rules
    _normalizeable_providers = {
        'gmail.com': {'remove_pattern': PLUS_AND_DOT},
        'googlemail.com': {'remove_pattern': PLUS_AND_DOT, 'alias_of': 'gmail.com'},
        'hotmail.com': {'remove_pattern': PLUS_ONLY},
        'live.com': {'remove_pattern': PLUS_AND_DOT},
        'outlook.com': {'remove_pattern': PLUS_ONLY},
    }

    @staticmethod
    def normalize_email(email: str) -> str:
        """
        Normalizes email address using provider-specific rules and patterns.
        """
        try:
            logging.info(f"Normalizing email: {email}")
            email = email.lower()
            email_parts = email.split('@')

            if len(email_parts) != 2:
                logging.warning(f"Invalid email format: {email}")
                return email

            username, domain = email_parts

            if domain in NormalizeEmail._normalizeable_providers:
                provider_rules = NormalizeEmail._normalizeable_providers[domain]

                # Apply the remove pattern if it exists
                if 'remove_pattern' in provider_rules:
                    username = re.sub(provider_rules['remove_pattern'], '', username)

                # Replace the domain with its alias if it exists
                if 'alias_of' in provider_rules:
                    domain = provider_rules['alias_of']

            normalized_email = f"{username}@{domain}"
            logging.info(f"Normalized email: {normalized_email}")
            return normalized_email

        except Exception as e:
            logging.error(f"Error normalizing email: {str(e)}")
            return email

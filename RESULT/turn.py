import logging
import os

import streamlit as st
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


def get_ice_servers():
    """
    Get the list of ICE servers from Twilio API.
    If the Twilio credentials are not set, fallback to a free STUN server from Google.

    Returns:
        List[Dict[str, str]]: A list of ICE servers.
    """
    try:
        # Get the Twilio account SID and auth token from environment variables
        account_sid = os.environ["TWILIO_ACCOUNT_SID"]
        auth_token = os.environ["TWILIO_AUTH_TOKEN"]
    except KeyError:
        # If the credentials are not set, fallback to a free STUN server from Google
        logger.warning(
            "Twilio credentials are not set. Fallback to a free STUN server from Google."
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    client = Client(account_sid, auth_token)

    try:
        # Create a new token to access the Twilio API
        token = client.tokens.create()
    except TwilioRestException as e:
        # If an error occurs while accessing the Twilio API, fallback to a free STUN server from Google
        st.warning(
            f"Error occurred while accessing Twilio API. Fallback to a free STUN server from Google. ({e})"
        )
        return [{"urls": ["stun:stun.l.google.com:19302"]}]

    # Return the list of ICE servers
    return token.ice_servers

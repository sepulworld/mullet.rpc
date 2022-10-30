import asyncio
import json

from okta_jwt_verifier import AccessTokenVerifier, IDTokenVerifier


loop = asyncio.get_event_loop()


def is_access_token_valid(token, issuer):
    jwt_verifier = AccessTokenVerifier(issuer=issuer, audience='api://default')
    try:
        loop.run_until_complete(jwt_verifier.verify(token))
        return True
    except Exception:
        return False


def is_id_token_valid(token, issuer, client_id, nonce):
    jwt_verifier = IDTokenVerifier(issuer=issuer, client_id=client_id, audience='api://default')
    try:
        loop.run_until_complete(jwt_verifier.verify(token, nonce=nonce))
        return True
    except Exception:
        return False


def load_config(fname='./client_secrets.json'):
    config = None
    with open(fname) as f:
        config = json.load(f)
    return config


oauth_config = load_config()
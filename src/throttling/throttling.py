import inspect, ipaddress

from typing import Optional

from functools import wraps

from fastapi import Request, status, HTTPException

from huggingface_hub import parse_huggingface_oauth

from upstash_ratelimit.asyncio import Ratelimit

from settings import ApplicationSettings

app_settings = ApplicationSettings()

def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def extract_client_ip_from_xff_header(request: Request, client_ip_is_rightmost_in_xff_header: bool = False) -> Optional[str]:
    header_value = request.headers.get("X-Forwarded-For")

    if not header_value:
        return None

    ip_candidates = [ ip.strip() for ip in header_value.split(",") if ip.strip() ]

    if not ip_candidates:
        return None

    candidate_ip = ip_candidates[-1] if client_ip_is_rightmost_in_xff_header else ip_candidates[0]

    return candidate_ip if is_valid_ip(candidate_ip) else None

def extract_ip_from_client(request: Request) -> Optional[str]:
    if not request.client:
        return None

    client_ip = getattr(request.client, "host", None)

    return client_ip if client_ip and is_valid_ip(client_ip) else None

def get_remote_address(request: Request) -> str:
    if app_settings.APP_TRUST_XFF_HEADER:
        ip_from_xff = extract_client_ip_from_xff_header(request, app_settings.APP_CLIENT_IP_IS_RIGHTMOST_IN_XFF_HEADER)
        if ip_from_xff:
            return ip_from_xff

    direct_ip = extract_ip_from_client(request)
    if direct_ip:
        return direct_ip

    return "127.0.0.1"

def get_identifier_for_rate_limiting(request: Request) -> str:
    if app_settings.APP_ENABLE_HF_AUTHENTICATION:
        oauth_info = parse_huggingface_oauth(request)

        if oauth_info:
            if oauth_info.user_info.preferred_username in app_settings.APP_RATE_LIMITING_HF_WHITELIST:
                return None

            return f'u:{oauth_info.user_info.sub}'

    return f'h:{get_remote_address(request)}'

def require_rate_limit(limiter: Ratelimit):
    def decorator(func):
        sig = inspect.signature(func)
        for idx, parameter in enumerate(sig.parameters.values()):
            if parameter.name == "request":
                break
        else:
            raise RuntimeError(f'No "request" argument found on function "{func}".')

        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request", args[idx] if args else None)

            if not isinstance(request, Request):
                raise RuntimeError('Parameter "request" must be an instance of "starlette.requests.Request"')

            if app_settings.APP_ENABLE_RATE_LIMITING:
                rate_limit_identifier = get_identifier_for_rate_limiting(request)

                if rate_limit_identifier:
                    response = await limiter.limit(rate_limit_identifier)

                    if not response.allowed:
                        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="You have exceeded the rate limit. Please try again later.")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
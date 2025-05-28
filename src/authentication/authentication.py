import inspect

from functools import wraps

from fastapi import Request, status, HTTPException

from huggingface_hub import parse_huggingface_oauth

from settings import ApplicationSettings

app_settings = ApplicationSettings()

def require_authentication():
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

            if app_settings.APP_ENABLE_HF_AUTHENTICATION:
                oauth_info = parse_huggingface_oauth(request)

                if not oauth_info:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please sign in using your Hugging Face account to continue.")

            return await func(*args, **kwargs)
        return wrapper
    return decorator
##################
# Import Modules #
##################

import json, httpx, requests

from urllib.parse import urlparse

from fastapi import FastAPI, status, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException

from authlib.integrations.starlette_client import OAuthError

from upstash_ratelimit.asyncio import Ratelimit, FixedWindow
from upstash_redis.asyncio import Redis

from huggingface_hub import attach_huggingface_oauth, parse_huggingface_oauth

from payloads.requests import ChatRequest, EmbedRequest, SearchRequest, ScrapeRequest, CreditRequest, SummarizeRequest, TraceRequest
from payloads.responses import ChatResponse, EmbedResponse, SearchResponse, ScrapeResponse, SummarizeResponse, TraceResponse, ErrorResponse, ValidationErrorResponse
from handlers import http_exception_handler, request_validation_error_handler, unhandled_exception_handler, oauth_error_handler
from authentication import require_authentication
from throttling import require_rate_limit
from tokenization import truncate_text_from_end, truncate_text_from_middle, preload_model_encodings
from settings import ApplicationSettings

########################
# Application Settings #
########################

app_settings = ApplicationSettings()

######################
# Model Tokenization #
######################

model_maximum_context_tokens_length = {
    "text-embedding-3-small" : 8191,
    "gpt-4o" : 128000
}

preload_model_encodings(model_maximum_context_tokens_length.keys())

###################
# API Application #
###################

templates = Jinja2Templates(directory="templates")

app = FastAPI(title="GiveBackGPT API", redoc_url=None, version=app_settings.APP_VERSION)

app.add_exception_handler(Exception, unhandled_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_error_handler)
app.add_exception_handler(OAuthError, oauth_error_handler)

app.mount("/static", StaticFiles(directory="static"), name="static")

#################
# Rate Limiters #
#################

redis = Redis(url=app_settings.APP_UPSTASH_REDIS_REST_URL, token=app_settings.APP_UPSTASH_REDIS_REST_TOKEN)

rate_limit_search = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_SEARCH_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_SEARCH_RATE_LIMIT_WINDOW), prefix="rl:search")
rate_limit_embed = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_EMBED_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_EMBED_RATE_LIMIT_WINDOW), prefix="rl:embed")
rate_limit_chat = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_CHAT_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_CHAT_RATE_LIMIT_WINDOW), prefix="rl:chat")
rate_limit_credit = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_CREDIT_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_CREDIT_RATE_LIMIT_WINDOW), prefix="rl:credit")
rate_limit_scrape = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_SCRAPE_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_SCRAPE_RATE_LIMIT_WINDOW), prefix="rl:scrape")
rate_limit_summarize = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_SUMMARIZE_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_SUMMARIZE_RATE_LIMIT_WINDOW), prefix="rl:summarize")
rate_limit_trace = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_TRACE_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_TRACE_RATE_LIMIT_WINDOW), prefix="rl:trace")
rate_limit_index = Ratelimit(redis=redis, limiter=FixedWindow(max_requests=app_settings.APP_INDEX_RATE_LIMIT_MAX_REQUESTS, window=app_settings.APP_INDEX_RATE_LIMIT_WINDOW), prefix="rl:index")

#############
# Endpoints #
#############

@app.post("/api/search",
          response_model=SearchResponse,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_403_FORBIDDEN: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_search)
async def search(request: Request, search_request: SearchRequest):
    return await internal_search(search_request, search_request.private_key if search_request.private_key else app_settings.APP_SERP_API_KEY)

@app.post("/api/embed",
          response_model=EmbedResponse,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_403_FORBIDDEN: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_embed)
async def embed(request: Request, embed_request: EmbedRequest):
    return await internal_embed(embed_request, embed_request.private_key if embed_request.private_key else app_settings.APP_OPENAI_API_KEY)

@app.post("/api/chat",
          response_model=ChatResponse,
          responses={
            status.HTTP_400_BAD_REQUEST: { "model": ErrorResponse },
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_403_FORBIDDEN: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_chat)
async def chat(request: Request, chat_request: ChatRequest):
    return await internal_chat(chat_request, chat_request.private_key if chat_request.private_key else app_settings.APP_OPENAI_API_KEY)

@app.post("/api/credit",
          status_code=status.HTTP_204_NO_CONTENT,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_credit)
async def credit(request: Request, credit_request: CreditRequest):
    await internal_credit(credit_request)

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.post("/api/scrape",
          response_model=ScrapeResponse,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_scrape)
async def scrape(request: Request, scrape_request: ScrapeRequest):
    return await internal_scrape(scrape_request, scrape_request.private_key if scrape_request.private_key else app_settings.APP_SCRAPING_BEE_API_KEY)

@app.post("/api/summarize",
          response_model=SummarizeResponse,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_403_FORBIDDEN: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_summarize)
async def summarize(request: Request, summarize_request: SummarizeRequest):
    return await internal_summarize(summarize_request, summarize_request.private_key if summarize_request.private_key else app_settings.APP_OPENAI_API_KEY)

@app.post("/api/trace",
          response_model=TraceResponse,
          responses={
            status.HTTP_401_UNAUTHORIZED: { "model": ErrorResponse },
            status.HTTP_403_FORBIDDEN: { "model": ErrorResponse },
            status.HTTP_422_UNPROCESSABLE_ENTITY: { "model": ValidationErrorResponse },
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse },
            status.HTTP_502_BAD_GATEWAY: { "model": ErrorResponse },
            status.HTTP_504_GATEWAY_TIMEOUT: { "model": ErrorResponse }
          })
@require_authentication()
@require_rate_limit(rate_limit_trace)
async def trace(request: Request, trace_request: TraceRequest):
    return await internal_trace(trace_request, trace_request.private_key if trace_request.private_key else app_settings.APP_OPENAI_API_KEY)

@app.get("/",
         response_class=HTMLResponse,
         responses={
            status.HTTP_429_TOO_MANY_REQUESTS: { "model": ErrorResponse },
            status.HTTP_500_INTERNAL_SERVER_ERROR: { "model": ErrorResponse }
         },
         include_in_schema=False)
@require_rate_limit(rate_limit_index)
async def index(request: Request):
    if app_settings.APP_ENABLE_HF_AUTHENTICATION:
        oauth_info = parse_huggingface_oauth(request)

        if oauth_info:
            return templates.TemplateResponse(request=request, name="index.html", context={"show_logout": True, "show_login": False})
        else:
            return templates.TemplateResponse(request=request, name="index.html", context={"show_logout": False, "show_login": True})

    return templates.TemplateResponse(request=request, name="index.html", context={"show_logout": False, "show_login": False})

if app_settings.APP_ENABLE_HF_AUTHENTICATION:
    attach_huggingface_oauth(app, route_prefix="/api")

#####################
# Internal Services #
#####################

async def internal_credit(credit_request: CreditRequest):
    credit_request_data = credit_request.model_dump()

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT, follow_redirects=True) as client:
            response = await client.post(
                app_settings.APP_GOOGLE_APPS_SCRIPT_URL,
                headers={
                    "Content-Type": "text/plain; charset=UTF-8"
                },
                json={
                    "results": credit_request_data['results'],
                    "authentication_key": app_settings.APP_GOOGLE_APPS_SCRIPT_AUTHENTICATION_KEY
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Credit Authors: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Credit Authors: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"Credit Authors: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    if result['status'] == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=result['status'], detail="Credit Authors: The requesting authentication key is not correct.")

    if result['status'] == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Credit Authors: The upstream service encountered an internal error.")

    if result['status'] != status.HTTP_200_OK:
        raise HTTPException(status_code=result['status'], detail=f"Credit Authors: The request failed with HTTP status code {result['status']}. Please try again later or contact support if the issue persists.")

async def internal_chat(chat_request: ChatRequest, api_key: str):
    try:
        api_key.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="LLM API: The requesting API key is not correct or properly configured.")

    chat_request_data = chat_request.model_dump()

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                },
                json={
                    "model": chat_request_data['model'],
                    "messages": chat_request_data['messages']
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"LLM API: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="LLM API: The requesting API key is not correct or properly configured.")

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are accessing the API from an unsupported country, region, or territory.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are sending requests too quickly, have run out of credits, or hit your maximum monthly spend.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="LLM API: The upstream service encountered an internal error.")

    if response.status_code == status.HTTP_400_BAD_REQUEST and json.loads(response.content)['error']['code'] == 'context_length_exceeded':
        raise HTTPException(status_code=response.status_code, detail="LLM API: This conversation exceeds the maximum context length. Please try a shorter message or start a new conversation.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"LLM API: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "text": result["choices"][0]["message"]["content"] }

async def internal_embed(embed_request: EmbedRequest, api_key: str):
    try:
        api_key.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Embeddings API: The requesting API key is not correct or properly configured.")

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.post(
                "https://api.openai.com/v1/embeddings",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                },
                json={
                    "input": truncate_text_from_end(embed_request.input, model_maximum_context_tokens_length[embed_request.model], embed_request.model),
                    "model": embed_request.model
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Embeddings API: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="Embeddings API: The requesting API key is not correct or properly configured.")

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(status_code=response.status_code, detail="Embeddings API: You are accessing the API from an unsupported country, region, or territory.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="Embeddings API: You are sending requests too quickly, have run out of credits, or hit your maximum monthly spend.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Embeddings API: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"Embeddings API: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "embedding": result["data"][0]["embedding"] }

async def internal_search(search_request: SearchRequest, api_key: str):
    try:
        api_key.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Web Search: The requesting API key is not correct or properly configured.")

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.post(
                "https://google.serper.dev/search",
                headers={
                    "X-API-KEY": api_key,
                    "Content-Type": "application/json; charset=utf-8"
                },
                json={
                    "q": search_request.query
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Web Search: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="Web Search: No valid API key provided.")

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(status_code=response.status_code, detail="Web Search: The account associated with this API key doesn't have permission to perform the request. This usually happens if the account has been deleted.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="Web Search: The number of requests sent using this API key exceeds the hourly throughput limit or your account has run out of searches.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Web Search: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"Web Search: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "results": list(map(lambda o: { "link": o["link"], "title": o["title"] }, result['organic'])) }

async def internal_scrape(scrape_request: ScrapeRequest, api_key: str):
    hostname = urlparse(scrape_request.url).hostname or ""

    if any(hostname == domain or hostname.endswith(f".{domain}") for domain in app_settings.APP_SCRAPE_DOMAINS_BLACKLIST):
        return { "text": "" }

    extract_rules = {"text": "body"}

    scraping_url = (
        f"https://app.scrapingbee.com/api/v1"
        f"?url={requests.utils.quote(scrape_request.url)}"
        f"&render_js=true"
        f"&extract_rules={requests.utils.quote(json.dumps(extract_rules))}"
        f"&api_key={api_key}"
    )

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.get(scraping_url)
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"Web Scraping: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="Web Scraping: No more credit available.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="Web Scraping: Too many concurrent requests.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Web Scraping: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"Web Scraping: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "text": result["text"] }

async def internal_summarize(summarize_request: SummarizeRequest, api_key: str):
    try:
        api_key.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="LLM API: The requesting API key is not correct or properly configured.")

    max_prompt_tokens = model_maximum_context_tokens_length[summarize_request.model] - 1000 # We leave some space for the output. For reference, 1 token is approximately 4 characters and 0.75 words in English.

    content = f'Summarize the following text in 30 words only and give only the summary without any other comment: "{summarize_request.input}"'

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                },
                json={
                    "model": summarize_request.model,
                    "messages": [{
                        "role": "user",
                        "content": truncate_text_from_end(content, max_prompt_tokens, summarize_request.model)
                    }]
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"LLM API: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="LLM API: The requesting API key is not correct or properly configured.")

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are accessing the API from an unsupported country, region, or territory.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are sending requests too quickly, have run out of credits, or hit your maximum monthly spend.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="LLM API: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"LLM API: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "text": result["choices"][0]["message"]["content"] }

async def internal_trace(trace_request: TraceRequest, api_key: str):
    try:
        api_key.encode('ascii')
    except UnicodeEncodeError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="LLM API: The requesting API key is not correct or properly configured.")

    max_prompt_tokens = model_maximum_context_tokens_length[trace_request.model] - 1000 # We leave some space for the output. For reference, 1 token is approximately 4 characters and 0.75 words in English.

    content = f'Return just the full name of the author of this webpage without any other comment. If you cannot find an author name just return "Unknown Author" without any other comment: "{trace_request.input}"'

    try:
        async with httpx.AsyncClient(timeout=app_settings.APP_REQUEST_TIMEOUT) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json; charset=utf-8"
                },
                json={
                    "model": trace_request.model,
                    "messages": [{
                        "role": "user",
                        "content": truncate_text_from_middle(content, max_prompt_tokens, trace_request.model)
                    }]
                })
    except httpx.ReadTimeout:
        raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f"LLM API: The upstream service did not respond in time.")

    if response.status_code == status.HTTP_401_UNAUTHORIZED:
        raise HTTPException(status_code=response.status_code, detail="LLM API: The requesting API key is not correct or properly configured.")

    if response.status_code == status.HTTP_403_FORBIDDEN:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are accessing the API from an unsupported country, region, or territory.")

    if response.status_code == status.HTTP_429_TOO_MANY_REQUESTS:
        raise HTTPException(status_code=response.status_code, detail="LLM API: You are sending requests too quickly, have run out of credits, or hit your maximum monthly spend.")

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="LLM API: The upstream service encountered an internal error.")

    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=response.status_code, detail=f"LLM API: The request failed with HTTP status code {response.status_code}. Please try again later or contact support if the issue persists.")

    result = response.json()

    return { "text": result["choices"][0]["message"]["content"] }
from typing import List, Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import field_validator

class ApplicationSettings(BaseSettings):
    APP_OPENAI_API_KEY: str
    APP_SERP_API_KEY: str
    APP_SCRAPING_BEE_API_KEY: str
    APP_GOOGLE_APPS_SCRIPT_URL: str
    APP_GOOGLE_APPS_SCRIPT_AUTHENTICATION_KEY: str
    APP_UPSTASH_REDIS_REST_URL: str
    APP_UPSTASH_REDIS_REST_TOKEN: str
    APP_SEARCH_RATE_LIMIT_MAX_REQUESTS: int
    APP_SEARCH_RATE_LIMIT_WINDOW: int
    APP_SCRAPE_RATE_LIMIT_MAX_REQUESTS: int
    APP_SCRAPE_RATE_LIMIT_WINDOW: int
    APP_CHAT_RATE_LIMIT_MAX_REQUESTS: int
    APP_CHAT_RATE_LIMIT_WINDOW: int
    APP_SUMMARIZE_RATE_LIMIT_MAX_REQUESTS: int
    APP_SUMMARIZE_RATE_LIMIT_WINDOW: int
    APP_TRACE_RATE_LIMIT_MAX_REQUESTS: int
    APP_TRACE_RATE_LIMIT_WINDOW: int
    APP_CREDIT_RATE_LIMIT_MAX_REQUESTS: int
    APP_CREDIT_RATE_LIMIT_WINDOW: int
    APP_INDEX_RATE_LIMIT_MAX_REQUESTS: int
    APP_INDEX_RATE_LIMIT_WINDOW: int
    APP_EMBED_RATE_LIMIT_MAX_REQUESTS: int
    APP_EMBED_RATE_LIMIT_WINDOW: int
    APP_ENABLE_RATE_LIMITING: bool
    APP_ENABLE_HF_AUTHENTICATION: bool
    APP_RATE_LIMITING_HF_WHITELIST: Union[str, List[str]]
    APP_REQUEST_TIMEOUT: float
    APP_SCRAPE_DOMAINS_BLACKLIST: Union[str, List[str]]
    APP_CLIENT_IP_IS_RIGHTMOST_IN_XFF_HEADER: bool
    APP_TRUST_XFF_HEADER: bool
    APP_VERSION: str

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')

    @field_validator("APP_RATE_LIMITING_HF_WHITELIST", "APP_SCRAPE_DOMAINS_BLACKLIST")
    @classmethod
    def assemble_rate_limiting_hf_whitelist(cls, value: Union[str, List[str]]) -> List[str]:
        if isinstance(value, str):
            return [ i.strip() for i in value.split(",") ]
        elif isinstance(value, List):
            return value
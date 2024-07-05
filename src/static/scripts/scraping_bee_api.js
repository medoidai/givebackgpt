import {
    HttpResponseError
} from './http_utils.js';

export async function fetchScrapedContent(url, scrapeApiKey) {
    const apiUrl = '/api/scrape';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            url: url,
            private_key: scrapeApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    const error_statuses = [502, 504];

    if (error_statuses.includes(http_response.status)) {
        throw new Error(`Scrape failed! HTTP error status: ${http_response.status} (${http_response.statusText})`);
    }

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result.text;
}
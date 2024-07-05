import {
    HttpResponseError
} from './http_utils.js';

export async function searchWithSerpApi(query, searchApiKey) {
    const apiUrl = '/api/search';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            query: query,
            private_key: searchApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result;
}
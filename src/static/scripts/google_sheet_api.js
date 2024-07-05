import {
    HttpResponseError
} from './http_utils.js';

export async function sendResultsToGoogleSheet(results) {
    const apiUrl = '/api/credit';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            results: results
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    if (!http_response.ok) {
        const json_result = await http_response.json();

        throw new HttpResponseError(http_response.status, json_result["error"]);
    }
}
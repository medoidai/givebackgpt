import {
    httpCall
} from './http_utils.js';

export async function searchWithSerpApi(query) {
    const apiUrl = 'https://google.serper.dev/search';

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-KEY': localStorage.getItem('serpApiKey')
        },
        body: JSON.stringify({
            q: query
        })
    };

    const http_call_response = await httpCall(apiUrl, requestOptions);

    const json_result = await http_call_response.json();

    return json_result;
}
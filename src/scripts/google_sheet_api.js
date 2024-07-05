import {
    httpCall
} from './http_utils.js';

export async function sendResultsToGoogleSheet(results) {
    const apiUrl = 'https://script.google.com/macros/s/AKfycbwoN4kCdPg83sKbsSzIw52JQOVQXTbWXTaWwY1x46BGpeVZtznPBe7QFDvB0P6uT58Z/exec';

    const requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "text/plain; charset=UTF-8"
        },
        body: JSON.stringify(results)
    };

    const http_call_response = await httpCall(apiUrl, requestOptions);

    const json_result = await http_call_response.json();

    if (!json_result.status || json_result.status === 'fail') {
        throw new Error('Failed to send results to Google Sheet');
    }

    return json_result;
}
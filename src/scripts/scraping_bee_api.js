import {
    httpCall
} from './http_utils.js';

export async function fetchScrapedContent(url) {
    const apiKey = localStorage.getItem('scrapeApiKey');

    const extractRules = encodeURIComponent(JSON.stringify({
        text: "body"
    }));

    const apiUrl = `https://app.scrapingbee.com/api/v1/?url=${encodeURIComponent(url)}&render_js=false&extract_rules=${extractRules}&api_key=${apiKey}`;

    const requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    const http_call_response = await httpCall(apiUrl, requestOptions);

    const json_result = await http_call_response.json();

    return json_result.text.substring(0, 15000);
}
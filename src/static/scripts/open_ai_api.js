import {
    HttpResponseError
} from './http_utils.js';

function calculateDotProduct(vectorA, vectorB) {
    return vectorA.reduce((acc, currentValue, index) => acc + (currentValue * vectorB[index]), 0);
}

export function calculateCosineSimilarity(vectorA, vectorB) {
    return calculateDotProduct(vectorA, vectorB);
}

export async function generateEmbedding(model, input, embeddingsApiKey) {
    const apiUrl = '/api/embed';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            model: model,
            input: input,
            private_key: embeddingsApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result.embedding;
}

export async function chatWithLLM(message, llmApiKey, conversationHistory = []) {
    const apiUrl = '/api/chat';

    conversationHistory.push({ role: 'user', content: message });

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            model: 'gpt-4o',
            messages: conversationHistory,
            private_key: llmApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result.text;
}

export async function traceAuthor(message, llmApiKey) {
    const apiUrl = '/api/trace';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            model: 'gpt-4o',
            input: message,
            private_key: llmApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result.text;
}

export async function summarizeContent(message, llmApiKey) {
    const apiUrl = '/api/summarize';

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({
            model: 'gpt-4o',
            input: message,
            private_key: llmApiKey || null
        })
    };

    const http_response = await fetch(apiUrl, requestOptions);

    const json_result = await http_response.json();

    if (!http_response.ok) {
        throw new HttpResponseError(http_response.status, json_result["error"]);
    }

    return json_result.text;
}
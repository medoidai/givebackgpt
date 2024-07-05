import {
    httpCall
} from './http_utils.js';

function calculateDotProduct(vectorA, vectorB) {
    return vectorA.reduce((acc, currentValue, index) => acc + (currentValue * vectorB[index]), 0);
}

export function calculateCosineSimilarity(vectorA, vectorB) {
    return calculateDotProduct(vectorA, vectorB);
}

export async function generateEmbedding(model, input) {
    const apiUrl = 'https://api.openai.com/v1/embeddings';

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('EmbeddingsApiKey')}`
        },
        body: JSON.stringify({
            input,
            model,
            dimensions: 1000
        })
    };

    const http_call_response = await httpCall(apiUrl, requestOptions);

    const json_result = await http_call_response.json();

    return json_result.data[0].embedding;
}

export async function generateLLMResponse(query, conversationHistory = []) {
    const apiUrl = 'https://api.openai.com/v1/chat/completions';

    conversationHistory.push({ role: 'user', content: query });

    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('LLMApiKey')}`
        },
        body: JSON.stringify({
            model: 'gpt-3.5-turbo',
            messages: conversationHistory
        })
    };

    const http_call_response = await httpCall(apiUrl, requestOptions);

    const json_result = await http_call_response.json();

    return json_result.choices[0].message.content;
}
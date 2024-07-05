import {
  fetchScrapedContent
} from './scraping_bee_api.js';

import {
  searchWithSerpApi
} from './serp_api.js';

import {
  HttpResponseError
} from './http_utils.js';

import {
  generateEmbedding,
  calculateCosineSimilarity,
  summarizeContent,
  traceAuthor
} from './open_ai_api.js';

import {
  appendSearchQuery,
  appendSearchResultsHeader,
  appendSearchProcessingMessage,
  removeSearchProcessingMessage,
  appendSearchErrorMessage,
  displayTopSearchResults,
} from './ui_utils.js';

export async function processSearchQueue(searchQueue, collectedResults, llmApiKey, embeddingsApiKey, scrapeApiKey, searchApiKey) {
  while (searchQueue.length > 0) {
    const llmResponse = searchQueue[0];

    try {
      const summary = await summarizeContent(llmResponse, llmApiKey);

      appendSearchQuery(summary);
      appendSearchResultsHeader();
      appendSearchProcessingMessage();
      const searchResults = await searchWithSerpApi(summary, searchApiKey);
      const topResults = await processSearchResults(searchResults, llmResponse, embeddingsApiKey, scrapeApiKey, llmApiKey);
      removeSearchProcessingMessage();
      displayTopSearchResults(topResults);
      collectedResults.push(...topResults);
    }
    catch (error) {
      console.error(error);

      removeSearchProcessingMessage();

      if (error instanceof HttpResponseError) {
        appendSearchErrorMessage(error.message);

        searchQueue.length = 0;

        throw error;
      }
    }
    finally {
      searchQueue.shift();
    }
  }
}

export async function processSearchResults(resultsJson, llmResponse, embeddingsApiKey, scrapeApiKey, llmApiKey) {
  const topResults = [];

  if (resultsJson.results && resultsJson.results.length > 0) {
      const llmResponseVector = await generateEmbedding('text-embedding-3-small', llmResponse, embeddingsApiKey);

      let count = 0;

      for (const result of resultsJson.results.slice(0, 10)) {
          if (count >= 3) break;

          try {
              const htmlContent = await fetchScrapedContent(result.link, scrapeApiKey);

              if (htmlContent.trim() === '') {
                  console.log(`Skipping link: ${result.link}`);

                  continue;
              }

              let domain = new URL(result.link).hostname;

              const author = await traceAuthor(htmlContent, llmApiKey);

              const searchResultContentVector = await generateEmbedding('text-embedding-3-small', htmlContent, embeddingsApiKey);

              const cosineSimilarity = calculateCosineSimilarity(searchResultContentVector, llmResponseVector);

              topResults.push({
                  author: `${author} (${domain})`,
                  title: result.title,
                  link: result.link,
                  similarity_score: (cosineSimilarity < 0 ? 0 : cosineSimilarity).toFixed(2)
              });

              count++;
          } catch (error) {
              console.error(error);

              if (error instanceof HttpResponseError) {
                  throw error;
              }
          }
      }

      topResults.sort((a, b) => b.similarity_score - a.similarity_score);
  }

  return topResults;
}
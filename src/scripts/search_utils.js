import {
  fetchScrapedContent
} from './scraping_bee_api.js';

import {
  searchWithSerpApi
} from './serp_api.js';

import {
  generateEmbedding,
  calculateCosineSimilarity,
  generateLLMResponse
} from './open_ai_api.js';

import {
  checkCreditAuthorsButtonClickableState,
  appendSearchQuery,
  appendSearchResultsHeader,
  appendSearchProcessingMessage,
  removeSearchProcessingMessage,
  displayTopSearchResults
} from './ui_utils.js';

export async function processSearchQueue(searchQueue, collectedResults) {
  while (searchQueue.length > 0) {
    const llmResponse = searchQueue[0];

    try {
      const summary = await generateLLMResponse(`Summarize the following text in 30 words only and give only the summary without any other comment: "${llmResponse}"`);

      appendSearchQuery(summary);
      appendSearchResultsHeader();
      appendSearchProcessingMessage();
      const searchResults = await searchWithSerpApi(summary);
      const topResults = await processSearchResults(searchResults, llmResponse);
      removeSearchProcessingMessage();
      displayTopSearchResults(topResults);
      collectedResults.push(...topResults);
    } catch (error) {
      console.error(error);
    } finally {
      checkCreditAuthorsButtonClickableState(collectedResults);
      searchQueue.shift();
    }
  }
}

export async function processSearchResults(resultsJson, llmResponse) {
  const topResults = [];

  if (resultsJson.organic && resultsJson.organic.length > 0) {
      const llmResponseVector = await generateEmbedding('text-embedding-3-small', llmResponse);

      let count = 0;

      for (const result of resultsJson.organic.slice(0, 10)) {
          if (count >= 3) break;

          if (result.link.includes("youtube.com") || result.link.includes("youtu.be")) {
              console.log(`Skipping YouTube link: ${result.link}`);

              continue;
          }

          try {
              const htmlContent = await fetchScrapedContent(result.link);

              let domain = new URL(result.link).hostname;

              const author = await generateLLMResponse(`Return just the full name of the author of this webpage without any other comment. If you cannot find an author name just return 'Unknown Author' without any other comment: "${htmlContent}"`);

              const searchResultContentVector = await generateEmbedding('text-embedding-3-small', htmlContent);
              
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
          }
      }

      topResults.sort((a, b) => b.similarity_score - a.similarity_score);
  }

  return topResults;
}
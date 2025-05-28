import {
  sendResultsToGoogleSheet
} from './google_sheet_api.js';

import {
  chatWithLLM
} from './open_ai_api.js';

import {
  processSearchQueue
} from './search_utils.js';

import {
  checkSendButtonClickableState,
  checkCreditAuthorsButtonClickableState,
  disableButton,
  appendResponseToChat,
  appendSearchElements,
  createLeaderboardLink,
  showErrorToast,
  appendChatRespondingMessage,
  removeChatRespondingMessage
} from './ui_utils.js';

import {
  HttpResponseError
} from './http_utils.js'

document.addEventListener('DOMContentLoaded', () => {
  const promptInput = document.getElementById('promptInput');
  const generateBtn = document.getElementById('generateBtn');
  const creditAuthorsBtn = document.getElementById('creditAuthorsBtn');
  const chat = document.getElementById('chat');
  const searchResults = document.getElementById('searchResults');

  const embeddingsApiKeyInput = document.getElementById('embeddingsApiKey');
  const llmApiKeyInput = document.getElementById('llmApiKey');
  const searchApiKeyInput = document.getElementById('searchApiKey');
  const scrapeApiKeyInput = document.getElementById('scrapeApiKey');

  const storedEmbeddingsApiKey = localStorage.getItem('EmbeddingsApiKey');
  const storedLlmApiKey = localStorage.getItem('LLMApiKey');
  const storedSearchApiKey = localStorage.getItem('serpApiKey');
  const storedScrapeApiKey = localStorage.getItem('scrapeApiKey');

  if (storedEmbeddingsApiKey) {
      embeddingsApiKeyInput.value = storedEmbeddingsApiKey;
  }

  if (storedLlmApiKey) {
      llmApiKeyInput.value = storedLlmApiKey;
  }

  if (storedSearchApiKey) {
      searchApiKeyInput.value = storedSearchApiKey;
  }

  if (storedScrapeApiKey) {
      scrapeApiKeyInput.value = storedScrapeApiKey;
  }

  embeddingsApiKeyInput.addEventListener('input', () => {
      localStorage.setItem('EmbeddingsApiKey', embeddingsApiKeyInput.value);
  });

  llmApiKeyInput.addEventListener('input', () => {
      localStorage.setItem('LLMApiKey', llmApiKeyInput.value);
  });

  searchApiKeyInput.addEventListener('input', () => {
      localStorage.setItem('serpApiKey', searchApiKeyInput.value);
  });

  scrapeApiKeyInput.addEventListener('input', () => {
      localStorage.setItem('scrapeApiKey', scrapeApiKeyInput.value);
  });

  let collectedResults = [];
  let searchQueue = [];
  let conversationHistory = [];

  chat.dataset.isProcessing = 'false';
  searchResults.dataset.isProcessing = 'false';

  checkSendButtonClickableState();
  checkCreditAuthorsButtonClickableState(collectedResults);

  promptInput.addEventListener('input', checkSendButtonClickableState);

  promptInput.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
          generateBtn.click();
      }
  });

  creditAuthorsBtn.addEventListener('click', async () => {
      try {
          disableButton(generateBtn);

          disableButton(creditAuthorsBtn);

          chat.dataset.isProcessing = 'true';

          const filteredResults = collectedResults.map(o => ({
              link: o.link,
              author: o.author,
              similarity_score: o.similarity_score
          }));

          await sendResultsToGoogleSheet(filteredResults);

          appendSearchElements([
              document.createTextNode(`✅ All the authors have been credited! Please visit GiveBackGPT's `),
              createLeaderboardLink('Google Sheet'),
              document.createTextNode(` to view the leaderboard.`)
          ]);

          collectedResults = [];
      } catch (error) {
          console.error(error);

          appendSearchElements([
              document.createTextNode(`⚠️ We couldn't credit the authors at this time. Please try again later. If the issue persists, send us your feedback and we will be happy to fix the problem. View the current leaderboard on GiveBackGPT's `),
              createLeaderboardLink('Google Sheet'),
              document.createTextNode(`.`)
          ]);
      } finally {
          chat.dataset.isProcessing = 'false';

          checkSendButtonClickableState();

          checkCreditAuthorsButtonClickableState(collectedResults);
      }
  });

  generateBtn.addEventListener('click', async () => {
      try {
          disableButton(generateBtn);

          disableButton(creditAuthorsBtn);

          chat.dataset.isProcessing = 'true';

          const promptInput = document.getElementById('promptInput');

          const query = promptInput.value.trim();

          appendResponseToChat('YOU', query);

          promptInput.value = '';

          appendChatRespondingMessage();

          const llmResponse = await chatWithLLM(query, llmApiKeyInput.value, conversationHistory);

          removeChatRespondingMessage();

          appendResponseToChat('LLM', llmResponse);

          conversationHistory.push({ role: 'assistant', content: llmResponse });

          searchQueue.push(llmResponse);
      }
      catch (error) {
          console.error(error);

          removeChatRespondingMessage();

          if (error instanceof HttpResponseError) {
              showErrorToast(error.message);
          }
      }
      finally {
          chat.dataset.isProcessing = 'false';

          checkSendButtonClickableState();
      }

      try {
          // Process the queue if not already processing
          if (searchQueue.length === 1) {
              searchResults.dataset.isProcessing = 'true';

              try {
                  await processSearchQueue(searchQueue, collectedResults, llmApiKeyInput.value, embeddingsApiKeyInput.value, scrapeApiKeyInput.value, searchApiKeyInput.value);
              }
              finally {
                  searchResults.dataset.isProcessing = 'false';
              }
          }
      }
      catch (error) {
          console.error(error);

          if (error instanceof HttpResponseError) {
              showErrorToast(error.message);
          }
      }
      finally {
          checkCreditAuthorsButtonClickableState(collectedResults);
      }
  });
});
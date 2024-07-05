export function checkCreditAuthorsButtonClickableState(collectedResults) {
    const creditAuthorsBtn = document.getElementById('creditAuthorsBtn');

    if (collectedResults.length === 0) {
        disableButton(creditAuthorsBtn);
    } else {
        enableButton(creditAuthorsBtn);
    }
}

export function disableButton(button) {
    button.disabled = true;
}

export function enableButton(button) {
    button.disabled = false;
}

export function displayTopSearchResults(topResults) {
    if (topResults.length === 0) {
        appendSearchNoResultsMessage();

        return;
    }

    const ol = document.createElement('ol');

    topResults.forEach(result => {
        const li = document.createElement('li');

        const link = document.createElement('a');
        link.href = result.link;
        link.textContent = result.author;
        link.target = "_blank";
        link.rel = "noopener noreferrer";
        link.style.color = 'blue';
        link.style.textDecoration = 'underline';

        li.appendChild(link);

        const ul = document.createElement('ul');

        const subLi = document.createElement('li');
        subLi.textContent = `Title: ${result.title}`;

        const subLi2 = document.createElement('li');
        subLi2.textContent = `Similarity: ${result.similarity_score}`;

        ul.appendChild(subLi);
        ul.appendChild(subLi2);
        li.appendChild(ul);
        ol.appendChild(li);
    });

    appendToSearch(ol);
}

export function appendToSearch(element) {
    const search = document.getElementById('searchResults');
    search.insertAdjacentElement('beforeend', element);
    search.scrollTop = search.scrollHeight;
}

export function appendToChat(element) {
    const chat = document.getElementById('chat');
    chat.insertAdjacentElement('beforeend', element);
    chat.scrollTop = chat.scrollHeight;
}

export function appendResponseToChat(sender, message) {
    const div1 = document.createElement('div');

    div1.classList.add('fw-bold', 'mb-1');
    div1.textContent = `${sender}:`;

    const div2 = document.createElement('div');

    div2.classList.add('mb-3');
    div2.textContent = message;

    appendToChat(div1);
    appendToChat(div2);
}

export function appendSearchQuery(summary) {
    const div1 = document.createElement('div');

    div1.classList.add('fw-bold', 'mb-1');
    div1.textContent = 'Web search query:';

    const div2 = document.createElement('div');

    div2.classList.add('mb-3');
    div2.textContent = summary;

    appendToSearch(div1);
    appendToSearch(div2);
}

export function appendSearchNoResultsMessage() {
    const div = document.createElement('div');

    div.classList.add('mb-3');

    div.textContent = 'No results found.';

    appendToSearch(div);
}

export function appendSearchResultsHeader() {
    const div = document.createElement('div');

    div.classList.add('fw-bold', 'mb-1');
    div.textContent = 'Top search results with response similarity:';

    appendToSearch(div);
}

export function appendSearchProcessingMessage() {
    const p = document.createElement('p');

    p.classList.add('mb-3');

    p.id = "processing-message";

    p.textContent = 'Processing...';

    appendToSearch(p);
}

export function removeSearchProcessingMessage() {
    const processingMessage = document.getElementById('processing-message');

    if (processingMessage) {
        processingMessage.remove();
    }
}

export function appendSearchElements(elements) {
    const div = document.createElement('div');

    div.classList.add('mb-3');

    elements.forEach(o => {
        div.appendChild(o);
    });

    appendToSearch(div);
}

export function createLeaderboardLink(link_text) {
    const link = document.createElement('a');

    link.href = 'https://docs.google.com/spreadsheets/d/1IWRny8x5eiWvlEl-mPqu4uGYjxyxjkVqOHxE5fIK2So/edit?usp=sharing';
    link.target = '_blank';
    link.textContent = link_text;

    return link;
}

export function checkSendButtonClickableState() {
    const promptInput = document.getElementById('promptInput');
    const generateBtn = document.getElementById('generateBtn');
    const chat = document.getElementById('chat');
    
    if (promptInput.value.trim() === '' || chat.dataset.isProcessing === 'true') {
        disableButton(generateBtn);
    } else {
        enableButton(generateBtn);
    }
}
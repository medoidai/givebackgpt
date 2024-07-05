# Medoid AI - GiveBackGPT

<p align="center">
  <img src="assets/logo.png" alt="GiveBackGPT Logo" />
</p>

<h4 align="center">An open initiative and a novel process to build fair AI economies that include creators for true and sustainable growth.</h4>

<p align="center">
	<a href="https://github.com/medoidai/givebackgpt/blob/main/LICENSE" target="blank"><img src="https://img.shields.io/github/license/medoidai/givebackgpt?style=flat-square" alt="GiveBackGPT Licence" /></a>
	<a href="https://github.com/medoidai/givebackgpt/fork" target="blank"><img src="https://img.shields.io/github/forks/medoidai/givebackgpt?style=flat-square" alt="GiveBackGPT Forks" /></a>
	<a href="https://github.com/medoidai/givebackgpt/stargazers" target="blank"><img src="https://img.shields.io/github/stars/medoidai/givebackgpt?style=flat-square" alt="GiveBackGPT Stars" /></a>
	<a href="https://github.com/medoidai/givebackgpt/issues" target="blank"><img src="https://img.shields.io/github/issues/medoidai/givebackgpt?style=flat-square" alt="GiveBackGPT Issues" /></a>
	<a href="https://github.com/medoidai/givebackgpt/pulls" target="blank"><img src="https://img.shields.io/github/issues-pr/medoidai/givebackgpt?style=flat-square" alt="GiveBackGPT Pull Requests" /></a>
</p>

<p align="center">
    <a href="https://github.com/medoidai/givebackgpt/issues/new/choose" target="blank">Report Bug</a>
    ·
    <a href="https://github.com/medoidai/givebackgpt/issues/new/choose" target="blank">Request Feature</a>
    ·
    <a href="https://www.linkedin.com/showcase/givebackgpt/" target="blank">Follow</a>
</p>

## 📜 Table of contents

- [Medoid AI - GiveBackGPT](#medoid-ai---givebackgpt)
  - [📜 Table of contents](#-table-of-contents)
  - [📚 What is it about?](#-what-is-it-about)
  - [✨ Features](#-features)
  - [🛠️ Technologies used](#️-technologies-used)
  - [🚀 Getting started](#-getting-started)
    - [📋 Prerequisites](#-prerequisites)
    - [📥 Installation](#-installation)
  - [🎯 Usage](#-usage)
    - [▶️ Run the app](#️-run-the-app)
    - [🎉 Try it out!](#-try-it-out)
  - [🤲 Can I contribute?](#-can-i-contribute)
  - [🌱 Next steps](#-next-steps)
  - [🙏 Support](#-support)
  - [📄 What license do you use?](#-what-license-do-you-use)

## 📚 What is it about?

<p align="center">
  <img src="assets/creators.png" />
</p>

**GiveBackGPT** is an initiative dedicated to creating a **fair and sustainable AI** ecosystem. This novel process orchestrates the automatic identification and crediting of **open-access content creators**, whose work is essential in training generative AI models and keeping them relatable.

By leveraging standard web search to find and credit content similar to AI-generated responses, GiveBackGPT aims to recognize and reward creators in a simple, platform-agnostic, and streamlined way. Placing creator crediting at the inference level aligns with the value extraction point, removing barriers for small AI teams to innovate and discouraging monopoly data licensing deals.

Our vision includes establishing a licensing framework where **GenAI vendors** pay for legal data access, supporting a more equitable AI economy. Additionally, an open fund governed democratically will provide monetary rewards to creators who register and grant AI usage rights.

Follow us for updates on our progress towards a comprehensive standalone solution and join us in supporting a **democratized AI future**.

## ✨ Features

| Feature                        | Description                                                                                                       |
|--------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Chat Interface                 | Enables users to interact with an LLM for text-based conversations                                                |
| Web Search                     | Searches the web and presents top-related web pages based on its responses                                        |
| Integration with External APIs | Provides capabilities for LLM responses, text embedding, web scraping, and web search                             |
| API Keys Storage Location      | Ensures storage of API keys exclusively within the user's local web browser                                       |
| GiveBackGPT Leaderboard        | Allows submission of top-related web pages to the GiveBackGPT leaderboard via Google Sheets API for author credit |
| Configuration Settings         | Offers tabs for managing and setting API keys for external services                                               |
| Responsive Design              | Utilizes Bootstrap framework for ensuring responsiveness across various devices                                   |

## 🛠️ Technologies used

* **HTML**: For structuring the content of the web application.
* **CSS**: For styling the application to ensure it is visually appealing and user-friendly.
* **ECMAScript (JavaScript)**: For adding interactivity and dynamic behavior to the application.
* **Bootstrap**: For a responsive and mobile-first design using pre-defined components and utilities.
* **Docker**: To ensure consistent and reliable deployment across different environments.
* **NGINX**: Used to serve the static content of the web application.

## 🚀 Getting started

Before moving on with the Installation, make sure the Prerequisites below are satisfied.

### 📋 Prerequisites

Make sure you have [Docker](https://www.docker.com/) and [Git](https://git-scm.com/) installed.

### 📥 Installation

- Clone the project's repository

```sh
git clone git@github.com:medoidai/givebackgpt.git
```

- Navigate to the project's directory

```sh
cd givebackgpt
```

## 🎯 Usage

### ▶️ Run the app

```sh
docker run --rm -p 80:80 --mount type=bind,source="$(pwd)"/src,target=/usr/share/nginx/html nginx:alpine
```

### 🎉 Try it out!

1. Launch the web application on your local environment by visiting http://localhost/

2. Navigate to the *SETTINGS* section and input your API keys across all tabs

<div align="center">
  <img src="assets/settings.png">
</div>

3. Type your question in the chat interface of *CHAT WITH ANY LLM* section and then click on the **SEND** button

<div align="center">
  <img src="assets/chat-with-llm.png">
</div>

4. To credit the authors in the *Similar Web Pages* section, click on the **CREDIT AUTHORS** button

<div align="center">
  <img src="assets/credit-authors.png">
</div>

## 🤲 Can I contribute?

Absolutely! The project is [Free Software](https://www.gnu.org/philosophy/free-sw.en.html) and we welcome your contributions!

## 🌱 Next steps

* TODO 1...
* TODO 2...
* TODO 3...

## 🙏 Support

We all need support and motivation. **GiveBackGPT** is not an exception. Please give this project a ⭐️ to encourage and show that you liked it. Don't forget to leave a star ⭐️ before you move away.

## 📄 What license do you use?

See our [LICENSE](LICENSE) for more details.

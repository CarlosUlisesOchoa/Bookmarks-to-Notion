<a name="readme-top"></a>
<div align="center">
  <h1>Bookmarks2Notion</h1>
  <a href="#!"><img src="https://img.shields.io/badge/latest%20release-v1.0.0-blue" /></a>
  <a href="#!"><img src="https://img.shields.io/tokei/lines/github/carlosulisesochoa/Bookmarks-to-Notion" /></a>
  <a href="#!"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
  <a href="#!"><img src="https://img.shields.io/badge/license-MIT-blue" /></a>
</div>

<br/>

Bookmarks2Notion is a script designed to import your bookmarks into Notion. Using a combination of web scraping and the OpenAI language model, it creates a new page in your Notion database for each bookmarked URL, allowing you to easily organize and access your bookmarks in one central location.

<br/>

<details>
  <summary>Table of Contents</summary>
	<ul>
		<li><a href="#screenshots">Screenshots</a></li>
		<li><a href="#prerequisites">Prerequisites</a></li>
		<li><a href="#environment-variables">Environment Variables</a></li>
		<li><a href="#how-to-setup-env-file">How to Setup '.env' file</a></li>
		<li><a href="#how-to-run">How to Run</a></li>
		<li><a href="#license">License</a></li>
		<li><a href="#about-developer">About Developer</a></li>
	</ul>
</details>

<br/>

## Screenshots

<img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/28354a47-1e06-4c1e-8a06-8e4f8d9ff2f1" alt="image" height=600>

<br/><br/>

<img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/335ecaf3-4c75-413c-8c74-fa07dcbf2720" alt="image" width=700>

<br/><br/>

<img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/9046cab8-bfb4-4e66-8c2a-51d193a97f55" alt="image" width=700>

<br/><br/>

## Prerequisites

In order to run this script, you will need:

- Python 3.8 or higher
- A Notion account
- An OpenAI account to use its API
- The bookmarks file you want to import into Notion

<br/>

## Environment Variables

The script uses environment variables to configure some settings. These variables must be declared in a `.env` file, which must be located in the same directory as the script. Here are the environment variables used:

- `BOOKMARKS_FILE`: Relative path to your bookmarks file.
- `OPENAI_API_KEY`: Your OpenAI's API.
- `NOTION_API_KEY`: Your Notion's API.
- `NOTION_DB_ID`: The ID of the Notion database where the pages will be created.
- `USER_AGENT`: The User-Agent header value to be used when making HTTP requests.
- `LANGUAGE`: The language to be used when processing the scraped information with OpenAI's language model.

Note: Instructions on how to get the API keys and database ID required for the `.env` file can be found in the [How to Setup '.env' file](#how-to-setup-env-file) section.

<br/>

## How to Setup '.env' file

  `OPENAI_API_KEY`: To generate an OpenAI API key, follow these steps:

  1. Go to the OpenAI website (https://openai.com/).
  2. Click on the 'Sign Up' button in the top right corner of the page.
  3. Fill out the registration form with your details and click on the 'Create Account' button.
  4. Once you have created an account, go to the 'API Keys' section of your account dashboard.
  5. Click on the 'Generate New Key' button to create a new API key.
  6. Copy the API key and paste it into the .env file, replacing the placeholder value for OPENAI_API_KEY.

  Note: You may need to provide additional information or complete additional steps to verify your identity or payment information before you can generate an API key.

`NOTION_API_KEY`: To generate a Notion API key, follow these steps:

1. Go to the Notion website (https://www.notion.com/).
2. Log in to your account.
3. Click on the 'Settings & Members' button in the top right corner of the page.
4. Click on the 'Integrations' tab.
5. Click on the 'Add a new integration' button.
6. Give your integration a name and click on the 'Submit' button.
7. Copy the API key and paste it into the .env file, replacing the placeholder value for NOTION_API_KEY.

Note: You may need to provide additional information or complete additional steps to verify your identity or payment information before you can generate an API key.

`NOTION_DB_ID`: To find the Notion database ID, follow these steps:

1. Go to the Notion website (https://www.notion.com/).
2. Log in to your account.
3. Open the database you want to use in your script.
4. Click on the 'Share' button in the top right corner of the page.
5. Click on the 'Copy link' button.
6. Paste the link into a text editor or a web browser.
7. Look for the string of characters between the last two slashes in the URL. This is the database ID.
![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/d43262cf-a33d-490f-9760-37c1c9b1e0fd)
8. Copy the database ID and paste it into the .env file, replacing the placeholder value for NOTION_DB_ID.

<br/>

## How to Run

1. Rename `.env.template` to `.env` and set the proper values

2. Add your URL's inside the file you specified. (default is bookmarks.txt)

3. Install the required Python packages using pip.

```
pip install -r requirements.txt
```

<br/>

4. Run the script:

```
python main.py
```

The script will read the URLs from the bookmarks file, scrape each web page, process the scraped information, and create a new page in Notion.

<br/>

## License

This project is released under the [MIT License](LICENSE).

<br/>

## About developer

Visit my web [Carlos Ochoa](https://carlos8a.com)

<br/>

---

**Note:** If you encounter any issues with the script, please report them [here](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/issues). Contributions are welcome!

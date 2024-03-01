# Bookmarks2Notion
<a name="readme-top"></a>
<div align="center">
	<p align="center">
		<a href="#!"><img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/63110d8d-dc76-4e1a-99e8-d605302e9968" width="350" /></a>
	</p>
	<a href="#!"><img src="https://img.shields.io/badge/latest%20release-v1.0.0-blue" /></a>
	<a href="#!"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen" /></a>
	<a href="#!"><img src="https://img.shields.io/badge/license-MIT-blue" /></a>
</div>

<br/>

Bookmarks2Notion is a script designed to import your browser bookmarks into Notion. Using a combination of web scraping and OpenAI API, it creates a new page in your Notion database for each bookmarked URL, allowing you to easily organize and access your bookmarks in one central location.

<hr/>

## Table of Contents

- [Screenshots](#screenshots)
- [Prerequisites](#prerequisites)
- [How to run](#how-to-run)
- [Environment variables](#environment-variables)
- [How to get required API key values](#how-to-get-required-api-key-values)
- [License](#license)
- [About developer](#about-developer)

<br/>

## Screenshots

Script running:

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/cb2a1bdc-d2a1-4f75-a0aa-6a4464dc492b)

Pages created in the Notion DB

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/0b1fdf1d-2899-41f9-b923-b5131b4692e7)

Generated page content (includes direct link, title, and description enriched with AI)

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/9046cab8-bfb4-4e66-8c2a-51d193a97f55)

<br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

In order to run this script, you will need:

- Python 3.8 or higher
- A Notion account
- An OpenAI account
- The bookmarks file you want to import into Notion (compatible with any text format: *.txt, *.html, etc)

<br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to run

1. Rename `.env.template` to `.env`
2. Inside `.env` set the value to environment variables ([How to do that?](#environment-variables)) 
3. Add your URL's inside the file you specified. (default is bookmarks.txt)
4. Install the required Python packages using pip.

```
pip install -r requirements.txt
```

5. Run the script:

```
py main.py
```

The script will read the URLs from the bookmarks file, scrape each web page, process the scraped information, and create a new page in your Notion DB.

<br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Environment variables

- `BOOKMARKS_FILE`: Relative path to your bookmarks file. <i>(Required)</i>
- `OPENAI_API_KEY`: Your OpenAI's API. <i>(Required)</i>
- `NOTION_API_KEY`: Your Notion's API. <i>(Required)</i>
- `NOTION_DB_ID`: The ID of the Notion database where the pages will be created. <i>(Required)</i>
- `USER_AGENT`: The User-Agent header value to be used when making HTTP requests. <i>(Optional)</i>
- `LANGUAGE`: The language to be used when processing the scraped information with OpenAI's language model. <i>(Optional)</i>

Note: Instructions on how to get the API key values and database ID can be found in the [How to get required API key values](#how-to-get-required-api-key-values) section.

<br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to get required API key values

Instructions to get required API key values:

### How to get OPENAI_API_KEY

To generate an OpenAI API key, follow these steps:

1. Go directly to OpenAI API keys section: https://platform.openai.com/api-keys) (You must be logged in)
2. Click on "Create new secret key"

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/f5b2b156-5110-48f8-a21e-7208b62ba1a0)

3. Now you can choose a name, after that click on "Create secret key"

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/8c37e88c-519e-46ba-87a4-185c1e646e51)
   
4. That's it, now you got the value for OPENAI_API_KEY

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/e0e812cd-4cec-405a-b4f1-b0ce4e281e33)

Note: You may need to provide additional information or complete additional steps to verify your identity or payment information before you can generate an API key.

### How to get NOTION_API_KEY

To generate a Notion API key, follow these steps:

1. Go to my integrations page: https://www.notion.com/my-integrations (You must be logged in)
2. Click on 'Create new integration'

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/ed4ba755-4e9e-4079-a1f0-5c909862dad2)

3. Fill this form and click 'Submit'

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/37d7560c-2158-451a-8901-b3c04f287388)

4. Now here is your Notion API key, click on 'Show' and copy it!

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/d3817b9f-4b9b-40e5-a407-e8e5d6d18d3e)

5. Congrats, now you got the value for NOTION_API_KEY.

### How to get NOTION_DB_ID

To find the Notion database ID, follow these steps:

1. Go to the Notion website (https://www.notion.com/).
2. Log in to your account.
3. Create a new database
4. Give access to Bookmarks-to-Notion integration. Just click three dots icon -> Connect to -> Bookmarks-to-Notion

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/b6b8417b-2da1-429f-851e-a060d4dc80cf)

5. Click on 'Share' and click on 'Copy link' button.

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/e890d0a6-fda4-43c4-8b1c-d67c65373892)

6. Paste the link into a text editor or a web browser.
7. Look for the string of characters between the last two slashes in the URL. This is the database ID.

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/d43262cf-a33d-490f-9760-37c1c9b1e0fd)

8. Copy the database ID and you got the value for NOTION_DB_ID.

<br/><br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is released under the [MIT License](LICENSE).

<br/>




## About developer

Visit my web [Carlos Ochoa](https://carlos8a.com)

<br/>




---

**Note:** If you encounter any issues with the script, please report them [here](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/issues). Contributions are welcome!

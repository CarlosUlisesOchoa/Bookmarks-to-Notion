<a name="readme-top"></a>
<div align="center">
	<h1>Bookmarks2Notion</h1>
	<p align="center">
		<a href="#!"><img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/63110d8d-dc76-4e1a-99e8-d605302e9968" width="350" /></a>
	</p>
	<a href="#!"><img src="https://img.shields.io/badge/latest%20release-v1.0.0-blue" /></a>
	<a href="#!"><img src="https://img.shields.io/tokei/lines/github/carlosulisesochoa/Bookmarks-to-Notion" /></a>
	<a href="#!"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen" /></a>
	<a href="#!"><img src="https://img.shields.io/badge/license-MIT-blue" /></a>
</div>

<br/>

Bookmarks2Notion is a script designed to import your browser bookmarks into Notion. Using a combination of web scraping and OpenAI API, it creates a new page in your Notion database for each bookmarked URL, allowing you to easily organize and access your bookmarks in one central location.

<hr/>
<br/>

<details>
  <summary>Table of Contents</summary>
	<ul>
		<li><a href="#screenshots">Screenshots</a></li>
		<li><a href="#prerequisites">Prerequisites</a></li>
		<li><a href="#how-to-run">How to Run</a></li>
		<li><a href="#environment-variables">Environment Variables</a></li>
		<li><a href="#how-to-get-required-api-key-values">How to get required API key values</a></li>
		<li><a href="#license">License</a></li>
		<li><a href="#about-developer">About Developer</a></li>
	</ul>
</details>

<br/>

## Screenshots

<p>Script running:</p>

<img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/cb2a1bdc-d2a1-4f75-a0aa-6a4464dc492b" alt="image" height=600>

<br/>

<p>Pages created in the Notion DB</p>

![image](https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/0b1fdf1d-2899-41f9-b923-b5131b4692e7)

<br/>

<p>Generated page content (includes direct link, title, and description enriched with AI)</p>

<img src="https://github.com/CarlosUlisesOchoa/Bookmarks-to-Notion/assets/26280134/9046cab8-bfb4-4e66-8c2a-51d193a97f55" alt="image" width=700>

<br/><br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Prerequisites

In order to run this script, you will need:

- Python 3.8 or higher
- A Notion account
- An OpenAI account
- The bookmarks file you want to import into Notion (compatible with any text format: *.txt, *.html, etc)

<br/><br/><br/>

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

<br/><br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Environment Variables

- `BOOKMARKS_FILE`: Relative path to your bookmarks file. <i>(Required)</i>
- `OPENAI_API_KEY`: Your OpenAI's API. <i>(Required)</i>
- `NOTION_API_KEY`: Your Notion's API. <i>(Required)</i>
- `NOTION_DB_ID`: The ID of the Notion database where the pages will be created. <i>(Required)</i>
- `USER_AGENT`: The User-Agent header value to be used when making HTTP requests. <i>(Optional)</i>
- `LANGUAGE`: The language to be used when processing the scraped information with OpenAI's language model. <i>(Optional)</i>

Note: Instructions on how to get the API key values and database ID can be found in the [How to get required API key values](#how-to-get-required-api-key-values) section.

<br/><br/><br/>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## How to get required API key values

Instructions to get required API key values:

### How to get OPENAI_API_KEY

To generate an OpenAI API key, follow these steps:

1. Go to the OpenAI website (https://openai.com/).
2. Click on the 'Sign Up' button in the top right corner of the page.
3. Fill out the registration form with your details and click on the 'Create Account' button.
4. Once you have created an account, go to the 'API keys' section of your account dashboard.
5. Click on the 'Generate New Key' button to create a new API key.
6. Copy the API key and you got the value for OPENAI_API_KEY

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

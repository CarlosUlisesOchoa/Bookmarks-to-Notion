import sys
import os
from dotenv import load_dotenv
import openai
from bs4 import BeautifulSoup
import requests
from notion_client import Client
import time
from urllib.parse import urlparse
import datetime


def print_ts(message=""):
    if len(message) == 0:
        print()
        return
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{timestamp}: {message}")


def get_web_info(url):
    # Function to scrape web page info
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    if len(soup.title.string) > 0:
        title = soup.title.string
    else:
        title = ""

    description = soup.find("meta", attrs={"name": "description"})

    if description:
        description = description["content"]
    else:
        description = "No description found."

    return title, description


def process_info_with_ai(url, title, description):

    language = os.getenv("LANGUAGE")

    if language is None:
        language = "english"

    openai_api = os.getenv("OPENAI_API_KEY")
    if openai_api is None:
        print_ts("Please set OPENAI_API_KEY in .env file")
        return "error"

    openai.api_key = openai_api

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    # prompt, english only
    # prompt = f"As a Notion page admin, you're tasked with creating Notion pages using the information provided as well as any pre-existing knowledge you have. The website has the title '{title}' and hostname '{hostname}', and its meta tag description is '{description}'. Please evaluate the title and, if necessary, simplify it for use in a Notion page (e.g., a title like 'Welcome to Flask etc...' could be simplified to 'Flask'). If there's no title, please replace it with 'No title found'. Following that, generate a detailed and engaging description. Remember not to include the URL or hostname in the description, and aim for a length between 400 to 550 characters. If there's insufficient information to create a comprehensive description, please use 'No information found'. Please format your final output like this: 'title|||description', which will make parsing easier."

    # new prompt, multilanguage v1
    # prompt = f"As a Notion page admin, you're tasked with creating Notion pages using the information provided as well as any pre-existing knowledge you have. The website has the title '{title}' and hostname '{hostname}', and its meta tag description is '{description}'. Please evaluate the title and, if necessary, simplify it for use in a Notion page (e.g., a title like 'Welcome to Flask etc...' could be simplified to 'Flask'). If there's no title, please replace it with 'No title found'. Following that, generate a detailed and engaging description. Remember not to include the URL or hostname in the description, and aim for a length between 400 to 550 characters. If there's insufficient information to create a comprehensive description, please use 'No information found'. Please format your final output like this: 'title|||description', which will make parsing easier. Lastly, please ensure that the title and description are in {language}."

    # new prompt, multilanguage v2
    prompt = f"As a Notion page admin, you're tasked with creating Notion pages using the information provided as well as any pre-existing knowledge you have. The website has the title '{title}' and hostname '{hostname}', and its meta tag description is '{description}'. Please evaluate the title and, if necessary, simplify it for use in a Notion page (e.g., a title like 'Welcome to Flask etc...' could be simplified to 'Flask'). If there's no title, please replace it with 'No title found'. Following that, generate a detailed and engaging description. Remember not to include the URL or hostname in the description, and aim for a length between 400 to 550 characters. If there's insufficient information to create a comprehensive description, please use 'No information found'. Be mindful to keep brand names and specific terminologies in their original language. Please format your final output like this: 'title|||description', which will make parsing easier. Lastly, please ensure that the title and description are in {language}."

    print_ts(f"Generating best page title and description with AI...")

    # Start the timer
    start_time = time.time()

    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.3,
            max_tokens=600,
            top_p=1,
            frequency_penalty=0.5,
            presence_penalty=0.5,
            stream=False
        )

        # End the timer
        end_time = time.time()

        # Convert to milliseconds
        elapsed_time = round((end_time - start_time) * 1000, 0)

        if response.choices and response.choices[0].text.strip():
            return response.choices[0].text.strip()
        else:
            print_ts("OpenAI API unknow error")
            return "error"

    except openai.OpenAIError as e:
        print_ts(f"OpenAI API Error: {str(e)}")
        return "error"

    except Exception as e:
        print_ts(f"Unexpected Error: {str(e)}")
        return "error"


def create_notion_page(url, title, description_content):
    # Function to create a new page in Notion

    print_ts("Creating Notion page...")

    notion_api_key = os.getenv("NOTION_API_KEY")
    if notion_api_key is None:
        print_ts("Please set NOTION_API_KEY in .env file")
        return "error"

    notion = Client(auth=notion_api_key)

    notion_db_id = os.getenv("NOTION_DB_ID")
    if notion_db_id is None:
        print_ts("Please set NOTION_DB_ID in .env file")
        return "error"

    page = notion.pages.create(
        parent={"database_id": notion_db_id},
        properties={
            "Nombre": {"title": [{"text": {"content": title}}]},
            "URL": {"url": url},
        },
        # Page content
        children=[
            {
                "object": "block",
                "paragraph": {"rich_text": [{"text": {"content": description_content}}]},
            }
        ]
    )

    return page


def scrap_web_info(url):
    print_ts(f"Scraping web info...")
    title, description = get_web_info(url)
    processed_info = process_info_with_ai(url, title, description)
    processed_title, processed_description = processed_info.split("|||")
    create_notion_page(url, processed_title, processed_description)


def main():
    print_ts()
    print_ts("Starting the script...")
    print_ts()
    load_dotenv()
    your_favorites_file = os.getenv("YOUR_FAVORITES_FILE")
    if your_favorites_file is None:
        print_ts("Please set YOUR_FAVORITES_FILE in .env file")
        sys.exit()

    with open(os.getenv("YOUR_FAVORITES_FILE"), "r") as f:
        urls = f.readlines()

    for url in urls:
        # Remove newline characters
        url = url.strip()
        try:
            print_ts(f"[ ======= {url} ======= ]")
            scrap_web_info(url)
            print_ts("Successfully created Notion page")
            print_ts()
        except Exception as e:
            print_ts(f"Failed to create a page for {url}: {e}")
            print_ts()


# Run the main function
if __name__ == "__main__":
    main()

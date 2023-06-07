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


load_dotenv()


def print_ts(message=""):
    # Prints a message with a timestamp
    if len(message) == 0:
        print()
        return
    timestamp = datetime.datetime.now().strftime("[%H:%M:%S]")
    print(f"{timestamp}: {message}")


def validate_environment_variable(variable_name):
    # Validates if an environment variable is set
    variable = os.getenv(variable_name)
    if variable is None:
        raise EnvironmentError(f"Couldn't load the env variable '{variable_name}', check the .env file")
    return variable


def get_web_info(url):
    # Scrapes a webpage and returns its title and description

    user_agent = os.getenv("USER_AGENT")
    if user_agent is None:
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"

    headers = {"User-Agent": user_agent}
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string if soup.title else ""
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"] if meta_description else ""

    return title, description


def process_info_with_ai(url, title, description):
    # Processes webpage info with an AI and returns a response

    language = os.getenv("LANGUAGE")
    if language is None:
        language = "english"

    openai.api_key = os.getenv("OPENAI_API_KEY")

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    prompt = f"As a Notion page admin, you're tasked with creating Notion pages using the information provided as well as any pre-existing knowledge you have. The website has the title '{title}' and hostname '{hostname}', and its meta tag description is '{description}'. Please evaluate the title and, if necessary, simplify it for use in a Notion page (e.g. if original title is like 'Welcome to Flask etc...' you could simplify it to just 'Flask'). If there's no title, please replace it with 'No title found'. Following that, generate a detailed and engaging description. Remember not to include the URL or hostname in the description, and aim for a length between 400 to 550 characters. If there's insufficient information to create a comprehensive description, please use 'No information found'. Be mindful to keep brand names and specific terminologies in their original language. Please format your final output like this: 'title|||description', which will make parsing easier. Lastly, please ensure that the title and description are in {language}."

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
            stream=False,
        )

        # End the timer
        end_time = time.time()

        # Convert to milliseconds
        elapsed_time = round((end_time - start_time) * 1000, 0)

        if response.choices and response.choices[0].text.strip():
            return response.choices[0].text.strip()
        else:
            raise Exception("OpenAI API unknow error")

    except openai.OpenAIError as e:
        raise Exception(f"OpenAI API Error: {str(e)}")

    except Exception as e:
        raise Exception(f"Unexpected Error: {str(e)}")


def create_notion_page(url, title, description_content):
    # Creates a new page in Notion
    print_ts("Creating Notion page...")

    notion_api_key = os.getenv("NOTION_API_KEY")
    notion = Client(auth=notion_api_key)

    notion_db_id = os.getenv("NOTION_DB_ID")

    page = notion.pages.create(
        parent={"database_id": notion_db_id},
        properties={
            "Name": {"title": [{"text": {"content": title}}]},
            "URL": {"url": url},
        },
        # Page content
        children=[
            {
                "object": "block",
                "paragraph": {
                    "rich_text": [{"text": {"content": description_content}}]
                },
            }
        ],
    )

    return page


def main():
    # Main function
    print_ts()
    print_ts("Starting the script...")
    print_ts()
    print_ts("Validating indispensable environment variables...")
    try:
        bookmarks_file = validate_environment_variable("BOOKMARKS_FILE")
        print_ts(f"BOOKMARKS_FILE: ✓")
        validate_environment_variable("OPENAI_API_KEY")
        print_ts(f"OPENAI_API_KEY: ✓")
        validate_environment_variable("NOTION_API_KEY")
        print_ts(f"NOTION_API_KEY: ✓")
        validate_environment_variable("NOTION_DB_ID")
        print_ts(f"NOTION_DB_ID: ✓")
    except EnvironmentError as e:
        print_ts(f"{str(e)}")
        sys.exit()

    print_ts("Indispensable environment variables loaded successfully!")
    print_ts()

    try:
        print_ts("Trying to load your bookmarks file...")
        with open(bookmarks_file, "r") as f:
            urls = f.readlines()
            if len(urls) == 0:
                raise Exception("Bookmarks file is empty")
            print_ts("Bookmarks file loaded successfully!")
            print_ts()
    except FileNotFoundError:
        print_ts(f"Failed to load your bookmarks file '{bookmarks_file}'")
        sys.exit()

    print_ts("Starting the main process...")
    print_ts()

    failed = 0
    succeeded = 0

    for url in urls:
        # Remove newline characters
        url = url.strip()
        try:
            print_ts(f"[ ======= {url} ======= ]")
            #
            # Scrapes a webpage, processes the info with an AI and creates a new page in Notion
            print_ts(f"Scraping web info...")
            title, description = get_web_info(url)
            if len(title) == 0 and len(description) == 0:
                raise Exception("Web scraping error")
            if "cloudflare" in title.lower() or "cloudflare" in description.lower():
                raise Exception("Web scraping error")

            processed_info = process_info_with_ai(url, title, description)
            processed_title, processed_description = processed_info.split("|||")
            create_notion_page(url, processed_title, processed_description)
            print_ts("Successfully created Notion page")
            succeeded += 1
        except Exception as e:
            failed += 1
            print_ts(f"Failed to create a Notion page. Error: {e}")
        finally:
            print_ts()
    
    print_ts(f"Total URL's: {urls.__len__()}")
    print_ts(f"Failed: {failed} | Succeeded: {succeeded}")

    print_ts()
    print_ts("Shutting down the script...")
    sys.exit()


# Run the main function
if __name__ == "__main__":
    main()

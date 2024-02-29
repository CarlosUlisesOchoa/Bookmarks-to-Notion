import sys
import os
from dotenv import load_dotenv
from openai import OpenAI
from bs4 import BeautifulSoup
import requests
from notion_client import Client
import time
from urllib.parse import urlparse
import datetime
import csv
import re


load_dotenv()


def extract_urls_from_file(file_path):
    url_pattern = re.compile(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    )
    try:
        with open(file_path, "r") as file:
            data = file.read()
            urls = re.findall(url_pattern, data)
    except UnicodeDecodeError:
        raise Exception(
            f"Cannot process '{file_path}'. It appears to be a binary file."
        )
    return urls


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
        raise EnvironmentError(
            f"Couldn't load the env variable '{variable_name}', check the .env file"
        )
    return variable


def log_failed_url(url, error):
    file = validate_environment_variable("FAILED_URLS_FILE")

    if file is None:
        file = "failed_jobs.csv"

    # Split the filename into name and extension
    base, extension = os.path.splitext(file)

    # Format the filename to append date like 'failed_jobs_2021-01-31.csv'
    file = f"{base}_{datetime.datetime.now().strftime('%Y-%m-%d')}{extension}"

    # Check if the file is empty (i.e., we're creating a new file)
    is_file_empty = not os.path.exists(file) or os.path.getsize(file) == 0

    with open(file, "a", newline="") as f:
        writer = csv.writer(f)
        # If it's a new file, write the headers
        if is_file_empty:
            writer.writerow(["Time", "URL", "Error"])
        # write into file like '12:00:00, https://www.google.com, <error message>'
        writer.writerow([datetime.datetime.now().strftime("%H:%M:%S"), url, str(error)])


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

    parsed_url = urlparse(url)
    hostname = parsed_url.netloc

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    ai_messages = [
        {
            "role": "assistant",
            "content": "I'm your Notion page creator. Please provide the details of the website you're working with and I will provide you a title and description suitable for a Notion page.",
        },
        {
            "role": "user",
            "content": f"Using the provided information about the website titled '{title}', which is hosted at '{hostname}', and described as '{description}', along with any pre-existing knowledge you have, I need you to perform a couple of tasks. First, if necessary, simplify the website's title for better suitability on a Notion page. Next, create a detailed and engaging description that fits the Notion page's context. This description should avoid including the URL or hostname, stay within 400 to 550 characters, and preserve the original brand names and terminologies. If there's not enough information for a detailed description, please summarize with 'No information found'. Remember, the final output should be strictly in the format: '{title}|||{description}'. Make sure the content aligns with {language} language standards.",
        },
    ]

    ai_model = os.getenv("OPENAI_API_MODEL")
    if ai_model is None:
        raise EnvironmentError(
            "Couldn't load the env variable 'OPENAI_API_MODEL', check the .env file"
        )

    ai_temperature = os.getenv("OPENAI_API_TEMPERATURE")
    # Check if temperature can be parsed to float. If not set it to 0.3
    try:
        ai_temperature = float(ai_temperature)
    except ValueError:
        ai_temperature = 0.3

    ai_max_tokens = os.getenv("OPENAI_API_MAX_TOKENS")
    # Check if max tokens can be parsed to int. If not set it to 1000
    try:
        ai_max_tokens = int(ai_max_tokens)
    except ValueError:
        raise EnvironmentError(
            "Couldn't load or parse the env variable 'OPENAI_API_MAX_TOKENS', check the .env file"
        )

    ai_frequency_penalty = os.getenv("OPENAI_API_FREQUENCY_PENALTY")
    # Check if penalty can be parsed to float. If not set it to 0.5
    try:
        ai_frequency_penalty = float(ai_frequency_penalty)
    except ValueError:
        ai_frequency_penalty = 0.5

    print_ts(f"Generating best page title and description with AI...")

    # Start the timer
    start_time = time.time()

    try:
        # Assuming the completion method or equivalent for detailed content generation
        response = client.chat.completions.create(
            model=ai_model,
            messages=ai_messages,
            temperature=ai_temperature,
            max_tokens=ai_max_tokens,
            frequency_penalty=ai_frequency_penalty,
        )

        # End the timer
        end_time = time.time()

        # Convert to milliseconds
        elapsed_time = round((end_time - start_time) * 1000, 0)

        if response.choices and response.choices[0].message.content.strip():
            return response.choices[0].message.content.strip()
        else:
            raise Exception("OpenAI API unknown error")

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
        urls = extract_urls_from_file(bookmarks_file)
        if len(urls) == 0:
            raise Exception("No URLs found in the file")
        print_ts("URLs loaded successfully!")
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
            log_failed_url(url, e)
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

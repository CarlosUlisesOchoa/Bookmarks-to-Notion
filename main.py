import os
from dotenv import load_dotenv
import openai
from bs4 import BeautifulSoup
import requests
from notion_client import Client
import time
from urllib.parse import urlparse


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


def process_description(url, title, description):
    # Function to use GPT-4 API to summarize the text

    openai.api_key = os.getenv("OPENAI_API_KEY")

    parsed_url = urlparse(url)

    hostname = parsed_url.netloc

    prompt = f"Consider the website identified by hostname '{hostname}', with the title '{title}', and the description '{description}'. Using any pre-existing knowledge you might have about the site, generate a detailed and accurate description. The description should not include the URL or hostname, and its length should range between 400 to 550 characters. In cases where sufficient information is unavailable to generate a comprehensive description, return 'No information found'."

    print(f"[OpenAI] Trying to obtain a description for {url}...")
    print()  # tetemp

    start_time = time.time()  # Start the timer

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

        end_time = time.time()  # End the timer
        elapsed_time_ms = (end_time - start_time) * \
            1000  # Convert to milliseconds
        # round to zero decimal places
        elapsed_time = round(elapsed_time_ms, 0)
        # print(f"OpenAI API elapsed time: {elapsed_time} ms")

        # Check if there are any choices in the response
        if response.choices and response.choices[0].text.strip():
            return response.choices[0].text.strip()
        else:
            return "No information found"

    except openai.OpenAIError as e:
        # Handle API error
        print(f"OpenAI API Error: {str(e)}")
        return "error"

    except Exception as e:
        # Handle other errors
        print(f"Error occurred: {str(e)}")
        return "error"

# Function to create a new page in Notion


def create_notion_page(url, title, description_content):

    print("Creating Notion page...")

    notion = Client(auth=os.getenv("NOTION_API_KEY"))

    page = notion.pages.create(
        parent={"database_id": os.getenv("NOTION_DB_ID")},
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
        # page2 = plugin.notion.pages.create(
        #     parent=parent, properties=properties, children=children
        # )
    )

    return page


# Function to create a new page for a given URL


def scrap_web_info(url):
    print("Scraping web info...")
    title, description = get_web_info(url)
    # print("--------- Create Notion page ---------------")  # tetemp
    # print(f"Title: {title}")  # tetemp
    print()  # tetemp
    processed_description = process_description(url, title, description)
    # print(f"Processed description: {processed_description}")  # tetemp
    # print()  # tetemp
    create_notion_page(url, title, processed_description)


# Main function to read the URLs and create the pages


def main():
    load_dotenv()
    with open(os.getenv("YOUR_FAVORITES_FILE"), "r") as f:
        urls = f.readlines()

    for url in urls:
        url = url.strip()  # Remove newline characters
        try:
            scrap_web_info(url)
            print(f"Successfully created a page for {url}")
        except Exception as e:
            print(f"Failed to create a page for {url}: {e}")


# Run the main function
if __name__ == "__main__":
    main()

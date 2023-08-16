import asyncio
import argparse
import traceback
import random
from typing import Type, Optional
from pydantic import BaseModel, Field
from superagi.tools.base_tool import BaseTool
from pyppeteer import launch
from bs4 import BeautifulSoup

class PyppeteerSchema(BaseModel):
    website_url: str = Field(
        ...,
        description="Valid website url without any quotes.",
    )
    
class PyppeteerTool(BaseTool):
    """
    Pyppeteer Tool Raw HTML

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "Pyppeteer Tool Raw HTML"
    description = (
        "Used to scrape a javascript generated website and extract the raw html of the rendered page."
    )
    args_schema: Type[PyppeteerSchema] = PyppeteerSchema

    class Config:
        arbitrary_types_allowed = True

    async def PyppeteerExtract(self, url: str, text_only: bool) -> str:
        USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36",
        ]

        random_user_agent = random.choice(USER_AGENTS)
        browser = await launch(headless=True, args=['--no-sandbox', f'--user-agent={random_user_agent}'])
        page = await browser.newPage()
        try:
            await page.goto(url, waitUntil='networkidle2')
            content = await page.content()

            if text_only:
                soup = BeautifulSoup(content, 'html.parser')
                content = soup.get_text("\n\r")
        except Exception as e:
            content = traceback.format_exc()
        finally:
            await browser.close()
        return content

    def _execute(self, website_url: str) -> tuple:
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(self.PyppeteerExtract(website_url, False))
        max_length = len(' '.join(content.split(" ")[:600]))
        return content[:max_length]


class PyppeteerToolTextOnly(PyppeteerTool):
    """
    Pyppeteer Tool Text Only

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "Pyppeteer Tool Text Only"
    description = (
        "Used to scrape a javascript generated website and extract only the text content of the page."
    )
    args_schema: Type[PyppeteerSchema] = PyppeteerSchema

    def _execute(self, website_url: str) -> tuple:
        loop = asyncio.get_event_loop()
        content = loop.run_until_complete(self.PyppeteerExtract(website_url, True))
        max_length = len(' '.join(content.split(" ")[:600]))
        return content[:max_length]

#For local debugging - you can run it from the command line.  Easier to debug Pyppeteer this way.
def main():
    parser = argparse.ArgumentParser(description='Scrape a website.')
    parser.add_argument('website_url', help='The URL of the site to scrape')
    parser.add_argument('--text_only', dest='text_only', action='store_true', help='Strip out the HTML and return only text.')
    parser.set_defaults(text_only=False)

    args = parser.parse_args()

    if args.text_only:
        tool = PyppeteerToolTextOnly()
        print(tool._execute(args.website_url))
    else:
        tool = PyppeteerTool()
        print(tool._execute(args.website_url))

if __name__ == "__main__":
    main()
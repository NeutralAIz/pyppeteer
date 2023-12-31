from abc import ABC
from typing import List
from superagi.tools.base_tool import BaseTool, BaseToolkit
from pyppeteer_tools import PyppeteerTool
from pyppeteer_tools import PyppeteerToolTextOnly


class PyppeteerWebScrapperToolkit(BaseToolkit, ABC):
    name: str = "Pyppeteer Toolkit"
    description: str = "Pyppeteer Tool kit contains all tools related extracting information from a javascript rendered website."

    def get_tools(self) -> List[BaseTool]:
        return [
            PyppeteerTool(), PyppeteerToolTextOnly(),
        ]

    def get_env_keys(self) -> List[str]:
        return []

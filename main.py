import requests

from bs4 import BeautifulSoup, NavigableString
from requests import Response


class DataRetriever:
    URL: str = "https://www.leagueofgraphs.com/summoner/{region}/{display_name}/last-30-days"
    HEADERS: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari"}

    def fetch_page(self, url: str) -> bytes:
        """
        Get the page content from the given URL.
        :param url: the URL to retrieve
        :return: the content of the page as bytes
        """
        try:
            response: Response = requests.get(url, headers=self.HEADERS)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to get page. {e}") from e

    def scrape_account(self, display_name: str, region: str) -> dict | None:
        """
            Scrape the data of a summoner's account from LeagueOfGraphs.
            :param display_name: the summoner's display name
            :param region: the region of the summoner's account
            :return: a tuple containing the summoner's data as a dictionary and the display name
        """

        page: bytes = self.fetch_page(self.URL.format(region=region.lower(), display_name=display_name))

        if page == "":
            return None

        soup: BeautifulSoup = BeautifulSoup(page, "html.parser")

        account_exists: BeautifulSoup | NavigableString | None = soup.find(class_="best-league")

        if not account_exists:
            print(
                f"There is no summoner on {str.lower(region)} named {display_name}"
            )
            return None

        return {
            "level": int(
                str(
                    str.split(
                        soup.find(class_="bannerSubtitle").text.strip(), "-"
                    )[0]
                )[5:]
            ),
            "rank": str(soup.find(class_="leagueTier").text.strip()),
            "games_played": int(
                soup.find(class_="summonerProfileQueuesTabs tabsContainer")
                .find(class_="tabs-content")
                .find("div", {"data-tab-id": "championsData-all-queues"})
                .find(class_="pie-chart small")
                .text.strip()
            ),
        }

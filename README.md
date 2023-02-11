# League-of-Legends-Account-Scraper
A python library for retrieving data from the website LeagueOfGraphs for a summoner's account.

# Requirements
* requests
* bs4

# Installation
```
pip install requests bs4
```

# Usage
```py
from DataRetriever import DataRetriever

data_retriever = DataRetriever()
summoner_data = data_retriever.scrape_account(display_name="Summoner Name", region="Region")

if summoner_data:
    print("Level:", summoner_data['level'])
    print("Rank:", summoner_data['rank'])
    print("Games Played:", summoner_data['games_played'])
else:
    print("Summoner not found.")

```


# Contributing
Contributions are welcome! Please open a pull request with any changes or improvements.

# License
This project is licensed under the MIT License.

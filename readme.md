# Discord Bot Sandbox


## Demo Features

### Simple Message Echo

[<img src="docs/echo_message_sample.png" />]()

### Simple Edit Echo

[<img src="docs/echo_edit_sample.png" />]()

### Image Search

Using API calls to fetch an image from a search engine.

[<img src="docs/image_search_sample.png" />]()

### Web Scraping

Scraping website and presenting them in digestible format.  
This example collects news data from Sky Sports website.

[<img src="docs/sky_sports_news_web_scraping_sample.png" />]()

### Event Monitoring

Monitoring live events and updating on Discord.  

#### Dummy Data
This example used randomly generated data at random interval.

[<img src="docs/monitor_event_sample.png" />]()

#### RSS Feed
This example tracks an RSS feed and displays any new updates.

[<img src="docs/rss_feed_sample.png" />]()


## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

- Put discord bot token in the `.env` file as shown in `.env.example`


## Run

```bash
source venv/bin/activate
python src/hello_world.py
```

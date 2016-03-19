# Personality Insight App Overview

The Twitter Insight app demonstrates a simple, reusable Python web application that uses Watson **Personality Insights** and **Insights for Twitter** service in Bluemix.


## Prerequisites

1. Install [cloud foundry command line interface] (https://github.com/cloudfoundry/cli/releases)
2. Install [Bluemix command line interface] (http://clis.ng.bluemix.net/ui/home.html)


## Run the app in Bluemix

1. Download the code to your computer: `git clone git@github.com:bulutmf/PerInsight.git`.
2. cd into the app directory: `cd PerInsight`
3. Open the `manifest.yml` file and edit `name` and `host` fields to something else. Don't use the **PerInsight** as it is already taken. Your host name should be unique in Bluemix, i.e. not taken by someone else.
4. Set the api end point to dedicated bluemix: `bluemix api https://api.w3ibm.bluemix.net`
5. Login: `bluemix login`.
6. Create a **Insights for Twitter** service: `cf create-service twitterinsights Free twitter-insights-service`
7. Create a **Personality Insights** service: `cf create-service personality_insights tiered personality-insights-service`
8. Push the application code to Bluemix: `cf push`

## Run the app locally - you should first follow above steps to run the app in Bluemix

1. [Install Python][] (if you haven't installed it yet)
2. Download the code to your computer: `git clone git@github.com:bulutmf/PerInsight.git`.
3. cd into the app directory: `cd PerInsight`
4. Install the required Python packages: `pip3.5 install -r requirements.txt`
5. Open the `server.py` file and set the values for `TWITTER_USERNAME`, `TWITTER_PASSWORD`, `PERSONALITY_INSIGHT_USERNAME` and `PERSONALITY_INSIGHT_PASSWORD`. You can find these values from Bluemix: Dashboard => Click on the app => Look for `Show Credentials` link on each of the service tiles.
6. Run `python3.5 server.py`
7. Access the running app in a browser at: [http://localhost:8000]

[Install Python]: https://www.python.org/downloads/

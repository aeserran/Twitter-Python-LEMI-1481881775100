# Twitter Insight App Overview

The Twitter Insight app demonstrates a simple, reusable Python web application that uses Watson **Personality Insights** and **Insights for Twitter** service in Bluemix.


## Prerequisites

1. Install [cloud foundry command line interface] (https://github.com/cloudfoundry/cli/releases)
2. Install [Bluemix command line interface] (http://clis.ng.bluemix.net/ui/home.html)


## Run the app in Bluemix

1. Download the code to your computer (or git clone git@github.com:bulutmf/PerInsight.git).
2. Go to the downloaded folder. `cd PerInsight`
3. Open the `manifest.yml` file.
4. Edit `name` and `host` to something else. Don't use the **PerInsight** as it is already taken. Your host name should be unique in Bluemix, i.e. not taken by someone else.
5. Set api end point to dedicated bluemix: `bluemix api https://api.w3ibm.bluemix.net`
6. Login: `bluemix login`. Enter your *username*, *password* and choose your org and Space (if you have multiple).
7. Push the application code to Bluemix: `cf push`

## Run the app locally

1. [Install Python][]
2. Download and extract the starter code from the Bluemix UI
3. cd into the app directory
4. Run `python server.py`
5. Access the running app in a browser at http://localhost:8000

[Install Python]: https://www.python.org/downloads/

import cherrypy
import os
import json
import requests

class PersonalityInsight(object):
    def __init__(self, vcapServices):

        self.TWITTER_USERNAME = "CHANGE_THIS_IF_YOU_ARE_RUNNING_LOCALLY"
        self.TWITTER_PASSWORD = "CHANGE_THIS_IF_YOU_ARE_RUNNING_LOCALLY"
        self.PERSONALITY_INSIGHT_USERNAME = "CHANGE_THIS_IF_YOU_ARE_RUNNING_LOCALLY"
        self.PERSONALITY_INSIGHT_PASSWORD = "CHANGE_THIS_IF_YOU_ARE_RUNNING_LOCALLY"

        self.NO_OF_TWEETS_TO_RETRIEVE = 20
        if vcapServices is not None:
            # Lets read the credentials for twitter service from bluemix
            services = json.loads(vcapServices)
            twitterServiceName = "twitterinsights"
            if twitterServiceName in services:
                self.TWITTER_USERNAME = services[twitterServiceName][0]["credentials"]["username"]
                self.TWITTER_PASSWORD = services[twitterServiceName][0]["credentials"]["password"]
            # Now lets read the credentials for Personality Insight Service from cf
            perInsightServiceName = "personality_insights"
            if perInsightServiceName in services:
                self.PERSONALITY_INSIGHT_USERNAME = services[perInsightServiceName][0]["credentials"]["username"]
                self.PERSONALITY_INSIGHT_PASSWORD = services[perInsightServiceName][0]["credentials"]["password"]

    @cherrypy.expose
    def index(self):
        return open(os.path.join("static", u'index.html'))

    # 1. Get the tweets from twitter
    # 2. Analyze it using Watson Personality Insight Service
    @cherrypy.expose
    def analyze(self, twitterHandle):
        # First lets get the tweets from Bluemix Twitter Service
        tweets = self.getTweets(twitterHandle)
        print("Number of tweets returned: %d" % tweets["search"]["current"])
        if tweets["search"]["current"] < 20:
            return {"error": "Analysis is not complete!"}

        # Now send tweets to Watson Personality Insight service and get the insight
        jsonContentItems = self.tweetsToContentItem(tweets)
        headers = {'content-type': 'application/json'}
        response = requests.post("https://gateway.watsonplatform.net/personality-insights/api/v2/profile", headers=headers, data=jsonContentItems, auth=(self.PERSONALITY_INSIGHT_USERNAME, self.PERSONALITY_INSIGHT_PASSWORD))
        analysis = json.loads(response.text)
        if response.status_code == requests.codes.ok:
            if analysis["tree"] is not None:
                return response.text

        return {"error": "Analysis is not complete!"}

    def getTweets(self, twitterHandle):
        payload = {"q": "from:" + twitterHandle, "lan": "en", "size": self.NO_OF_TWEETS_TO_RETRIEVE}
        response = requests.get("https://cdeservice.mybluemix.net:443/api/v1/messages/search", params=payload, auth=(self.TWITTER_USERNAME, self.TWITTER_PASSWORD))
        tweets = json.loads(response.text)
        return tweets

    # Convert tweets to content items to conform with Watson Personality Insight input format for json
    def tweetsToContentItem(self, tweets):
        contentItems = []
        for tweet in tweets["tweets"]:
            item = {
                "id": tweet["message"]["id"],
                "userid":tweet["message"]["actor"]["id"],
                "created": "",
                "updated": "",
                "contenttype": "text/plain",
                "charset": "UTF-8",
                "language": "en-us",
                "content": tweet["message"]["body"],
                "parentid": "",
                "reply": False,
                "forward": False
            }
            contentItems.append(item)
        return json.dumps({"contentItems": contentItems})

if __name__ == '__main__':
    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))
    cherrypy.config.update({
        "server.socket_host": HOST_NAME,
        "server.socket_port": PORT_NUMBER,
    })

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
            },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
            }
     }

    cherrypy.quickstart(PersonalityInsight(os.getenv("VCAP_SERVICES")), "/", conf)

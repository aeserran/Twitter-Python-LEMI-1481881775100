import cherrypy
import os
import json
import requests

class PersonalityInsight(object):
    twitterUsername = "ENTER_TWITTER_USERNAME_FROM_BLUEMIX"
    twitterPassword = "ENTER_TWITTER_PASSWORD_FROM_BLUEMIX"
    perInsightUsername = "ENTER_PERSONALITY_INSIGHT_USERNAME_FROM_BLUEMIX"
    perInsightPassword = "ENTER_PERSONALITY_INSIGHT_PASSWORD_FROM_BLUEMIX"
    def __init__(self, vcapServices):
        if vcapServices is not None:
            print("Parsing vcapServices...")
            services = json.loads(vcapServices)
            # Lets read the credentials for twitter service from cf
            twitterServiceName = "twitterinsights"
            if twitterServiceName in services:
                twitterUsername = services[twitterServiceName][0]["credentials"]["username"]
                twitterPassword = services[twitterServiceName][0]["credentials"]["password"]
            # Now lets read the credentials for Personality Insight Service from cf
            perInsightServiceName = "personality_insights"
            if perInsightServiceName in services:
                perInsightUsername = services[perInsightServiceName][0]["credentials"]["username"]
                perInsightPassword = services[perInsightServiceName][0]["credentials"]["password"]

    @cherrypy.expose
    def index(self):
        return """<html>
          <head></head>
          <body>
            <form method="get" action="analyze">
              <input type="text" value="" placeholder="Twitter Handle" name="twitterHandle" />
              <button type="submit">Get my personality!</button>
            </form>
          </body>
        </html>"""

    @cherrypy.expose
    def analyze(self, twitterHandle):
        # First lets get the tweets from Bluemix Twitter Service
        if twitterHandle is None or twitterHandle == "":
            return "Please provide a twitter handle!"

        tweets = self.getTweets(twitterHandle)
        print("Number of tweets returned: %d" % tweets["search"]["current"])

        if tweets["search"]["current"] < 20:
            return "Number of tweets returned is " + str(tweets["search"]["current"]) + ". Try to provide more than that for a meaningful result!"

        # Create content items to conform with Watson Personality Insight input format
        contentItems = []
        for tweet in tweets["tweets"]:
            item = {"id": tweet["message"]["id"], "userid":tweet["message"]["actor"]["id"], "created": "", "updated": "", "contenttype": "text/plain", "charset": "UTF-8", "language": "en-us", "content": tweet["message"]["body"], "parentid": "", "reply": False, "forward": False}
            contentItems.append(item)
        jsonContentItems = json.dumps({"contentItems": contentItems})
        #print(jsonContentItems)

        # Now execute the request to Watson Personality Insight service
        headers = {'content-type': 'application/json'}
        response = requests.post("https://gateway.watsonplatform.net/personality-insights/api/v2/profile", headers=headers, data=jsonContentItems, auth=(self.perInsightUsername, self.perInsightPassword))
        analysis = json.loads(response.text)
        if response.status_code == requests.codes.ok:
            print("There are %d words in the input (min. 3500 for statistically meaningful result.)" % analysis["word_count"])
            if analysis["tree"] is not None:
                return self.getHTML(analysis)
            else:
                return "Analysis is not complete!"
        else:
            return analysis["error"]

    def getTweets(self, twitterHandle):
        noOfTweet = 20
        payload = {"q": "from:" + twitterHandle, "lan": "en", "size": noOfTweet}
        response = requests.get("https://cdeservice.mybluemix.net:443/api/v1/messages/search", params=payload, auth=(self.twitterUsername, self.twitterPassword))
        tweets = json.loads(response.text)
        return tweets

    def getHTML(self, analysis):
        personality = analysis["tree"]["children"][0]
        needs = analysis["tree"]["children"][1]
        values = analysis["tree"]["children"][2]

        # Personality
        html = "<h2>Personality</h2>"
        for item in personality["children"][0]["children"]:
            html += item["name"] + ": " + str("%.2f%%" % (item["percentage"]*100))
            html += "<br>"
        #html += "</p>"

        # Needs
        html += "<h2>Needs</h2>"
        for item in needs["children"][0]["children"]:
            html += item["name"] + ": " + str("%.2f%%" % (item["percentage"]*100))
            html += "<br>"
        html += "</p>"

        #Values
        html += "<h2>Values</h2>"
        for item in values["children"][0]["children"]:
            html += item["name"] + ": " + str("%.2f%%" % (item["percentage"]*100))
            html += "<br>"
        html += "</p>"

        return html


if __name__ == '__main__':
    # Get host/port from the Bluemix environment, or default to local
    HOST_NAME = os.getenv("VCAP_APP_HOST", "127.0.0.1")
    PORT_NUMBER = int(os.getenv("VCAP_APP_PORT", "3000"))
    cherrypy.config.update({
        "server.socket_host": HOST_NAME,
        "server.socket_port": PORT_NUMBER,
    })

    cherrypy.quickstart(PersonalityInsight(os.getenv("VCAP_SERVICES")))

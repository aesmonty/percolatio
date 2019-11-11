
import datetime


def getTestGrant(foundation_name):

    return {
        "Foundation": {
            "Name": foundation_name
        },

        "Grant": {
            "title": "Test grant is the best",
            "tagList": ["test_tag_1", "test_tag_2"],
            "isPreFunded": True,
            "numberOfGrantees": "1",
            "amountPerGrantee": "10000",
            "nonFinancialRewards": True,
            "applicationsStartDate": str(datetime.datetime.now()),
            "applicationsEndDate": str(datetime.datetime.now() + datetime.timedelta(days=7)),
            "description": "Lorem ipsum",
            "externalWebsite": "https://stackoverflow.com/",
            "otherDetails": 'Another detail'
        }
    }

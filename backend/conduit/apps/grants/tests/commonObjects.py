
import datetime


def getTestGrant(foundation_name):

    return {
        "Foundation": {
            "Name": foundation_name
        },

        "Grant": {
            "title": "Test grant is the best",
            "tagList": ["test_tag_1", "test_tag_2"],
            "numberOfGrantees": "1",
            "nonFinancialRewards": True,
            "description": "Lorem ipsum",
            "externalWebsite": "https://stackoverflow.com/",
            "otherDetails": 'Another detail',
            # Optional Parameters
            "isPreFunded": True,
            "amountPerGrantee": "10000",
            "applicationsStartDate": str(datetime.date.today()),
            "applicationsEndDate": str(datetime.date.today() + datetime.timedelta(days=7)),
        }
    }

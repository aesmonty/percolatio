
from faker import Faker
fake = Faker()


def getGrantBasic(foundation_name):
    return {
        "Foundation": {
            "Name": foundation_name
        },
        "Grant": {
            "title": fake.company(),
            "description": fake.paragraph(),
            "minAmountPerGrantee": fake.random.pyint(min_value=0, max_value=9999)
        }
    }


def getGrantComplete():
    pass


def getTestGrant(foundation_name):

    return {
        "Foundation": {
            "Name": foundation_name
        },

        "Grant": {
            "title": "Test grant is the best",
            "description": "Lorem ipsum",
            "state": "Receiving applications",
            "minAmountPerGrantee": "10000",

            # Optional Parameters
            "tagList": ["test_tag_1", "test_tag_2"],
            "externalWebsite": "https://stackoverflow.com/",
            "otherDetails": 'Another detail',
            "allowDonations": True,  # Default True
            "otherAwards": "Stripe credits",  # Default empty
        }
    }

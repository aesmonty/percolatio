
from faker import Faker
fake = Faker()


def getGrantBasic(foundation_name):
    return {
        "Grant": {
            "FoundationName": foundation_name,
            "title": fake.company(),
            "description": fake.paragraph(),
            "minAmountPerGrantee": fake.random_int(0, 9999)
        }
    }


def getGrantComplete(foundation_name):
    return {
        "Grant": {
            "FoundationName": foundation_name,
            "title": fake.company(),
            "description": fake.paragraph(),
            "minAmountPerGrantee": fake.random_int(0, 9999),
            "state": fake.random_int(1, 5),
            "tagList": fake.words(nb=3, ext_word_list=None, unique=True),
            'externalWebsite': fake.uri(),
            'allowDonations': bool(fake.random_int(0, 1)),
            'otherAwards': fake.paragraph(),
            'otherDetails': fake.paragraph(),
        }
    }

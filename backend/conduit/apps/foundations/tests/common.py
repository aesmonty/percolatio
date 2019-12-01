from faker import Faker
fake = Faker()


def getFoundationBasic(foundation_name=None):
    return {
        'foundation': {
            'name': foundation_name or fake.company(),
            'description': fake.paragraph(),
            'website': None
        }
    }


def getFoundationComplete(foundation_name=None):
    return {
        'foundation': {
            'name': foundation_name or fake.company(),
            'description': fake.paragraph(),
            'website': fake.uri(),
            'taglist': fake.words(nb=3, ext_word_list=None, unique=True)
        }
    }

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# homepage = 'https://www.onehippo.org/'
# homepage2 = 'https://www.onehippo.com/'
# homepage3 = 'http://www.onehippo.com/'
# homepages = [homepage, homepage2, homepage3]
homepages = ['https://www.onehippo.org/', 'https://www.onehippo.com/en', 'https://www.onehippo.com/de',
             'http://marketplace.onehippo.com/', 'https://www.onehippo.com/nl/', 'https://www.onehippo.com/nl',
             'https://www.onehippo.org/7_8', 'https://www.onehippo.org/7_9', 'https://www.onehippo.org/10',
             'http://www.onehippo.com/connect', 'https://www.onehippo.com/de/', 'http://www.onehippo.co.uk/site/dotorg',
             'http://www.onehippo.co.uk/site/dotorg/7_9', 'http://www.onehippo.co.uk/site/dotorg/7_8',
             'https://www.onehippo.com/old_en', 'http://www.onehippo.com/connect/',
             'http://www.onehippo.co.uk/site/dotorg/', 'https://www.onehippo.org/10/', 'https://www.onehippo.org/7_6',
             'https://www.onehippo.org/7_7', 'https://www.onehippo.org/partner/', 'https://www.onehippo.org/partner']


def get_keywords(url, items=False):
    """
    This method gets the keywords from a URL or a list of URLs
    :param url:'The URL to get the keywords from
    :param items: If true, only get the keywords from one URL:
    Otherwise, get the keywords from a list of URLs
    :return: A ordered and without duplicates list of keywords
    """
    if not items:
        # Remove the first and last URLs from a transactionPath?
        url = url[1:-1]
    for home_page in homepages:
        url = url.replace(home_page, " ")
    url = url.replace(".html", " ")
    url = url.replace(".xml", " ")
    url = url.replace(".php", " ")
    url = url.replace("/", " ")
    url = url.replace("-", " ")
    url = url.replace(".", " ")
    url = url.replace(",", " ")
    url = url.replace("\'", " ")
    path_tokens = word_tokenize(url)
    sw = set(stopwords.words('english'))
    sw.add('en')
    sw.add('nl')
    sw.add('de')
    sw.add('txt')
    sw.add('oh')
    sw.add('1')
    sw.add('login')
    sw.remove('about')
    sw.remove('why')
    result = [w for w in path_tokens if w not in sw]
    return sorted(set(result))

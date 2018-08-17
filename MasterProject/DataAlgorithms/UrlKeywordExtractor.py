from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# homepage = 'https://www.onehippo.org/'
# homepage2 = 'https://www.onehippo.com/'
# homepage3 = 'http://www.onehippo.com/'
# homepages = [homepage, homepage2, homepage3]
# homepages = ['https://www.onehippo.org/', 'https://www.onehippo.com/en', 'https://www.onehippo.com/de',
#              'http://marketplace.onehippo.com/', 'https://www.onehippo.com/nl/', 'https://www.onehippo.com/nl',
#              'https://www.onehippo.org/7_8', 'https://www.onehippo.org/7_9', 'https://www.onehippo.org/10',
#              'http://www.onehippo.com/connect', 'https://www.onehippo.com/de/', 'http://www.onehippo.co.uk/site/dotorg',
#              'http://www.onehippo.co.uk/site/dotorg/7_9', 'http://www.onehippo.co.uk/site/dotorg/7_8',
#              'https://www.onehippo.com/old_en', 'http://www.onehippo.com/connect/',
#              'http://www.onehippo.co.uk/site/dotorg/', 'https://www.onehippo.org/10/', 'https://www.onehippo.org/7_6',
#              'https://www.onehippo.org/7_7', 'https://www.onehippo.org/partner/', 'https://www.onehippo.org/partner']

homepages = ['https://www.hellermanntyton.de/', 'http://www.hellermanntyton.fi/', 'http://www.hellermanntyton.dk/',
             'http://www.hellermanntyton.es/', 'http://www.hellermanntyton.it/', 'http://www.hellermanntyton.co.uk/',
             'https://www.hellermanntyton.com/', 'http://www.hellermanntyton.no/', 'http://www.hellermanntyton.si/',
             'http://www.hellermanntyton.se/', 'http://www.hellermanntyton.fr/', 'http://www.hellermanntyton.co.za/',
             'http://www.hellermanntyton.ru/', 'http://www.hellermanntyton.com.cn/', 'https://www.hellermanntyton.nl/',
             'https://www.hellermanntyton.at/', 'http://www.hellermanntyton.hu/', 'http://www.hellermanntyton.com.au/',
             'http://www.hellermanntyton.cz/', 'http://www.hellermanntyton.co.in/', 'http://www.hellermanntyton.com.sg/',
             'http://www.htdata.co.uk/', 'http://www.hellermanntyton.pl/', 'http://www.hellermanntyton.co.uk:80/',
             'http://www.hellermanntyton.dk:80/', 'http://www.HellermannTyton.fr/', 'https://www.staeng.co.uk/',
             'http://www.hellermanntyton.ch/', 'http://www.hellermanntyton.com.tr/', 'http://www.HELLERMANNTYTON.RU/',
             'https://www.hellermanntyton.de:443/', 'https://www.hellermanntyton.at:443/',
             'https://www.hellermanntyton.nl:443/', 'https://www.hellermanntyton.com:443/',
             'https://www.n46-163-91-254.cnet.hosteurope.de/', 'https://www.forum.hellermanntyton.se/',
             'http://WWW.HELLERMANNTYTON.CO.UK/', 'https://www.HellermannTyton.nl/']


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
    url = url.replace(".aspx", " ")
    url = url.replace("/", " ")
    url = url.replace("-", " ")
    url = url.replace(".", " ")
    url = url.replace(",", " ")
    url = url.replace("{", " ")
    url = url.replace("}", " ")
    url = url.replace("&", " ")
    url = url.replace("@", " ")
    url = url.replace("\'", " ")
    path_tokens = word_tokenize(url)
    sw = set(stopwords.words('english'))
    sw.add('en')
    sw.add('nl')
    sw.add('de')
    sw.add('fi')
    sw.add('dk')
    sw.add('es')
    sw.add('it')
    sw.add('uk')
    sw.add('no')
    sw.add('si')
    sw.add('se')
    sw.add('fr')
    sw.add('za')
    sw.add('ru')
    sw.add('cn')
    sw.add('at')
    sw.add('hu')
    sw.add('au')
    sw.add('cz')
    sw.add('in')
    sw.add('sg')
    sw.add('pl')
    sw.add('ch')
    sw.add('tr')
    sw.add('UK')
    sw.add('CO')
    sw.add(':443')
    sw.add(':80')
    sw.add('co')
    sw.add('txt')
    sw.add('oh')
    sw.add('1')
    sw.add('login')
    sw.remove('about')
    sw.remove('why')
    result = [w for w in path_tokens if w not in sw]
    no_integers = [x for x in result if not any(c.isdigit() for c in x)]
    return sorted(set(no_integers))

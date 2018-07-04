from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

homepage = 'https://www.onehippo.org/'
homepage2 = 'https://www.onehippo.com/'
homepage3 = 'http://www.onehippo.com/'
homepages = [homepage, homepage2, homepage3]


def get_keywords(url):
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
    sw.add('net')
    sw.add('com')
    sw.add('1')
    sw.add('login')
    sw.remove('about')
    sw.remove('why')
    result = [w for w in path_tokens if w not in sw]
    return set(result)


from urllib.parse import urlparse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

url = '[https://www.onehippo.org/library/concepts/error-pages-and-error-handling/' \
      '1.-handling-error-codes-and-exceptions-by-the-web.xml.html]'
homepage = 'https://www.onehippo.org/'
homepage2 = 'https://www.onehippo.com/en'
if not url.__contains__('login'):
    path = url[1:-1]
    path = path.replace(homepage, " ")
    path = path.replace(homepage2, " ")
    path = path.replace(".html", " ")
    path = path.replace(".xml", " ")
    path = path.replace("/", " ")
    path = path.replace("-", " ")
    path = path.replace(".", " ")
    path = path.replace(",", " ")
    path = path.replace("\'", " ")

    path_tokens = word_tokenize(path)
    sw = set(stopwords.words('english'))
    fs = [w for w in path_tokens if not w in sw]

#url[2:-2]
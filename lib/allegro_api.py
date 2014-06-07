import sys
import urllib
import getopt

sys.path.append('libs')
from bs4 import BeautifulSoup


def open_url(url):
    """Function for open url """
    opener = urllib.FancyURLopener({})
    resq = opener.open(url)
    myhtml = resq.read()
    soup = BeautifulSoup(myhtml, 'lxml')
    return soup


def allegro_api(name):
    """Function for finding price and url of product"""
    soup = open_url(
        'http://allegro.pl/listing/listing.php?counters=\
        1&offerTypeBuyNow=1&order=p&standard_allegro=1&string={}'.format(name))
    try:
        price = soup.findAll('span', 'buy-now dist')[0].text[10:-4]
        price = price.replace(',', '.')
        url = soup.findAll('article')[0].findAll('a')[0]['href']
        url = "http://allegro.pl" + url
        soup_image = open_url(url)
        image_url = soup_image.findAll(
            'div', 'galleryContainer'
        )[0].span['content']
        return [float(price), url, image_url]
    except IndexError:
        return False


def usage():
    """Help function"""
    return "To search item price write: --name procuct_name"


def poss_parameters():
    """Function to posibility to use command line for search price and urls"""
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'hn:', ['help', 'name=']
        )
    except getopt.GetoptError as err:
        return str(err), usage()
    for opt, arg in options:
        if opt in ('-h', '--help'):
            return usage()
        elif opt in ('-n', '--name'):
            name = arg
        else:
            assert False
    return allegro_api(name)


def main():
    """Main function to recognize if we use poss parametrs or normal in code"""
    if sys.argv[1:]:
        return poss_parameters()
    else:
        return allegro_api('canon450')

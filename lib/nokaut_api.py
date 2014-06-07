"""API nokaut"""
#!usr/bin/env python
from lxml import etree
import urllib2
import getopt
import sys


def nokaut_api(prod_name, api_key):
    """Function for parse xml for geting price and url"""
    api = "http://api.nokaut.pl/?format=rest&key=%s&method=nokaut.product.\
getByKeyword&keyword=%s" % (api_key, prod_name)
    response = urllib2.urlopen(api)
    xml = ""
    for line in response:
        xml = "".join([xml, line.rstrip(), "\n"])
    root = etree.XML(xml)
    prices = [price.text for price in root.findall(".//price_min")]
    urls = [url.text for url in root.findall(".//url")]
    images = [image.text for image in root.findall(".//image_large")]
    zipped = zip(prices, urls, images)
    if zipped == []:
        return False
    else:
        prices = [
            [
                float(price.replace(',', '.')), url, image
            ] for price, url, image in zipped
        ]
        dic = {price: url for price, url, images in prices}
        dic2 = {price: images for price, url, images in prices}
        min_price = [min(price) for price in prices]
        return (
            sorted(min_price)[0],
            dic[sorted(min_price)[0]],
            dic2[sorted(min_price)[0]]
        )


def usage():
    """Help function"""
    return "To search item price write: --name product_name and --key api_key"


def poss_parameters():
    """Function to posibility to use command line for search price and urls"""
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'hn:k:', ['help', 'name=', 'key=']
        )
    except getopt.GetoptError as err:
        return str(err), usage()
    for opt, arg in options:
        if opt in ('-h', '--help'):
            return usage()
        elif opt in ('-n', '--name'):
            name = arg
        elif opt in ('-k', '--key'):
            key = arg
        else:
            assert False
    return nokaut_api(name, key)


def main():
    """Main function to recognize if we use poss parametrs or normal in code"""
    if sys.argv[1:]:
        return poss_parameters()
    else:
        return nokaut_api('macbook', 'a8839b1180ea00fa1cf7c6b74ca01bb5')

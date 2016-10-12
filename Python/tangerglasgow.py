#!/usr/bin/env python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import httplib2
import urllib
import os
from urlparse import urlparse

# create a subclass and override the handler methods


class MyHTMLParser(HTMLParser):

    def getUrlTabFrom(self, attrs):
        for attr in attrs:
            if (attr[0] == 'url'):
                return attr[1]
        return None

    def handle_starttag(self, tag, attrs):
        if tag == 'enclosure':
            try:
            #print "-> ", attrs[0][1]
                tgurl = self.getUrlTabFrom(attrs)
                if tgurl is not None:
                    #print tgurl
                    up = urlparse(tgurl)
                    f = '/home/yvan/Musique/Couleur3/'\
                    'TangerGlasgow/' + os.path.basename(up.path)
                    if not os.path.exists(f):
                        print 'Téléchargement de ', f
                        urllib.urlretrieve(tgurl, f)
                    else:
                        print f, " existe déjà"
            except Exception as e:
                print "Erreur ", e.message


def getTangerGlasgow():
    h = httplib2.Http()
    tgc3 = "http://www.rts.ch/couleur3/programmes/"\
    "tanger-glasgow/podcast/?flux=rss"
    r, content = h.request(tgc3, "GET")
    parser = MyHTMLParser()
    parser.feed(content)


getTangerGlasgow()

##CODE TAKEN FROM: https://github.com/aboyle/RegulomeDB-Tools/blob/master/RegulomeDBWebInterface.py
##RUNS VERY SLOW
import sys
import os
import urllib
import urllib2
import time

url = 'http://regulome.stanford.edu/download'

class HttpBot:
    """an HttpBot represents one browser session, with cookies."""
    def __init__(self):
        cookie_handler= urllib2.HTTPCookieProcessor()
        redirect_handler= urllib2.HTTPRedirectHandler()
        http_handler= urllib2.HTTPHandler()
        error_handler=urllib2.HTTPErrorProcessor()
        self._opener = urllib2.build_opener(cookie_handler,redirect_handler, http_handler,error_handler)
        #urllib2.install_opener(self._opener)

    def GET(self, url):
        return self._opener.open(url).read()

    def POST(self, url, parameters):     
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = { 'User-Agent' : user_agent }
        return self._opener.open(url, urllib.urlencode(parameters))

def lookup(rsID):
    bot = HttpBot()

    x = bot.POST('http://regulome.stanford.edu/results',{'data': rsID})

    pageData = x.read()

    pageData = pageData.split("<input type=\"hidden\" name=\"sid\" value=\"")
    sid = pageData[1].split("\" />")[0]

    x = bot.POST("http://regulome.stanford.edu/download", {'format':'full', 'sid':sid})

    pageData = x.read()
    if len(pageData) > 0:
        pageData = pageData.split("\n",1)
        pageData = pageData[1]
    else:
        pageData = ''


    return pageData


##MAIN------------------------------------------------------------------------------------
ifstream = open('test_snplist.txt', 'r')
coordText = ifstream.read()
coordText = coordText.strip().split('\n')
ifstream.close()

ofstream = open('gTex_results.txt','w')

for c in coordText:
    result = lookup(c)
    if len(result) > 0:
        result = result.split('\t')
        structures = result[3].split(',')
        ofstream.write(str(c)+'\n')
        ofstream.write('<Type|Procedure|Tissue|Gene>\n')
        motifs = [d for d in structures if d.count('Motif') != 0]
        if len(motifs) >0:
            for m in motifs:
                ofstream.write(str(m)+'\n')
            ofstream.write('\n')
        else:
            ofstream.write('NO MOTIF DATA\n')
            ofstream.write('\n')
    else:
        ofstream.write('SNP DATA NOT FOUND\n')
        ofstream.write('\n')

ofstream.close()


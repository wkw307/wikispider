# -*- coding: utf-8 -*
import scrapy
import os
import sys
import os.path
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')

class WikiSpider(scrapy.Spider):
    name = "wiki"

    global f

    def start_requests(self):
        rootdir1 = "/Users/wkw307/Desktop/1"
        urlroot = 'https://en.wikipedia.org/wiki/'
        rootdir = r'/Users/wkw307/Documents/data/'
        for dirpath, dirnames, filenames in os.walk(rootdir1):
            for filename in filenames:
                topicname = filename.split(".")

                os.mkdir(rootdir + topicname[0])
                yield scrapy.Request(url=urlroot+topicname[0], callback=self.parse, meta={'topic':topicname[0]})

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        [s.extract() for s in soup.findAll('img')]
        [s.extract() for s in soup.findAll('annotation')]
        [s.extract() for s in soup.findAll('sup')]
        #topicname = soup.find("h1").get_text()
        if(soup.find("h2").get_text() == "Contents"):
            h2 = soup.find_all("h2")[1];
        else:
            h2 = soup.find_all("h2")[0];
        h2name = h2.find("span").get_text();
        if(h2name == "References" or h2name == "See also" or h2name == ""):
            return
        h2name = h2name.replace("/","@")
        f = open("/Users/wkw307/Documents/data/" + response.meta['topic'] + "/" + h2name + ".txt", 'w')
        while(1):
            if(h2.next_sibling.next_sibling == '\n'):
                h2 = h2.next_sibling.next_sibling
                continue
            elif(h2.next_sibling.next_sibling.name == 'h2'):
                if(h2.next_sibling.next_sibling.get_text() == "See also[edit]" or h2.next_sibling.next_sibling.get_text() == "References[edit]" or h2.next_sibling.next_sibling.get_text() == "External links[edit]" or h2.next_sibling.next_sibling.get_text() == "Notes[edit]"):
                    f.close();
                    break
                else:
                    h2 = h2.next_sibling.next_sibling
                    f.close()
                    h2name = h2.find("span").get_text()
                    h2name = h2name.replace("/", "@")
                    #print h2name
                    f=open("/Users/wkw307/Documents/data/" + response.meta['topic'] + "/" + h2name + ".txt",'w')
                    continue
            elif (h2.next_sibling.next_sibling.name == "dl" or h2.next_sibling.next_sibling.name == "h3" or h2.next_sibling.next_sibling.name == "pre" or h2.next_sibling.next_sibling.name == "h4" or h2.next_sibling.next_sibling.name == "table" or h2.next_sibling.next_sibling.name == "div"):
                h2 = h2.next_sibling.next_sibling
                continue
            else:
                h2 = h2.next_sibling.next_sibling
                f.write(h2.get_text())

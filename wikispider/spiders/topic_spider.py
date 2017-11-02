# -*- coding: utf-8 -*
import scrapy
import os
import sys
import os.path

class TopicSpider(scrapy.Spider):
    name = "topic"

    def start_requests(self):
        rootdir = "/Users/wkw307/topics"
        urlroot = "http://202.117.54.39:8080/Yotta/AssembleAPI/getTreeByTopicForFragment?ClassName=数据结构&TermName="
        datadir = "/Users/wkw307/Desktop/data"
        for dirpath, dirnames, filenames in os.walk(datadir):
            for filename in filenames:
                topicname = filename.split('.')[0]

                yield scrapy.Request(url=urlroot+topicname,callback=self.parse,meta={'topic':topicname})

    def parse(self, response):
        #print response.body
        #print response.meta['topic']
        f = open("/Users/wkw307/topics/" + response.meta['topic'] + ".json",'w')
        f.write(response.body)
        f.close()
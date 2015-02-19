# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoursesItem(scrapy.Item):
    # define the fields for your item here like:
      crn = scrapy.Field()
      subjectCode = scrapy.Field()
      courseCode = scrapy.Field()
      sectNum = scrapy.Field()
      credit = scrapy.Field()
      courseName = scrapy.Field()
      profName = scrapy.Field()
      capacity = scrapy.Field()
      seatAvailable = scrapy.Field()
      startDate = scrapy.Field()
      endDate = scrapy.Field()

    # schedule
      days = scrapy.Field()
      startTime = scrapy.Field()
      endTime = scrapy.Field()
      location = scrapy.Field()
      courseType = scrapy.Field()
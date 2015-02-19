import scrapy
from courses.items import CoursesItem
oddFx = False
subFx = 0

class CoursesSpider(scrapy.Spider):
    name = "courses"
    allowed_domains = ["sis.hawaii.edu/"]
    start_urls = [
        "https://www.sis.hawaii.edu/uhdad/avail.classes?i=MAN&t=201530&s=FIL"
    ]

    def parse(self, response):
        global oddFx
        global subFx
        for idx, sel in enumerate(response.css('table.listOfClasses tr:not(.section-comment-course)')):
#        loopCount = len(response.css('table.listOfClasses tr:not(.section-comment-course)'))
#        for idx in range(loopCount):
            print "------------LOGGING------------"
            item = CoursesItem()
            print idx
            print "subFx: "+str(subFx)
            oddFx = idx
            #in the case of there being odd-days, like with the language classes
            oddCh = response.css('td.default:nth-child(3)').extract()[idx][27:-5]
            if oddCh == '': 
                print "oddCh TRUE " + str(oddFx)
                item['crn'] = response.css('td.default:nth-child(2) a::text').extract()[idx]
                item['profName'] = response.css('td.default:nth-child(7) span::text').extract()[idx]
                item['location'] = response.css('td.default:nth-child(11) span::text').extract()[idx]
                idx = idx + 1
                courseName = response.css('td.default:nth-child(5)').extract()[idx][20:-5]
            else:
                print "oddCh FALSE " + str(oddFx)
                item['crn'] = response.css('td.default:nth-child(2) a::text').extract()[idx]
                item['profName'] = response.css('td.default:nth-child(7) span::text').extract()[idx]
                item['location'] = response.css('td.default:nth-child(11) span::text').extract()[idx]
                if subFx > idx: idx = subFx
                else: idx = oddFx
                courseName = response.css('td.default:nth-child(5)').extract()[idx][20:-5]

            item['subjectCode'] = response.css('td.default:nth-child(3)::text').extract()[idx].split(' ', 1)[0]
            item['courseCode'] = response.css('td.default:nth-child(3)::text').extract()[idx].split(' ', 1)[1]

##            item['sectNum'] = response.css('td.default:nth-child(4)::text').extract()[idx]
##            item['seatAvailable'] = response.css('td.default:nth-child(8)::text').extract()[idx]
##            item['credit'] = response.css('td.default:nth-child(6)::text').extract()[idx]

            #in the case of there needing Restriction to be stated/marked
            if "<br>" in courseName:
                restriction = courseName.split('<br>', 1)[1]
                courseName = courseName.split('<br>', 1)[0]
                #in the case of there being no Restriction (but use of parenthesis for some detail)
                if "Restriction" not in restriction: focus = restriction
            if "rowspan" in courseName:
                courseName = courseName[12:]

                idx = idx + 1
                grabTime2 = response.css('td.default:nth-child(9)').extract()[idx][20:-5]
                if "TBA" in grabTime2:
                    startTime2 = 'TBA' 
                    endTime2 = 'TBA'
                else:
                    grabTime2 = grabTime2[7:]
                    startTime2 = grabTime2.split('-<spacer></spacer>', 1)[0]
                    endTime2 = grabTime2.split('-<spacer></spacer>', 1)[1]
                #startDate2 = response.css('td.default:nth-child(11)::text').extract()[idx].split('-', 1)[0]
                #endDate2 = response.css('td.default:nth-child(11)::text').extract()[idx].split('-', 1)[1]
                Days2 = response.css('td.default:nth-child(8)::text').extract()[idx]
                #Loc2 = response.css('td.default:nth-child(10) span::text').extract()[idx]
                idx = idx - 1
                print "Time2: "+str(startTime2)+" | "+str(endTime2)
            item['courseName'] = courseName

            #startTime/endTime problem caused by <spacer> tag & TBA
            grabTime = response.css('td.default:nth-child(10)').extract()[idx][20:-5]
            if "TBA" in grabTime:
                startTime = 'TBA' 
                endTime = 'TBA'
            else:
                grabTime = grabTime[7:]
                startTime = grabTime.split('-<spacer></spacer>', 1)[0]
                endTime = grabTime.split('-<spacer></spacer>', 1)[1]
##            item['startTime'] = startTime
##            item['endTime'] = endTime

##            item['startDate'] = response.css('td.default:nth-child(12)::text').extract()[idx].split('-', 1)[0]
##            item['endDate'] = response.css('td.default:nth-child(12)::text').extract()[idx].split('-', 1)[1]
##            item['days'] = response.css('td.default:nth-child(9)::text').extract()[idx]
            
            if oddFx<idx:
                subFx = idx + 1
                idx = idx - 1
                print "oddFx < idx"
            else:
                subFx = idx
                print "oddFx !< idx"
            print "subFx: "+str(subFx)

##            if item['courseName'].find('L')>4: item['courseType'] = "lab"
##            else: item['courseType'] = "lecture"
            yield item
            print idx
            
            print "------------LOGGED ------------"
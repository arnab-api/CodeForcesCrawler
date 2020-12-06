#   Arnab Sen Sharma
#   Lecturer, Department of CSE
#   Shahjalal University of Science and Technology

import scrapy
import re


class CodeforcesSpider(scrapy.Spider):
    name = 'codeforces'
    allowed_domains = ['codeforces.com']
    start_urls = ['http://codeforces.com//']

    user_arr = ['dot_0']

    def start_requests(self):
        # profile_root = 'http://codeforces.com//profile//'
        # for user in self.user_arr:
        #     yield scrapy.Request(url=profile_root+user, callback=self.parse_profiles)

        contest_root = 'http://codeforces.com//contests/with//'
        for user in self.user_arr:
            user_url = contest_root+user
            print(">>>>>>>>>>>>>> ", user_url)
            yield scrapy.Request(url=user_url, callback=self.parse_individul_contests)

    # def parse_profiles(self, response):
    #     rating = response.css('div.userbox > div.info > ul > li > span::text')[0].extract()
    #     user_id = response.request.url.split('//')[-1]

    #     print(user_id)
    #     yield {
    #         'user_id': user_id,
    #         'rating': rating 
    #     }
    
    def parse_individul_contests(self, response):
        table = response.xpath('//*[@class="tablesorter user-contests-table"]') 
        contest_elements = table.css('tbody > tr')

        user_id = response.request.url.split('//')[-1]

        contest_info_arr = []
        for contest in contest_elements:
            title_element = contest.css('td')[1]
            href = title_element.css('a::attr(href)').extract()[0]
            title = title_element.css('a::attr(title)').extract()[0]

            rank_elem = contest.css('td')[2]
            rank = rank_elem.css('a::text').extract()[0].strip()

            solved_elem = contest.css('td')[3]
            solved = solved_elem.css('a::text').extract()[0].strip()

            rating_elem = contest.css('td')[4]
            delta_rating = rating_elem.css('span::text').extract()[0]

            rating_elem = contest.css('td')[5]
            new_rating = rating_elem.css('td::text').extract()[0].strip()

            single_contest_info = {
                    "contest_href"  : href,
                    "contest_title" : title,
                    "rank"          : rank,
                    "solved"        : solved,
                    "delta_rating"  : delta_rating,
                    "new_rating"    : new_rating,
                    "date"          : "N/A"
                }
            contest_info_arr.append(
                single_contest_info
            )
            contest_url = 'http://codeforces.com/' + href
            # print(contest_url, single_contest_info)
            info =  {
                "user"    : user_id,
                "contest" : single_contest_info
            }
            # contest_url = "http://codeforces.com//contest//1300"
            print(" >>>>>>>>>>>>>>>>>>", contest_url)
            yield scrapy.Request(url = contest_url, callback = self.access_blog, meta={'info': info})

            # break

        # yield {
        #     "user_id"       : user_id,
        #     "contest_track" : contest_info_arr
        # }

    def access_blog(self, response):
            info = response.meta.get('info')

            try:
                print("         <<<<<<<<<<<<<<<<<<< blog accessed")
                blog = response.xpath('//*[@id="sidebar"]/div[4]/ul/li[1]/span[1]/a')[0]
                blog_link = 'http://codeforces.com/' + blog.css('a::attr(href)')[0].extract()
                
                yield scrapy.Request(url = blog_link, callback = self.get_contest_date, meta={'info': info})
            
            except:
                yield info

    def get_contest_date(self, response):
            info = response.meta.get('info')
            print(info['contest']['contest_href'])
            date_elem = []
            date = "N/A"
            try:
                date_elem = response.xpath('//*[@id="pageContent"]/div[2]/div[2]/div/div[2]/span[1]')[0]
                date = date_elem.css('span::attr(title)').extract()[0]
            except:
                date_elem = response.xpath('//*[@id="pageContent"]/div/div/div/div[2]/span[1]')[0]
                date = date_elem.css('span::attr(title)').extract()[0]

            info = response.meta.get('info')
            info['contest']['date'] = date

            print("XXXXXXXXXXXXX", info)

            yield info




            

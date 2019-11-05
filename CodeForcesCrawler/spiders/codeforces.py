#   Arnab Sen Sharma
#   Lecturer, Department of CSE
#   Shahjalal University of Science and Technology

import scrapy
import re


class CodeforcesSpider(scrapy.Spider):
    name = 'codeforces'
    allowed_domains = ['http://codeforces.com//']
    start_urls = ['http://codeforces.com//']

    user_arr = ['arnab_sust', 'dot_0']

    def start_requests(self):
        # profile_root = 'http://codeforces.com//profile//'
        # for user in self.user_arr:
        #     yield scrapy.Request(url=profile_root+user, callback=self.parse_profiles)

        contest_root = 'http://codeforces.com//contests/with//'
        for user in self.user_arr:
            yield scrapy.Request(url=contest_root+user, callback=self.parse_individul_contests)

    def parse_profiles(self, response):
        rating = response.css('div.userbox > div.info > ul > li > span::text')[0].extract()
        user_id = response.request.url.split('//')[-1]

        print(user_id)
        yield {
            'user_id': user_id,
            'rating': rating 
        }
    
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

            contest_info_arr.append(
                {
                    "contest_href"  : href,
                    "contest_title" : title,
                    "rank"          : rank,
                    "solved"        : solved,
                    "delta_rating"  : delta_rating,
                    "new_rating"    : new_rating
                }
            )

        yield {
            "user_id"       : user_id,
            "contest_track" : contest_info_arr
        }
            



            

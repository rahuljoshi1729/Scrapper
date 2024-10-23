import scrapy 
from scrapy_splash import SplashRequest
import json
import re
class my_spider(scrapy.Spider):
    name = "my_spider"
    # The username will be passed through the crawl command
    def __init__(self, username='', **kwargs):
        self.start_urls = [f'https://www.codechef.com/users/{username}']
        super().__init__(**kwargs)
    
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2}, endpoint='render.html')    
        
    def contesting(self,response):
        all_contest=[]
        contests= response.css("div.content")
        for contest in contests:
            contest_dict={}    
            contest_dict["contest_name"]=contest.css("h5 span::text").get() 
            contest_dict["contest_questions"]=contest.css("p span span::text").getall()
            all_contest.append(contest_dict) 
        return all_contest
    
    def extract_submissions(self, response):
    # Extract the script content that contains 'userDailySubmissionsStats'
        script_content = response.xpath("//script[contains(text(), 'userDailySubmissionsStats')]/text()").get()
        if script_content:
            # Use regex to locate and extract the JSON-like array within 'userDailySubmissionsStats'
            pattern = re.compile(r"userDailySubmissionsStats\s*=\s*(\[\{.*?\}\])\s*;", re.DOTALL)
            match = pattern.search(script_content)
            
            if match:
                json_data = match.group(1)
                daily_submissions = json.loads(json_data)
                return daily_submissions
        
        return None
    
    #extracting rating
    def extract_rating(self,response):
        script_content = response.xpath("//script[contains(text(), 'all_rating')]/text()").get()
        if script_content:
            #using regex
            pattern = re.compile(r"all_rating\s*=\s*(\[\{.*?\}\])\s*;", re.DOTALL)
            match =pattern.search(script_content)
            
            if match:
                json_data=match.group(1)
                try:
                    all_ratings=json.loads(json_data)
                    return all_ratings
                except json.JSONDecodeError as e:
                    print(f"Error while decoding JSON: {e}")
        return None
    
    
    
    def parse(self,response):
        user_details_list = response.css("section.user-details label::text").extract()
        #extracting the rating and username
        rating = response.css("section.user-details span.rating::text").get()
        if rating:
            rating = rating.strip()
            #extracting username
            username = response.css("section.user-details span.m-username--link::text").get()
            #extracting rating number and division
            rating_number=response.css("div.rating-number::text").get()
            division=response.xpath("/html/body/main/div/div/div/aside/div[1]/div/div[1]/div[2]/text()").get()
            #highest rating
            highest_rating=response.css("div.rating-header small::text").get(default=None) or response.xpath("/html/body/main/div/div/div/aside/div[1]/div/div[1]/small/text()").get(default=None)
            global_rank=response.css("div.rating-ranks ul.inline-list li:first-child strong::text").get(default=None) or response.xpath("/html/body/main/div/div/div/aside/div[1]/div/div[2]/ul/li[1]/a/strong/text()").get(default=None)
            country_rank=response.css("div.rating-ranks ul.inline-list li:nth-child(2) strong::text").get(default=None) or response.xpath("/html/body/main/div/div/div/aside/div[1]/div/div[2]/ul/li[2]/a/strong/text()").get(default=None)
            
            #No. of contest participated
            contest_participated=response.css("div.contest-participated-count b::text").get(default=None) or response.xpath("/html/body/main/div/div/div/div/div/section[3]/div[1]/div/b/text()").get(default=None)
            
            
            #total questions solved
            total_questions=response.xpath("/html/body/main/div/div/div/div/div/section[4]/h3[4]/text()").get(default=None)
            
            #extracting daily submissions
            daily_submissions=self.extract_submissions(response)
            all_ratings=self.extract_rating(response)
                
            
        else:
            username = response.css("section.user-details li:contains('Username:') span::text").get() or response.xpath("//label[text()='Username:']/following-sibling::span/text()").get()
            rating_number=None
            division=None
            highest_rating=None
            global_rank=None
            country_rank=None
            contest_participated=None

            total_questions=response.xpath("//h3[contains(text(), 'Total Problems Solved')]/text()").get(default=None)
    
            daily_submissions=None
            all_ratings=None

            
            
        #extracting user profile
        user_profile_img=response.css("header img.profileImage::attr(src)").get()    
        
        #extracting country name and flag
        if 'Country:' in user_details_list:
            country_flag=response.css("section.user-details img.user-country-flag::attr(src)").get() or response.xpath("/html/body/main/div/div/div/div/div/section[1]/ul/li[2]/span/img/@src").get()
            country_name=response.css("section.user-details span.user-country-name::text").get() or response.xpath("/html/body/main/div/div/div/div/div/section[1]/ul/li[2]/span/span/text()").get()
        else:
            country_flag=None
            country_name=None  
        
        #extracting student/profession 
        if 'Student/Professional:' in user_details_list:
            student_profession=response.css("section.user-details li:contains('Student/Professional:') span::text").get() or response.xpath("//label[text()='Student/Professional:']/following-sibling::span/text()").get()
        else:
            student_profession=None    
        
        #extracting student institute
        if 'Institution:' in user_details_list:
            student_institute=response.css("section.user-details li:contains('Institution:') span::text").get() or response.xpath("//label[text()='Institution:']/following-sibling::span/text()").get()
        else:
            student_institute=None    
        
        #extracting the plan of the user    
        if 'CodeChef Pro Plan:' in user_details_list:
            plan=response.css("section.user-details li:contains('CodeChef Pro Plan:') span::text").get().split('.')[0] or response.xpath("//label[text()='CodeChef Pro Plan:']/following-sibling::span/text()").get().strip().split('.')[0].strip()
        else:
            plan=None    
        """      
        for month, days_data in heat_map.items():
            yield {
                'month': month,
                'data': days_data
            }    
        """
        
        yield {
            'rating': rating,
            'rating_number': rating_number,
            'division':division,
            'username': username,
            'user_profile_img': user_profile_img,
            'country_name': country_name,
            'country_flag': country_flag,
            'student_profession': student_profession,
            'student_institute': student_institute,
            'plan': plan,
            'highest_rating':highest_rating,
            'country_rank':country_rank,
            'global_rank':global_rank,
            'contest_participated':contest_participated,
            "total_question":total_questions, 
            "daily_submissions":daily_submissions,
            "all_ratings":all_ratings
        }
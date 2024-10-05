import scrapy 
from collections import defaultdict
from datetime import datetime

class myspider(scrapy.Spider):
    name = "my_spider"
    # The username will be passed through the crawl command
    def __init__(self, username='', **kwargs):
        self.start_urls = [f'https://www.codechef.com/users/{username}']
        super().__init__(**kwargs)
        
    def contesting(self,response):
        all_contest=[]
        contests= response.css("div.content")
        for contest in contests:
            contest_dict={}    
            contest_dict["contest_name"]=contest.css("h5 span::text").get() 
            contest_dict["contest_questions"]=contest.css("p span span::text").getall()
            all_contest.append(contest_dict) 
        return all_contest
    
    def heat_mapping(self,response):
        heatmap_data_by_month = defaultdict(list)
        print(response.css("div.heatmap-content rect.day"))
        print("hello")
        for rec in response.css("rect.day"):
            
            date = rec.attrib.get('data-date')
            data_count = rec.attrib.get('data-count', '0')  # Default to '0' if no submission
            category = rec.attrib.get('category', '0')      # Default to '0' if no category
            
            # Parse the date and get the month
            parsed_date = datetime.strptime(date, '%Y-%m-%d')
            month_key = parsed_date.strftime('%Y-%m')  # Format the month as YYYY-MM
            
            heatmap_data_by_month[month_key].append({
                'date': date,
                'data_count': data_count,
                'category': category})
        return heatmap_data_by_month    
        
        
    def parse(self,response):
        user_details_list = response.css("section.user-details label::text").extract()
        print(user_details_list)
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
            
            #function to extract contest details
            #all_contest=self.contesting(response)
            all_contest=None
            
            #total questions solved
            total_questions=response.xpath("/html/body/main/div/div/div/div/div/section[4]/h3[4]/text()").get(default=None)
            
            #heat map data
            heat_map=self.heat_mapping(response)
            
        else:
            username = response.css("section.user-details li:contains('Username:') span::text").get() or response.xpath("//label[text()='Username:']/following-sibling::span/text()").get()
            rating_number=None
            division=None
            highest_rating=None
            global_rank=None
            country_rank=None
            contest_participated=None
            all_contest=None
            total_questions=response.xpath("//h3[contains(text(), 'Total Problems Solved')]/text()").get(default=None)
            heat_map=None

            
            
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
            
        for month, days_data in heat_map.items():
            yield {
                'month': month,
                'data': days_data
            }    
        
        
        '''yield {
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
            "all_contest":all_contest,
            "total_question":total_questions, 
            "heat_map":heat_map
        }'''
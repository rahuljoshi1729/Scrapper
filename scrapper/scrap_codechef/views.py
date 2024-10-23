from django.shortcuts import render
from rest_framework.views import APIView
from  rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup
from requests_html import HTMLSession
import asyncio
import re
import json

class codechef(APIView):
    def post(self, request, username):
        try:
            if username:
                url = f"https://www.codechef.com/users/{username}"
                session = HTMLSession()
                response = session.get(url)
                if response.status_code == 200:
                    result = response.html.html
                    soup=BeautifulSoup(result,'html.parser')

                    if soup:
                        user_details_list = [label.get_text(strip=True) for label in soup.select("section.user-details label")]
                        print(user_details_list)
                        #getting rating
                        a=soup.select_one("section.user-details span.rating")
                        rating = a.get_text(strip=True) if a else None
                        
                        #getting rating 
                        rating_number = soup.select_one("div.rating-number")
                        rating_number = rating_number.get_text(strip=True) if rating_number else None
                        
                        #getting highest rarting
                        highest_rating = soup.select_one("div.rating-header small")
                        highest_rating = highest_rating.get_text(strip=True) if highest_rating else None    
                        
                        #divison
                        division = soup.select_one("div.rating-header div:nth-of-type(2)")
                        division_text = division.get_text(strip=True) if division else None
                        
                        # Global and country rank
                        global_rank = soup.select_one("div.rating-ranks ul.inline-list li:first-child strong")
                        global_rank = global_rank.get_text(strip=True) if global_rank else None

                        country_rank = soup.select_one("div.rating-ranks ul.inline-list li:nth-child(2) strong")
                        country_rank = country_rank.get_text(strip=True) if country_rank else None
                        
                        # Number of contests participated
                        contest_participated = soup.select_one("div.contest-participated-count b")
                        contest_participated = contest_participated.get_text(strip=True) if contest_participated else None

                        # Total questions solved
                        total_questions = soup.find("h3", string=re.compile('Total Problems Solved'))
                        total_questions = total_questions.get_text(strip=True) if total_questions else None
                        
                        #extract user submission
                        submission=self.extract_submissions(soup)
                        
                        #extarct rating chart
                        ratings=self.extract_rating(soup)
                        
                        #extracting user details
                        if "Student/Professional:" in user_details_list:
                            profession=soup.select_one("section.user-details li:-soup-contains('Student/Professional:') span")
                            student_profession = profession.get_text(strip=True) if profession else None
                        else:
                            student_profession = None

                        
                        #extract country details    
                        if 'Country:' in user_details_list:
                            country_flag = soup.select_one("section.user-details img.user-country-flag")
                            country_flag = country_flag['src'] if country_flag else None
                            
                            country_name = soup.select_one("section.user-details span.user-country-name")
                            country_name = country_name.get_text(strip=True) if country_name else None
                        else:
                            country_flag = None
                            country_name = None   
                        
                                                
                        #extract the plan 
                        if 'CodeChef Pro Plan:' in user_details_list:
                            plan_label = soup.find('label', text='CodeChef Pro Plan:')
                            if plan_label:
                                # Find the corresponding sibling span element
                                plan = plan_label.find_next('span')
                                plan=plan.get_text(strip=True).split('.')[0] if plan else None
                                
                        print(username,rating_number,division,highest_rating,global_rank,country_rank,contest_participated,total_questions,student_profession,country_flag,country_name,plan)
                        print(ratings)
                        print(submission)
                    return Response({"username":username,
                                    "rating_number":rating,
                                    "division":division_text,
                                    "highest_rating":highest_rating,
                                    "global rank":global_rank,
                                    "country_rank":country_rank,
                                    "contest_participated":contest_participated,
                                    "total_questions":total_questions,
                                    "student/professional":student_profession,
                                    "country_name":country_name,
                                    "country_flag":country_flag,
                                    "codechef plan":plan,
                                    "user_submissions": submission,
                                    "ratings":ratings}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                    
    #function to extract submission                
    def extract_submissions(self, soup):
            # the script content that contains 'userDailySubmissionsStats'
            script_content = soup.find("script", text=re.compile('userDailySubmissionsStats'))
            if script_content:
                pattern = re.compile(r"userDailySubmissionsStats\s*=\s*(\[\{.*?\}\])\s*;", re.DOTALL)
                match = pattern.search(script_content.string)

                if match:
                    json_data = match.group(1)
                    daily_submissions = json.loads(json_data)
                    return daily_submissions

            return None
    
    #extract rating chart
    def extract_rating(self, soup):
        script_content = soup.find("script", text=re.compile('all_rating'))
        if script_content:
            pattern = re.compile(r"all_rating\s*=\s*(\[\{.*?\}\])\s*;", re.DOTALL)
            match = pattern.search(script_content.string)

            if match:
                json_data = match.group(1)
                try:
                    all_ratings = json.loads(json_data)
                    return all_ratings
                except json.JSONDecodeError as e:
                    print(f"Error while decoding JSON: {e}")    

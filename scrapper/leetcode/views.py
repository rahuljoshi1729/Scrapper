from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import json

#code to extract using API GRAPHQL
#a new data has been added to the response data
class userprofile(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            limit = request.data['limit']
            query = """
            query getUserProfile($username: String!) {
                allQuestionsCount {
                    difficulty
                    count
                }
                matchedUser(username: $username) {
                    username
                    githubUrl
                    twitterUrl
                    linkedinUrl
                    contributions {
                        points
                        questionCount
                        testcaseCount
                    }
                    profile {
                        realName
                        userAvatar
                        birthday
                        ranking
                        reputation
                        websites
                        countryName
                        company
                        school
                        skillTags
                        aboutMe
                        starRating
                    }
                    badges {
                        id
                        displayName
                        icon
                        creationDate
                    }
                    upcomingBadges {
                        name
                        icon
                    }
                    activeBadge {
                        id
                        displayName
                        icon
                        creationDate
                    }
                    submitStats {
                        totalSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                        acSubmissionNum {
                            difficulty
                            count
                            submissions
                        }
                    } 
                    submissionCalendar
                    
                    tagProblemCounts {
                        advanced {
                            tagName
                            problemsSolved
                        }
                        intermediate {
                            tagName
                            problemsSolved
                        }
                        fundamental {
                            tagName
                            problemsSolved
                        }
                    }
                }
                userContestRanking(username: $username) {
                    attendedContestsCount
                    rating
                    globalRanking
                    totalParticipants
                    topPercentage
                    badge {
                        name
                    }
                }
                userContestRankingHistory(username: $username) {
                    attended
                    rating
                    ranking
                    trendDirection
                    problemsSolved
                    totalProblems
                    finishTimeInSeconds
                    contest {
                        title
                        startTime
                    }
                }
            }
            """
        
            graphql_url = 'https://leetcode.com/graphql'
            headers = {
                'content-type': 'application/json',
                'Referer': 'https://leetcode.com',
            }
            
            body = {
                'query': query,
                'variables': {
                    'username': username,
                    'limit': limit
                }
            }
            
            try:
                response = requests.post(graphql_url, headers=headers, data=json.dumps(body))
                result = response.json()
                if 'errors' in result:
                    return Response({'message': result['errors'][0]['message']}, status=status.HTTP_404_NOT_FOUND)
                else:
                    #filtering
                    contest_ranking_history = result['data']['userContestRankingHistory']
                    attended_contests = [contest for contest in contest_ranking_history if contest['attended']]
                    
                    #response data
                    response_data = {
                        **result['data'],
                        'userContestRankingHistory': attended_contests  
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

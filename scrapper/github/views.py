from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import requests
from .serializers import *

class github(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            if not username:
                return Response({'status':'Failure','message':'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
            url = f'https://api.github.com/users/{username}'
            
            request=requests.get(url)
            response=request.json()
        
            if request.status_code==200:
                serializer=userserializer(data=response)
                if serializer.is_valid():
                    followers_url = serializer.data['followers_url']
                    follower_request = requests.get(followers_url)
                    followers_response = follower_request.json()
                    follower_data=data_followerserializer(data=followers_response,many=True)
                    if not follower_data.is_valid():
                        follower_data=None
                        print(f'error in follower serializer{follower_data.errors}')
                    else:
                        follower_data=follower_data.data
                    
                    repo_url = serializer.data['repos_url']
                    repo_request = requests.get(repo_url)
                    repo_response = repo_request.json()
                    repo_seralizer = reposerializer(data=repo_response,many=True)
                    if repo_seralizer.is_valid():
                        """ for repo_obj in repo_seralizer.data:
                            contributors_url=repo_obj['contributors_url']
                            if contributors_url:
                                contributors_request=requests.get(contributors_url)
                                contributors_response=contributors_request.json()
                                if contributors_request.status_code==200:
                                    contributor_data=contributorserializer(data=contributors_response,many=True)
                                    if contributor_data.is_valid():
                                        print(True)
                                        repo_obj['contributors']=contributor_data.data
                                    else:
                                        repo_obj['contributors']=None
                                else:
                                    repo_obj['contributors']=None        """
                        repo_seralizer=repo_seralizer.data
                    else:
                        print(f'error in repo serializer{repo_seralizer.errors}')  
                        repo_seralizer=None 
                        
                        
                    return Response({'status':'Success','userdata':serializer.data,'follower_data':follower_data,'repo_data': repo_seralizer},status=status.HTTP_200_OK)
                return Response({'status':'Success','data':response},status=status.HTTP_200_OK)
            else:
                return Response({'status':'Failure','message':'User not found'},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'status':'failure','message':str(e)},status=status.HTTP_400_BAD_REQUEST)
            
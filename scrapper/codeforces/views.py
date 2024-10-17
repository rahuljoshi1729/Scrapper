from django.shortcuts import render
from rest_framework import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import grequests
from .serializers import *

class codeforces(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            if not username:
                return Response({'status':'Failure','message':'Username is required'},status=status.HTTP_400_BAD_REQUEST)
            
            rating_url = f'https://codeforces.com/api/user.rating?handle={username}'
            info_url = f'https://codeforces.com/api/user.info?handles={username}&checkHistoricHandles=false'
            status_url = f'https://codeforces.com/api/user.status?handle={username}&from=1&count=1000'
            
            request=[
                grequests.get(rating_url),
                grequests.get(info_url),
                grequests.get(status_url)
            ]
            
            responses = grequests.map(request)
            
            ratingdata=responses[0].json() if responses[0].status_code==200 else None
            userdata=responses[1].json() if responses[1].status_code==200 else None
            submissiondata=responses[2].json() if responses[2].status==200 else None
            
            
        except Exception as e: 
            return Response({'status':'Failure','message':e},status=status.HTTP_400_BAD_REQUEST)    

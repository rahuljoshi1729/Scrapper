from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import requests

class github(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            if not username:
                return Response({'status':'Failure','message':'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
            url = f'https://api.github.com/users/{username}'
            
            response=requests.get(url)
            
            if response.status_code==200:
                data=response.json()
                return Response({'status':'Success','data':data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status':'failure','message':str(e)},status=status.HTTP_400_BAD_REQUEST)
            
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
import aiohttp
import asyncio
from .serializers import *
from datetime import datetime, timedelta
import requests

class codeforces(APIView):
    def post(self, request):
        try:
            username = request.data['username']
            if not username:
                return Response({'status':'Failure','message':'Username is required'}, status=status.HTTP_400_BAD_REQUEST)

            rating_url = f'https://codeforces.com/api/user.rating?handle={username}'
            info_url = f'https://codeforces.com/api/user.info?handles={username}&checkHistoricHandles=false'
            status_url = f'https://codeforces.com/api/user.status?handle={username}&from=1&count=1000'

            # Synchronous requests
            rating_response = requests.get(rating_url)
            info_response = requests.get(info_url)
            status_response = requests.get(status_url)

            if rating_response.status_code != 200 or info_response.status_code != 200 or status_response.status_code != 200:
                return Response({'status': 'Failure', 'message': 'Error fetching data from Codeforces'}, status=status.HTTP_400_BAD_REQUEST)

            rating_data = rating_response.json()
            user_data = info_response.json()
            submission_data = status_response.json()


            # Calculate 6 months ago
            now = datetime.now()
            six_months_ago = now - timedelta(days=6 * 30)

            # Filter submissions submitted after 6 months
            filtered_submissions = [
                {
                    'contestId': submission['contestId'],
                    'creationTimeSeconds': datetime.fromtimestamp(submission['creationTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')
                }
                for submission in submission_data['result']
                if datetime.fromtimestamp(submission['creationTimeSeconds']) >= six_months_ago
            ]

            submission_serializer = submissionserializer(data=filtered_submissions, many=True)
            if not submission_serializer.is_valid():
                print(submission_serializer.errors)

            return Response({
                'status': 'Success',
                'rating': rating_data,
                'user': user_data,
                'submissions': submission_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'Failure', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

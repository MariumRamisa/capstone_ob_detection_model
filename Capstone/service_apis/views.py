from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ImageInfo
from rest_framework import status
from .object_detection import detect
import os
import cv2
import uuid
import base64
import numpy as np
from datetime import datetime
from django.conf import settings
import pytz

media_path = settings.MEDIA_ROOT
localhost = settings.LOCALHOST
media_url = settings.MEDIA_URL
compression_params = [cv2.IMWRITE_JPEG_QUALITY, 50]

class InsertInfo(APIView):
    def post(self, request, *args, **kwargs):
        try:
            name = request.data.get('name')
            total_detected_objects = request.data.get('total_detected_objects')
            detected_objects = request.data.get('detected_objects')
            time = request.data.get('time')
            ImageInfo.objects.create(
                name=name,
                total_detected_objects=total_detected_objects,
                detected_objects=detected_objects,
                time=time, 
            )
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
class GetInfo(APIView):
    def get(self, request, *args, **kwargs):
        try:
            print("Function called")
            time = request.query_params.get('time')
            data = ImageInfo.objects.get(time=time)
            return Response({'name': data.name, 'total_detected_objects': data.total_detected_objects, 'detected_objects': data.detected_objects, 'time': data.time}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class GetAllInfo(APIView):
    def get(self, request, *args, **kwargs):
        message = "Data Fetched Successful"
        total = 0
        try:
            data = ImageInfo.objects.all()
            response = []
            for i in data:
                response.append({'name': str(localhost+media_url+str(i.date)+"/"+i.name), 'total_detected_object_count': i.total_detected_objects, 'detected_objects': i.detected_objects, 'time': i.time, 'date': i.date})
            total = len(response)
            return Response({
                'status': status.HTTP_200_OK,
                'message': message,
                'total': total,
                'data': response
            }, status=status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            print("Error: ", e)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'total': 0,
                'data': response
            }, status=status.HTTP_400_BAD_REQUEST)
        
class GetInfoByDateRange(APIView):
    def get(self, request, *args, **kwargs):
        message = "Data Fetched Successful"
        total = 0
        try:
            start_date = request.query_params.get('start_date')
            end_date = request.query_params.get('end_date')
            data = ImageInfo.objects.filter(date__range=[start_date, end_date])
            response = []
            for i in data:
                response.append({'name': str(localhost+media_url+str(i.date)+"/"+i.name), 'total_detected_object_count': i.total_detected_objects, 'detected_objects': i.detected_objects, 'time': i.time, 'date': i.date})
            total = len(response)
            return Response({
                'status': status.HTTP_200_OK,
                'message': message,
                'total': total,
                'data': response
            }, status=status.HTTP_200_OK)
        except Exception as e:
            message = str(e)
            print("Error: ", e)
            return Response({
                'status': status.HTTP_400_BAD_REQUEST,
                'message': message,
                'total': 0,
                'data': response
            }, status=status.HTTP_400_BAD_REQUEST)
  
class StoreDetectionResults(APIView):
    def post(self, request, *args, **kwargs):
        try:
            print("Function called")
            base64_image = request.data.get('base64_image')
            name = str(uuid.uuid4()) + '.jpg'
            image_base64_decode = base64.b64decode(base64_image)
            im_arr = np.frombuffer(image_base64_decode, dtype=np.uint8)
            image_np = cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)
            detected_objects, total_products = detect(image_np)
            current_date = datetime.now().date()
            savepath = os.path.join(media_path, str(current_date))
            os.makedirs(savepath, exist_ok=True)
            cv2.imwrite(os.path.join(savepath,name), image_np, compression_params)
            ImageInfo.objects.create(
                    name=name,
                    total_detected_objects=total_products,
                    detected_objects=detected_objects,
                    time=str(datetime.now().astimezone(pytz.timezone('Asia/Dhaka')).strftime('%H:%M:%S.%f')),
                    date = current_date
            )
            print(f"Detected objects in {detected_objects}")
            print("=====================================================")
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error: ", e)
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        




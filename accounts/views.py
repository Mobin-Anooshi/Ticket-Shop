from .serializer import UserRegisterSerializer,DriverDocumentsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from permissions import IsDriver



class UserRegisterView(APIView):
    def post(self,request,*args,**kwargs):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(ser_data.data)
        return Response(ser_data.errors)

class UserRegisterDriverView(APIView):
    def post(self,request,*args,**kwargs):
        ser_data = UserRegisterSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create_driver(ser_data.validated_data)
            return Response(ser_data.data)
        return Response(ser_data.errors)

class DriverCompleteRegister(APIView):
    permission_classes = [IsDriver,]
    def post(self,request):
        ser_data = DriverDocumentsSerializer(data=request.POST)
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data, request)
            return Response(ser_data.data)
        return Response(ser_data.errors)

class AdminRegisterView(APIView):
    pass


from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Travel,TravelDetails
from .serializer import TravelSerializer ,TravelDetailsSerializer



class HomeView(APIView):
    def get(self,request):
        return Response({'message':'Hello'})

class TravelView(APIView):
    def get(self,request):
        travels = Travel.objects.all()
        ser_data = TravelDetailsSerializer(instance=travels, many=True)
        return Response(data=ser_data.data)
    def post(self,request):
        travel_data = request.data.get('travel')
        travel_details_data = request.data.get('travel_details')

        if not travel_data and not travel_details_data :
            return Response({'message':'اطلاعات کافی نیست'})

        ser_travel_data = TravelSerializer(data=travel_data)
        if ser_travel_data.is_valid():
            travel_insrance = Travel.objects.create(
                origin=ser_travel_data['origin'],
                destination=ser_travel_data['destination'],
                departure_time=ser_travel_data['departure_time'],

            )
        else:
            return Response(ser_travel_data.errors)
        travel_details_data['travel_id'] = travel_insrance.id
        ser_travel_details_data = TravelDetailsSerializer(data=travel_details_data)
        if ser_travel_details_data.is_valid():
            ser_travel_details_data.save()
        else:
            travel_insrance.delete()
            return Response(ser_travel_details_data.errors)

        return Response ({
            'travel':ser_travel_data,
            'travel_details':ser_travel_details_data
            })



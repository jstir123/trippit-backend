from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, TripSerializer, TripPictureSerializer, TripItinerarySerializer
from .models import UserProfile, Trip, TripPicture, TripItinerary
from .permissions import IsOwnerOrReadOnly


class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=serializer.initial_data['password'])

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = []
        else:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        return [permission() for permission in permission_classes]

class AddTrip(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        trips = Trip.objects.all()
        serializer = TripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        data['user'] = request.user.id
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TripDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        trip = self.get_object(pk=pk)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        trip = self.get_object(pk=pk)
        data = request.data
        data['user'] = request.user.id
        data['location'] = trip.location
        data['lat'] = trip.lat
        data['lon'] = trip.lon
        serializer = TripSerializer(trip, data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        trip = self.get_object(pk=pk)
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ItineraryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return TripItinerary.objects.get(pk=pk)
        except TripItinerary.DoesNotExist:
            raise Http404

    def post(self, request):
        data = request.data
        serializer = TripItinerarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TripPictureView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return TripPicture.objects.get(pk=pk)
        except TripPicture.DoesNotExist:
            raise Http404

    def post(self, request):
        data = request.data
        tripId = data['tripId']
        urls = data.get('urls', [])
        pictures = []
        
        for u in urls:
            name = u.get('name', None)
            url = u.get('url', None)
            picture = {'trip': tripId, 'name': name, 'url':url}
            pictures.append(picture)

        serializer = TripPictureSerializer(data=pictures, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        item = self.get_object(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
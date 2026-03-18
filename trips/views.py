from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from trips.serializers import PlaceSerializer, PlaceUpdateSerializer, TravelProjectCreateSerializer, TravelProjectSerializer
from .models import TravelProject, Place

# Create your views here.
class TravelProjectViewSet(viewsets.ModelViewSet):
    queryset = TravelProject.objects.all()
    serializer_class = TravelProjectSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return TravelProjectCreateSerializer
        return TravelProjectSerializer
    
    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        if project.places.filter(is_visited=True).exists():
            return Response(
                {"error": "Cannot delete project with visited places."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)
    

class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = TravelProjectSerializer

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return PlaceUpdateSerializer
        return PlaceSerializer
    
    def get_queryset(self):
        return Place.objects.filter(project_id=self.kwargs['project_pk'])
    
    def perform_create(self, serializer):
        project = get_object_or_404(TravelProject, pk=self.kwargs['project_pk'])
        serializer.save(project=project)

    def perform_update(self, serializer):
        serializer.save()
        place = serializer.instance
        project = place.project
        if project.places.filter(is_visited=False).count() == 0:
            project.is_completed = True
            project.save()

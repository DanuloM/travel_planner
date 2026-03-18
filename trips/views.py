from rest_framework.exceptions import ValidationError
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
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'project_pk' in self.kwargs:
            context['project'] = get_object_or_404(TravelProject, pk=self.kwargs['project_pk'])
        return context
    
    def perform_create(self, serializer):
        project = get_object_or_404(TravelProject, pk=self.kwargs['project_pk'])
        if project.places.count() >= 10: # type: ignore
            raise ValidationError("A project cannot have more than 10 places.")
        serializer.save(project=project)

    def perform_update(self, serializer):
        serializer.save()
        place = serializer.instance
        project = place.project
        
        all_visited = project.places.filter(is_visited=False).count() == 0
        
        if all_visited and not project.is_completed:
            project.is_completed = True
            project.save()
        elif not all_visited and project.is_completed:
            project.is_completed = False
            project.save()

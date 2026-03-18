from .models import TravelProject, Place
from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']

class TravelProjectSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, read_only=True)

    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date', 'is_completed', 'places']


class TravelProjectCreateSerializer(serializers.ModelSerializer):
    places = PlaceSerializer(many=True, required=False)

    class Meta:
        model = TravelProject
        fields = ['id', 'name', 'description', 'start_date', 'places']

    def validate_places(self, value):
        if len(value) > 10:
            raise serializers.ValidationError("A project cannot have more than 10 places.")
        return value
    
    def create(self, validated_data):
        places_data = validated_data.pop('places', [])
        project = TravelProject.objects.create(**validated_data)
        for place_data in places_data:
            Place.objects.create(project=project, **place_data)
        return project
    
class PlaceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['notes', 'is_visited']

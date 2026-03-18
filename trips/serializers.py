from .models import TravelProject, Place
from .services import validate_artwork
from rest_framework import serializers

class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ['id', 'external_id', 'notes', 'is_visited']

    
    def validate_external_id(self, value):
        if not validate_artwork(value):
            raise serializers.ValidationError("Artwork not found in Art Institute API.")
        return value
    

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
            
        external_ids = [p['external_id'] for p in value]
        if len(external_ids) != len(set(external_ids)):
            raise serializers.ValidationError("Duplicate places are not allowed.")
            
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

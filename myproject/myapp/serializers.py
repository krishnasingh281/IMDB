from rest_framework import serializers
from .models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        exclude = ['watching']
        

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many = True, read_only = True)
    plaform = serializers.CharField(source= 'platform.name')
    class Meta:
        model = WatchList
        fields = '__all__'

   
class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
    watching = WatchListSerializer(many = True, read_only = True)
    class Meta:
        model = StreamPlatform
        fields = '__all__'
        

        
        
        
        

# def name_length(value):
#     if len(value)<2:
#         raise serializers.ValidationError('name should be more then 2 words! ...')

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only = True)
#     name = serializers.CharField(validators = [name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return WatchList.objects.create(**validated_data)
    
#     def update(self, instance, validate_data):
#         instance.name = validate_data.get('name', instance.name)
#         instance.description = validate_data.get('description', instance.description)
#         instance.active = validate_data.get('active', instance.active)
#         instance.save()
#         return instance
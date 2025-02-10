from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import StreamPlatform, WatchList, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
# from rest_framework.views import APIView
# from rest_framework import status, mixins
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from .permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .throttling import ReviewCreateThrottle, RewviewListThrottle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# jaisa ki hame pata ki by this way we  reduce the lenghth/line of code so it is convinient method
class WatchListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    
class WatchListDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer
    

class StreamPlatformView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    
    
    
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        # Get the primary key (movie ID) from the URL
        pk = self.kwargs.get('pk')
        watching = get_object_or_404(WatchList, pk=pk)

        # Check if the user has already reviewed this movie
        review_user = self.request.user
        review_queryset = Review.objects.filter(watching=watching, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie!')
        
        if watching.number_rating == 0:
            watching.avg_rating = serializer.validated_data['rating']
        else:
            watching.avg_rating = (watching.avg_rating + serializer.validated_data['rating'])/ 2 
            
        watching.number_rating = watching.number_rating +1
        watching.save()

        # Save the review with the associated movie and user
        serializer.save(watching=watching, review_user=review_user)
        
        # hum yaha parr kab tak ruk skte hai ?....
        
        
#generic use karke sabse simple ....
class ReviewList_1(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # throttle_classes = [RewviewListThrottle, AnonRateThrottle]
    # def get_queryset(self):
    #     pk = self.kwargs['pk']
    #     return Review.objects.filter(watching = pk)
    
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    
    
class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username = username)
    
    
class UserReview_1(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # def get_queryset(self):
        # rating = self.kwargs['rating']
        # rating = self.request.query_params.get('rating')
        # return Review.objects.filter(rating = rating)
    
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'rating', 'active']
    

class watchmovie(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['^review_user__username']
    
    
# # mixin wala hai .....
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)
    
    


    
# class WatchListAV(APIView):
#     def get(self, request):
#         movies = WatchList.objects.all()
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class MovieDetail(APIView):
#     def get(self, request, pk):
#         movie = get_object_or_404(WatchList, pk=pk)
#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         movie = get_object_or_404(WatchList, pk=pk)
#         serializer = WatchListSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         movie = get_object_or_404(WatchList, pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
        
    
# class StreamPlatfromAV(APIView):
#     def get(self, request):
#         platforms = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(platforms, many = True, context={'request': request})
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = StreamPlatformSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#            return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
       
       
# class StreamPlatfromAV_detail(APIView):
#     def get(self, request, pk):
#         movie = get_object_or_404(StreamPlatform, pk=pk)
#         serializer = StreamPlatformSerializer(movie, context={'request': request})
#         return Response(serializer.data)
    
#     def put(self, request, pk ):
#         platforms = get_object_or_404(StreamPlatform, pk =pk)
#         serializer = StreamPlatformSerializer(platforms, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         movie = get_object_or_404(StreamPlatform, pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

               
           
# #sirf APIView use karte hai isme long method 
# class ReviewsAV(APIView):
    
#     def get(self, request):
#         review = Review.objects.all()
#         serializer = ReviewSerializer(review, many = True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ReviewSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        

# class ReviewsDetailAV(APIView):
    
#     def get(self, request, pk):
#         review = get_object_or_404(Review, pk =pk)
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)
    
#     def post(self, request, pk):
#         review = get_object_or_404(Review, pk =pk)
#         serializer = ReviewSerializer(review, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     def delete(self, request, pk):
#         review = get_object_or_404(Review,pk=pk)
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
       
            







# @api_view(['GET', 'POST'])
# def movie_list(request):
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         serializer = MovieSerializer(movies, many=True)
#         return Response(serializer.data)
    
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

# @api_view(['GET', 'PUT', 'DELETE','POST'])
# def movie_detail(request, pk ):
#     if request.method == 'GET':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk = pk)
#         serializer = MovieSerializer(movie, data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'POST':
#         serializer = MovieSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
        
#     if request.method == 'DELETE':
        
#         movie = Movie.objects.get(pk = pk)
#         movie.delete()
#         return Response("hello")
        
        


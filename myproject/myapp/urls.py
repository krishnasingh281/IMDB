from django.urls import path
from . import views
urlpatterns = [
    path('', views.WatchListView.as_view(), name='movie-list'),
    path('<int:pk>', views.WatchListDetail.as_view(), name='movie-detail'),
    path('platforms/', views.StreamPlatformView.as_view(), name='streamplatform-list'),
    path('platforms/<int:pk>', views.StreamPlatformDetail.as_view(), name='streamplatform-detail'),
    # path('review/', views.ReviewList_1.as_view(), name = 'review-list'),
    # path('review/<int:pk>', views.ReviewDetail.as_view(), name = 'review-detail'),
    path('review/', views.ReviewList_1.as_view(), name = 'review-list'),
    path('platform/review/<int:pk>', views.ReviewDetail.as_view(), name = 'review-detail'),
    path('watchlist/<int:pk>/review-create', views.ReviewCreate.as_view(), name='review-create'),
    path('review/<str:username>/', views.UserReview.as_view(), name = 'user-review-detail'),
    path('movie/', views.UserReview_1.as_view(), name = 'user-review-detail'),
    path('moviee/', views.watchmovie.as_view(), name = 'movie-dekho'),
]

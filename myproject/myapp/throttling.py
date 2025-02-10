from rest_framework.throttling import UserRateThrottle

class ReviewCreateThrottle(UserRateThrottle):
    scope = 'review-create'
    
class RewviewListThrottle(UserRateThrottle):
    scope = 'review-list'
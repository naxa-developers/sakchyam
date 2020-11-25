from dashboard.models import UserProfile

def message_processor(request):
    if request.user.is_authenticated:
        id = request.user.id
        test = UserProfile.objects.filter(user=request.user)
    else:
        test = None
    return {
        'thumbnaildata': test
    }

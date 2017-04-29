from .models import UserProfile
from .forms import UserRegForm
from registration.signals import user_registered

def create_profile(sender, user, request, **kwargs):
    form = UserRegForm(request.POST)
    data = UserProfile(user=user)
    data.address = form.data['address']
    data.city = form.data['city']
    data.state = form.data['state']
    data.country = form.data['country']
    data.interests = form.data['interests']
    data.save()

user_registered.connect(create_profile, sender=UserProfile)
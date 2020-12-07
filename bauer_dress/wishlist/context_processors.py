from .models import Wishlist
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

def wishlist(request):
	if request.user.is_authenticated:
		try:
			wishlist = Wishlist.objects.get(user=request.user)
		except ObjectDoesNotExist:
			wishlist = Wishlist.objects.create(user=request.user)

		return {'wishlist': wishlist}
	else:
		return {'wishlist': None}
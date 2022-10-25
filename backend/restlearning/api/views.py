from rest_framework.response import Response
import json
from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer


@api_view(["POST"])
def api_home(request, *args, **kwargs):

	serializer = ProductSerializer(data=request.data)
	if serializer.is_valid(raise_exception=True):
		# data = serializer.save()
		print(serializer.data)
		return Response(serializer.data)
	return Response({"invalid": "not good data"}, status=400)

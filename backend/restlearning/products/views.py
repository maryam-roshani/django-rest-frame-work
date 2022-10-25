from rest_framework import authentication, generics, mixins, permissions
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .permissions import IsStaffEditorPermission
from api.authentication import TokenAuthentication

class ProductListCreateApiView(generics.ListCreateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	authentication_classes = [
		authentication.SessionAuthentication,
		TokenAuthentication
	]
	permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

	
	def perform_create(self, serializer):
		print(serializer.validated_data)
		title = serializer.validated_data.get('title')
		content = serializer.validated_data.get('content') or None
		if content is None:
			content = title
		serializer.save(content=content)


product_list_create_view = ProductListCreateApiView.as_view()



class ProductUpdateApiView(generics.UpdateAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	permission_classes = [permissions.DjangoModelPermissions]
	lookup_field = 'pk'

	def perform_update(self, serializer):
		instance = serializer.save()

product_update_view = ProductUpdateApiView.as_view()



class ProductDestroyApiView(generics.DestroyAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

	def perform_destroy(self, instance):
		super().perform_destroy(instance)

product_delete_view = ProductDestroyApiView.as_view()


	
class ProductDetailApiView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer


product_detail_view = ProductDetailApiView.as_view()



class ProductMixinView(
	mixins.CreateModelMixin,
	mixins.ListModelMixin,
	mixins.RetrieveModelMixin,
	generics.GenericAPIView
	):
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	lookup_field = 'pk'

	def get(self, request, *args, **kwargs):
		print(args, kwargs)
		pk = kwargs.get('pk')
		if pk is not None:
			return self.retrieve(request, *args, **kwargs)
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

	def perform_create(self, serializer):
		print(serializer.validated_data)
		title = serializer.validated_data.get('title')
		content = serializer.validated_data.get('content') or None
		if content is None:
			content = "thats very very cool!"
		serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()




@api_view(["POST", "GET"])
def product_alt_view(request, pk=None, *args, **kwargs):
	method = request.method

	if method == "GET":
		if pk is not None:
			# detail view
			obj = get_object_or_404(Product, pk=pk)
			data = ProductSerializer(obj, many=False).data 
			return Response(data)
		# list view
		queryset = Product.objects.all()
		data = ProductSerializer(queryset, many=True).data
		return Response(data)
	if method == "POST":
		# create an item
		serializer = ProductSerializer(data=request.data)
		if serializer.is_valid(raise_exception=True):
			title = serializer.validated_data.get('title')
			content = serializer.validated_data.get('content') or None
			if content is None:
				content = title
			serializer.save(content=content)
			return Response(serializer.data)
	return Response({"invalid": "not good data"}, status=400)



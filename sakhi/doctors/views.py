from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from .serializers import GetAllDocsSerializer, DoctorsCategorySerializer
from .models import DoctorCategory, Doctors

class GetCategories(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = DoctorsCategorySerializer
    queryset = DoctorCategory.objects.all()
     
class GetDoctors(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = GetAllDocsSerializer

    def get_queryset(self):
        c = self.request.query_params.get('location', None)
        category = self.request.query_params.get('category', None)
        queryset = Doctors.objects.all()

        if c:
            c_lower = c.lower()
            queryset = queryset.filter(city__iexact=c_lower)

            if not queryset.exists():
                return Doctors.objects.none()

        if category:
            try:
                category_instance = DoctorCategory.objects.get(name=category)
                queryset = queryset.filter(category=category_instance)
            except DoctorCategory.DoesNotExist:
                return Doctors.objects.none()

        return queryset.order_by('-rating')

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'message': 'Data fetched successfully!',
                'data': serializer.data,
                'status': 200,
                'status_text': 'ok'
            }, status=200)
        except Exception as e:
            return Response({
                'message': 'Error!',
                'error': str(e),
                'status': 400,
                'status_text': 'error'
            }, status=400)


class GetDoc(generics.RetrieveAPIView):
    permission_class = [AllowAny]
    serializer_class = GetAllDocsSerializer
    queryset = Doctors.objects.all()
    lookup_field = 'pk'
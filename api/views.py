from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import ContactSerializer
from .models import Contact


class IdentityView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = []

    def post(self, request):
        ...
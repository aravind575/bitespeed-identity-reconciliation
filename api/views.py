from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import ContactSerializer, ContactListSerializer
from .models import Contact


class IdentityView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = []

    def post(self, request):
        email = request.data.get('email', None)
        phoneNumber = request.data.get('phoneNumber', None)

        if email is None and phoneNumber is None:
            return Response({
                "message": "Please provide either an email or a phone number."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # pass the data to serializer which saves to db following given constraints
        entry = ContactSerializer(data={
            "phoneNumber": phoneNumber,
            "email": email
        })
        entry.is_valid()
        entry.save()

        contactData = ContactListSerializer(entry).data

        return Response({
            "contact": contactData
        }, status=status.HTTP_201_CREATED)


        
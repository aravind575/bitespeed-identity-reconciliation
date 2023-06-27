from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status, serializers

from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiExample, OpenApiResponse, OpenApiParameter

from .serializers import ContactSerializer, ContactListSerializer
from .models import Contact


class IdentityView(APIView):
    permission_classes = [AllowAny]
    # authentication_classes = []

    @extend_schema(
    request=inline_serializer(
        name="requestIdentitySerializer",
        fields={
            "email": serializers.CharField(default="aravindsridhar575@gmail.com"),
            "phone": serializers.CharField(default="7030102822"),
        }
    ),
    responses={201: OpenApiResponse(
        response=inline_serializer(
            name="responseIdentitySerializer",
            fields={
                "contact": serializers.DictField(default={
                    "primaryContatctId": 7,
			        "emails": [],
			        "phoneNumbers": [],
                    "secondaryContactIds": []
                })
            }
        )
    )})

    def post(self, request):
        email = request.data.get('email', None)
        phoneNumber = request.data.get('phoneNumber', None)

        if email is None and phoneNumber is None:
            return Response({
                "message": "Please provide either an email or a phone number."
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # pass the data to serializer which saves to db following given constraints
        db_operation = ContactSerializer(data={
            "phoneNumber": phoneNumber,
            "email": email,
        })
        db_operation.is_valid(raise_exception=True)
        entry = db_operation.save()

        # generate response data
        contactData = ContactListSerializer(entry).data

        return Response({
            "contact": contactData
        }, status=status.HTTP_201_CREATED)


        
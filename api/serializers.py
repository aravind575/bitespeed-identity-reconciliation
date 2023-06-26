from rest_framework import serializers
import serpy

from django.db.models import Q

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

    def create(self, validated_data):
        phone_number = validated_data.get('phoneNumber')
        email = validated_data.get('email')

        if Contact.objects.filter(phoneNumber=phone_number, email=email).exists():
            return None
        
        pMatch = Contact.objects.filter(phoneNumber=phone_number).order_by('-createdAt').first() if phone_number else None
        eMatch = Contact.objects.filter(email=email).order_by('-createdAt').first() if phone_number else None

        if pMatch and eMatch:
            if pMatch.linkPrecedence == eMatch.linkPrecedence == 'primary':
                target, other = pMatch, eMatch if pMatch.createdAt < eMatch.createdAt else eMatch, pMatch
                other.linkedId = target.id
                other.linkPrecedence = 'secondary'
                other.save(update_fields=['linkedId', 'linkedPrecedence'])
                return None
        
        target = pMatch if pMatch else eMatch

        validated_data['linkedId'] = target.id
        validated_data['linkedPrecedence'] = 'secondary'

        return super().create(validated_data)


class ContactListSerializer(serpy.Serializer):
    ll_query = serpy.MethodField()
    primaryContactId = serpy.MethodField()
    emails = serpy.MethodField()
    phoneNumbers = serpy.MethodField()
    secondaryContactIds = serpy.MethodField()

    def get_query(self, obj):
        linkedList = []
        node = obj
        
        while node.linkedPrecedence != 'primary':
            linkedList.append(node)
            node = Contact.objects.get(id=node.linkedId)
        
        linkedList.append(node)
        return linkedList
    
    def get_ll_query(self, obj):
        return self.get_query(obj)

    def get_primaryContactId(self, obj):
        primary_contact = self.ll_query[-1]
        return primary_contact.id

    def get_emails(self, obj):
        emails = set()
        for q in self.ll_query:
            email = q.email
            emails.add(email)
        return list(emails)

    def get_phoneNumbers(self, obj):
        phoneNumbers = set()
        for q in self.ll_query:
            phoneNumber = q.phoneNumber
            phoneNumbers.add(phoneNumber)
        return list(phoneNumber)

    def get_secondaryContactIds(self, obj):
        secondaryIds = []
        for q in self.ll_query:
            secondaryIds.append(q.id)
        secondaryIds.remove(self.primaryContactId)
        return secondaryIds
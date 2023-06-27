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

        exact_match = Contact.objects.filter(phoneNumber=phone_number, email=email).first()
        if exact_match:
            return exact_match
        
        pMatch = Contact.objects.filter(phoneNumber=phone_number).order_by('-createdAt').first() if phone_number else None
        eMatch = Contact.objects.filter(email=email).order_by('-createdAt').first() if phone_number else None

        if pMatch is None and eMatch is None:
            return super().create(validated_data)

        if pMatch and eMatch:
            if pMatch.linkPrecedence == eMatch.linkPrecedence == 'primary':
                target, other = (pMatch, eMatch) if pMatch.createdAt < eMatch.createdAt else (eMatch, pMatch)
                other.linkedId = target.id
                other.linkPrecedence = 'secondary'
                other.save(update_fields=['linkedId', 'linkPrecedence'])
                return other
            return pMatch
        
        target = pMatch if pMatch else eMatch
        print(pMatch, eMatch, target)

        validated_data['linkedId'] = target.id
        validated_data['linkPrecedence'] = 'secondary'

        return super().create(validated_data)


class ContactListSerializer(serpy.Serializer):
    primaryContactId = serpy.MethodField()
    emails = serpy.MethodField()
    phoneNumbers = serpy.MethodField()
    secondaryContactIds = serpy.MethodField()

    def get_primaryContactId(self, obj):
        node = obj
        while node.linkPrecedence != 'primary':
            node = Contact.objects.get(id=node.linkedId)
        return node.id

    def get_emails(self, obj):
        emails = set()

        if not hasattr(self, 'primaryContactId'):
            self.primaryContactId = self.get_primaryContactId(obj)
        
        emails.add(Contact.objects.get(id=self.primaryContactId).email)

        down_nodes = Contact.objects.filter(linkedId=self.primaryContactId)
        while down_nodes.first():
            nxt = []
            for nde in down_nodes:
                emails.add(nde.email)
                nxt.append(nde.id)
            down_nodes = Contact.objects.filter(linkedId__in=nxt)

        return list(emails)

    def get_phoneNumbers(self, obj):
        phones = set()

        phones.add(Contact.objects.get(id=self.primaryContactId).phoneNumber)

        down_nodes = Contact.objects.filter(linkedId=self.primaryContactId)
        while down_nodes.first():
            nxt = []
            for nde in down_nodes:
                phones.add(nde.phoneNumber)
                nxt.append(nde.id)
            down_nodes = Contact.objects.filter(linkedId__in=nxt)

        return list(phones)


    def get_secondaryContactIds(self, obj):
        contacts = []

        down_nodes = Contact.objects.filter(linkedId=self.primaryContactId)
        while down_nodes.first():
            nxt = []
            for nde in down_nodes:
                nxt.append(nde.id)
            contacts += nxt
            down_nodes = Contact.objects.filter(linkedId__in=nxt)

        return contacts
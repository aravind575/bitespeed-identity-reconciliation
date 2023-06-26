from django.db import models


class Contact(models.Model):
    phoneNumber = models.CharField(max_length=10, null=True)
    email = models.EmailField(max_length=254, null=True)
    linkedId = models.BigIntegerField(null=True)
    linkPrecedence = models.CharField(max_length=10, choices=[("secondary", "Secondary"), ("primary", "Primary")])
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.linkPrecedence} Contact - {self.id}"

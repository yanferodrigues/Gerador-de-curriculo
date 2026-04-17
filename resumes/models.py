import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Resume(models.Model):
    id         = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    name       = models.CharField(max_length=100, default='Sem título')
    template   = models.CharField(max_length=30, default='executive')
    data       = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f'{self.name} ({self.user.username})'

    def to_dict(self):
        return {
            'id':         str(self.id),
            'name':       self.name,
            'template':   self.template,
            'data':       self.data,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }

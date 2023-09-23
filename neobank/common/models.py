from django.db import models
from django.db.models.query import F, Q
from django.utils import timezone

from simple_history.models import HistoricalRecords

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    history = HistoricalRecords(inherit=True)
    
    class Meta:
        abstract = True

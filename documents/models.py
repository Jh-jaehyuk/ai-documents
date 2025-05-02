from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models

# Create your models here.
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    s3_key = models.CharField(max_length=512)
    extracted_text = models.TextField(blank=True, null=True)
    # Asynchronize test
    summary = models.TextField(blank=True, null=True)
    keywords = ArrayField(models.CharField(max_length=100), default=list)
    recommended_documents = models.ManyToManyField('self',blank=True, symmetrical=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pk}번째 문서\n소유자: {self.user.username}\n파일명: {self.title}"

    class Meta:
        db_table = "documents"
        verbose_name = "문서"
        verbose_name_plural = "문서 목록"

from django.urls import path

from documents.views import upload_document, success_upload_document

urlpatterns = [
    path('upload/', upload_document, name='upload_document'),
    path('upload-success/', success_upload_document, name='document_success'),
]
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from documents.forms import DocumentForm
from documents.models import Document
from documents.s3_utils import upload_file_to_s3, download_file_from_s3

from documents.tasks import summarize_and_recommend


# Create your views here.
@login_required(login_url=settings.LOGIN_REDIRECT_URL)
def upload_document(request):
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES)

        if form.is_valid():
            file = request.FILES['file']
            title = form.cleaned_data['file'].name
            s3_key = f"document/{request.user.id}/{file.name}"

            upload_file_to_s3(file, s3_key)

            s3_file = download_file_from_s3(s3_key)

            text_content = s3_file.read().decode('utf-8')

            document = Document.objects.create(
                user=request.user,
                title=title,
                s3_key=s3_key,
                extracted_text=text_content
            )

            # 비동기 처리 요청 >> 문서 요약 및 비슷한 문서 찾기
            summarize_and_recommend.delay(document.id)

            return redirect('document_success')

    else:
        form = DocumentForm()

    return render(request, 'documents/upload.html', {'form': form})

def success_upload_document(request):
    return render(request, 'documents/success.html')

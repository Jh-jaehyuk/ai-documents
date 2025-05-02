from celery import shared_task
from django.db.models import Q

from documents.llm_utils import summarize_with_ollama, extract_keywords
from documents.models import Document


@shared_task
def summarize_and_recommend(document_id):
    doc = Document.objects.get(pk=document_id)

    # 1. 문서 요약(Ollama 이용)
    summary = summarize_with_ollama(doc.extracted_text)
    doc.summary = summary

    # 2. 키워드 추출
    keywords = extract_keywords(summary)
    doc.keywords = keywords
    doc.save()

    q = Q()
    for kw in keywords:
        q |= Q(keywords__icontains=kw)

    similar_docs = Document.objects.filter(q).exclude(pk=doc.id)[:3]
    doc.recommended_documents.set(similar_docs)
    doc.save()

    return {"message": "The requested operation has been successfully completed."}
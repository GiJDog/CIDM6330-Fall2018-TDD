from django.shortcuts import redirect, render
from applicationforms.models import ApplicationFormItem, ApplicationForm

def home_page(request):
    return render(request, 'home.html')

def view_applicationform(request, applicationform_id):
    applicationform_ = ApplicationForm.objects.get(id=applicationform_id)
    return render(request, 'applicationform.html', {'applicationform': applicationform_})

def new_applicationform(request):
    applicationform_ = ApplicationForm.objects.create()
    ApplicationFormItem.objects.create(text=request.POST['item_text'], applicationform=applicationform_)
    return redirect(f'/applicationforms/{applicationform_.id}/')

def add_item(request, applicationform_id):
    applicationform_ = ApplicationForm.objects.get(id=applicationform_id)
    ApplicationFormItem.objects.create(text=request.POST['item_text'], applicationform=applicationform_)
    return redirect(f'/applicationforms/{applicationform_.id}/')
# Create your models here testd.
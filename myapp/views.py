import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import FieldError
from django.shortcuts import redirect
from django.shortcuts import render

from myapp.registry_class import ModelsRegistryHolder
from myapp.services import add_classes_to_server

'''def person(request):
    template = "person_upload.html"

    if request.method =="POST":
        form = PersonForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = PersonForm()
    context = {
        'form': form,
    }
    return render(request,template,context)

def person_detail(request):
    template = "person_upload.html"

    if request.method =="POST":
        form = Person_detailForm(request.POST)

        if form.is_valid():
            form.save()
    else:
        form = Person_detailForm()
    context = {
        'form': form,
    }
    return render(request,template,context)'''


@permission_required('admin.can_add_log_entry')
def person_upload(request):
    template = "person_upload.html"

    prompt = {

    }
    if request.method == "GET":
        return render(request, template, prompt)
    csv_file = request.FILES.get('file')
    if not csv_file:
        messages.error(request, "Please attach a csv file")
        return redirect('/upload-csv/')
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not csv file')
        return redirect('/upload-csv/')
    add_classes_to_server()
    model = ModelsRegistryHolder().get(request.POST.get('model'))
    if not model:
        messages.error(request, f"Specified model not found {request.POST.get('model')}")
        return redirect('/upload-csv/')

    try:
        model.execute(csv_file)
    except Exception as e:
        messages.error(request, f"Exception Occured - {e}")
        return redirect('/upload-csv/')
    context = {}
    return render(request, template, context)

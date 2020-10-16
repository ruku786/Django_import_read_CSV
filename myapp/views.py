import csv
import io

from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import FieldError
from django.shortcuts import redirect
from django.shortcuts import render

from myapp.registry_class import ModelsRegistryHolder

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
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    model = ModelsRegistryHolder().get(request.POST.get('model'))
    if not model:
        messages.error(request, f"Specified model not found {request.POST.get('model')}")
        return redirect('/upload-csv/')

    data_list = [{k: v for k, v in x.items()}
                 for x in
                 csv.DictReader(io_string, delimiter=',', quotechar="|", skipinitialspace=True)]
    try:
        for row in data_list:
            _, created = model.objects.update_or_create(**row)
    except FieldError as e:
        exc = str(e).split('.')[1]
        messages.error(request,
                       f"Invalid headers in csv for model {request.POST.get('model')}, {exc}")
    context = {}
    return render(request, template, context)

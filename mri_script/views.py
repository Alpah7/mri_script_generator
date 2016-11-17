from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from .forms import ScriptForm
from .models import Choice, Question
import csv
import fileinput
import os

def index(request):
    if request.method == 'GET':
        form = ScriptForm()
    else:
        # A POST request: Handle Form Upload
        form = ScriptForm(request.POST) # Bind data from request.POST into a PostForm

        # If data is valid, proceeds to create a new post and redirect the user
        if form.is_valid():
            wordReplacements = {
                'numsub': str(form.cleaned_data['number_of_subjects']),
                'numscan': str(form.cleaned_data['number_of_scans_per_subject']),
                'numrun': str(form.cleaned_data['number_of_runs_per_scan']),
                'slice': str(form.cleaned_data['number_of_slices_in_functional_scan']),
                'numtr': str(form.cleaned_data['number_of_trs_in_a_run']),
                'lengthtr': str(form.cleaned_data['tr_length'])
            }
            
            content = open(GenerateScript(wordReplacements))
            #return HttpResponse(content, content_type='text/plain')
            response = HttpResponse(content, content_type='text/x-script.sh')
            response['Content-Disposition'] = 'attachment; filename="MRIScript.sh"'
            JavaTest()
            
            return response
            
    context = {'form': form}
    return render(request, 'mri_script/index.html', context)


def JavaTest():
    return HttpResponse("<script>ShowHiddenText();</script>")

def help(request):
    context = {}
    return render(request, 'mri_script/help.html', context)

def contact(request):
    context = {}
    return render(request, 'mri_script/contact.html', context)

def GenerateScript(wordReplacements):
    settings_dir = os.path.dirname(__file__)
    PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
    input_path = PROJECT_ROOT + "/mri_script/static/mri_script/preprocess.sh"
    output_path = PROJECT_ROOT + "/mri_script/static/mri_script/output.sh"

    with open(output_path, "w") as output_file, open(input_path) as input_file:
        for line in input_file:
            output_file.write(transform_line(wordReplacements, line))
    
    return output_path

def transform_line(wordReplacements, line):
    for key, value in wordReplacements.items():
        line = line.replace(key, value)
    return line

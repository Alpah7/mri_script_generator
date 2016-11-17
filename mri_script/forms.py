from django import forms

from .models import Script

class ScriptForm(forms.Form):
    number_of_subjects = forms.IntegerField(label='Number of Subjects', required=True)
    number_of_scans_per_subject = forms.IntegerField(label='Number of Scans per Subject', required=True)
    number_of_runs_per_scan = forms.IntegerField(label='Number of Runs per Scan', required=True)
    number_of_slices_in_functional_scan = forms.IntegerField(label='Number of Slices in Functional Scan', required=True)
    tr_length = forms.IntegerField(label='TR Length', required=True)
    number_of_trs_in_a_run = forms.IntegerField(label='Number of TRs in a Run', required=True)
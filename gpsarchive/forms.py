from django import forms
from .models import  gpxfile, gpxtrack
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import User

class UploadGpxForm(forms.ModelForm):

    title = forms.CharField(max_length=100)
    description = forms.CharField(max_length=200)
    #callsign = forms.CharField( max_length=100)
    date = forms.DateTimeField(initial=timezone.now )
    gpx_file = forms.FileField(required='FALSE')
    #author = forms.ForeignKey(User)
    class Meta:
        model = gpxfile
        fields = ['title','description','date', 'gpx_file']



    #def clean_gpx_file(self):
     #   uploaded_file = self.cleaned_data['gpx_file']
      #  print(uploaded_file.content_type)

#        content_type = uploaded_file.content_type
 #       allowed_content_types = ['text/xml', 'application/octet-stream', 'application/gpx+xml']
  #      if content_type in allowed_content_types:
   #         if uploaded_file.size > 2621440:
    #            raise forms.ValidationError(_('Please keep filesize under 2.5 MB. Current filesize %s') % (filesizeformat(uploaded_file._size)))
        
     #   else:
      #      raise forms.ValidationError(_('Filetype not supported.'))

        #return uploaded_file 




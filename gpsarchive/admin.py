#from django.contrib.gis.admin import OSMGeoAdmin
#from django.contrib.gis import admin as geoadmin
from django.contrib import admin
from .models import   gpxfile, gpxtrack, gpxcompare

#@admin.register(Spot)
#class SpotAdmin(OSMGeoAdmin):
 #   list_display = ('name', 'location')

#geoadmin.site.register(GPoint, geoadmin.OSMGeoAdmin)
#geoadmin.site.register(GTrack, geoadmin.OSMGeoAdmin)
admin.site.register(gpxfile)  
admin.site.register(gpxtrack)
admin.site.register(gpxcompare)    

# Register your models here.

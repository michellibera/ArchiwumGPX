from django.shortcuts import render, redirect
from .forms import UploadGpxForm
from .models import  gpxfile,  gpxtrack, gpxcompare
from django.http import HttpResponseRedirect
#from django.contrib.gis.geos import Point, LineString, MultiLineString
from django.conf import settings
from django.views.generic import  TemplateView, ListView, CreateView, DetailView, DeleteView
#from django.core.files.storage import default_storage
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

import gpxpy
import gpxpy.gpx
import folium
import pandas as pd



def home(request):
    #context = {
        #'notes': Note.objects.all()
    #}
    return render(request, 'gpsarchive/home.html')




def upload_success(request):
    return render(request, 'gpsarchive/success.html')


def file_list(request):
  files = gpxfile.objects.all()
  return render(request, 'gpsarchive/file_list.html', {'files':files})




def gpxupload(request):
  if request.method == 'POST':
      file_instance = gpxtrack()
      form = UploadGpxForm(request.POST, request.FILES)
      if form.is_valid():
          form.save()
          #SaveGPXtoPostGIS(request.FILES['gpx_file'], file_instance)
          return redirect('success')
  else:
      form = UploadGpxForm()
  return render(request, 'gpsarchive/form.html', {'form':form})




# views for track

class TrackCreateView(LoginRequiredMixin, CreateView):
    model = gpxtrack
    template_name = 'gpsarchive/newtrack.html'
    fields = ['title', 'description', 'date', 'gpx_file']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TrackListView(ListView):
    model = gpxtrack
    template_name = 'gpsarchive/track_list.html' # <app>/<model>_<view_type>.html
    context_object_name = 'gpxtrack'
    ordering = ['-date']

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-date')



class TrackDetailView(UserPassesTestMixin, DetailView):
    model = gpxtrack

    def get_context_data(self, **kwargs):

        #fname = '3359239_S6cTWEY.gpx'

        obj = gpxtrack.objects.get(pk=self.kwargs.get('pk'))
        fname = obj.gpx_file.name

        if obj.author == self.request.user:

        
          gpx = gpxpy.parse(open(settings.MEDIA_ROOT+'/'+fname)) 
          #gpx = gpxpy.parse(open(settings.MEDIA_ROOT+'/gpxstorage'+'/'+fname))



          if gpx.tracks:
            track_list_of_points = [] 
            for track in gpx.tracks:
                  for segment in track.segments:                
                      for point in segment.points:
                          #point_in_segment = Point(point.longitude, point.latitude)
                          track_list_of_points.append(tuple([point.latitude, point.longitude]))     #(point_in_segment.coords)

                  #new_track_segment = LineString(track_list_of_points)
              
              #new_track.track = MultiLineString(new_track_segment)
              


          lat_middle,lon_middle=track_list_of_points[int(len(track_list_of_points) / 2)]
          lat_end,lon_end=track_list_of_points[-1]
          lat_start,lon_start=track_list_of_points[1]

          figure = folium.Figure()
          m = folium.Map(

              location=[lat_middle, lon_middle],
              zoom_start=12,
              tiles='Stamen Terrain'
          )
          m.add_to(figure)


          folium.PolyLine(
            track_list_of_points,
            color='red',
            weight=4.5,
            opacity=.5
          ).add_to(m)

          html_camino_start = """Start of day"""
          popup = folium.Popup(html_camino_start, max_width=400)
          #nice green circle
          folium.vector_layers.CircleMarker(
          location=[lat_start, lon_start], 
          radius=9, 
          color='white', 
          weight=1, 
          fill_color='green', 
          fill_opacity=1, 
          popup=html_camino_start
          ).add_to(m)

          #OVERLAY triangle
          folium.RegularPolygonMarker(
          location=[lat_start, lon_start], 
          fill_color='white', 
          fill_opacity=1, 
          color='white', 
          number_of_sides=3, 
          radius=3, 
          rotation=0, 
          popup=html_camino_start
          ).add_to(m)



          folium.Marker(
              location=[45.3288, -121.6625],
              popup='Mt. Hood Meadows',
              icon=folium.Icon(icon='cloud')
          ).add_to(m)

          
          figure.render()
          return {"map": figure}

    def test_func(self):
        gpxtrack = self.get_object()
        if self.request.user == gpxtrack.author:
            return True
        return False

class TrackDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = gpxtrack
    success_url = reverse_lazy('track-list')
    def test_func(self):
        gpxtrack = self.get_object()
        if self.request.user == gpxtrack.author:
            return True
        return False


#views for compare


class CompareCreateView(LoginRequiredMixin, CreateView):
    model = gpxcompare
    template_name = 'gpsarchive/newcompare.html'
    fields = ['title', 'description', 'date', 'gpx_file_track', 'gpx_file_route']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class CompareListView(ListView):
    model = gpxcompare
    template_name = 'gpsarchive/gpxcompare_list.html' # <app>/<model>_<view_type>.html
    context_object_name = 'gpxcompare'
    ordering = ['-date']

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user).order_by('-date')



class CompareDetailView(UserPassesTestMixin, DetailView):
    model = gpxcompare

    def get_context_data(self, **kwargs):

        

        obj = gpxcompare.objects.get(pk=self.kwargs.get('pk'))
        fname1 = obj.gpx_file_track.name
        fname2 = obj.gpx_file_route.name

        if obj.author == self.request.user:

        
          gpx_t = gpxpy.parse(open(settings.MEDIA_ROOT+'/'+fname1)) 
          gpx_r = gpxpy.parse(open(settings.MEDIA_ROOT+'/'+fname2)) 
          



          if gpx_t.tracks:
            track_list_of_points = [] 
            for track in gpx_t.tracks:
                  for segment in track.segments:                
                      for point in segment.points:
                          #point_in_segment = Point(point.longitude, point.latitude)
                          track_list_of_points.append(tuple([point.latitude, point.longitude]))     #(point_in_segment.coords)
          elif gpx_t.routes:
            track_list_of_points = []
            for route in gpx_t.routes:
                  for point in route.points:
                    track_list_of_points.append(tuple([point.latitude, point.longitude]))


                  #new_track_segment = LineString(track_list_of_points)
              
              #new_track.track = MultiLineString(new_track_segment)
              

          if gpx_r.tracks:
            route_list_of_points = [] 
            for track in gpx_r.tracks:
                  for segment in track.segments:                
                      for point in segment.points:
                          #point_in_segment = Point(point.longitude, point.latitude)
                          route_list_of_points.append(tuple([point.latitude, point.longitude]))
          elif gpx_r.routes:
            route_list_of_points = []
            for route in gpx_r.routes:
                  for point in route.points:
                    route_list_of_points.append(tuple([point.latitude, point.longitude]))
        


          lat_middle,lon_middle=track_list_of_points[int(len(track_list_of_points) / 2)]
          lat_end,lon_end=track_list_of_points[-1]
          lat_start,lon_start=track_list_of_points[1]

          figure = folium.Figure()
          m = folium.Map(

              location=[lat_middle, lon_middle],
              zoom_start=12,
              tiles='Stamen Terrain'
          )
          m.add_to(figure)


          folium.PolyLine(
            track_list_of_points,
            color='red',
            weight=4.5,
            opacity=.5
          ).add_to(m)

          folium.PolyLine(
            route_list_of_points,
            color='green',
            weight=4.5,
            opacity=.5
          ).add_to(m)

          html_camino_start = """Start of day"""
          popup = folium.Popup(html_camino_start, max_width=400)
          #nice green circle
          folium.vector_layers.CircleMarker(
          location=[lat_start, lon_start], 
          radius=9, 
          color='white', 
          weight=1, 
          fill_color='green', 
          fill_opacity=1, 
          popup=html_camino_start
          ).add_to(m)

          #OVERLAY triangle
          folium.RegularPolygonMarker(
          location=[lat_start, lon_start], 
          fill_color='white', 
          fill_opacity=1, 
          color='white', 
          number_of_sides=3, 
          radius=3, 
          rotation=0, 
          popup=html_camino_start
          ).add_to(m)



          folium.Marker(
              location=[45.3288, -121.6625],
              popup='Mt. Hood Meadows',
              icon=folium.Icon(icon='cloud')
          ).add_to(m)

          
          figure.render()
          return {"map": figure}
    def test_func(self):
        gpxcompare = self.get_object()
        if self.request.user == gpxcompare.author:
            return True
        return False


class CompareDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = gpxcompare
    success_url = reverse_lazy('compare-list')
    def test_func(self):
        gpxcompare = self.get_object()
        if self.request.user == gpxcompare.author:
            return True
        return False

# Create your views here.

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadForm
from django.http import HttpResponse
import gpxpy
import matplotlib
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

def file_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # ファイルの処理
            handle_upload_file(request.FILES['file'])
            request.FILES['file'] = None
            # file_obj = request.FILES['file']
            return HttpResponseRedirect('/')
    else:
        form = UploadForm()
    return render(request, 'file_upload/upload.html',{'form': form})

def handle_upload_file(file_obj):
    file_path = 'media/gpx/' + file_obj.name 
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            destination.write(chunk)
    x = []
    y = []
    gpx_file = open('media/gpx/' + file_obj.name, 'r')
    gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                x.append(point.latitude)
                y.append(point.longitude)
    plt.plot(x,y,linewidth = 3.0, color="white")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.gca().invert_xaxis()
    plt.savefig('media/png/'+'test.png', transparent=True)

    os.remove(file_path)

def file_download(request):
    file_path = 'media/png/test.png'
    response = HttpResponse(open(file_path, 'rb').read(), content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename="test.png"'
    return response


from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadForm
from django.http import HttpResponse
import gpxpy
import matplotlib
import re
import environ
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
from logging import getLogger, StreamHandler, DEBUG

#環境変数読み込み
env = environ.Env()
env.read_env('.env')

#ロガー
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)
logger.propagate = False

def file_upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            if re.search(r".gpx", request.FILES['file'].name):
                # ファイルの処理
                logger.debug(request.FILES)
                handle_upload_file(request.FILES['file'])
                # request.FILES['file'] = None
                return file_download(request)
            else:
                return render(request, 'file_upload/upload.html',{'form': form, 'error_msg': 'ファイルの拡張子がgpxではありません。'})
    else:
        logger.debug('get /')
        form = UploadForm()
        request.FILES['file']=None
    return render(request, 'file_upload/upload.html',{'form': form})

def handle_upload_file(file_obj):
    file_path = 'media/gpx/' + file_obj.name 
    with open(file_path, 'wb+') as destination:
        for chunk in file_obj.chunks():
            logger.debug('chunk')
            destination.write(chunk)

    x = []
    y = []
    gpx_file = open('media/gpx/' + file_obj.name, 'r')
    gpx = gpxpy.parse(gpx_file)
    gpx_file.close()

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                x.append(point.latitude)
                y.append(point.longitude)
    plt.figure()
    plt.plot(x,y,linewidth = 2.0, color="white")
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().axes.xaxis.set_visible(False)
    plt.gca().axes.yaxis.set_visible(False)
    plt.gca().invert_xaxis()

    png_filename = re.sub(r".gpx",'',file_obj.name)
    plt.savefig('media/png/'+png_filename+'.png', transparent=True)

    # gpxファイルが溜まっていくのでアップロードされたgpxファイルは削除する
    os.remove(file_path)

def file_download(request):
    # form = UploadForm()
    # file_path = 'media/png/test.png'
    download_filename = re.sub(r".gpx",'',request.FILES['file'].name)+'.png'
    download_path = env('DOMAIN_URL') + 'media/png/' + download_filename
    # response = HttpResponse(open(file_path, 'rb').read(), content_type='image/png')
    # response['Content-Disposition'] = 'attachment; filename="test.png"'
    # return response
    # return render(request, 'file_upload/upload.html',{'form': form, 'download_path': download_path})
    return render(request, 'file_upload/download.html',{'download_filename': download_filename, 'download_path': download_path})

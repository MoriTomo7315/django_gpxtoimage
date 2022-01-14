from fileinput import close
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.shortcuts import render
from .forms import UploadForm
from django.http import HttpResponse
import gpxpy
import matplotlib
import re
import urllib.parse
#バックエンドを指定
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import io
from logging import getLogger, StreamHandler, DEBUG

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
                file_obj = request.FILES['file']
                # buf = handle_upload_file(file_obj)
                file_path_and_name = 'media/gpx/' + file_obj.name
                with open(file_path_and_name, 'wb+') as destination:
                    for chunk in file_obj.chunks():
                        logger.debug('chunk')
                        destination.write(chunk)

                x = []
                y = []
                gpx_file = open(file_path_and_name, 'r')
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

                buf = io.BytesIO()
                plt.savefig(buf, format="png",transparent=True)

                os.remove(file_path_and_name)
                response = HttpResponse(buf.getvalue(), content_type="image/png")
                buf.close()

                download_filename = re.sub(r".gpx",'',file_obj.name)+'.png'
                response['Content-Disposition'] = 'attachment; filename='+download_filename
                return response
            else:
                return render(request, 'file_upload/upload.html',{'form': form, 'error_msg': 'ファイルの拡張子がgpxではありません。'})
    else:
        logger.debug('get /')
        form = UploadForm()
        request.FILES['file']=None
    return render(request, 'file_upload/upload.html',{'form': form})
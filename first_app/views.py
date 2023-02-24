from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt, csrf_protect
import cv2
import pytesseract
import os
from pathlib import Path
from django.http import JsonResponse
import json
# Create your views here.

def index(request):
    myObj = {'insert_me' : "Hello I am from views.py !!!"}
    return render(request, 'index.html', context=myObj)

# def index(request):
#     return HttpResponse("Hello World!")

@csrf_exempt
def upload_docs(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file']
            print(uploaded_file.name)
            fs = FileSystemStorage()
            if fs.exists(uploaded_file.name) == False:
                fs.save(uploaded_file.name, uploaded_file)

                currentPath = Path(__file__).resolve().parent.parent
                filePath = os.path.join(currentPath, "media")
                filePath = os.path.join(filePath, uploaded_file.name)

                img_cv = cv2.imread(filePath)
                img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
                textFromImage = pytesseract.image_to_string(img_rgb)
                
                fs.delete(uploaded_file.name) # delete image immedietly

                response_data = {}
                response_data['test'] = textFromImage
                return HttpResponse(json.dumps(response_data), content_type="application/json")
                # return HttpResponse(textFromImage)
        except KeyError:
            return HttpResponse("Request has no resource file attached")
    return HttpResponse('Oops something went wrong :(')
    

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        # print(uploaded_file.name)
        # print(uploaded_file.size)
        # uploaded_file.name = 'test.png'
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'upload.html')

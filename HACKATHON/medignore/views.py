from django.shortcuts import render
from decouple import config
import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
from xml.etree import ElementTree

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View

from .forms import PhotoForm
from .models import Photo

import time
import cv2
import json
import requests
import sys
import re

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 100

def search(request):
    return render(request, 'medignore/search.html')


def result(request):
    param = request.GET.get('param') # search.html 에서 GET으로 받은 쿼리들 밑에 넣어줘야함
    # param이 보험코드면 1. 품목 목록에서 이름 뽑아오고 2. 이름으로 임부 주의사항 뽑기
    import openpyxl
 
    # 엑셀파일 열기
    wb = openpyxl.load_workbook('product_detail.xlsx')
    
    # 현재 Active Sheet 얻기
    ws = wb.active
    # ws = wb.get_sheet_by_name("Sheet1")
    
    # 국영수 점수를 읽기
    for r in ws.rows:
        row_index = r[0].row   # 행 인덱스
        kor = r[1].value
        eng = r[2].value
        math = r[3].value
        sum = kor + eng + math
    
        # 합계 쓰기
        ws.cell(row=row_index, column=5).value = sum
    
        print(kor, eng, math, sum)
    
    # 엑셀 파일 저장
    wb.save("score2.xlsx")
    wb.close()
    
    return render(request, 'medignore/result.html',{'param':data})

def main(request):
    return render(request, 'medignore/main.html')


def test(request):
    kakao_key = config('KAKAO_KEY')
    if request.method == 'POST':
       
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
            image= './'+photo.file.url
            print(f'image url : {image}')
            key = kakao_key
            output = practice(image, key)
            resultOutput =output['result']['recognition_words']
            regex =re.compile('\d{9}')
            for item in resultOutput:
                mo = regex.search(item)
                if mo != None:
                    print(mo.group()) 
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:     
        photos_list = Photo.objects.all()
        return render(request, 'medignore/drag_and_drop_upload.html', {'photos': photos_list})

def kakao_ocr_resize(image_path: str):
 
    image = cv2.imread(image_path)
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape

        image_path = "{}_resized.jpg".format(image_path)
        cv2.imwrite(image_path, image)

        return image_path
    return None


def kakao_ocr_detect(image_path: str, appkey: str):

    API_URL = 'https://kapi.kakao.com/v1/vision/text/detect'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"file": data})


def kakao_ocr_recognize(image_path: str, boxes: list, appkey: str):
 
    API_URL = 'https://kapi.kakao.com/v1/vision/text/recognize'

    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

    image = cv2.imread(image_path)
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()

    return requests.post(API_URL, headers=headers, files={"file": data}, data={"boxes": json.dumps(boxes)})


def practice(a, b):
    image_path, appkey = a, b
    resize_impath = kakao_ocr_resize(image_path)
    if resize_impath is not None:
        image_path = resize_impath
        print("원본 대신 리사이즈된 이미지를 사용합니다.")

    output = kakao_ocr_detect(image_path, appkey).json()
    print("[detect] output:\n{}\n".format(output))

    boxes = output["result"]["boxes"]
    boxes = boxes[:min(len(boxes), LIMIT_BOX)]
    output = kakao_ocr_recognize(image_path, boxes, appkey).json()
    return output
 

def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))


# def result(request):
#     return render(request, 'medignore/result.html')
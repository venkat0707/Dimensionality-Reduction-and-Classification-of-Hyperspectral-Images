from django.shortcuts import render
import requests
import sys
import os
import time
from subprocess import run,PIPE
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.staticfiles import finders
from main.settings import ALGO_FOLDER



def button(request):
    return render(request,'home.html')

def external(request):
    no_of_samples= request.POST.get('param')
    technique=request.POST['technique']

    image=request.FILES['ima']
    print("Dataset:-",image)
    fs=FileSystemStorage()
    filename=fs.save(image.name,image)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    print(f'Number of Components:- {no_of_samples}')
    if (technique=="1"):print("Technique:- Principle Component Analysis")
    else:print("Technique:- Incremental Principle Component Analysis")
    print("File_Name:-",filename)
   # print("Full_Path:-", fileurl)
    print("Templete_Path:-",templateurl)
    start = time.time()
    image= run([sys.executable,ALGO_FOLDER+'algo.py',str(fileurl),str(filename),str(no_of_samples),str(technique)],shell=False,stdout=PIPE)
    print(image.stdout)
    end = time.time()
    print(end-start)
    
    f1 = open(ALGO_FOLDER+'size1.txt', 'r')
    f2 = open(ALGO_FOLDER+'size2.txt', 'r')
    file_content1 = f1.read()
    file_content2 = f2.read()
  
   
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':image.stdout,'file_content1': file_content1,'file_content2': file_content2})
    

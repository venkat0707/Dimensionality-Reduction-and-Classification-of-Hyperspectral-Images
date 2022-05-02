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
    #getting number of components from the user
    no_of_samples= request.POST.get('param')
    #dimensionality reduction technique(PCA/IPCA)
    technique=request.POST['technique']
    #accessing the hypespectral dataset name
    image=request.FILES['ima']
    print("Dataset:-",image)
    fs=FileSystemStorage()
    #saving the hyperspectral dataset to the file storage (media file)
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
    #executing algo.py to get the resulted outputs(file name,number of samples,type of dimensionality reduction technique)
    image= run([sys.executable,ALGO_FOLDER+'algo.py',str(fileurl),str(filename),str(no_of_samples),str(technique)],shell=False,stdout=PIPE)
    print(image.stdout)
    end = time.time()
    print(end-start)
    # size1.txt file containes shape of the hypespectral dataset before the dimensionality recution  
    f1 = open(ALGO_FOLDER+'size1.txt', 'r')
    file_content1 = f1.read()
    # size2.txt file containes shape of the hypespectral dataset after the dimensionality recution  
    f2 = open(ALGO_FOLDER+'size2.txt', 'r')
    file_content2 = f2.read()
  
   
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':image.stdout,'file_content1': file_content1,'file_content2': file_content2})
    

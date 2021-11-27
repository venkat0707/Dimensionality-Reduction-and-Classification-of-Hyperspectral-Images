from django.shortcuts import render
import requests
import sys
from subprocess import run,PIPE
from django.core.files.storage import FileSystemStorage

def button(request):
    return render(request,'home.html')

def external(request):
    image=request.FILES['ima']
    print("Dataset:-",image)
    fs=FileSystemStorage()
    filename=fs.save(image.name,image)
    fileurl=fs.open(filename)
    templateurl=fs.url(filename)
    print("File_Name:-",filename)
    print("Full_Path:-", fileurl)
    print("Templete_Path:-",templateurl)
    image= run([sys.executable,'//home//venky//algo.py',str(fileurl),str(filename)],shell=False,stdout=PIPE)
    print(image.stdout)
    return render(request,'home.html',{'raw_url':templateurl,'edit_url':image.stdout})
    

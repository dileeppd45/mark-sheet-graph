import csv

from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from django.db import connection
from django.contrib import messages
from django.core.files.storage import FileSystemStorage


from . import views
import pandas as pd
import sys
import matplotlib
matplotlib.use('Agg')
from django.shortcuts import render
import matplotlib.pyplot as plt
import numpy as np
import io
import base64









def add_marksheet(request):
    if request.method == "POST":
        f = request.FILES['file']
        df = pd.read_csv(f)
        print(df)
        l = []
        n = []
        p = []
        for index, row in df.iterrows():
            print(index)
            name = row["name"]
            mark = row["mark"]
            percent = (int(mark)/100)*100
            l.append(name)
            n.append(mark)
            p.append(percent)
            print(name)
            print(mark)
        s= int(0)
        for i in l:
            s = s+1

        cursor = connection.cursor()
        cursor.execute("select * from marksheet")
        data = cursor.fetchone()
        if data == None:
            for i in range(s):
                cursor.execute("insert into marksheet values(null,'"+str(l[i])+"','"+str(n[i])+"','"+str(p[i])+"','1')")
        else:
            cursor.execute("select marksheetid from marksheet")
            ma = []
            id = cursor.fetchall()
            id = list(id)
            for i in id:
                q = int(i[0])
                ma.append(q)
            maxv = max(ma)
            k = int(maxv)+1
            for i in range(s):
                cursor.execute("insert into marksheet values(null,'"+str(l[i])+"','"+str(n[i])+"','"+str(p[i])+"','"+str(k)+"')")
            # print(f"Name: {name}, mark: {mark}")
        return render(request,'add_sheet.html')
    else:
        return render(request,'add_sheet.html')

def view_sheets(request):
    cursor = connection.cursor()
    cursor.execute("select marksheetid from marksheet")
    data = cursor.fetchall()
    print(data)
    print('hello')
    data = set(data)
    data =list(data)
    l = []
    for i in data:
        m = int(i[0])
        print(i[0])
        l.append(m)
    l = list(l)
    l = sorted(l)
    print(l)
    h = int(0)
    for i in l:
        h=h+1

    m = {}
    m = set(m)
    for i in range(h):
        s = (l[i])
        m.add(s)
    print(m)
    m= sorted(m)

    return render(request,'view_marksheets.html',{'data':m})

def view_pychart(request,id):
    cursor = connection.cursor()
    cursor.execute("select * from marksheet where marksheetid ='"+str(id)+"' ")
    data = cursor.fetchall()
    sata = list(data)
    print(sata)
    data = []
    labels=[]
    for i in sata:
        data.append(float(i[3]))
        labels.append(str(i[1])+' mark: '+str(i[2]))
    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    # ax.legend()

    # Save the plot as an image in a BytesIO buffer.
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convert the buffer data to a base64 string.
    chart_image = base64.b64encode(buffer.read()).decode('utf-8')
    return render(request, 'line_chart.html',{'chart_image': chart_image})

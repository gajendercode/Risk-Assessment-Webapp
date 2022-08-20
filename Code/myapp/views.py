from django.http.response import HttpResponse
from django.shortcuts import render,HttpResponse
from django.http import HttpResponse
import requests
import cve
import json
import pandas as pd
from collections import Counter
# Create your views here.

des=[]
context={}
def index(request):
	return render(request, 'Index.html')

def home(request):
	return render(request, 'Home.html')

def team(request):
	return render(request, 'Team.html')
    
def assets(request):
    return render(request,'test.html')




def vulnerabilities(request):
    assetname=request.POST.get('assetname')
    df=cve.search('','2018',assetname)
    vulnerability=df.sort_values(['baseScore','CVE_ID'],ascending=False)[:5].reset_index().to_json(orient ='records')
    # df=pd.read_csv('/home/akku/Desktop/cs_631A_project/practise1/myapp/cve.csv')
    # vulnerability=df.sort_values(['baseScore','CVE_ID'],ascending=False)[:5].reset_index().to_json(orient ='records')
    data = []
    data = json.loads(vulnerability)
    print(type(data))
    # global des
    # des=list(vulnerability['Description'])
    global context
    context = {'d': data}
    context['asset']=assetname
    #context.add('d',data)
    
  
    return render(request, 'api_test.html', context)
    
def show_vul_list(request):
    return render(request,'show_vul_list.html',context)

 
# def threats(request):
#         questions=None
#         if request.GET.get('search'):
#             search = request.GET.get('search')
#             questions = Queries.objects.filter(query__icontains=search)

#             name = request.GET.get('name')
#             query = Queries.object.create(query=search, user_id=name)
#             query.save()

#         return render(request, 'basicapp/index.html',{
#             'questions': questions,
#         })

def Threats_input(request):
    #threat=request.POST('productTable')
    return render(request,'Threats_input.html')

def threats(request):
    threat1=request.POST.get('threat1')
    threat2=request.POST.get('threat2')
    threat3=request.POST.get('threat3')
    threat4=request.POST.get('threat4')
    threat_list=[threat1,threat2,threat3,threat4]
    global context
    context['t']=threat_list
    return render(request,'tableForm.html',context)

def consequence_threat(request):
    return render(request,'consequence_matrix.html',context)

def tableForm(request):
    income=request.POST.getlist('income')
    reputation=request.POST.getlist('reputation')
    business=request.POST.getlist('business')
    
    total_income=[]
    total_reputation=[]
    total_business=[]
    global context
    for i in range(0,20,4):
        each_row = income[i:i+4]
        count_dict = dict(Counter(each_row))
        max_key = max(count_dict, key=count_dict.get)
        total_income.append(max_key)
        
    # print(total_income)
    context['total_income']= total_income

    for i in range(0,20,4):
        each_row = reputation[i:i+4]
        count_dict = dict(Counter(each_row))
        max_key = max(count_dict, key=count_dict.get)
        total_reputation.append(max_key)
        
    # print(total_reputation)
    context['total_reputation']= total_reputation

    for i in range(0,20,4):
        each_row = business[i:i+4]
        count_dict = dict(Counter(each_row))
        max_key = max(count_dict, key=count_dict.get)
        total_business.append(max_key)
        
    # print(total_business)
    context['total_business']= total_business
    for i in range(0,5):
        context['d'][i]['total_income'] = total_income[i]
        context['d'][i]['total_reputation'] = total_reputation[i]
        context['d'][i]['total_business'] = total_business[i]
    
    return render(request,'consequence_matrix.html',context)

def find_overall(total,c):
    overall = []
    for i in range(len(total)):
        if (total[i] == 'high' and c == 'high') or (total[i] == 'high' and c == 'medium') or (total[i] == 'medium' and c == 'high'):
            overall.append('high')
            continue
        elif (total[i] == 'medium' and c == 'medium') or (total[i] == 'high' and c == 'low') or (total[i] == 'low' and c == 'high'):
            overall.append('medium')
            continue
        else:
            overall.append('low')

    return overall
def max_fun(a,b,c):
    high=0
    medium=0
    low=0
    
    if(a=='high'):
        high+=1
    elif(a=='medium'):
        medium+=1
    else:
        low+=1
        
    if(b=='high'):
        high+=1
    elif(b=='medium'):
        medium+=1
    else:
        low+=1
        
    if(c=='high'):
        high+=1
    elif(c=='medium'):
        medium+=1
    else:
        low+=1
    

    if(medium>=high) and (medium>=low):

        return 'MEDIUM'

    elif(high>=medium) and (high>=low):

        return 'HIGH'

    else:

        return 'LOW'
    # return l
def funccc(like,cons):
    c=''
    if(cons=="HIGH" and like=='HIGH'):
        c='HIGH'
    elif(cons=="HIGH" and like=='MEDIUM'):
        c='HIGH'
    elif(cons=="HIGH" and like=='LOW'):
        c='MEDIUM'
    elif(cons=="MEDIUM" and like=='HIGH'):
        c='HIGH'
    elif(cons=="MEDIUM" and like=='MEDIUM'):
        c='MEDIUM'
    elif(cons=="MEDIUM" and like=='LOW'):
        c='LOW'
    elif(cons=="LOW" and like=='HIGH'):
        c='MEDIUM'
    elif(cons=="LOW" and like=='MEDIUM'):
        c='LOW'
    elif(cons=="LOW" and like=='LOW'):
        c='LOW'
    return c
def consequence_matrix(request):
    global context
    income_c=request.POST.get('income')
    reputation_c=request.POST.get('reputation')
    business_c=request.POST.get('business')
    context['income_c']=income_c
    context['reputation_c']=reputation_c
    context[' business_c']= business_c
    
    
    overall_income = find_overall(context['total_income'],income_c)
    overall_reputation = find_overall(context['total_reputation'],reputation_c)
    overall_business = find_overall(context['total_business'],business_c)
    
    final_final=[] 
    
    for i in range(0,5):
        final_final.append(max_fun(overall_income[i],overall_reputation[i],overall_business[i]))
        
    

    for i in range(0,5):
        context['d'][i]['overall_income'] = overall_income[i]
        context['d'][i]['overall_reputation'] =overall_reputation[i]
        context['d'][i]['overall_business'] = overall_business[i]
        context['d'][i]['final'] = final_final[i]
        
    return render(request,'final_risk_matrix.html',context)
   
    
    
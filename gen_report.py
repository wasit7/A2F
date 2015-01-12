#!/usr/bin/python
#-*-coding: utf-8 -*-
"""
Created on Tue Jan 06 16:29:22 2015

@author: Wasit
"""

import numpy as np
import pandas as pd
#boundary T score
#boundary=[50, 55, 60, 70, 80, 85, 90]
boundary=[40, 45, 50, 60, 70, 80, 85]
gtext=['F','D','D+','C','C+','B','B+','A']
gnum={'F':0.0,'D':1.0,'D+':1.5,'C':2.0,'C+':2.5,'B':3.0,'B+':3.5,'A':4.0}
bin_width=1
offset=70
def Weight2T(x,mu,sigma):
    return (x-mu)/sigma*10+offset
def T2Weight(t,mu,sigma):
    return (t-offset)*sigma/10+mu
def grade(scores, breakpoints=boundary, 
          grades=gtext):
    num_grades=gnum
    from bisect import bisect
    g=[]
    sumg=0.0
    for s in scores:
         i= bisect(breakpoints, s)
         g.append(grades[i])
         sumg=sumg+num_grades[grades[i]]
    return (g,sumg/len(scores)) 


if __name__ == "__main__":
    import os
    src_name=''
    for root, dirs, files in os.walk('./'):
        for f in files:
            print f
            if f.startswith('mark') and (f.endswith('xlsx') or f.endswith('xlsx')):
                src_name=f
    
    #ID    Name   Subtask-Maxmark-Weight ...
    exf = pd.ExcelFile(src_name,encoding='utf-8')
    df_raw= exf.parse( exf.sheet_names[-1] )
    headers=df_raw.columns
    #dict of series
    dict_mark={}
    dict_mark['_score']=np.zeros(df_raw.shape[0])
    for i,name in enumerate(headers):
        print name
        if i<=1:
            col_name=name
        else:
            smw=name.split('-')
            col_name=smw[0]+':%s,[%s]'%(smw[1],smw[2])
            maxmark=smw[1]
            weight=smw[2]
            #compute weighted score
            inc=float(weight)*df_raw[name].astype('float')/float(maxmark)
            dict_mark['_score']=dict_mark['_score']+inc
        dict_mark[col_name]=df_raw[name]
    df_mark= pd.DataFrame(dict_mark)

    
    
    ## 1. save the output weighted score
    mu=np.mean(df_mark['_score'])
    sigma=np.std(df_mark['_score'])    
    num_students=df_mark.shape[0]
    if(num_students<10):
        df_mark['T_score']=df_mark['_score']
    else:
        df_mark['T_score']=Weight2T( df_mark['_score'],mu,sigma)
    g,gbar=grade(df_mark['T_score'])
    df_mark['Grade']=g
    
    
    ## 2. histrogram
    from matplotlib import pyplot as plt
    import matplotlib.mlab as mlab
    plt.close('all')
    
    
    fig, ax1 = plt.subplots()
    n, bins, patches=ax1.hist(df_mark['_score'].astype('int'),
             bins=np.arange(0,100,bin_width),
            facecolor='green',edgecolor = "darkgreen", alpha=0.5)
    ax1.hold(True)
    ax1.set_ylabel('Histogram', color='g')
    yup=1.5    
    ypos=np.max(n)*yup
    ax1.axis([30, 100, 0, ypos])
    for i in xrange(len(boundary)) :
        if(num_students<10):
            wscore= boundary[i]
        else:
            wscore=T2Weight(boundary[i],mu,sigma)
        
        t=ax1.text(wscore-0.5,ypos-0.2,'%s $\leq\,%.1f$'%(gtext[i],wscore),rotation=90,fontsize=10)
        t.set_bbox(dict(color='red', edgecolor='red'))
        ax1.axvline(wscore, linewidth=1, color='r', alpha=0.5,linestyle='dashed')
    if(num_students<10):
        ax1.text(boundary[-1]+5,ypos/2,'A',fontsize=14)
        ax1.text(boundary[0]-5,ypos/2,'F',fontsize=14)
    else:
        ax1.text(T2Weight(boundary[-1]+5,mu,sigma),ypos/2,'A',fontsize=14)
        ax1.text(T2Weight(boundary[0]-5,mu,sigma),ypos/2,'F',fontsize=14)
    
    ax2=ax1.twinx()
    #ax2.axis([30, 100, 0, 1.0])
    ax2.axis(xmin=30,xmax=100)
    x=np.arange(30,100,1)
    y = mlab.normpdf(x, mu, sigma)
    ax2.plot(x, y, 'r')
    ax2.set_ylabel('Probability', color='r')
    ax1.set_xlabel('weigthed score [100]')
    plt.grid(True)
    plt.title('%s, mean grade: %.2f\n$\mu=%.3f,\, \sigma=%.3f$'%(src_name,gbar,mu,sigma))
    plt.show()

#save graph
    from matplotlib.backends.backend_pdf import PdfPages
    pp = PdfPages('out.pdf')
    plt.savefig(pp, format='pdf')
    pp.savefig()
    pp.close()
#save grade boundary
    text_boundary=[]
    final_boundary=[]
    text_Tboundary=[]
    if(num_students<10):#fixed
        final_boundary=boundary
    else:
        final_boundary=[]
        for i in xrange(len(boundary)):
            final_boundary.append(T2Weight(boundary[i],mu,sigma))
    
    for i in xrange(len(boundary)-1):
        text_Tboundary.append("%.3f < %-2s <= %.3f"%(boundary[i],gtext[i+1],boundary[i+1]))
        text_boundary.append("%.3f < %-2s <= %.3f"%(final_boundary[i],gtext[i+1],final_boundary[i+1]))
    
    text_Tboundary.insert(0,"%06.3f < %-2s <= %.3f"%(0.0,gtext[0],boundary[0]))
    text_Tboundary.append("%.3f < %-2s <= %.3f"%(boundary[-1],gtext[-1],100.0))
    
    text_boundary.insert(0,"%06.3f < %-2s <= %.3f"%(0.0,gtext[0],final_boundary[0]))
    text_boundary.append("%.3f < %-2s <= %.3f"%(final_boundary[-1],gtext[-1],100.0))
    
    dict_grade={'Grade':gtext,'ScoreBoundary':text_boundary,'TScoreBoundary':text_Tboundary}
    df_grade= pd.DataFrame(dict_grade)
    df_grade=df_grade.sort(['ScoreBoundary'],ascending=False)
    #save
    from pandas import ExcelWriter
    wt = ExcelWriter('out.xlsx')
    #sort by id
    df_mark=df_mark.sort(['ID'])
    df_mark.to_excel(wt,'mark',index=False)
    df_grade.to_excel(wt,'_boundary',index=False)
    wt.save()
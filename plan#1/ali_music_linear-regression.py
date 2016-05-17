#coding:utf-8
'''
输入：songs.csv & user_actions.csv
输出：#.txt（某个歌手在未来某天的歌曲收听量）
'''


import datetime
import time
from sklearn import linear_model

def artist_songs(song_file):#生成歌手歌曲字典及歌手列表
    f=open(song_file,'r')
    art_songs={}
    for line in f.readlines():
        data=line.strip('\n').split(',')
        try:
            art_songs[data[1]]=art_songs[data[1]]+','+data[0]
        except:
            art_songs[data[1]]=data[0]
    artist=[]
    for a in art_songs:
        artist.append(a)
    return art_songs,artist

def position(art_songs,artist,s):#判断歌曲s的位置
    for i in range(len(artist)):
        if s in art_songs[artist[i]]:
            songs=art_songs[artist[i]].split(',')
            s_index=[i,songs.index(s)]
        else:
            pass
    return s_index

def artist_list(art_songs,artist,actionfile):#生成歌手每首歌各每天的统计表
    art_list=[]
    for i in range(len(artist)):
        n=len(art_songs[artist[i]].split(','))#每个歌手有几首歌
        m=(datetime.datetime(2015,8,30)-datetime.datetime(2015,3,1)).days+1#数据一共有多少天
        art_list.append([[0 for ii in range(m)]for jj in range(n)])#初始化
    f=open(actionfile,'r')
    flag=0
    while flag==0:
        line=f.readline()
        if line=='':
            flag=1
        else:
            data=line.strip('\n').split(',')
            s_index=position(art_songs,artist,data[1])
            ptime=time.localtime(int(data[2]))
            t=(datetime.datetime(ptime[0],ptime[1],ptime[2])-datetime.datetime(2015,3,1)).days#此行数据时间对应的统计表位置
            art_list[s_index[0]][s_index[1]][t]=art_list[s_index[0]][s_index[1]][t]+1
    return art_list

def predict_model(art_list,artist,saveaddr):#预测模型——线性回归，用前一天的数据预测后一天的数据（一元线性回归）
    artist_predict=[]
    for i in range(len(art_list)):
        song_value=[]
        for j in range(len(art_list[i])):
            x=[];y=[]
            for k in range(len(art_list[i][j])-1):
                x.append([art_list[i][j][k]])
                y.append(art_list[i][j][k+1])
            regr=linear_model.LinearRegression()
            regr.fit(x,y)
            value=[]
            v=float(art_list[i][j][-1])
            for inx in range(60):#往后预测多少天
                v=regr.predict(v)[0]
                value.append(v)
            song_value.append(value)
        artist_predict.append(map(sum,zip(*song_value)))
    f=open(saveaddr,'w')
    for jnx in range(len(artist_predict)):
        for znx in range(len(artist_predict[jnx])):
            time_value=datetime.datetime(2015,8,31)+datetime.timedelta(days=znx+1)
            year=str(time_value.year)
            if len(str(time_value.month))==1:
                month='0'+str(time_value.month)
            else:
                month=str(time_value.month)
            if len(str(time_value.day))==1:
                day='0'+str(time_value.day)
            else:
                day=str(time_value.day)
            t=year+month+day
            f.write(artist[jnx]+','+str(int(artist_predict[jnx][znx]))+','+t+'\n')
    f.close()
    
    
    
    
            
art_songs,artist=artist_songs('D:\\ali_music\\songs.csv')
art_list=artist_list(art_songs,artist,'D:\\ali_music\\user_actions.csv')
predict_model(art_list,artist,'D:\\out.txt')        
        
        

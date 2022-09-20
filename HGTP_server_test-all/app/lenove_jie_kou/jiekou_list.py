# -*- coding: utf-8 -*-
__author__ = 'SUNZHEN519'
#根据列表执行运行文件
from tempfile import mktemp
from app import app
from flask import send_from_directory,send_file,Response
import socket
import os
import time
import sqlite3
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask import current_app
from flask import Flask, render_template, session, redirect, url_for, flash,jsonify
import json
import demjson
from functools import wraps
import sys
from app.sql_chemy.example_db import *
sys.path.append(r'C:\exec\jie_kou_test')
#不是自动打开的页面，可以查看调试信息
def jiekou_list_show(func):
  def jiekou_list_showee():
      func()
      if request.method == 'GET':
              yewu_name=''
              select_huanjing=''
              huanjing=''
              huanjing_list=''
              select_huanjing=''
              re_all_mulu=''
              gen_mulu=''
      return render_template('/hualala/pages/jiekou_list.html', yewu_name=yewu_name,select_huanjing=select_huanjing,
                                 huanjing=huanjing_list,all_mulu=re_all_mulu,gen_mulu=gen_mulu
                                 )
  return jiekou_list_showee
def jiekou_result_run(func):
    def result_run():
        func()
        if request.method=="POST":
            all_url=[]
            ip=request.headers.get('X-Real-IP')
            huanjing = [os.path.join(current_app.config.get('JIE_KOU_URL'), i.decode('gb2312')) for i in
                        os.listdir(current_app.config.get('JIE_KOU_URL'))
                        if i.strip() != '' and 'git' not in i]
            if 'jie_kou_huan_jing' in list(session.keys()):
                pass
            else:
                session['jie_kou_huan_jing'] = huanjing[0]
            url=session['jie_kou_huan_jing']
            all_req=[z.split('#')  for z in request.form['ame'].split(',') if z.strip()!='']
            for i in all_req:
                             all_url.append(os.path.join(os.path.join(url, i[0]),i[1]))
            print(all_url)
            all_run.run(all_url, r'C:\work\lenove_jie_kou',ip)
            error='1'
            """
            try:
                all_run.run(all_url, r'C:\work\lenove_jie_kou')
            except Exception,e:
                error=e
                """
            return jsonify(a=str(error))
    return result_run
#脚本输入测试信息
import chardet
def jiaobenshuru(func):
 def zz():
    if request.method=='POST':
       ip=request.headers.get('X-Real-IP')
       current_app.config[request.headers.get('X-Real-IP')+'last_change']=request.form
       name = request.form['name']
       data=request.form['shuru']+'##'+request.form['shuchu']
       g.cu.execute('UPDATE jie_kou_test SET name=?,data=? WHERE num=? and ip=?',
                     (name, data,'run',request.headers.get('X-Real-IP')))
       g.db.commit()
       return jsonify(da=1)
 return zz
#接口url 插入数据库
def url_insert(func):
    def hk():
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        if request.method=='GET':
            mulu=request.args.get('mulu')
            if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?',(request.headers.get('X-Real-IP'),request.args.get('statu'))).fetchall())>0:
                cu.execute('update jiekou_mulu set mulu=?,update_time=? where ip=? and statu=?',(request.args.get('mulu'),str(time.time()),request.headers.get('X-Real-IP'),request.args.get('statu')))
            else:
              cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?,"1")',
                           [(request.args.get('statu'), request.args.get('mulu'),request.headers.get('X-Real-IP'), str(time.time()))])
        else:
                mulu=os.path.join(request.form['gen_mulu'],request.form['huanjing'],request.form['mulu'].split('#')[0],request.form['mulu'].split('#')[1])
                if len(cu.execute('select * from jiekou_mulu where ip=? and statu=?',
                                  (request.headers.get('X-Real-IP'), request.form['statu'])).fetchall()) > 0:
                    cu.execute('update jiekou_mulu set mulu=?,update_time=? where ip=? and statu=?', (
                    mulu, str(time.time()), request.headers.get('X-Real-IP'), request.form['statu']))
                else:
                    cu.executemany('INSERT INTO jiekou_mulu VALUES (null,?,?,?,?,"1")',
                                   [(request.args.get('statu'), mulu, request.headers.get('X-Real-IP'),
                                     str(time.time()))])
        db.commit()
        db.close()
        #调用本地server把目录请求发送
        # url = 'http://' + request.headers.get('X-Real-IP') + ':'+current_app.config.get('LOCAL_SERVER_PORT')+'/jiankong_mulu'
        # print(url)
        # test_data = {'mulu': mulu.replace('\\','/')}
        # # test_data_urlencode = urllib.parse.urlencode(test_data)
        # # req = urllib.request.Request(url=url, data=test_data_urlencode)
        # # res_data = json.loads(urllib.request.urlopen(req).read())
        # res_data= json.loads(requests.post(url,test_data).text)
        session['调试']=request.args.get('mulu')
        return jsonify(statu="success")
    return hk
#本地server 获取要监控的目录地址
def get_mulua(func):
    @wraps(func)
    def hk():
        if '调试' in session:
            mulu=session['调试']
        else:
            db = sqlite3.connect(current_app.config.get('JIE_KOU'))
            cu = db.cursor()
            mulu=cu.execute('select mulu from jiekou_mulu where ip=? and statu=?',(request.headers.get('X-Real-IP'),request.form['statu'])).fetchall()
            db.close()
        return jsonify(mulu=mulu)
    return hk
#返回调试首页
def shishitiaoshi(func):
    @wraps(func)
    def aa():
                    #判断是否是获取的别的地址的server
                    if 'yidi_mulu_ip' in list(session.keys()) and session['yidi_mulu_ip']!='127.0.0.1' and session['yidi_mulu_ip']!=request.headers.get('X-Real-IP'):
                              yidi_ip='1'
                    else:
                        yidi_ip='q'
                    try :
                        current_app.config[request.headers.get('X-Real-IP') + 'last_change']
                    except:
                        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
                        cu = db.cursor()
                        data=cu.execute('select * from jie_kou_test where num=? and ip=?',("run",request.headers.get('X-Real-IP'))).fetchall()
                        if len(data)>0:
                            case_name = 'none'
                            shuru = 'none'
                            shuchu = 'none'
                            jiekou_name = 'none'
                            result_statu = 'none'
                        else:
                            case_name = 'none'
                            shuru = 'none'
                            shuchu = 'none'
                            jiekou_name = 'none'
                            result_statu = 'none'
                    else:
                        data=current_app.config[request.headers.get('X-Real-IP')+'last_change']
                        case_name=data['comment']
                        shuru=json.dumps(json.loads(json.dumps(demjson.decode(data['shuru'])), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
                        shuchu=json.dumps(json.loads(json.dumps(demjson.decode(data['shuchu'])), parse_int=int), indent=4, sort_keys=False,
                                   ensure_ascii=False)
                        jiekou_name=data['name']
                        result_statu='none'
                    if request.method == "GET":
                         if 'yidi_mulu_ip' not in list(session.keys()):
                             return redirect(url_for('uplate_jiekou_list'))
                         port=current_app.config.get('LOCAL_SERVER_PORT')
                         return render_template('/hualala/pages/shishitiaoshi.html',port=port,yidi_mulu_ip=session['yidi_mulu_ip'].strip(),yidi_ip=yidi_ip,case_name=case_name,shuru=shuru,shuchu=shuchu,jiekou_name=jiekou_name,result_statu=result_statu)
                    else:
                        if 'request_url' not in list(data.keys()):
                            request_url = ""
                        else:
                            request_url = data['request_url']
                        return jsonify(case_name=case_name,shuru=shuru,shuchu=shuchu,jiekou_name=jiekou_name,result_statu=result_statu,request_url=request_url)
    return aa
#批量运行接口
import requests
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
def piliang_run(func):
    @wraps(func)
    def ceshipi():
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        if 'local_today_pic' in list(current_app.config.keys()):
            current_app.config.pop('local_today_pic')
        if 'local_seven_pic' in list(current_app.config.keys()):
            current_app.config.pop('local_seven_pic')
        if 'local_seven_pic' not  in list(current_app.config.keys()):
            print((77777777777777777777777777777777777777777777))
        session['run_time'] = str(time.time())
        ip_dizhi=request.form['ip_dizhi']
        #print  request.form['all_jiekou_re']
        ip = request.headers.get('X-Real-IP')
        all_mulu=json.loads(request.form['all_jiekou_re'])['all_mulu']
        for k,i in enumerate(all_mulu):
            if request.headers.get('X-Real-IP') + 'all_url' in session:
                gen_mulu=session[request.headers.get('X-Real-IP') + 'all_url']
            else:
                gen_mulu=request.form['gen_mulu']
            all_mulu[k]=os.path.join(gen_mulu,request.form['huanjing'],i.split('#')[0],i.split('#')[1]).replace('\\','/')
        #把实时运行信息清空
        cu.execute('delete from jiekou_result where ip="%s"' % ip)
        #更新运行状态从0变为1
        if len(cu.execute('select * from jiekou_mulu where ip=? and statu=? ',(request.headers.get('X-Real-IP'),'批量')).fetchall())>0:
             cu.execute('update jiekou_mulu set run_statu="1",update_time=? where ip=? and statu=?',
                   (time.time(),request.headers.get('X-Real-IP'),'批量'))
        else:
            cu.execute('insert into  jiekou_mulu values(null,?,?,?,?,?)',( '批量',request.form['gen_mulu'],request.headers.get('X-Real-IP'),time.time(),1))
        db.commit()
        #把运行信息插入数据库
        db.commit()
        db.close()
        data=json.dumps({'all_jiekou':all_mulu,'huanjing':request.form['huanjing'],'run_time':session['run_time'],'gen_mulu':request.form['gen_mulu'],'ip_dizhi':request.form['ip_dizhi'],'ip':request.headers.get('X-Real-IP')})
        # url = 'http://' + ip_dizhi.strip() + ':'+current_app.config.get('LOCAL_SERVER_PORT')+'/piliang_run'
        # test_data = {'data': data}
        # z=requests.post(url,test_data)
        # res_data=z.text
        # test_data_urlencode = urllib.parse.urlencode(test_data)
        # req = urllib.request.Request(url=url, data=test_data_urlencode)
        # res_data = urllib.request.urlopen(req)
        # try :
        #    res_data = urllib2.urlopen(req)
        # except:
        #     time.sleep(1)
        #     res_data = urllib2.urlopen(req)
        return jsonify(data='success',return_data=data)
    return ceshipi
#获取后端发过来的本地批量运行的结果并存入数据库中
def  piliang_run_resulttt(func):
    @wraps(func)
    def piliang_run_result1():
        db = sqlite3.connect(current_app.config.get('JIE_KOU'))
        cu = db.cursor()
        all_db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        all_cu = all_db.cursor()
        data=request.form['result']
        time_test=request.form['time']
        name=request.form['jeikou_name']
        ip = request.form['ip']
        if 'user_name'  not in list(session.keys()):
             session['user_name']=all_cu.execute('select name from  user where ip like "%s"'  % ('%' + ip +'%')).fetchall()[0][0]
        if 'local_seven_pic' in list(current_app.config.keys()):
            current_app.config.pop('local_seven_pic')
        pass_num = 0
        fail_num = 0
        result_data = json.loads(request.form['result'])
        for i in list(result_data.keys()):
            if result_data[i]['assert_result'] == True:
                pass_num += 1
            else:
                fail_num += 1
        # 转成七天前的时间戳
        otherStyleTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        seven_day = int(time.mktime(time.strptime(otherStyleTime, "%Y-%m-%d"))) - 604800
        seven_day = time.strftime("%Y-%m-%d", time.localtime(seven_day))
        user_team=all_cu.execute('select team from  user_team where user=? ',(session['user_name'],)).fetchall()
        if len(user_team)==0:
            user_team='无分组'
        else:
            user_team=user_team[0][0]
        user_name=session['user_name']
        time_this_datay=time.strftime("%Y-%m-%d", time.localtime(time.time()))
        case_num=len(json.loads(request.form['result']))
        if len(tody_tongji.query.filter_by(name=user_name,riqi=time_this_datay,jiekou_name=name).all())==0:
            z = tody_tongji(session['user_name'], name, str(case_num), str(pass_num), str(fail_num), user_team, time_this_datay,'1')
            db_chemy.session.add(z)
            db_chemy.session.commit()
        else:
            data_first=tody_tongji.query.filter_by(name=user_name,riqi=time_this_datay,jiekou_name=name).first()
            data_first.jiekou_num=str(int(data_first.jiekou_num)+1)
            if  int(data_first.case_num)<case_num:
               data_first.case_num=str(case_num)
            data_first.pass_num = str(int(data_first.pass_num) + pass_num)
            data_first.fail_num = str(int(data_first.fail_num) + fail_num)
            db_chemy.session.commit()
        all_cu.execute('delete from local_tongji  where name=? and time<=?', (session['user_name'], seven_day))
        #根据time来判断是否属于同一批次的结果
        before_detail=all_cu.execute('select * from local_tongji where  name= "%s" and time="%s"' % ( session['user_name'],otherStyleTime)).fetchall()
        if len(before_detail)==0:
            if fail_num==0:
                all_cu.executemany('INSERT INTO local_tongji VALUES (null,?,?,?,?,?,?,?,?)',
                                   [(session['user_name'], otherStyleTime,1,0,fail_num, pass_num,user_team,1)])
            else:
                all_cu.executemany('INSERT INTO local_tongji VALUES (null,?,?,?,?,?,?,?,?)',
                               [(session['user_name'], otherStyleTime, 0,1,fail_num,pass_num,user_team,1)])
        else:
            pass_jiekou=int(before_detail[0][3])
            fail_jiekou=int(before_detail[0][4])
            if fail_num==0:
                pass_jiekou+=1
            else:
                fail_jiekou+=1
            fail_num+=int(before_detail[0][5])
            pass_num+=int(before_detail[0][6])
            num = int(before_detail[0][8])+1
            #print all_cu.execute('update   local_tongji   set pass_jiekou=? where name=? and time=?',(session['user_name'],otherStyleTime))
            all_cu.execute('UPDATE local_tongji SET pass_jiekou=?,fail_jiekou=?,fail_case_num=?,pass_case_num=?,num=? WHERE name=? and time=?',
                            (str(pass_jiekou),str(fail_jiekou), str(fail_num), str(pass_num),str(num), session['user_name'], otherStyleTime))
            all_db.commit()
        cu.execute('delete from jiekou_result where ip="%s" and time!="%s"' %(ip,time_test))
        cu.executemany('INSERT INTO jiekou_result VALUES (?,?,?,?,null,"本地批量运行")',
                       [(name, ip, data, time_test)])
        all_db.commit()
        all_db.close()
        db.commit()
        db.close()
        return jsonify(statu='success')
    return piliang_run_result1
#获取后端发过来的本地批量运行的结果并存入数据库中
def piliang_git_result(func):
    def ceshi_pi_gi11t():
       func()
       current_app.config['NUM_JISHU']=current_app.config.get('NUM_JISHU')+1
       if 'seven_ci'  in list(current_app.config.keys()):
           current_app.config.pop('seven_ci_pic')
       if 'today_ci_pic'  in list(current_app.config.keys()):
           current_app.config.pop('today_ci_pic')
       if 'ci_seven_data' in list(current_app.config.keys()):
               current_app.config.pop('ci_seven_data')
       if 'ci_today_data' in list(current_app.config.keys()):
               current_app.config.pop('ci_today_data')
       db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
       cu = db.cursor()
       db_jeikou = sqlite3.connect(current_app.config.get('JIE_KOU'))
       cu_jiekou = db_jeikou.cursor()
       all_git_url=[i[0] for i in cu_jiekou.execute('select name from git_detail').fetchall()]
       git_url_detail={}
       for k,i in cu_jiekou.execute('select name,branch from  git_detail').fetchall():
           git_url_detail[k.split('/')[-1].split('.git')[0]+i]=[k,i]
       id=request.form['id']
       run_id=request.form['run_id']
       case_name=request.form['jeikou_name']
       result=request.form['result']
       git_barnch=request.form['git_branch']
       git_url_table=cu_jiekou.execute('select beizhu from git_detail where  name=? and branch=?' , (request.form['git_base_name'],git_barnch)).fetchall()[0][0]
       beofre_result=cu.execute('select run_result from dingshi_run where id="%s"'  % str(id)).fetchall()[0][0]
       beofre_result=json.loads(beofre_result)
       # beofre_result[case_name+'##'+git_url_table]=result
       all_name = []
       z=request.form['path_mulu']
       for i in range(3):
           if len(all_name) == 0:
               all_name.append(os.path.basename(z))
           else:
               all_name.insert(0, os.path.basename(z))
           z = os.path.dirname(z)
       del z
       result_detail = {
           "git_beizhu": git_url_table,
           "all_name": all_name
       }
       beofre_result[json.dumps(result_detail)] = result
       cu.executemany('update  dingshi_run  set run_result=? where id=?',
                      [(json.dumps(beofre_result),id)])
       #获取失败psss数量
       pass_num=0
       fail_num=0
       result_data=json.loads(request.form['result'])
       for i in list(result_data.keys()):
           if result_data[i]['assert_result']==True:
               pass_num+=1
           else:
               fail_num+=1
       git_url=[git_url_detail[i] for i in list(git_url_detail.keys()) if i in request.form['path_mulu']][0]
       name=cu.execute('select name from dingshi_run where id=%s'  % id).fetchall()[0][0]
       otherStyleTime = time.strftime("%Y-%m-%d", time.localtime(time.time()))
       #转成七天前的时间戳
       seven_day=int(time.mktime(time.strptime(otherStyleTime, "%Y-%m-%d")))-604800
       seven_day=time.strftime("%Y-%m-%d", time.localtime(seven_day))
       cu.execute('delete   from ci_tongji where time<=?'  , (seven_day,)).fetchall()
       before_log_detail=cu.execute('select * from ci_tongji where dingshiid_or_name=? and git_url=? and branch=?'  , (run_id,git_url[0],git_url[1])).fetchall()
       run_id = request.form['run_id']
       if len(before_log_detail)==0:
            cu.executemany('INSERT INTO ci_tongji VALUES (null,?,?,?,?,?,?,?,?)',
                                 [(name,git_url[0], run_id, '1', fail_num, pass_num, otherStyleTime,git_url[1])])
       else:
           jiekou_num=int(before_log_detail[0][4])+1
           pass_num += int(before_log_detail[0][6])
           fail_num += int(before_log_detail[0][5])
           cu.execute('UPDATE ci_tongji SET jiekou_num=?,fail_case_num=?,pass_case_num=? WHERE id=?',
                        (jiekou_num, fail_num, pass_num, before_log_detail[0][0]))
       db_jeikou.close()
       db.commit()
       db.close()
       return jsonify(statu='success')
    return ceshi_pi_gi11t
#从数据库中拉取数据，生成批量测试结果
def run_jiekou(func):
  def ceshi():
    func()
    ip = request.headers.get('X-Real-IP')
    if request.method == "GET":
        #根据ip地址读取测试数据
        g.cu.execute('select * from  jiekou_result where ip=?', (ip,))
        data = g.cu.fetchall()
        tim=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(float(data[-1][-1])))
        all=[]
        if len(data)!=0:
             for i in data:
                 name=i[0]
                 detail=[]
                 statu=0
                 count=len(eval(i[2]))
                 fail=0
                 succ=0
                 for k,z in list(eval(i[2]).items()):
                     z=json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(z))), parse_int=int), indent=4, sort_keys=False,
                  ensure_ascii=False)
                     result,id,comment,req=k.split('jo.in')
                     req=json.loads(req)
                     req = json.dumps(json.loads(json.dumps(demjson.decode(json.dumps(req))), parse_int=int), indent=4,
                                    sort_keys=False,
                                    ensure_ascii=False)
                     if s_assert.walk_find(json.loads(result),json.loads(z))==False:
                         statu=1
                         fail+=1
                         detail.append(["failCase",id.split('.')[0],comment,result,z,req])
                     else:
                         succ+=1
                         detail.append(["passCase", id.split('.')[0], comment, result,z,req])
                 detail=sorted(detail,key=lambda x:x[1])
                 if statu==1:
                         all.append([name,"failClass",[count,succ,fail,count],detail])
                 elif statu==0:
                         all.append([name,"passClass", [count, succ, fail, count], detail])
        #z中元素第一个接口名字，第二个接口的count，第三个用例状态，最后一个列表d第一个为用例状态，第二个用例id，第三个用例comment，第四个用例的接口数据
        return render_template('/result/test_result.html',z=all,time=tim)
  return ceshi
#返回接口批量运行页面
def jiekou_piliang(func):
    @wraps(func)
    def ceshizhong():
        db = sqlite3.connect(current_app.config.get('DB_DIZHI'))
        cu = db.cursor()
        jiekou_db=sqlite3.connect(current_app.config.get('JIE_KOU'))
        jiekou_cu = jiekou_db.cursor()
        name = cu.execute(
            'select name from user where ip="%s" order by time desc limit 0,1' % request.headers.get('X-Real-IP')).fetchall()
        if len(name) == 0:
            return redirect(url_for('login_new'))
        else:
            name = name[0][0]
        if request.method == 'GET':
            git_detail = [list(i) for i in jiekou_cu.execute('select * from git_detail  ').fetchall()]
            for i in git_detail:
                i[3] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(i[3])))
            email_detail = [i[0] for i in
                            cu.execute('select address from email_address where user="%s"' % (name)).fetchall()]
            fajianren = [i[0] for i in db.execute('select email_user from fajianren where name="%s"' % name).fetchall()]
            dingshi_detail = [[i[1], i[2], i[4], i[6]] for i in cu.execute(
                'select * from dingshi_run where name="%s" order by update_time desc ' % (name)).fetchall()]
            jobs = [i[0] for i in db.execute('select job_name from jekins where name="%s"' % name).fetchall()]
            for k, i in enumerate(dingshi_detail):
                i.insert(0, i[0])
                i[1] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(i[0])))
                if i[-2].strip() == '0':
                    i[-2] = 'ready'
                elif i[-2].strip() == '1':
                    i[-2] = 'running'
                elif i[-2].strip() == '2':
                    i[-2] = 'over'
            time_date = time.strftime('%Y-%m-%d ', time.localtime(time.time()))
            server_detail = [i[1] for i in cu.execute('select * from all_server where statu="1"').fetchall()]
            db.close()
            jiekou_db.commit()
            jiekou_db.close()
            return render_template('/hualala/pages/jiekou_page.html', git_detail=git_detail, email_detail=email_detail,
                                   time_date=time_date, dingshi_detail=dingshi_detail, fajianren=fajianren, jobs=jobs,
                                   server_detail=server_detail)
        else:
            git_url = request.form['git'].strip()
            git_beizhu = request.form['beizu'].strip()
            git_branch = request.form['branch'].strip()
            if git_url.strip() != '' and git_beizhu.strip() != '':
                jiekou_cu.executemany('INSERT INTO git_detail VALUES (?,?,?,?,?,?)',
                               [(git_url, git_beizhu, name, str(time.time()), '', git_branch)])
                db.commit()
                jiekou_db.commit()
                jiekou_db.close()
                db.close()
            return jsonify(a='1')
    return ceshizhong
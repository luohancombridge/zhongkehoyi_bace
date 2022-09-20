import pymysql
import traceback
from flask import render_template, flash, redirect,request,g,Response,stream_with_context
from flask_bootstrap import Bootstrap
from flask import Blueprint, jsonify, request
# 计算原始分区间
class get_all_sum(object):
    def __init__(self,kaohao):
        self.kaohao=kaohao
        self.conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        # 得到一个可以执行SQL语句的光标对象
        self.cursor = self.conn.cursor()
        self.all_xueke={
            "化学": 100004,
            "政治": 100007,
            "生物": 100005,
            "地理": 100008,
        }
        self.all_xueke_qujian={
        }
    #计算分数区间真实的
    def git_gudingfen_qujian(self):
        statu_this=0
        for k,i in self.all_xueke.items():
            sql='SELECT score FROM exam_score_transfer_for_bi WHERE exam_id=%s and school_code!= "" and subject_code=%s GROUP BY student_code'  % (str(self.kaohao),str(i))
            self.cursor.execute(sql)
            self.this_all_data=sorted([float(i[0]) for i in self.cursor.fetchall()],reverse=True)
            if len(  self.this_all_data)>0:
                statu_this=1
            else:
                continue
            self.a_score= [self.this_all_data[0],self.this_all_data[int(len(self.this_all_data)*0.15)]]
            self.b_score=[self.jisuan_guding_qujian(int(len(self.this_all_data)*0.15)),self.this_all_data[int(len(self.this_all_data)*0.5)]]
            self.c_score=[self.jisuan_guding_qujian(int(len(self.this_all_data)*0.5)),self.this_all_data[int(len(self.this_all_data)*0.85)]]
            self.d_score=[self.jisuan_guding_qujian(int(len(self.this_all_data)*0.85)),self.this_all_data[int(len(self.this_all_data)*0.98)]]
            self.e_score=[self.jisuan_guding_qujian(int(len(self.this_all_data)*0.98)),self.this_all_data[-1]]
            self.all_xueke_qujian[k] = [self.a_score,self.b_score,self.c_score,self.d_score,self.e_score]
        if statu_this==0:
            return {
                "statu":'error',
                "detail":"BI表查不到数据"
            }
        return self.all_xueke_qujian
    #参数为上一个区间的下标，找出不一样的下一个区间的上标
    def jisuan_guding_qujian(self,a):
        data=self.this_all_data[a-1]
        return_data=None
        for i in self.this_all_data[a+1:]:
           if i != data:
              return_data = i
              break
        return return_data
class get_all_fufen(object):
    def __init__(self,kaohao):
        self.conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        # 得到一个可以执行SQL语句的光标对象
        self.kaohao = kaohao
        self.cursor = self.conn.cursor()
        self.all_xueke = {
            "物理": 100003,
            "化学": 100004,
            "政治": 100007,
            "生物": 100005,
            "地理": 100008,
            '数学':100002,
            "语文":100001,
            "英语":100016,
            "历史":100006
        }
        self.all_xueke_score = {
            "化学": {},
            "政治": {},
            "生物": {},
            "地理": {}
        }
        self.jifenqujian = get_all_sum(self.kaohao).git_gudingfen_qujian()
        self.fufenqujian=[[100,86],[85,71],[70,56],[55,41],[40,30]]
        self.all_studend_all_score={}
    #计算分数区间真实的
    def get_fufen(self):
            for k,i in  self.all_xueke.items():
                sql='SELECT exam_registration_no,student_name,subject_code,score,school_code,grade_code,class_code,class_name FROM exam_score_transfer_for_bi WHERE exam_id=%s and subject_code=%s' \
                    ' and school_code!= "" GROUP BY student_code' % (str(self.kaohao),str(i))
                self.cursor.execute(sql)
                this_all_data =  self.cursor.fetchall()
                this_all_data =[list(xx) for xx in this_all_data]
                jisuanhou_data=[]
                all_class_type = {}
                print (k,i)
                for zz,s in enumerate(this_all_data):
                             exam_registration_no,student_name,xueke,fenshu,school_code,grade_code,class_code,class_name=s
                             if class_code not in all_class_type.keys():
                                  sql =  'SELECT class_type FROM exam_business2.school_class_ralate  WHERE school_code = {} and class_code ={}'.format(str(school_code),str(class_code))
                                  self.cursor.execute(sql)
                                  this_class_type=self.cursor.fetchall()
                                  if len(this_class_type)==0:
                                         class_type = 0
                                  else :
                                         class_type = this_class_type[0][0]
                                  all_class_type[class_code] =class_type
                             else :
                                   class_type = all_class_type[class_code]
                             fenshu=float(fenshu)
                             if this_all_data[zz][0] not in  self.all_studend_all_score.keys():
                                self.all_studend_all_score[this_all_data[zz][0]] = {
                                    "班级信息": {
                                        'class_type': class_type,
                                        'school_code':school_code,
                                        'grade_code':grade_code,
                                        'class_code':class_code,
                                        'class_name':class_name,
                                        'student_name':student_name
                                    },
                                    "原始分":{
                                        k:fenshu
                                    },
                                    "赋分":{
                                        k: fenshu
                                    }
                                }
                             else:
                                 self.all_studend_all_score[this_all_data[zz][0]]["原始分"][k] = fenshu
                             if k in self.jifenqujian.keys():
                                 qujian = self.jifenqujian[k]
                                 qujian_type=0
                                 for uu,i in enumerate(qujian):
                                       if fenshu<=i[0] and fenshu>=i[1]:
                                           yuanshifen_qujian=i
                                           qujian_type= uu
                                           break
                                 fufen_qujian = self.fufenqujian[qujian_type]
                                 # this_all_data[zz][-1]=self.jisuan_fufen(yuanshifen_qujian,fufen_qujian,fenshu)
                                 fufen=self.jisuan_fufen(yuanshifen_qujian,fufen_qujian,fenshu)
                                 self.all_xueke_score[k][this_all_data[zz][0]]=fufen
                                 self.all_studend_all_score[this_all_data[zz][0]]["赋分"][k]=fufen
            self.all_score_list=[]
            for k,i in self.all_studend_all_score.items():
                self.all_score_list.append([k,i])
            return  [self.all_studend_all_score,self.all_score_list]
    #第一个为原始分区间列表，第二个为赋分区间列表，第三个为真正的分数
    def jisuan_fufen(self,yuanshifen,fufen,tr):
            y1 = yuanshifen[1]
            y2 = yuanshifen[0]
            t1 = fufen[1]
            t2 = fufen[0]
            y = tr
            jiasun1 = t2 * (y - y1)
            jisuan2 = t1 * (y2 - y)
            fenmu = y2 - y1
            fenzi = jiasun1 + jisuan2
            if fenzi==0 or fenmu==0:
                return 0
            return round(fenzi / fenmu)
    #计算学科组合分数及排名，参数第一个为考号，第二个为一个列表，里面为学科名列表
def get_zuhe_paiming(kaohao,zuhe_list,all_studend_all_score,all_score_list,fufen_or_yuanshifen):
        this_all_score = all_studend_all_score[kaohao]
        class_type= all_studend_all_score[kaohao]['班级信息']['class_type']
        zuhefen = 0
        yuanshifen_all=0
        for ss in zuhe_list:
            if fufen_or_yuanshifen == '赋分':
                if ss not in ['数学', '英语', '物理', '历史', '语文']:
                    zuhefen = zuhefen + this_all_score['赋分'][ss]
                else:
                    zuhefen = zuhefen + this_all_score['原始分'][ss]
            else:
                zuhefen = zuhefen + this_all_score['原始分'][ss]
            yuanshifen_all = yuanshifen_all + this_all_score['原始分'][ss]
        school_code = this_all_score['班级信息']['school_code']
        class_code = this_all_score['班级信息']['class_code']
        len_get=len(zuhe_list)
        li_wen_ban=[]
        for i in all_score_list:
            if i[1]['班级信息']['class_type'] == class_type:
                li_wen_ban.append(i)
        all_score_list=sorted(li_wen_ban,key= lambda x : jiafen_top(x,zuhe_list,fufen_or_yuanshifen),reverse=True)
        mingci= None
        xuexiao_mingci = 0
        banji_minci = 0
        status_aa=0
        # "班级信息": {
        #     'school_code': school_code,
        #     'grade_code': grade_code,
        #     'class_code': class_code
        # },
        all_score_list_this= []
        for k,i in enumerate(all_score_list):
            if '2101050276' == i[0]:
                pass
            if i[1]['班级信息']['class_type'] ==class_type:
                all_score_list_this.append(i)
        for k,i in enumerate(all_score_list_this):
                if '2101050276' == i[0]:
                    pass
                this_zuhefen = 0
                if fufen_or_yuanshifen == '赋分':
                    for ss in zuhe_list:
                        if ss not  in ['数学','英语','物理','历史','语文']:
                             this_zuhefen=this_zuhefen+i[-1]['赋分'][ss]
                        else:
                            this_zuhefen = this_zuhefen + i[-1]['原始分'][ss]
                else:
                    for ss in zuhe_list:
                        # 解决某学科没有成绩的问题
                        this_zuhefen = this_zuhefen + i[-1]['原始分'].get(ss, 0)
                if i[-1]['班级信息']['school_code'] == school_code:
                    xuexiao_mingci = xuexiao_mingci +1
                    if i[-1]['班级信息']['class_code'] == class_code:
                         banji_minci = banji_minci +1
                if this_zuhefen == zuhefen:
                    if i[-1]['班级信息']['school_code'] != school_code:
                        xuexiao_mingci = xuexiao_mingci + 1
                        banji_minci = banji_minci + 1
                    elif  i[-1]['班级信息']['school_code'] != school_code and i[-1]['班级信息']['class_code'] == class_code:
                        banji_minci = banji_minci + 1
                    mingci= k+1
                    break
        lianmengmingci = mingci
        return {
            "联盟名次":mingci,
            "学校名次": xuexiao_mingci,
            "班级名次": banji_minci,
            "分数":zuhefen,
            "原始分":yuanshifen_all
        }
    #顺序加分数
def jiafen_top(x,ge_list,fufen_or_yuanshifen):
        u=0
        for i in ge_list:
            if fufen_or_yuanshifen == '赋分':
                if i not in x[-1]['赋分'].keys():
                    try:
                      u = x[-1]['原始分'][i] + u
                    except:
                        pass
                else:
                   u=x[-1]['赋分'][i]+u
            else:
                # 解决某学科没有成绩的问题
                u = x[-1]['原始分'].get(i, 0) + u
        return u

def get_zuhe_paiming_banji(kaoshihao,banji_id,zuhe_list,all_studend_all_score,all_score_list,fufen_or_yuanshifen):
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        # 得到一个可以执行SQL语句的光标对象
        cursor = conn.cursor()
        sql = 'SELECT DISTINCT(class_code) FROM exam_score_transfer_for_bi WHERE exam_id=%s and class_name="%s"' \
              ' and school_code!= "" GROUP BY student_code' % (str(kaoshihao), str(banji_id))
        cursor.execute(sql)
        banji_id = cursor.fetchall()[0][0]
        if type(zuhe_list) ==list:
            xueke = zuhe_list
        else:
            xueke =zuhe_list
        all_student_score = {}
        top_score=0
        low_score=0
        pingjun_score=0
        fencha=0
        all_score=[]
        zero_all=0
        for k,i in all_studend_all_score.items():
            if  int(i['班级信息']['class_code']) == int (banji_id) :
                zuhefen = 0
                yuanshifen_all = 0
                fenshu= 0
                # fenshu= i['原始分'][xueke]
                for z in xueke:
                    fenshu= fenshu+i['原始分'][z]
                if fenshu ==0 :
                    zero_all =zero_all +1
                else:
                    all_score.append(fenshu)
                    if fenshu>top_score:
                        top_score = fenshu
                    if low_score==0 or fenshu<low_score :
                        low_score= fenshu
        fencha=   top_score - low_score
        all_score_sum = 0
        for i in all_score:
            all_score_sum = all_score_sum + i
        pingjun_score = all_score_sum/len(all_score)
        return  {
            "最高分":top_score,
            "最低分":low_score,
            "分差":fencha,
            "平均分":pingjun_score,
            "零分人数":zero_all
        }
import json
def get_xuanke_student(func):
    def get_xuanke_student():
        func()
        all_json = json.loads(request.get_data())
        all_json['xuanke_xuexiao_id'] =1541982701274267648
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_business2',charset='utf8')
        sql='SELECT DISTINCT(mix_subject_code),mix_subject_name FROM student_choose_subject_volunteer'
        cursor = conn.cursor()
        cursor.execute(sql)
        subject_detail = {}
        for k,i  in enumerate( cursor.fetchall()) :
            subject_detail[i[0]] =i[1].split(',')
        sql = 'SELECT subject_compose FROM `exam_student` WHERE  exam_base_id =%s  AND  exam_code = "%s"  ' %\
              ( str(all_json['kaoshihao']),str(all_json['xuehao']))
        cursor = conn.cursor()
        cursor.execute(sql)
        student_code = cursor.fetchall()
        if len(student_code) ==0 :
            return  jsonify(return_data= {
                'statu':'error',
                'detail':"查不到学生号"
            })
        else :
            student_code = student_code[0][0]
        # 得到一个可以执行SQL语句的光标对象
        conn.close()
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_business2'    ,charset='utf8')
        cursor = conn.cursor()
        sql='SELECT * FROM `student_todo` WHERE student_id ={} AND todo_type = 1 and school_id = {}  ' \
            ' and todo_name_code={} order by create_time desc'.format(student_code,all_json['xuanke_xuexiao_id'],str(all_json['kaoshihao']))
        cursor.execute(sql)
        todo_id = cursor.fetchall()
        if len(todo_id) ==0 :
            return jsonify(return_data={
                'statu':'error',
                'detail':"找不到todo_id"
            })
        else :
            todo_id = todo_id[0][0]
        sql = 'SELECT four_choose_two_subject_one_name,four_choose_two_subject_tow_name,mix_subject_name FROM `student_choose_subject_volunteer` WHERE student_todo_id = {} and choose_type = 1'.format(todo_id)
        cursor.execute(sql)
        xueke_first = cursor.fetchall()
        if len(xueke_first) ==0:
            xueke_first = '无第一志愿'
        else :
            if xueke_first[0][0] =='0':
                xueke_first = '无第一志愿'
            else :
              xueke_first = {
                  "第一选择":xueke_first[0][0],
                  "第二选呢":xueke_first[0][1],
                  "总选科":xueke_first[0][2]
              }
        sql = 'SELECT four_choose_two_subject_one_name,four_choose_two_subject_tow_name, mix_subject_name FROM `student_choose_subject_volunteer` WHERE student_todo_id = {} and choose_type = 2'.format(todo_id)
        cursor.execute(sql)
        xueke_second = cursor.fetchall()
        print (xueke_second)
        if len(xueke_second) ==0:
            xueke_second = '无第二志愿'
        else :
            if  xueke_second[0][0] == '0':
                xueke_second = '无第二志愿'
            else:
              xueke_second = {
                  "第一选择":xueke_second[0][0],
                  "第二选呢":xueke_second[0][1],
                  "总选科":xueke_second[0][2]
              }
        conn.close()
        return jsonify(return_data={"todo_id": todo_id, '第一志愿': xueke_first, "第二志愿": xueke_second})
    return get_xuanke_student
import redis
def chushihua_xuanke_def(func):
    def chushihua_xuanke_def():
        func()
        all_json = json.loads(request.get_data())
        kaoshihao = all_json['kaoshihao']
        xuanxiaoid_xuanke= all_json['xuanxiaoid_xuanke']
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        sql = 'SELECT exam_registration_no,student_code,class_name,class_code FROM exam_score_transfer_for_bi WHERE exam_id= %s  and school_code= %s' %\
              ( str(all_json['kaoshihao']), str(xuanxiaoid_xuanke))
        cursor = conn.cursor()
        cursor.execute(sql)
        student_code = cursor.fetchall()
        if len(student_code) ==0 :
            return {
                'statu':'error',
                'detail':"查不到数据，请确认输入是否正确"
            }
        all_student_code = {}
        for i in student_code:
            all_student_code[i[0]]={
                "student_code": i[1],
                "class_name": i[2],
                "class_code": i[3]
            }
        conn.close()
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_business2'    ,charset='utf8')
        cursor = conn.cursor()
        sql='SELECT id,student_id FROM `student_todo` WHERE  todo_type = 1 and school_id = {}  ' \
            ' and todo_name_code={} order by create_time desc'.format(all_json['xuanxiaoid_xuanke'],str(all_json['kaoshihao']))
        cursor.execute(sql)
        todo_id = cursor.fetchall()
        if len(todo_id) ==0 :
            return {
                'statu':'error',
                'detail':"找不到todo_id"
            }
        all_todo_dict= {}
        for i in todo_id:
            all_todo_dict[i[1]] = i[0]
        all_tode_id = tuple([i[0] for i in todo_id])
        sql = 'SELECT student_todo_id,four_choose_two_subject_one_name,four_choose_two_subject_tow_name,mix_subject_name FROM `student_choose_subject_volunteer` WHERE student_todo_id in  {} and choose_type = 1'.format(str(all_tode_id))
        cursor.execute(sql)
        all_xuanke = cursor.fetchall()
        if len(all_xuanke) ==0:
            return {
                'statu': 'error',
                'detail': "查不到选科信息"
            }
        all_xuanke_dict_first={}
        for  i in all_xuanke:
            all_xuanke_dict_first[i[0]]= {
                "four_choose_two_subject_one_name":i[1],
                "four_choose_two_subject_tow_name":i[2],
                "mix_subject_name":i[3]
            }
        sql = 'SELECT student_todo_id,four_choose_two_subject_one_name,four_choose_two_subject_tow_name,mix_subject_name FROM `student_choose_subject_volunteer` WHERE student_todo_id in  {} and choose_type = 2'.format(str(all_tode_id))
        cursor.execute(sql)
        all_xuanke = cursor.fetchall()
        if len(all_xuanke) ==0:
            return {
                'statu': 'error',
                'detail': "查不到选科信息"
            }
        all_xuanke_dict_second={}
        for  i in all_xuanke:
            all_xuanke_dict_second[i[0]]= {
                "four_choose_two_subject_one_name":i[1],
                "four_choose_two_subject_tow_name":i[2],
                "mix_subject_name":i[3]
            }
        conn.close()
        for k,i in all_todo_dict.items():
            this_dict = {}
            if i in all_xuanke_dict_first.keys():
                this_dict['all_xuanke_dict_first'] = all_xuanke_dict_first[i]
            if i in all_xuanke_dict_second.keys():
                this_dict['all_xuanke_dict_second'] = all_xuanke_dict_second[i]
            all_todo_dict[k] = this_dict
        for k ,i in all_student_code.items():
            thi_dict= i
            student_code = int(i['student_code'])
            this_dict={}
            if student_code not in all_todo_dict.keys():
                this_dict['xuanke_dict'] = {}
            else:
                 this_dict['xuanke_dict']=all_todo_dict[student_code]
            all_student_code[k].update(this_dict)
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if r.get('xuanke') == None:
            r.set('xuanke','{}')
        else:
            rdist_dit = json.loads(r.get('xuanke'))
            rdist_dit[xuanxiaoid_xuanke] = all_student_code
            r.set('xuanke',json.dumps(rdist_dit))
        return jsonify(statu='success')
    return chushihua_xuanke_def

def banjixuankezuhe_def(func):
    def banjixuankezuhe_def():
        func()
        all_json = json.loads(request.get_data())
        banji_ming = all_json['banjiming']
        kaoshihao = all_json['kaoshihao']
        xuexiaoid = all_json['xuexiaoid']
        banji_num =0
        xuanke_num =0
        only_fist=0
        first_second=0
        first_num_fenlei={
            "wuli":0,
            "lishi":0
        }
        second_num_fenlei={
            "wuli":0,
            "lishi":0
        }
        all_c = {'物,政,化',"物,政,生","物,政,地","物,生,化","物,地,生","物,地,化", "历,政,地","历,政,生","历,政,化","历,地,生","历,地,化","历,生,化"}
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        if r.get('xuanke') == None:
           return "请先初始化数据"
        else:
            rdist_dit = json.loads(r.get('xuanke'))
            if rdist_dit =={}:
                 return "请先初始化数据"
            all_didi ={}
            for i in all_c:
                all_didi[i] = {
                    '第一志愿':0,
                    "第二志愿":0,
                    "学生code":{
                        "第一志愿":[],
                        "第二志愿":[]
                    }
                }
            for k, i in rdist_dit[xuexiaoid].items():
                    banji_name = i['class_name']
                    if banji_name.strip() == banji_ming.strip():
                        banji_num =banji_num+1
                        statu=0
                        only_first_statu=0
                        all_check=0
                        if 'all_xuanke_dict_first' in i['xuanke_dict'].keys():
                            if i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name'] !='0':
                                xuanke_num = xuanke_num+1
                                only_first_statu=1
                                statu=1
                                all_check= all_check+1
                                if '物' in i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']:
                                    first_num_fenlei['wuli'] = first_num_fenlei['wuli']+1
                                else:
                                    first_num_fenlei['lishi'] = first_num_fenlei['lishi'] + 1
                                all_didi[i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']]['学生code']['第一志愿'].append(i['student_code'])
                                all_didi[i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']]['第一志愿'] =  all_didi[i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']]['第一志愿'] +1
                        if 'all_xuanke_dict_second' in i['xuanke_dict'].keys():
                            if i['xuanke_dict']['all_xuanke_dict_second']['mix_subject_name'] != '0':
                                    only_first_statu=0
                                    all_check = all_check + 1
                                    if '物' in i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']:
                                        second_num_fenlei['wuli'] = second_num_fenlei['wuli'] + 1
                                    else:
                                        second_num_fenlei['lishi'] = second_num_fenlei['lishi'] + 1
                                    if i['xuanke_dict']['all_xuanke_dict_second']['mix_subject_name'] != '0':
                                       if statu==0:
                                          xuanke_num = xuanke_num+1
                                       all_didi[i['xuanke_dict']['all_xuanke_dict_first']['mix_subject_name']]['学生code'][
                                           '第二志愿'].append(i['student_code'])
                                       all_didi[i['xuanke_dict']['all_xuanke_dict_second']['mix_subject_name']]["第二志愿"] =  all_didi[i['xuanke_dict']['all_xuanke_dict_second']['mix_subject_name']]["第二志愿"]+1
                        if only_first_statu==1:
                            only_fist =only_fist+1
                        if all_check==2:
                            first_second=first_second+1
            return jsonify(return_data= {
                "班级名":banji_ming,
                "统计":all_didi,
                "班级人数":banji_num,
                "选科人数":xuanke_num,
                "只选了第一志愿人数":only_fist,
                "第一第二志愿均选":first_second,
                "第一志愿分类":first_num_fenlei,
                "第二志愿分类":second_num_fenlei
            })
    return banjixuankezuhe_def



def fenshuduantongji_get_def_d(func):
    def fenshuduantongji_get_def_d():
        func()
        all_data= json.loads(request.get_data())
        request_data = all_data['request_data']
        banjiming = request_data['banjiming']
        begin_fen = request_data['begin_fen']
        wenlike=int(request_data['wenlike'])
        end_fen = request_data['end_fen']
        kemu =  request_data['kemu']
        kaoshihao = all_data['kaoshihao']
        xuexiaoid = all_data['xuexiaoid']
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        this_dict = json.loads(r.get('return_Data'))[str(kaoshihao)][0]
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        sql = 'SELECT exam_registration_no,student_code,class_code FROM exam_score_transfer_for_bi WHERE exam_id= %s  and school_code= %s and class_name="%s"' %\
              ( str(kaoshihao), str(xuexiaoid),banjiming)
        cursor = conn.cursor()
        cursor.execute(sql)
        all_stu_list = cursor.fetchall()
        if len(all_stu_list) == 0:
            return jsonify(return_data={
                "statu":"error",
                "detail":"查不到班级数据"
            })
        all_stu_sc={}
        wenzong=['历史','地理','政治']
        lizong= ['物理','化学','生物']
        wenke=['历史','地理','政治','语文','英语','数学']
        like=['物理','化学','生物','语文','英语','数学']
        for k,i in enumerate(all_stu_list):
            if kemu=='文综' or kemu=='文科' :
                this_all_score=0
                if kemu=='文综':
                    tiaoshi_t = wenzong
                else:
                    tiaoshi_t = wenke
                for simple_kemu in tiaoshi_t:
                    this_all_score=this_all_score+this_dict[i[0]]['原始分'][simple_kemu]
                if this_all_score!=0:
                   all_stu_sc[i[0]] = this_all_score
            elif kemu=='理综' or kemu=='理科'  :
                this_all_score = 0
                if kemu=='理综':
                    tiaoshi_t = lizong
                else:
                    tiaoshi_t = like
                for simple_kemu in tiaoshi_t:
                    this_all_score = this_all_score + this_dict[i[0]]['原始分'][simple_kemu]
                if this_all_score != 0:
                  all_stu_sc[i[0]] = this_all_score
            else :
                if this_dict[i[0]]['原始分'][kemu] != 0:
                   all_stu_sc[i[0]] = this_dict[i[0]]['原始分'][kemu]
        this_num = 0
        for k,i in all_stu_sc.items():
            if int(begin_fen)<i<=int(end_fen):
                this_num=this_num+1
        bili = (this_num / len(all_stu_sc)) * 100
        bili = round(bili, 2)
        return jsonify(return_data={
            "statu":"success",
            "this_num":this_num,
            "bili":bili
        })
    return fenshuduantongji_get_def_d


def  fenshuduantongji_get(func):
    def fenshuduantongji_get():
        func()
        all_json= json.loads(request.get_data())
        banjiming=all_json['request_data']['banjiming']
        mingci=all_json['request_data']['mingci']
        kemu = all_json['request_data']['kemu']
        kaoshihao = all_json['kaoshihao']
        xuexiaoid = all_json['xuexiaoid']
        type_str= all_json['request_data']['type_str']
        fanwei = all_json['request_data']['fanwei']
        conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',
                               user='QA',password='hmk#%^&djofsdh',database='exam_databoard',charset='utf8')
        sql = 'SELECT distinct(class_code) FROM exam_score_transfer_for_bi WHERE exam_id= %s  and school_code= %s and class_name="%s"' %\
              ( str(kaoshihao), str(xuexiaoid),banjiming)
        cursor = conn.cursor()
        print (2)
        cursor.execute(sql)
        class_id = cursor.fetchall()
        if len(class_id) ==0:
            return  jsonify(return_data={
                'statu':"fail",
                "detail":"查不到班级id"
            })
        else :
            class_id = int(class_id[0][0])
        sql = 'SELECT class_type FROM exam_business2.school_class_ralate  WHERE school_code = {} and class_code ={}'.format(
            str(xuexiaoid), str(class_id))
        cursor.execute(sql)
        class_type =cursor.fetchall()
        if len(class_type) ==0:
            class_type = 0
        else :
           class_type = int(cursor.fetchall()[0][0])
        sql = 'SELECT distinct(student_code) FROM exam_score_transfer_for_bi WHERE exam_id= %s  and school_code= %s and class_name="%s"' %\
              ( str(kaoshihao), str(xuexiaoid),banjiming)
        cursor = conn.cursor()
        cursor.execute(sql)
        all_student_list = cursor.fetchall()
        all_statudent_num= len(all_student_list)
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        this_dict = json.loads(r.get('return_Data'))[str(kaoshihao)][0]
        all_dict_list=[]
        class_num=0
        if fanwei == '学校':
            for k,i in this_dict.items():
                if int(i['班级信息']['class_code']) ==class_id:
                    class_num = class_num+1
                if i['班级信息']['class_type'] == class_type:
                   if int(i['班级信息']['school_code']) ==  int (all_json['xuexiaoid']):
                            if kemu  in i['原始分'].keys():
                                if int(i['原始分'][kemu])!=0:
                                     all_dict_list.append([int(i['班级信息']['class_code']),int(i['原始分'][kemu])])
        elif fanwei == '联盟':
            for k,i in this_dict.items():
                if int(i['班级信息']['class_code']) ==class_id:
                    class_num = class_num+1
                if i['班级信息']['class_type'] == class_type  and  kemu in i['原始分'].keys():
                    if int(i['原始分'][kemu]) !=0:
                          all_dict_list.append([int(i['班级信息']['class_code']),int(i['原始分'][kemu])])
        all_score_list=sorted(all_dict_list,key= lambda x : x[1],reverse=True)
        return_num = 0
        if type_str =='名次':
            for i in all_score_list[int(mingci)-10:int(mingci)]:
                if i[0] == class_id :
                    return_num = return_num +1
            print (all_statudent_num)
            return jsonify(return_data={
                "all_num":len(all_dict_list),
                "statu":"success",
                "return_num":return_num,
                "bili":str(round((return_num/class_num)*100,2))+'%'
            })
        else:
            begin_num=round(int(len(all_score_list)*((int(mingci)-10)/100)))
            stop_num= round(int(len(all_score_list)*(int(mingci)/100)))
            for i in all_score_list[begin_num:stop_num]:
                if i[0] == class_id :
                    return_num = return_num +1
            print (len(all_score_list))
            print (begin_num)
            print (stop_num)
            return jsonify(return_data={
                "all_num": len(all_dict_list),
                "statu":"success",
                "return_num":return_num,
                "bili":str(round((return_num/class_num)*100,2))+'%'
            })
    return fenshuduantongji_get
if __name__=='__main__':
    z=get_all_sum()
    z.git_gudingfen_qujian()


import pymysql
from collections import Counter

class get_kaoshi_data(object):
    def __init__(self,school_id,grade_id,yearterm_id):
        self.school_id=school_id
        self.grade_id=grade_id
        self.yearterm_id=yearterm_id
        self.conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',user='QA',password='hmk#%^&djofsdh',charset='utf8')
        self.cursor = self.conn.cursor()
        self.examlist=[]   # 考试id
        self.examnamelist=[]   # 考试id
        self.entrance_count_list=[]   # 参考人数
        self.entrance_list=[]   # 参考率

    # 第一版由于数据不全 暂时废弃
    # def get_kaoshi_basedata(self):
    #     sql='''
    #         SELECT 
    #             a.exam_id, -- 考试id
    #             base.exam_name, -- 考试名称
    #             a.school_code, -- 学校id
    #             a.school_name, -- 学校名称
    #             a.grade_code, -- 年级id
    #             a.grade_name, -- 年级名称
    #             a.entrance_count, -- 参考人数,
    #             a.entrance -- 参考率
    #         FROM
    #             `exam_business2`.`exam_base` base 
    #         JOIN 
    #         (SELECT 
    #             t.school_code school_code, -- 学校id
    #             t.school_name school_name, -- 学校名称
    #             t.grade_code grade_code, -- 年级id
    #             t.grade_name grade_name, -- 年级名称
    #             t.exam_id exam_id, -- 考试id
    #             COUNT(DISTINCT t.student_code) entrance_count, -- 参考人数,
    #             ROUND(COUNT(DISTINCT t.student_code) / xs.zx_rs,3) entrance -- 参考率
    #         FROM
    #             `exam_business2`.`stu_subject_score` t 
    #             LEFT JOIN 
    #                 (SELECT data_id, grade_id, COUNT(*) zx_rs -- 在校人数
    #                 FROM `khfw_uc`.`uc_user_student` t1 
    #                 WHERE del_flag = 0 
    #                 GROUP BY data_id, grade_id) xs 
    #                 ON t.school_code = xs.data_id AND t.grade_code = xs.grade_id 
    #         WHERE t.school_code = %s AND t.grade_code = %s
    #         GROUP BY t.exam_id) a   
    #         ON base.exam_id = a.exam_id
    #         WHERE base.delete_flag = 0    
    #         ORDER BY create_time DESC
    #     '''%(self.school_id, self.grade_id)
    #     self.cursor.execute(sql)
    #     sqldata = self.cursor.fetchall()
    #     if sqldata:
    #         for d in sqldata:
    #             self.examlist.append(d[0])
    #             self.examnamelist.append(d[1])
    #             self.entrance_count_list.append(d[6])
    #             self.entrance_list.append(d[7])
    #     return self.examlist, self.examnamelist, self.entrance_count_list, self.entrance_list

    def get_kaoshi_basedata(self):
        sql='''
            SELECT 
            exam_id  -- 考试id
            ,exam_name  -- 考试名称
            ,school_code  -- 学校id
            ,school_name  -- 学校名称
            ,COUNT(DISTINCT student_code) entrance_count  -- 参考人数,
            ,ROUND(COUNT(DISTINCT student_code) / xs.zx_rs, 3) entrance  -- 参考率
            FROM
            `exam_databoard`.`exam_score_transfer_for_bi`
            LEFT JOIN 
                (SELECT 
                data_id  -- 学校id
                ,grade_id
                ,COUNT(*) zx_rs  -- 在校人数
                FROM
                `khfw_uc`.`uc_user_student` t1 
                WHERE del_flag = 0 
                GROUP BY data_id, grade_id) xs 
                ON school_code = xs.data_id 
                AND grade_code = xs.grade_id 
            WHERE school_code = %s 
            AND is_del = 0 
            AND grade_code = %s 
            AND score_type IN (0, 2, 3)   -- 经研发确认score_type 为3 的数据也是属于正常考试分数
            GROUP BY exam_id 
            ORDER BY create_time DESC
        '''%(self.school_id, self.grade_id)
        self.cursor.execute(sql)
        sqldata = self.cursor.fetchall()
        if sqldata:
            for d in sqldata:
                self.examlist.append(d[0])
                self.examnamelist.append(d[1])
                self.entrance_count_list.append(d[4])
                self.entrance_list.append(d[5])
        return self.examlist, self.examnamelist, self.entrance_count_list, self.entrance_list       
   


class get_xuanke_data(object):
    def __init__(self,school_id,examlist):
        self.school_id=school_id
        self.examlist=examlist
        self.conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',user='QA',password='hmk#%^&djofsdh',charset='utf8')
        self.cursor = self.conn.cursor()
        self.xuankerenshu_2to1_list=[]    # 二选一的人数列表
        self.wuli_id = "100003"    # 物理科目id
        self.wuli_renshu_list = []    # 选择物理人数
        self.lishi_id = "100006"    # 历史科目id
        self.lishi_renshu_list = []    # 选择历史人数
        # self.xuanke_subject_id = {
        #     1: "物,政,化", 2: "物,政,生", 3: "物,政,地", 4: "物,生,化", 5: "物,地,生", 6: "物,地,化",
        #     7: "历,政,地", 8: "历,政,生", 9: "历,政,化", 10: "历,地,生", 11: "历,地,化", 12: "历,生,化",
        # }
        self.xuanke_subject_result = []

    def get_xuanke_2to1_data(self):
        for exam_id in self.examlist:
            sql='''
                SELECT 
                  kaoshi.student_code -- 学生id
                  ,kaoshi.student_name -- 学生名称
                  ,xuanke.two_choose_one_subject_code wuliorlishi -- 二选一科目code
                  ,xuanke.mix_subject_name xuankezuhe -- 选科的组合，一共12个组合
                FROM
                  `exam_databoard`.`exam_score_transfer_for_bi` kaoshi 
                JOIN 
                    (SELECT 
                      data_id -- 学校id
                      ,grade_id
                      ,COUNT(*) zx_rs -- 在校人数
                    FROM
                      `khfw_uc`.`uc_user_student` t1 
                    WHERE del_flag = 0 
                    GROUP BY data_id, grade_id) xs 
                    ON kaoshi.school_code = xs.data_id 
                    AND kaoshi.grade_code = xs.grade_id
                JOIN `exam_business2`.`student_todo` todo -- 关联选科任务表
                    ON kaoshi.exam_id = todo.todo_name_code 
                    AND kaoshi.student_code = todo.student_id 
                    AND todo.todo_type = 1 -- 取第一志愿
                    AND todo.todo_status = 1 
                    AND todo.del_tag = 0 
                JOIN `exam_business2`.`student_choose_subject_volunteer` xuanke -- 关联选科任务表
                    ON todo.id = xuanke.student_todo_id 
                    AND xuanke.choose_type = 1 
                WHERE kaoshi.school_code = %s 
                  AND kaoshi.exam_id = %s 
                  AND kaoshi.is_del = 0 
                  AND kaoshi.grade_code = 10 
                  AND kaoshi.score_type IN (0, 2, 3)   -- 经研发确认score_type 为3 的数据也是属于正常考试分数  
                GROUP BY kaoshi.student_code
            '''%(self.school_id, exam_id)
            self.cursor.execute(sql)
            sqldata = self.cursor.fetchall()
            if not sqldata:
                self.xuankerenshu_2to1_list.append(0)
                self.wuli_renshu_list.append(0)
                self.lishi_renshu_list.append(0)
            else:
                wuli_or_lishi_list, xuanke_subject_list = [], []
                for s in sqldata:
                    wuli_or_lishi_list.append(s[2])
                    xuanke_subject_list.append(s[3])
                # wuli_or_lishi_list = [ i[2] for i in sqldata ]
                self.xuankerenshu_2to1_list.append(len(wuli_or_lishi_list))
                wuli_or_lishi_result = Counter(wuli_or_lishi_list)
                self.wuli_renshu_list.append(wuli_or_lishi_result.get(self.wuli_id, 0))
                self.lishi_renshu_list.append(wuli_or_lishi_result.get(self.lishi_id, 0))
                self.xuanke_subject_result.append(dict(Counter(xuanke_subject_list)))
        return self.xuankerenshu_2to1_list, self.wuli_renshu_list, self.lishi_renshu_list, self.xuanke_subject_result   


class get_score_data(object):
    def __init__(self,school_id,examlist):
        self.school_id=school_id
        self.examlist=examlist
        self.conn = pymysql.connect(host='rm-2zeo67yg67a61ancn4o.mysql.rds.aliyuncs.com',user='QA',password='hmk#%^&djofsdh',charset='utf8')
        self.cursor = self.conn.cursor()
        self.score_line_list = []    # 分数线 
        self.total_score_list = []    # 物理科目id
        self.exam_subject_list = []   # 考试科目


    def get_score_line_data(self):
        for exam_id in self.examlist:
            sql='''
                SELECT 
                  qingbei_line_score "清本线"
                  ,first_undergraduate_score "一本线"
                  ,second_undergraduate_score "二本线" 
                FROM
                  `exam_databoard`.`report_param_config` 
                WHERE school_code = %s AND exam_id = %s 
            '''%(self.school_id, exam_id)
            self.cursor.execute(sql)
            sqldata = self.cursor.fetchall()
            if not sqldata:
                self.score_line_list.append([0, 0, 0])
            else:
                self.score_line_list.append([sqldata[0][0], sqldata[0][1], sqldata[0][2]])
        return self.score_line_list


    # 第一版由于数据不全 暂时废弃
    # def get_total_score_data(self):
    #     for exam_id in self.examlist:
    #         sql='''
    #             SELECT 
    #               SUM(total_score) total_score 
    #             FROM
    #               `exam_business2`.`stu_subject_score` 
    #             WHERE school_code = %s AND exam_id = %s 
    #             GROUP BY student_code 
    #             ORDER BY total_score DESC  
    #         '''%(self.school_id, exam_id)
    #         self.cursor.execute(sql)
    #         sqldata = self.cursor.fetchall()
    #         if sqldata:
    #             total_score = [ s[0] for s in sqldata ]
    #         self.total_score_list.append(total_score)       
    #     return self.total_score_list


    def get_total_score_data(self):
        for exam_id in self.examlist:
            sql='''
                SELECT 
                  SUM(score) total_score 
                FROM
                  `exam_databoard`.`exam_score_transfer_for_bi`
                WHERE school_code = %s  
                  AND is_del = 0 
                  AND exam_id = %s 
                  AND score_type IN (0, 2, 3)   -- 经研发确认score_type 为3 的数据也是属于正常考试分数 
                GROUP BY student_code 
                ORDER BY total_score DESC
            '''%(self.school_id, exam_id)
            self.cursor.execute(sql)
            sqldata = self.cursor.fetchall()
            if sqldata:
                total_score = [ s[0] for s in sqldata ]
            self.total_score_list.append(total_score)       
        return self.total_score_list
 


    # 由于第一版没有关联考试科目表，暂时写死
    # def get_subject_score_data(self):
    #     all_subject_score_list = []
    #     self.get_exam_subject_data()
    #     for n in range(len(self.examlist)):
    #         exam_id = self.examlist[n]
    #         all_subject_score = {}
    #         for exam_subject, exam_name in self.exam_subject_list[n]:
    #             score_list = []
    #             sql='''
    #                 SELECT 
    #                   total_score 
    #                 FROM
    #                   `exam_business2`.`stu_subject_score` 
    #                 WHERE school_code = %s 
    #                   AND exam_id = %s
    #                   AND subject_code = %s 
    #                 ORDER BY total_score DESC 
    #             '''%(self.school_id, exam_id, exam_subject)
    #             self.cursor.execute(sql)
    #             sqldata = self.cursor.fetchall()
    #             if sqldata:
    #                 score_list = [ s[0] for s in sqldata ]
    #             all_subject_score[exam_name] = score_list
    #         all_subject_score_list.append(all_subject_score)       
    #     return all_subject_score_list


    def get_subject_score_data(self):
        subject_list = {
            100001: "语文",
            100002: "数学",
            100003: "物理",
            100004: "化学",
            100005: "生物",
            100006: "历史",
            100007: "政治",
            100008: "地理",
            100016: "英语",
        }
        return_score_list = []
        for n in range(len(self.examlist)):
            exam_id = self.examlist[n]
            all_subject_score = {}
            for subject_id in subject_list:
                sql='''
                    SELECT 
                      score 
                    FROM
                      `exam_databoard`.`exam_score_transfer_for_bi` 
                    WHERE school_code = %s 
                      AND exam_id = %s  
                      AND is_del = 0  
                      AND score_type IN (0, 2, 3) 
                      AND subject_code = %s 
                    GROUP BY student_code 
                    ORDER BY score DESC 
                '''%(self.school_id, exam_id, subject_id)
                self.cursor.execute(sql)
                sqldata = self.cursor.fetchall()
                if sqldata:
                    score_list = [ s[0] for s in sqldata ]
                all_subject_score[subject_list[subject_id]] = score_list
            return_score_list.append(all_subject_score)       
        return return_score_list

        



    def get_exam_subject_data(self):
        for exam_id in self.examlist:
            sql='''
                SELECT 
                  subject_code,
                  subject_name
                FROM
                  `exam_business2`.`exam_subject` 
                WHERE state = 0 
                  AND exam_base_id = %s 
            '''%(exam_id)
            self.cursor.execute(sql)
            sqldata = self.cursor.fetchall()
            if sqldata:
                self.exam_subject_list.append([ [s[0],s[1]] for s in sqldata ])       
        return self.exam_subject_list
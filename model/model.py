import json
import sqlite3
from spyne import Integer, Unicode
from spyne import ServiceBase, rpc

# Database setup
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    student_name TEXT NOT NULL,
    chinese_score INTEGER NOT NULL,
    math_score INTEGER NOT NULL,
    english_score INTEGER NOT NULL
)
''')
conn.commit()


class Student(object):
    def __init__(self, _id, _student_name, _chinese_score, _math_score, _english_score):
        self.id = _id
        self.student_name = _student_name
        self.chinese_score = _chinese_score
        self.math_score = _math_score
        self.english_score = _english_score


class Students(object):
    def get_student_list(self, current_page, page_size):
        offset = current_page * page_size
        cursor.execute('SELECT * FROM students LIMIT ? OFFSET ?', (page_size, offset))
        rows = cursor.fetchall()
        return [Student(*row) for row in rows]

    def add_student(self, _id, _student_name, _chinese_score, _math_score, _english_score):
        if self.query_student(_id) is not None:
            return None
        cursor.execute('INSERT INTO students (id, student_name, chinese_score, math_score, english_score) VALUES (?, ?, ?, ?, ?)', 
                      (_id, _student_name, _chinese_score, _math_score, _english_score))
        conn.commit()
        return Student(_id, _student_name, _chinese_score, _math_score, _english_score)

    def edit_student(self, _id, _student_name, _chinese_score, _math_score, _english_score):
        if self.query_student(_id) is None:
            return None
        cursor.execute('UPDATE students SET student_name = ?, chinese_score = ?, math_score = ?, english_score = ? WHERE id = ?',
                       (_student_name, _chinese_score, _math_score, _english_score, _id))
        conn.commit()
        return self.query_student(_id)

    def delete_student(self, id):
        student = self.query_student(id)
        if student is None:
            return None
        cursor.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        return student

    def query_student(self, _id):
        cursor.execute('SELECT * FROM students WHERE id = ?', (_id,))
        row = cursor.fetchone()
        if row:
            return Student(*row)
        return None
    
    def get_ranked_students(self, subject, current_page, page_size):
        offset = current_page * page_size
        valid_subjects = ['chinese_score', 'math_score', 'english_score']
        if subject not in valid_subjects:
            return []
        cursor.execute(f'SELECT * FROM students ORDER BY {subject} DESC LIMIT ? OFFSET ?', (page_size, offset))
        rows = cursor.fetchall()
        return [Student(*row) for row in rows]
    
    def get_average_score(self, subject):
        valid_subjects = ['chinese_score', 'math_score', 'english_score']
        if subject not in valid_subjects:
            return 0
        cursor.execute(f'SELECT AVG({subject}) FROM students')
        result = cursor.fetchone()
        return round(result[0], 2) if result[0] is not None else 0


student_mgr = Students()


class PyWebService(ServiceBase):
    ...

    @rpc(_returns=Unicode)
    def get_version(self):
        """
        获取系统版本
        :return:
        """
        return json.dumps({'version': 1.0})

    @rpc(Integer, Integer, _returns=Unicode)
    def get_student_list(self, current_page, page_size):
        """
        获取学生列表
        :return:
        """
        return json.dumps(student_mgr.get_student_list(current_page, page_size), default=lambda obj: obj.__dict__)

    @rpc(Integer, Unicode, Integer, Integer, Integer, _returns=Unicode)
    def add_student(self, id, student_name, chinese_score, math_score, english_score):
        """
        添加新学生
        :return:
        """
        result = student_mgr.add_student(id, student_name, chinese_score, math_score, english_score)
        if result is None:
            return json.dumps({"error": "id already exists"})
        return json.dumps(result, default=lambda obj: obj.__dict__)

    @rpc(Integer, Unicode, Integer, Integer, Integer, _returns=Unicode)
    def edit_student(self, id, student_name, chinese_score, math_score, english_score):
        """
        编辑学生信息
        :return:
        """
        result = student_mgr.edit_student(id, student_name, chinese_score, math_score, english_score)
        if result is None:
            return json.dumps({"error": "student not found"})
        return json.dumps(result, default=lambda obj: obj.__dict__)

    @rpc(Integer, _returns=Unicode)
    def delete_student(self, id):
        """
        删除学生
        :return:
        """
        result = student_mgr.delete_student(id)
        if result is None:
            return json.dumps({"error": "student not found"})
        return json.dumps(result, default=lambda obj: obj.__dict__)

    @rpc(Integer, _returns=Unicode)
    def query_student(self, id):
        """
        查询学生信息
        :return:
        """
        student = student_mgr.query_student(id)
        if student:
            return json.dumps(student, default=lambda obj: obj.__dict__)
        return json.dumps(None)
    
    @rpc(Unicode, Integer, Integer, _returns=Unicode)
    def get_ranked_students(self, subject, current_page, page_size):
        """
        按科目成绩排名获取学生列表
        :return:
        """
        return json.dumps(student_mgr.get_ranked_students(subject, current_page, page_size), default=lambda obj: obj.__dict__)
    
    @rpc(Unicode, _returns=Unicode)
    def get_average_score(self, subject):
        """
        获取指定科目的平均分
        :return:
        """
        average = student_mgr.get_average_score(subject)
        return json.dumps({"subject": subject, "average_score": average})

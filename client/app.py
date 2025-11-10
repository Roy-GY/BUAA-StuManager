from flask import Flask, request, jsonify, render_template
import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)

# SOAP client setup
wsdl_url = "http://127.0.0.1:9567/PyWebService/"
headers = {'content-type': 'text/xml;charset=UTF-8'}


# Home route
@app.route('/')
def home():
    return render_template('index.html')


# Route to render add user page
@app.route('/add_student_page')
def add_student_page():
    return render_template('add_student.html')


# Route to get student list
@app.route('/get_student_list', methods=['GET'])
def get_student_list():
    current_page = request.args.get('current_page', default=0, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:get_student_list>
                 <pyw:current_page>{current_page}</pyw:current_page>
                 <pyw:page_size>{page_size}</pyw:page_size>
              </pyw:get_student_list>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:get_student_listResult', namespace)
    if element is None:
        return jsonify({"error": "No data found"}), 404
    data = element.text
    return jsonify(data)


# Route to add a student
@app.route('/add_student', methods=['POST'])
def add_student():
    data = request.json

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:add_student>
                 <pyw:id>{data['id']}</pyw:id>
                 <pyw:student_name>{data['student_name']}</pyw:student_name>
                 <pyw:chinese_score>{data['chinese_score']}</pyw:chinese_score>
                 <pyw:math_score>{data['math_score']}</pyw:math_score>
                 <pyw:english_score>{data['english_score']}</pyw:english_score>
              </pyw:add_student>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    print(response.text)  # Debug print to see the SOAP response
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:add_studentResult', namespace)
    if element is None:
        return jsonify({"error": "Failed to add student"}), 500

    result = element.text
    if "error" in result:
        return result, 500
    return jsonify(result)


@app.route('/get_ranked_students', methods=['GET'])
def get_ranked_students():
    subject = request.args.get('subject', type=str)
    current_page = request.args.get('current_page', default=0, type=int)
    page_size = request.args.get('page_size', default=10, type=int)
    
    if subject not in ['chinese_score', 'math_score', 'english_score']:
        return jsonify({"error": "Invalid subject"}), 400

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:get_ranked_students>
                 <pyw:subject>{subject}</pyw:subject>
                 <pyw:current_page>{current_page}</pyw:current_page>
                 <pyw:page_size>{page_size}</pyw:page_size>
              </pyw:get_ranked_students>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:get_ranked_studentsResult', namespace)
    if element is None:
        return jsonify({"error": "No data found"}), 404
    data = element.text
    return jsonify(data)


@app.route('/get_average_score', methods=['GET'])
def get_average_score():
    subject = request.args.get('subject', type=str)
    
    if subject not in ['chinese_score', 'math_score', 'english_score']:
        return jsonify({"error": "Invalid subject"}), 400

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:get_average_score>
                 <pyw:subject>{subject}</pyw:subject>
              </pyw:get_average_score>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:get_average_scoreResult', namespace)
    if element is None:
        return jsonify({"error": "Failed to get average score"}), 500
    data = element.text
    return jsonify(data)


@app.route('/delete_student', methods=['DELETE'])
def delete_student():
    id = request.args.get('id', type=int)
    if id is None:
        return jsonify({"error": "Index is required"}), 400

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:delete_student>
                 <pyw:id>{id}</pyw:id>
              </pyw:delete_student>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:delete_studentResult', namespace)
    if element is None:
        return jsonify({"error": "Failed to delete student"}), 500

    result = element.text
    if "error" in result:
        return result, 500
    return jsonify(result)


@app.route('/query_student', methods=['GET'])
def query_student():
    student_id = request.args.get('id', type=int)
    if student_id is None:
        return jsonify({"error": "Student ID is required"}), 400

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:query_student>
                 <pyw:id>{student_id}</pyw:id>
              </pyw:query_student>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:query_studentResult', namespace)
    if element is None:
        return jsonify({"error": "Student not found"}), 404

    result = element.text
    return jsonify(result)


@app.route('/edit_student', methods=['PUT'])
def edit_student():
    student_id = request.args.get('id', type=int)
    student_name = request.args.get('student_name')
    chinese_score = request.args.get('chinese_score', type=int)
    math_score = request.args.get('math_score', type=int)
    english_score = request.args.get('english_score', type=int)

    if None in (student_id, student_name, chinese_score, math_score, english_score):
        return jsonify({"error": "All fields are required"}), 400

    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="PyWebService2">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:edit_student>
                 <pyw:id>{student_id}</pyw:id>
                 <pyw:student_name>{student_name}</pyw:student_name>
                 <pyw:chinese_score>{chinese_score}</pyw:chinese_score>
                 <pyw:math_score>{math_score}</pyw:math_score>
                 <pyw:english_score>{english_score}</pyw:english_score>
              </pyw:edit_student>
           </soapenv:Body>
        </soapenv:Envelope>
       """
    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    root = ET.fromstring(response.text)
    namespace = {'pyw': 'PyWebService2'}
    element = root.find('.//pyw:edit_studentResult', namespace)
    if element is None:
        return jsonify({"error": "Failed to edit student"}), 500

    result = element.text
    if "error" in result:
        return result, 500
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)

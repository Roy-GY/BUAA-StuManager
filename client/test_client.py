import requests
import json
import xml.etree.ElementTree as ET
from suds.client import Client


def test1():
    wsdl_url = "http://127.0.0.1:9567/PyWebService/?wsdl"
    client = Client(wsdl_url)  # 创建一个webservice接口对象
    # resp = client.service.get_version()  # 调用这个接口下的get_version方法，无参数
    resp = client.service.get_user_list(0, 10)  # 调用这个接口下的get_version方法，无参数
    print(json.loads(resp))


def test_2():
    wsdl_url = "http://127.0.0.1:9567/PyWebService/"
    headers = {'content-type': 'text/xml;charset=UTF-8',
               'User-Agent': 'Apache-HttpClient/4.5.5 (Java/16.0.1)',
               }
    namespace = 'PyWebService2'
    current_page = 0
    page_size = 10
    body = f"""
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:pyw="{namespace}">
           <soapenv:Header/>
           <soapenv:Body>
              <pyw:get_user_list>
                 <!--Optional:-->
                 <pyw:current_page>{current_page}</pyw:current_page>
                 <!--Optional:-->
                 <pyw:page_size>{page_size}</pyw:page_size>
              </pyw:get_user_list>
           </soapenv:Body>
        </soapenv:Envelope>
       """

    response = requests.post(wsdl_url, data=body, headers=headers, verify=False)
    print(response.text)
    # 将返回结果转换成Element对象
    root = ET.fromstring(response.text)

    # 定义命名空间
    namespace_ = {'web': f'{namespace}'}

    # 找到返回数据的元素
    element = root.find('.//{%s}get_user_listResult' % namespace, namespace_)

    if element is None:
        print("No data found")
        return None

    # 提取数据
    data = element.text
    # 打印数据
    print("=================================================================")
    print(data)


# test1()
test_2()

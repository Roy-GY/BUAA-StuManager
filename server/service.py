import sys, os
# 把项目根目录加入搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from spyne import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server
from model.model import PyWebService   

if __name__ == '__main__':
    soap_app = Application([PyWebService], 'PyWebService2',
                           in_protocol=Soap11(validator='lxml'),
                           out_protocol=Soap11())
    wsgi_app = WsgiApplication(soap_app)

    host = "0.0.0.0"
    port = 9567
    server = make_server(host, port, wsgi_app)
    print('BUAA-StuManager Started')
    print('http://' + host + ':' + str(port) + '/PyWebService/?wsdl')
    server.serve_forever()

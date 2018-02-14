def template(file_name):
    """
    模版函数，返回HTML字符串
    """
    with open('templates/' + file_name, encoding='utf-8') as f:
        content = f.read()
    return content


def index(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    return header + '\r\n' + body


def error(request):
    header = 'HTTP/1.1 404 NOT Found\r\nContent-Type: text/html\r\n'
    body = template('404.html')
    return header + '\r\n' + body


def login(request):
    if request.method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('login.html')
        return header + '\r\n' + body
    elif request.method == 'POST':
        data = request.form()
        if data['username'] == '200OK' and data['password'] == '123':
            body = template('login.html')
            body = body.replace('{{ message }}', '登陆成功')
        else:
            body = template('login.html')
            body = body.replace('{{ message }}', '登录失败')
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        return header + '\r\n' + body
    else:
        return error(request)


router_dict = {
    '/': index,
    '/login': login,
}

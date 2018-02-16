from models.user import User


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
        pass
    else:
        return error(request)


def register(request):
    if request.method == 'GET':
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = template('register.html')
        user_data = [user.username for user in User.filter_by(password='123')]
        body = body.replace('{{ message }}', '<br>'.join(user_data))
        return header + '\r\n' + body
    elif request.method == 'POST':
        data = request.form()
        User.create_obj(**data)
        body = template('register.html')
        body = body.replace('{{ message }}', '注册成功')
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        return header + '\r\n' + body
    else:
        return error(request)


router_dict = {
    '/': index,
    '/login': login,
    '/register': register,
}

from random import randint

from models.user import User


sessions = {}


def template(file_name):
    """
    模版函数，返回HTML字符串
    """
    with open('templates/' + file_name, encoding='utf-8') as f:
        content = f.read()
    return content


def index(request):
    if 'Cookie' in request.headers:
        session_id = request.headers['Cookie'].split(':', 1)[1]
        # 根据session_id取出用户
        username = sessions[session_id]
    else:
        username = 'nobody'
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    body = body.replace('{{ username }}', username)
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
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        if User.validate(data['username'], data['password']):
            # 产生一个32位0-9字符串
            session_id = ''.join(str(randint(0, 9)) for _ in range(32))
            # 保存session值
            sessions[session_id] = data['username']
            header += 'Set-Cookie: session_id:{}'.format(session_id)
            body = template('login.html')
            body = body.replace('{{ message }}', '登陆成功')
        else:
            body = template('login.html')
            body = body.replace('{{ message }}', '登录失败')
        return header + '\r\n' + body
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

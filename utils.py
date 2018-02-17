from models.user import User


def current_user(request):
    from routes import sessions
    if 'Cookie' in request.headers:
        session_id = request.headers['Cookie'].split(':', 1)[1]
        # 根据session_id取出用户
        user_id = sessions.get(session_id, None)
        if not user_id:
            return None
        return User.get_by(id=user_id)
    else:
        return None


def template(file_name):
    """
    模版函数，返回HTML字符串
    """
    with open('templates/' + file_name, encoding='utf-8') as f:
        content = f.read()
    return content


def redirect(new_route):
    """
    重定向函数
    """
    header = get_headers(code=302, Location=new_route)
    return header + '\r\n\r\n'


def get_headers(code=200, **extra_headers):
    """
    生成response头部函数
    """
    header = 'HTTP/1.1 {} OK\r\nContent-Type: text/html\r\n'.format(code)
    data = []
    for k, v in extra_headers.items():
        data.append('{}: {}'.format(k, v))
    header += '\r\n'.join(data)
    return header


def login_required(f):
    def decorator(request):
        user = current_user(request)
        if user:
            return f(request)
        else:
            return get_headers(code=302, Location='/login') + '\r\n'
    return decorator

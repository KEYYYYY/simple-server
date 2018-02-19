import os

from jinja2 import Environment, FileSystemLoader

from models.user import User
from models.todo import Todo

# __file__ 就是本文件的名字
# 得到用于加载模板的目录
path = '{}/templates/'.format(os.path.dirname(__file__))
# 创建一个加载器, jinja2 会从这个目录中加载模板
loader = FileSystemLoader(path)
# 用加载器创建一个环境, 有了它才能读取模板文件
env = Environment(loader=loader)


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


def template(path, **kwargs):
    """
    本函数接受一个路径和一系列参数
    读取模板并渲染返回
    """
    t = env.get_template(path)
    return t.render(**kwargs)


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


def owner_required(f):
    def decorator(request):
        user = current_user(request)
        id = request.form().get('id', -1)
        obj = Todo.get_by(id=int(id))
        if obj.user_id == user.id:
            return f(request)
        else:
            return get_headers(code=302, Location='/login') + '\r\n'
    return decorator

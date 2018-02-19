from random import randint

from models.todo import Todo
from models.user import User
from utils import (current_user, get_headers, login_required, owner_required,
                   template)

sessions = {}


@login_required
def index(request):
    if request.method == 'GET':
        user = current_user(request)
        todos = Todo.filter_by(user_id=user.id)
        body = template('index.html', username=user.username, todos=todos)
        return get_headers() + '\r\n' + body
    if request.method == 'POST':
        data = request.form()
        Todo.create_obj(user_id=current_user(request).id, **data)
        return get_headers(code=302, Location='/') + '\r\n'


@owner_required
@login_required
def delete(request):
    data = request.form()
    obj_id = data.get('id', -1)
    Todo.delete(int(obj_id))
    return get_headers(code=302, location='/') + '\r\n'


@owner_required
@login_required
def update(request):
    if request.method == 'GET':
        id = request.form().get('id', -1)
        todo = Todo.get_by(id=int(id))
        body = template('update.html', id=id, title=todo.title)
        return get_headers() + body + '\r\n'
    elif request.method == 'POST':
        data = request.form()
        obj_id = data.get('id', -1)
        # 这里id是整型
        todo = Todo.get_by(id=int(obj_id))
        todo.title = data['title']
        todo.save()
        return get_headers(code=302, Location='/') + '\r\n'
    else:
        return error(request)


def error(request):
    header = get_headers(code=404)
    body = template('404.html')
    return header + '\r\n' + body


def login(request):
    if request.method == 'GET':
        header = get_headers()
        body = template('login.html')
        return header + '\r\n' + body
    elif request.method == 'POST':
        data = request.form()
        user = User.validate(data['username'], data['password'])
        if user:
            # 产生一个32位0-9字符串
            session_id = ''.join(str(randint(0, 9)) for _ in range(32))
            # 保存session值
            sessions[session_id] = user.id
            kwargs = {
                'Location': '/',
                'Set-Cookie': 'session_id:{}'.format(session_id),
            }
            # 设置返回头部信息，制造重定向
            header = get_headers(code=302, **kwargs)
            return header + '\r\n'
        else:
            header = get_headers()
            body = template('login.html', message='登录失败')
            return header + '\r\n' + body
    else:
        return error(request)


def register(request):
    if request.method == 'GET':
        header = get_headers()
        body = template('register.html')
        return header + '\r\n' + body
    elif request.method == 'POST':
        data = request.form()
        global next_id
        User.create_obj(**data)
        body = template('register.html', messgae='注册成功')
        header = get_headers()
        return header + '\r\n' + body
    else:
        return error(request)


router_dict = {
    '/': index,
    '/login': login,
    '/register': register,
    '/delete': delete,
    '/update': update,
}

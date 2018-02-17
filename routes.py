from random import randint

from models.todo import Todo
from models.user import User
from utils import current_user, get_headers, login_required, template

sessions = {}
next_id = 1


@login_required
def index(request):
    if request.method == 'GET':
        user = current_user(request)
        username = user.username
        body = template('index.html')
        body = body.replace('{{ username }}', username)
        todos = [str(todo.title) for todo in Todo.filter_by(user_id=user.id)]
        body = body.replace('{{ todos }}', '<br>'.join(todos))
        return get_headers() + '\r\n' + body
    if request.method == 'POST':
        data = request.form()
        Todo.create_obj(user_id=current_user(request).id, **data)
        return get_headers(code=302, Location='/') + '\r\n'


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
            body = template('login.html')
            body = body.replace('{{ message }}', '登录失败')
            return header + '\r\n' + body
    else:
        return error(request)


def register(request):
    if request.method == 'GET':
        header = get_headers()
        body = template('register.html')
        user_data = [user.username for user in User.filter_by(password='123')]
        body = body.replace('{{ message }}', '<br>'.join(user_data))
        return header + '\r\n' + body
    elif request.method == 'POST':
        data = request.form()
        global next_id
        User.create_obj(id=next_id, **data)
        next_id += 1
        body = template('register.html')
        body = body.replace('{{ message }}', '注册成功')
        header = get_headers()
        return header + '\r\n' + body
    else:
        return error(request)


router_dict = {
    '/': index,
    '/login': login,
    '/register': register,
}

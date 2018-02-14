import socket
import ssl
import re


def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    '''
    if url[:7] == 'http://':
        protocol = 'http'
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        protocol = 'http'
        u = url

    i = u.find('/')
    if u.find('/') == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    port_dict = {
        'http': 80,
        'https': 443,
    }
    port = port_dict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = h[1]
    return protocol, host, port, path


def response_by_socket(s):
    """
    通过socket取出服务器返回的信息
    """
    response_b = b''
    while 1:
        r = s.recv(1024)
        if len(r) == 0:
            break
        response_b += r
    return response_b.decode('utf-8')


def parse_response(response_str):
    """
    根据返回的信息解析出method和path以及body
    """
    h, body = response_str.split('\r\n\r\n', 1)

    # ok
    # print('请求的头部为', h + '\n')
    # print('body为', b + '\n')

    s, headers = h.split('\r\n', 1)

    # 请求头部字典
    headers_dict = {}
    for i in headers.split('\r\n'):
        headers_dict[i.split(': ', 1)[0]] = i.split(': ', 1)[1]
    code = s.split()[1]
    if code in ('301', '302', '303'):
        get(headers_dict['Location'])
    else:
        parse_body(body)


def parse_body(body):
    p_name = re.compile(
        r'<span class="title">(\w+)</span>'
    )
    p_grade = re.compile(
        r'<span class="rating_num" property="v:average">(\d.\d)</span>')
    p_i = re.compile(
        r'<span class="inq">(\w+)</span>'
    )
    # p_p = re.compile(
    #     r'<span>(\d+)人评价</span>'
    # )
    name_list = []
    grade_list = []
    inq_list = []
    # p_list = []
    for item in p_name.finditer(body):
        name_list.append(item.group(1))
    for item in p_grade.finditer(body):
        grade_list.append(item.group(1))
    for item in p_i.finditer(body):
        inq_list.append(item.group(1))
    # for item in p_p.finditer(body):
    #     p_list.append(item.group(1))
    for name, grade, inq in zip(name_list, grade_list, inq_list):
        print(name, grade, inq)


def get(url):
    """
    向给定url发起请求，得到body
    """
    protocol, host, port, path = parsed_url(url)
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    s.connect((host, port))

    req_str = 'GET {path} HTTP/1.1\r\nhost: {host}\r\nConnection: close\r\n\r\n'.format(
        path=path,
        host=host,
    )
    s.send(req_str.encode('utf-8'))
    response_str = response_by_socket(s)
    parse_response(response_str)


def main():
    url = 'http://movie.douban.com/top250'
    get(url)


if __name__ == '__main__':
    main()

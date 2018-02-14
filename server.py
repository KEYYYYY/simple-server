import socket


def resove_req(request_str):
    """
    处理请求：
    1. 解析出method和path
    2. 根据path选取路由函数
    3. 执行函数返回结果
    """
    method, path, headers_dict, body = parse_request(request_str)
    response = response_by_path(path)
    return response


def parse_request(request_str):
    """
    解析出method和path
    """
    h, body = request_str.split('\r\n\r\n', 1)

    # ok
    # print('请求的头部为', h + '\n')
    # print('body为', b + '\n')

    s, headers = h.split('\r\n', 1)

    # 请求头部字典
    headers_dict = {}
    for i in headers.split('\r\n'):
        headers_dict[i.split(': ', 1)[0]] = i.split(': ', 1)[1]
    return s.split()[0], s.split()[1], headers_dict, body


def response_by_path(path):
    '''
    根据请求path得到响应函数并执行
    '''
    router_dict = {
        '/': index,
    }
    view_func = router_dict.get(path, error)
    response = view_func()
    with open('response_log.txt', 'a') as f:
        f.write(response + '\n')
    return response


def index():
    header = 'HTTP/1.1 200 ok\r\nContent-Type: text/html\r\n'
    return header + '\r\n' + '<h1>Hello World</h1>'


def error():
    header = 'HTTP/1.1 404 NOT Found\r\nContent-Type: text/html\r\n'
    return header + '\r\n' + '<h1>Not Found</h1>'


def run(host='', port=2000):
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            s.listen(5)
            conn, address = s.accept()
            request = conn.recv(1024)
            request_str = request.decode('utf-8')
            with open('request_log.txt', 'a') as f:
                f.write('请求的主机信息' + str(address) + '\n')
                f.write(request_str)
            response = resove_req(request_str)
            conn.sendall(response.encode('utf-8'))
            conn.close()


if __name__ == '__main__':
    run()

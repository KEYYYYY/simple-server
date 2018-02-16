import socket
import routes


class Request:
    def __init__(self, request_str):
        self._parse(request_str)

    def _parse(self, request_str):
        """
        根据请求字符串解析需要的信息
        """
        h, body = request_str.split('\r\n\r\n', 1)
        self.body = body

        s, headers = h.split('\r\n', 1)
        s = s.split(maxsplit=2)
        self.method = s[0]
        path_and_qs = s[1]

        # 如果?在http报文的第一行出现说明请求的path后面跟有参数
        if '?' in path_and_qs:
            self.path, self.qs = path_and_qs.split('?', 1)
        else:
            self.path = path_and_qs
            self.qs = ''

        # 请求头部字典
        headers_dict = {}
        for i in headers.split('\r\n'):
            headers_dict[i.split(': ', 1)[0]] = i.split(': ', 1)[1]
        self.headers = headers_dict

    def form(self):
        """
        解析请求的数据
        """
        data = {}
        if self.method == 'POST':
            # 如果是POST请求则数据在body里
            body_list = self.body.split('&')
            for item in body_list:
                k, v = item.split('=')
                data[k] = v
        if self.method == 'GET':
            # 如果是GET请求数据在url上
            data_list = self.qs.split('&')
            for item in data_list:
                k, v = item.split('=')
                data[k] = v
        return data


def resove_req(request_str):
    """
    处理请求：
    1. 解析出method和path
    2. 根据path选取路由函数
    3. 执行函数返回结果
    """
    request = Request(request_str)
    response = get_response(request)
    return response


def get_response(request):
    '''
    根据请求path得到响应函数并执行
    '''
    view_func = routes.router_dict.get(request.path, routes.error)
    response = view_func(request)
    with open('response_log.txt', 'a') as f:
        f.write(response + '\n')
    return response


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

import os
import tornado.ioloop
import tornado.httpserver
import tornado.escape
from tornado.options import define, options
# ./application/server.pyからApplicationクラスをインポート
from application.server import Application

# Define command line arguments
# 起動時のオプションを指定する
define("port", default=3000, help="run on the given port", type=int)


def main():
    '''
    mainの関数
    ここから始まる
    '''
    # tornadoのサーバーを起動する
    # tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    port = int(os.environ.get("PORT", options.port))
    print("server is running on port {0}".format(port))
    http_server.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex)

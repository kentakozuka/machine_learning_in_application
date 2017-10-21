# OSに依存した機能を使うための標準ライブラリ
import os
import tornado.web
from ml.model_api import ModelAPI
from ml.data_processor import DataProcessor
from ml.resource import Resource


DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/feedbacks.txt")


class IndexHandler(tornado.web.RequestHandler):
    '''
    ルートディレクトリにリクエストがあった場合に呼び出される
    '''
    def get(self):
        self.render("index.html", title="title")


class PredictionHandler(tornado.web.RequestHandler):
    '''
    /predictにリクエストが会った時に呼び出される
    '''

    # POSTメソッドのハンドラ
    def post(self):

        # レスポンス用マップを作成
        resp = {"result": str(-1)}
        # 送られてきたデータを受け取る
        data = self.get_arguments("data[]")

        r = Resource()

        # path が実在するディレクトリの場合
        if not os.path.isdir(r.model_path):
            # model.pyのインポート
            from ml.model import NumberRecognizeNN
            # trainer.pyのインポート
            from ml.trainer import Trainer

            # モデル作成クラス (Chainer)
            model = NumberRecognizeNN(r.INPUT_SIZE, r.OUTPUT_SIZE)
            # トレーニングクラス
            trainer = Trainer(model, r)
            # トレーニングデータを取得
            x, y = r.load_training_data()
            # トレーニング実施
            trainer.train(x, y)

        # モデルをAPIに保存
        api = ModelAPI(r)

        if len(data) > 0:
            _data = [float(d) for d in data]
            # 送られてきたデータから予測値を算出
            predicted = api.predict(_data)
            # レスポンスにデータを格納
            resp["result"] = str(predicted[0])

        # データを送信
        self.write(resp)


class FeedbackHandler(tornado.web.RequestHandler):
    '''
    /feedbackにリクエストがあった時に呼び出される
    '''

    # POSTメソッドのハンドラ
    def post(self):
        data = self.get_arguments("data[]")
        if len(data) > 0:
            r = Resource()
            r.save_data(DATA_PATH, data)
        else:
            result = "feedback format is wrong."

        resp = {"result": ""}
        self.write(resp)


class Application(tornado.web.Application):
    '''
    Applicationオブジェクトは、アプリケーション全体の設定をするために使われます。
    run_application.pyの中でインスタンス化され、HTTPServerに渡される。
    '''

    # コンストラクタ
    def __init__(self):
        # ハンドラを設定する
        handlers = [
            (r"/", IndexHandler),
            (r"/predict", PredictionHandler),
            (r"/feedback", FeedbackHandler),
        ]

        # 設定
        settings = dict(
            template_path   = os.path.join(os.path.dirname(__file__), "templates"),
            static_path     = os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret   = os.environ.get("SECRET_TOKEN", "__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__"),
            xsrf_cookies    = True,
            debug           = True,
        )

        super(Application, self).__init__(handlers, **settings)

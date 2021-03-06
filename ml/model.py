import chainer
import chainer.functions as F
import chainer.links as L


class NumberRecognizeNN(chainer.Chain):
    '''
    文字認識クラス
    Chainerを継承
    ここは要勉強
    '''
    
    def __init__(self, input_size, output_size, hidden_size=200, layer_size=3):
        '''
        コンストラクタ
        '''

        # 入力ノード数
        self.input_size     = input_size
        # 出力ノード数
        self.output_size    = output_size
        # 中間ノード数
        self.hidden_size    = hidden_size
        # レイヤー数
        self.layer_size     = layer_size

        # 親クラスのコンストラクタを呼び出し
        super(NumberRecognizeNN, self).__init__(
            l1  =   L.Linear(self.input_size, hidden_size), # 1レイヤー
            l2  =   L.Linear(hidden_size, hidden_size),     # 2レイヤー
            l3  =   L.Linear(hidden_size, self.output_size),# 3レイヤー
        )

    # 伝播の処理
    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        o = F.sigmoid(self.l3(h2))
        return o

from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    title = "青空文庫のランキングを抽出するやつ"

    # 時期
    select_date = request.form.get('select_date')

    # # ランキング種別
    # select_type = request.form.get('select_type')

    print("date:", select_date)
    # print("type:", select_type)

    dic_dates = {
        '2021-06-01': '2021年6月',
        '2021-05-01': '2021年5月',
        '2021-04-01': '2021年4月',
        '2021-03-01': '2021年3月',
    }

    default_date = '2021-05-01'

    ranking = [
        {
            'rank': 1,
            'title': '〔雨ニモマケズ〕',
            'title_link': 'https://www.aozora.gr.jp/cards/000081/files/45630_23908.html',
            'author': '宮沢賢治',
            'author_link': 'https://www.aozora.gr.jp/index_pages/person81.html'
        },
        {
            'rank': 2,
            'title': 'こころ',
            'title_link': 'https://www.aozora.gr.jp/cards/000148/files/773_14560.html',
            'author': '夏目漱石',
            'author_link': 'https://www.aozora.gr.jp/index_pages/person148.html'
        },{
            'rank': 3,
            'title': '星めぐりの歌',
            'title_link': 'https://www.aozora.gr.jp/cards/000081/files/45630_23908.html',
            'author': '宮沢賢治',
            'author_link': 'https://www.aozora.gr.jp/index_pages/person81.html'
        },
    ]

    return render_template('index.html',
                           title=title,
                           select_date=select_date,
                           dic_dates=dic_dates,
                           default_date=default_date,
                           ranking=ranking)

# おまじない
if __name__ == "__main__":
    app.run(debug=True)

from lib import *

from flask import Flask, render_template, request
app = Flask(__name__)

def get_dic_dates(df):
    timestamps = get_timestamp_list(df)
    dates = get_date_list(df)

    dic_dates = {}
    for x in zip(timestamps, dates):
        dic_dates[x[0]] = x[1]
    
    return dic_dates

@app.route('/', methods=['GET', 'POST'])
def index():
    title = "青空文庫のランキングを抽出するやつ"

    # ランキングのリンク一覧をDataFrameにする
    df = extract_ranking_links_as_data_frame()

    # 時期の一覧を取得する
    dic_dates = get_dic_dates(df)

    # 時期の初期値：最新の日時
    default_date = get_latest_timestamp(df)

    # フォーム：時期を選択する
    select_date = request.form.get('select_date')
    if select_date is None:
        select_date = default_date
    print("date:", select_date)

    ranking = [
        {
            'rank': 1,
            'title': '〔雨ニモマケズ〕',
            'title_link': 'https://www.aozora.gr.jp/cards/000081/files/45630_23908.html',
            'author': '宮沢賢治',
        },
        {
            'rank': 2,
            'title': 'こころ',
            'title_link': 'https://www.aozora.gr.jp/cards/000148/files/773_14560.html',
            'author': '夏目漱石',
        },{
            'rank': 3,
            'title': '星めぐりの歌',
            'title_link': 'https://www.aozora.gr.jp/cards/000081/files/45630_23908.html',
            'author': '宮沢賢治',
        },
    ]

    return render_template('index.html',
                           title=title,
                           select_date=select_date,
                           dic_dates=dic_dates,
                           ranking=ranking)

# おまじない
if __name__ == "__main__":
    app.run(debug=True)

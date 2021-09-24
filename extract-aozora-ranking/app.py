from lib import *

from flask import Flask, render_template, request, redirect
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

    # 時期に対応するランキングURLを取得する
    url_rank, _ = get_urls_by_timestamp(df, select_date)

    # 時期に対応するランキングをDataFrameとして取得する
    df_rank = get_df_ranking(url_rank)

    # ランキングを辞書に変換する
    # ranking = [
    #     {
    #         'rank': 1,
    #         'title': '〔雨ニモマケズ〕',
    #         'title_link': 'https://www.aozora.gr.jp/cards/000081/files/45630_23908.html',
    #         'author': '宮沢賢治',
    #     },
    #     ...
    # ]
    ranking = df_rank.to_dict(orient='records')

    # テンプレートからHTMLを生成する
    return render_template('index.html',
                           title=title,
                           select_date=select_date,
                           dic_dates=dic_dates,
                           ranking=ranking)

# XHTMLページにリダイレクトする
@app.route('/xhtml', methods=['GET'])
def xhtml():
    # 作品ページのURLを取得
    url_card = request.args.get('q')

    # XHTMLのURLを取得
    url_xhtml = get_xhtml_link(url_card)

    # XHTMLページにリダイレクトする
    return redirect(url_xhtml, code=302)

# おまじない
if __name__ == "__main__":
    app.run(debug=True)

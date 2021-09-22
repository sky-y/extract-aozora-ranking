from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "Hello World"
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

    return render_template('index.html',
                           title=title,
                           select_date=select_date,
                           dic_dates=dic_dates,
                           default_date=default_date)

# おまじない
if __name__ == "__main__":
    app.run(debug=True)

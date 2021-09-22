from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    name = "Hello World"
    title = "青空文庫のランキングを抽出するやつ"

    # 時期
    select_date = request.form.get('select_date')

    # ランキング種別
    select_type = request.form.get('select_type')

    print("date:", select_date)
    print("type:", select_type)

    return render_template('index.html',
                           title=title,
                           select_date=select_date,
                           select_type=select_type)

# おまじない
if __name__ == "__main__":
    app.run(debug=True)

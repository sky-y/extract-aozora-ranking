from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import re

KEY_TIMESTAMP = 'タイムスタンプ'
KEY_URL_XHTML = 'URL (XHTML版)'
KEY_URL_TXT = 'URL (テキスト版)'
KEY_DATE = '年月'

# Chrome Optionsの設定（headlessモード）
# https://tanuhack.com/stable-selenium/
options = Options()
options.add_argument('--headless')                 # headlessモードを使用する
options.add_argument('--disable-gpu')              # headlessモードで暫定的に必要なフラグ(そのうち不要になる)
options.add_argument('--disable-extensions')       # すべての拡張機能を無効にする。ユーザースクリプトも無効にする
options.add_argument('--proxy-server="direct://"') # Proxy経由ではなく直接接続する
options.add_argument('--proxy-bypass-list=*')      # すべてのホスト名
options.add_argument('--start-maximized')          # 起動時にウィンドウを最大化する


# ランキング表のリンク一覧（日付順で並んでいる表）をリストにして返す
# リスト構造: [日付, URL(XHTML版ランキング), URL(テキスト版ランキング)]
def extract_ranking_links_as_list():
    browser = webdriver.Chrome(chrome_options=options)
    browser.get('https://www.aozora.gr.jp/access_ranking/')
    
    tables = browser.find_elements_by_tag_name('table')

    # 2番目のtableに最新のランキング項目が入っている
    table_index = 1
    table = tables[table_index]

    # ランキング表のリンク一覧を抽出する
    trs = table.find_elements_by_tag_name('tr')

    rank_list = []
    for tr in trs:    
        tds = tr.find_elements_by_tag_name('td')
        str_date = tds[0].text
        str_url_xhtml = tds[1].find_element_by_tag_name('a').get_attribute('href')
        str_url_txt = tds[2].find_element_by_tag_name('a').get_attribute('href')

        rank_list.append([str_date, str_url_xhtml, str_url_txt])
    
    browser.quit()
    return rank_list

# ランキング表のリンク一覧をDataFrameとして返す
def extract_ranking_links_as_data_frame():
    link_list = extract_ranking_links_as_list()

    df = pd.DataFrame(link_list, columns=[KEY_DATE, KEY_URL_XHTML, KEY_URL_TXT])
    df[KEY_TIMESTAMP] = pd.to_datetime(df[KEY_DATE], format='%Y年%m月')

    # 新しい方を上にする
    df_sorted = df.sort_values(by=KEY_TIMESTAMP, ascending=False) 
    return df_sorted

# タイムスタンプのリストを返す
def get_timestamp_list(df):
    return df[KEY_TIMESTAMP].dt.strftime('%Y-%m-%d').tolist()

# 最新のタイムスタンプを取得する
def get_latest_timestamp(df):
    return df[KEY_TIMESTAMP][0].strftime('%Y-%m-%d')

# 日付のリストを返す
def get_date_list(df):
    return df[KEY_DATE].tolist()

# DataFrameから特定のタイムスタンプを持つ行を抽出する
def extract_df_by_timestamp(df, timestamp):
    return df[df[KEY_TIMESTAMP] == timestamp]

# 特定のタイムスタンプにおいて、URL（XHTML版、テキスト版のそれぞれ）を返す
def get_urls_by_timestamp(df, timestamp):
    df_target = extract_df_by_timestamp(df, timestamp).iloc[0]
    return df_target[KEY_URL_XHTML], df_target[KEY_URL_TXT]

# ランキング表のデータフレームを取得する
def get_df_ranking(url):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)

    table = browser.find_elements_by_tag_name("table")[0]
    table_html = table.get_attribute('outerHTML')
    browser.quit()

    # DataFrameとしてHTMLを読み込む
    # ただしこの時点ではリンクは読み込まれない
    table_pd = pd.read_html(table_html, header=0)[0]

    # 別途BeautifulSoupでHTMLを読み込み、作品のリンクを取得する
    table_bs = BeautifulSoup(table_html, 'html.parser')
    a_cards_bs = table_bs.find_all('a', href=re.compile('https://www\.aozora\.gr\.jp/cards/'))
    table_pd['リンク（作品）'] = [link.get('href') for link in a_cards_bs]

    # ラベルを変更し、不要な列を削除
    labels = ['rank', 'title', 'author', 'access', 'title_link']
    table_pd = table_pd.set_axis(labels, axis='columns')
    table_pd = table_pd.drop('access', axis=1)
    
    return table_pd

# 特定の順位のタイトル・URL・著者名を取得する
def extract_info_from_table_element(url, rank_index):
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    table = browser.find_elements_by_tag_name("table")[0]
    
    trs = table.find_elements_by_tag_name('tr')
    
    title = trs[rank_index].find_elements_by_tag_name('td')[1].text
    url = trs[rank_index].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').get_attribute('href')
    author = trs[rank_index].find_elements_by_tag_name('td')[2].text
    
    browser.quit()
    return title, url, author

def get_xhtml_link(url_sakuhin):
    # 作品ページに飛ぶ
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url_sakuhin)
    
    # リンクに「html」が含まれる要素を抽出する（XHTML版）
    extension = 'html'
    elems_link = browser.find_elements_by_partial_link_text(extension)
    url_xhtml_content = elems_link[0].get_attribute('href')
    browser.quit()

    return url_xhtml_content

# 作品ページのURLからXHTMLソースを取得する
def get_xhtml(url_sakuhin):
    url_xhtml_content = get_xhtml_link(url_sakuhin)
    
    # XHTML本体（ソース）に飛ぶ
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url_xhtml_content)

    content = browser.page_source
    
    browser.quit()
    return content

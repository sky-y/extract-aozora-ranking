from selenium import webdriver
import pandas as pd
import requests
import zipfile
import codecs

# DataFrame用の列
KEY_TIMESTAMP = 'タイムスタンプ'
KEY_URL_XHTML = 'URL (XHTML版)'
KEY_URL_TXT = 'URL (テキスト版)'
KEY_DATE = '年月'

# ランキング表のリンク一覧（日付順で並んでいる表）をリストにして返す
# リスト構造: [日付, URL(XHTML版ランキング), URL(テキスト版ランキング)]
def extract_ranking_links_as_list():
    browser = webdriver.Chrome()
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

# DataFrameから特定のタイムスタンプを持つ行を抽出する
def extract_df_by_timestamp(df, timestamp):
    return df[df[KEY_TIMESTAMP] == timestamp]

# 特定のタイムスタンプにおいて、URL（XHTML版、テキスト版のそれぞれ）を返す
def get_urls_by_timestamp(df, timestamp):
    df_target = extract_df_by_timestamp(df, timestamp)
    return df_target.at[0,KEY_URL_XHTML], df_target.at[0,KEY_URL_TXT]

# 特定の順位のタイトル・URL・著者名を取得する
def extract_info_from_table_element(url, rank_index):
    browser = webdriver.Chrome()
    browser.get(url)
    table = browser.find_elements_by_tag_name("table")[0]
    
    trs = table.find_elements_by_tag_name('tr')
    
    title = trs[rank_index].find_elements_by_tag_name('td')[1].text
    url = trs[rank_index].find_elements_by_tag_name('td')[1].find_element_by_tag_name('a').get_attribute('href')
    author = trs[rank_index].find_elements_by_tag_name('td')[2].text
    
    browser.quit()
    return title, url, author

# 作品ページのURLからXHTMLソースを取得する
def get_xhtml(url_sakuhin):
    # 作品ページに飛ぶ
    browser = webdriver.Chrome()
    browser.get(url_sakuhin)
    
    # リンクに「html」が含まれる要素を抽出する（XHTML版）
    extension = 'html'
    elems_link = browser.find_elements_by_partial_link_text(extension)
    url_xhtml_content = elems_link[0].get_attribute('href')
    
    # XHTML本体（ソース）に飛ぶ
    browser.get(url_xhtml_content)
    
    browser.quit()
    return browser.page_source
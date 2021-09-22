from lib import *
import pandas as pd

time_stamp = '2021-06-01'
rank = 1

df = extract_ranking_links_as_data_frame()
url_rank, _ = get_urls_by_timestamp(df, time_stamp)

print(url_rank)

title, url_sakuhin, author = extract_info_from_table_element(url_rank, rank)

print(title, url_sakuhin, author)

xhtml_content = get_xhtml(url_sakuhin)

print(xhtml_content)
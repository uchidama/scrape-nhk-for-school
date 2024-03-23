# seleniumでNHK for Schoolのプログラム一覧を取得する
# 
# 必要なライブラリのインストール
# pip3 install selenium
# pip3 install chromedriver-binary-auto

import csv
import chromedriver_binary  # chromedriver-binary-autoをインポート
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin  # URLを結合するために必要
import os  # osモジュールをインポート

# あらすじページを処理する関数
def process_outline_page(outline_url, driver):
    driver.get(outline_url)

    # ページが完全にロードされるまで待機
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'item'))
        )
    except TimeoutException:
        # レイアウト違いでタイムアウトすることがあるので、その場合はスキップする
        print("Timeout while loading outline page:", outline_url)
        return ""

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='item')

    result_text = ""  # 結果を格納するための文字列

    for div in divs:
        div_title = div.find('div', class_='title')
        if div_title:
            span_text = div_title.find('span').text if div_title.find('span') else 'No span text found'
            # spanタグを除外して残りのテキストを取得
            span_tag = div_title.find('span')
            if span_tag:
                span_tag.extract()  # spanタグを除去
            remaining_text = div_title.text.strip()  # 残りのテキスト

        summary = div.find('p', class_='summary')

        #print("div_title_span:", span_text)
        #print("div_title_remaining:", remaining_text)
        #print("summary:", summary.text if summary else 'No summary found')

        # 結果文字列に各要素を追加
        result_text += f"【{span_text}】\n{remaining_text}\n{summary.text if summary else 'No summary found'}\n\n"

    return result_text
        
# 番組ページを処理する関数
def process_program_page(program_url, driver, title, csv_writer):
    driver.get(program_url)

    # ページが完全にロードされるまで待機
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'itemList'))
        )
    except TimeoutException:
        # レイアウト違いでタイムアウトすることがあるので、その場合はスキップする
        print("Timeout while loading program page:", program_url)
        return


    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find_all('div', class_='itemList')
    for div in divs:
        div_subtitle = div.find('div', class_='subTitle')
        div_caption = div.find('div', class_='caption')
        a_tag = div.find('a')
        episode_url = a_tag['href']
        print("div_subtitle:", div_subtitle.text)
        print("div_caption:", div_caption.text)
        print("episode_url:", episode_url)

        # hrefに '?das_id=' が含まれている場合、別の関数を呼び出す
        outline_url = ""
        outline_text = ""

        if 'bangumi/?das_id=' in episode_url:
            outline_url = episode_url.replace("bangumi/", "outline/")
            outline_text = process_outline_page(outline_url, driver)
            time.sleep(1)
        
        csv_writer.writerow([title,
                             program_url,
                             div_subtitle.text if div_subtitle else '',
                             episode_url,
                             div_caption.text if div_caption else '',
                             outline_url,
                             outline_text])
        
        

# chromedriver-binary-auto がパスを自動的に設定するので、直接 WebDriver を呼び出せます
driver = webdriver.Chrome()

# まずは番組一覧ページを開く
url = 'https://www.nhk.or.jp/school/program/'
driver.get(url)

WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'itemKyouka'))
)

# JavaScriptが実行された後のHTMLを取得
html = driver.page_source

# HTML を表示（または解析する）
#print(html)

soup = BeautifulSoup(html, 'html.parser')

# classがitemKyoukaのdivタグを抽出
divs = soup.find_all('div', class_='itemKyouka')

# 出力ディレクトリを作成
output_directory = 'dataset_root/data/'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)  # ディレクトリが存在しない場合は作成

output_file = os.path.join(output_directory, 'nhk_for_school_outline_data.csv')
#output_file = 'dataset_root/data/nhk_for_school_outline_data.csv'

# 結果をテキストファイルに書き込む
with open(output_file, 'w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['title', 'program_url', 'subtitle', 'episode_url', 'caption', 'outline_url', 'outline'])

    for div in divs:
        div_title = div.find('div', class_='title')
        print(div_title.text)
        a_tag = div.find('a')
        if a_tag and 'href' in a_tag.attrs:
            href = a_tag['href']
            program_url = urljoin(url, href)  # urljoinを使用して正しい絶対URLを生成
            #program_url = "https://www.nhk.or.jp/kokokoza/butsurikiso/"    # テスト用
            print(program_url)
            process_program_page(program_url, driver, div_title.text, csv_writer)
            # 各番組のページへ
            #driver.get(full_url)
            # 10秒間プログラムを停止する
            #time.sleep(10)
            time.sleep(1)
            #break

# 結果が書き込まれたファイル名を出力
print(f"リンクは {output_file} に保存されました。")

# ブラウザを閉じる
driver.quit()

# 出力フォーマットはWikipediaにならう
# https://huggingface.co/datasets/Cohere/wikipedia-2023-11-embed-multilingual-v3

# title,program_url,subtitle,episode_url,caption,outline_url,outline


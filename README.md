# Scrape NHK for School

このプロジェクトは、NHK for Schoolのウェブサイトから教育プログラムのあらすじ（アウトライン）をスクレイピングしてCSV形式で保存するPythonスクリプトです。

## 機能

- NHK for Schoolの各プログラムのあらすじをスクレイピング
- 収集したデータをCSVファイルに出力

## 前提条件

このスクリプトを実行する前に、Python3がインストールされていることを確認してください。

## 環境設定

プロジェクトの依存関係を管理するために、Pythonの仮想環境を使用します。次の手順に従って仮想環境を設定し、必要なパッケージをインストールしてください。

### 仮想環境の作成

```bash
python3 -m venv myenv  # 新しい仮想環境を作成
source myenv/bin/activate  # 新しい仮想環境をアクティベート
```

### 依存関係のインストール

```bash
pip install -r requirements.txt  # 必要なパッケージをインストール
```

## 実行方法

セットアップが完了したら、以下のコマンドでスクリプトを実行します。

```bash
python scrape_nhk_for_school_outline_data.py
```

## 出力

スクリプトは`dataset_root/data/`ディレクトリに`nhk_for_school_outline_data.csv`という名前のCSVファイルを生成します。このファイルには、スクレイピングしたデータが含まれます。

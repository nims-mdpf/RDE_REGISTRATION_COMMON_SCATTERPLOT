# 散布図プロットデータセットテンプレート

## 概要

テキストファイルに記載されたテキストファイルを読み取り、散布図を描画するデータセットテンプレートです。

* DT0006: 試料メタあり＋自由記述メタ(key1～10)あり

## 基本情報

### コンテナ情報

* 【コンテナ名】nims_common_scatterplot_registration

### テンプレート情報

* DT0006:
  * 【データセットテンプレートID】NIMS_DT0006_SCATTERPLOT_REGISTRATION_v1.0
  * 【データセットテンプレート名日本語】散布図プロットデータセットテンプレート
  * 【データセットテンプレート名英語】scatter plot dataset template
  * 【データセットテンプレートの説明】入力されたテキストファイルから散布図を作成
* 【バージョン】1.0
* 【データセット種別】その他
* 【データ構造化】あり (システム上「あり」を選択)
* 【取り扱い事業】NIMS研究および共同研究プロジェクト (PROGRAM)
* 【装置名】(なし)

## データ登録方法

1. 以下の内容を送り状から入力してください。
   1. テキストファイルに書かれたヘッダー情報と計測部分のセクションの区切り行番号を、送り状から入力する。
   1. グラフのxy軸のラベル名を送り状から入力する。
1. 登録したいファイルを登録ファイル欄にドラッグアンドドロップする。

> 複数ファイルを登録する際、それぞれのファイルに、送り状に違う値(Value)を設定したい場合は、エクセルインボイスを使用する。

## 入力データの仕様について

### ファイル全体について

- 記述の順番と記述ルールは、 先にヘッダー情報、その後計測データを記述
- _拡張子は、csv, text, ras, dat, pklなど未定_
- `#`, `;`, `!`で始まる行はコメント行として認識。
- 区切り文字の判定は、セクション区切り文字列、コメント文以外の先頭行から自動的に検出。

### ヘッダーについて

- ヘッダーの開始は、`[]`, `()`, `{}`で囲まれた文字列もしくは`header`という文字列情報が付与される。もしくはヘッダー情報が付与されない。また、`header`という文字は大文字小文字問わない。
- ヘッダーの各行の構成は、`key/value`形式
- keyとvalueの区切り: タブ、 `|`、 `:`、 `;`、 カンマ、などの英数字日本語以外の文字1字。ただし、スペースは区切り文字として認識しない。
- keyとvalueの構成について、一対多が含まれるケースも想定。この場合、最初の文字列をkey, 残りをvalueとしてテキストとして認識させる。

### 計測部分について

- 計測部分の開始は、`[]`, `()`, `{}`で囲まれた文字列もしくは`mesurement`、`data`の情報が付与される。`mesurement`、`data`という文字は大文字小文字問わない。
- 散布図で表現できる2列のデータのみを受け付ける。1列のデータ、2列以上のデータは例外を搬送
- 計測データの区切りは、スペース、カンマ、タブ区切りのどれか

> 上記のファイル構成の具体例は、リポジトリ直下のinputdataディレクトリを参照してください。

## 構成

### レポジトリ構成

```
simple_registration
├── LICENSE
├── README.md
├── container
│   ├── Dockerfile
│   ├── Dockerfile_nims (NIMSイントラ用)
│   ├── data (入出力(下記参照))
│   ├── main.py
│   ├── modules (ソースコード)
│   ├── pip.conf
│   ├── pyproject.toml
│   ├── requirements-test.txt
│   ├── requirements.txt
│   ├── tests (テストコード)
│   └── tox.ini
├── .gitlab-ci.yml
├── docs
│   └── 設計書
│       └── データセットテンプレート_散布図プロット_設計書.xlsx
├── inputdata(入力データ)
│   ├── pattern1
│   │   ├── inputdata
│   │   └── invoice
│   ├── pattern2
│   │   ├── inputdata
│   │   └── invoice
│   ├── pattern3
│   │   ├── inputdata
│   │   └── invoice
│   ├── pattern4
│   │   ├── inputdata
│   │   └── invoice
│   └── pattern5
│       ├── inputdata
│       └── invoice
└── templates
    └── template
        ├── batch.yaml
        ├── catalog.schema.json
        ├── invoice.schema.json
        ├── jobs.template.yaml
        ├── metadata-def.json
        └── tasksupport

```

### 動作環境

- Python: 3.11, 3.10, 3.9
- RDEToolKit: 1.0.1

### 動作環境ファイル入出力

```
container/data
├── inputdata
│   └── 登録ファイル欄にドラッグアンドドロップした任意のファイル
├── invoice
│   └── invoice.json (送り状)
├── main_image
│   └── 散布図画像ファイル
├── meta
│   └── metadata.json (中身は空)
├── other_image
│   └──  なし
├── raw
│   └── inputdataからコピーした入力ファイル
├── structured
│   ├── data.csv
│   └── header.csv
├── tasksupport
│   ├── default_value.csv
│   ├── invoice.schema.json
│   ├── metadata-def.json
│   └── rdeconfig.yaml
└── thumbnail
    └──  (サムネイル用)代表画像ファイル
```

### RELEASE

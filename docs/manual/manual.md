# 散布図プロットデータセットテンプレート

## 概要

テキストファイルに記載されたテキストファイルを読み取り、散布図を描画するデータセットテンプレートです。

## 対象とする装置または計測手法

- 計測手法: なし
- 対象装置: なし

## データタイルの構成要素

### 入力ファイルの一覧

| No  | 内容           | 必須 | 本ドキュメントでの仮名 |
| --- | -------------- | ---- | ---------------------- |
| 1   | テキストデータ | 〇   | 入力ファイル           |

### 入力ファイルの仕様

#### ファイル全体

- ヘッダー情報と計測部の2部構成のファイルを入力すること

  ```text
  [Header]
  ExperimentName,Example Experiment
  Date,2024-08-07
  Operator,John Doe
  Temperature,25.0,25.5,26.0
  Pressure,1.0,1.1,1.2
  Comment,This is a test experiment

  [Data]
  Time,Value
  0,0.1
  1,0.15
  2,0.2
  3,0.25
  ```

- 拡張子は問いませんが、バイナリや装置特有のファイルは読み込めない可能性があります。
- `#`, `;`, `!`で始まる行はコメント行として認識されます。
- 命名規則等はありません。
- 各セクションは、以下のセクション名で
- 区切り文字は、自動的に検出されます。

#### ヘッダーについて

- ヘッダーの開始は、`[]`, `()`, `{}`で囲まれた`header`もしくは、`meta`という文字列情報が付与される。また、`header`という文字は大文字小文字問わない。もしくは、ヘッダー文字列が存在しない場合でも解釈できます。
- ヘッダーの各行の構成は、`key/value`形式にすること
- keyとvalueの区切り: タブ、 `|`、 `:`、 `;`、 カンマ、などの英数字日本語以外の文字1字。ただし、スペースは区切り文字として認識しません。
- keyとvalueの構成について、一対多が含まれるケースも想定。この場合、最初の文字列をkey, 残りをvalueとしてテキストとして認識させる。`key1,value1,value2,value3`とあった場合、`value1,value2,value3`は文字列として認識されます。

#### 計測部分について

- 計測部分の開始は、`[]`, `()`, `{}`で囲まれた文字列もしくは`mesurement`、`data`の情報が付与される。`mesurement`、`data`という文字は大文字小文字問わない。
- 散布図で表現できる2列以上のデータのみを受け付ける。列の指定は、送り状から指定する。

> 上記のファイル構成の具体例は、リポジトリ直下のinputdataディレクトリを参照してください。

### 出力ファイル

| ファイル名                         | 種別           | 説明・処理内容                                                                                           |
| ---------------------------------- | -------------- | -------------------------------------------------------------------------------------------------------- |
| <入力ファイル名>.(csvなどの拡張子) | 入力ファイル   | バイナリは読み取り不可                                                                                   |
| metadata.json                      | メタデータ     | metadata-def.jsonにoriginalNameキーが存在し、かつ該当のkey名が入力ファイルに存在する場合メタデータを出力 |
| <入力ファイル名>.(csvなどの拡張子) | rawデータ      |                                                                                                          |
| header.csv                         | 構造化ファイル | 入力ファイルのヘッダー部分のcsv                                                                          |
| data.csv                           | 構造化ファイル | 入力ファイルの計測部分のcsv                                                                              |
| <入力ファイル名>.png               | 画像ファイル   | 送り状から指定された列情報をもとに、散布図を描画                                                         |
| <入力ファイル名>_1.png             | サムネイル画像 |                                                                                                          |

### メタ

#### 送り状メタ（インボイス項目、手入力メタ）

##### 固有情報

| 項目名                           | 必須 | タクソノミー | 日本語名             | 英語名                           | type   | 単位 | 初期値 | 備考 |
| -------------------------------- | ---- | ------------ | -------------------- | -------------------------------- | ------ | ---- | ------ | ---- |
| measurement_data_start_character |      |              | 計測データ開始文字列 | Measurement Data Start Character | string |      |        |      |
| x-axis_column_index              |      |              | x軸列番号            | x-axis column index              | number |      |        |      |
| x-axis_column_index              |      |              | y軸列番号            | y-axis column index              | number |      |        |      |
| x-axis_column_index              |      |              | x軸ラベル名          | xaxis label name                 | string |      |        |      |
| x-axis_column_index              |      |              | y軸ラベル名          | yaxis label name                 | string |      |        |      |

#### 抽出メタ（構造化処理で抽出するメタ）

- 開設したデータセットに依存します。

| パラメータ名 | 取得元 | タクソノミー | RDE2.0 日本語名 | RDE2.0 英語名 | type | 単位 | 初期値 | 備考 |
| :----------- | :----- | :----------- | :-------------- | :------------ | :--- | :--- | :----- | :--- |

## データカタログ項目

データカタログの項目です。データカタログはデータセット管理者がデータセットの内容を第三者に説明するためのスペースです。

| RDE2.0用パラメータ名   | 日本語語彙     | 英語語彙               | データ型 | 備考 |
| :--------------------- | :------------- | :--------------------- | :------- | :--- |
| catalog                | データカタログ | Data Catalog           | object   |      |
| dataset_title          | データセット名 | Dataset Title          | string   |      |
| abstract               | 概要           | Abstract               | string   |      |
| data_creator           | 作成者         | Data Creator           | string   |      |
| language               | 言語           | Language               | string   |      |
| experimental_apparatus | 使用装置       | Experimental Apparatus | string   |      |
| data_distribution      | データの再配布 | Data Distribution      | string   |      |
| raw_data_type          | データの種類   | Raw Data Type          | string   |      |
| stored_data            | 格納データ     | Stored Data            | string   |      |
| remarks                | 備考           | Remarks                | string   |      |
| references             | 参考論文       | References             | string   |      |

## 構造化処理の詳細

### datasets_process.py

このファイルは、カスタム処理モジュールを管理するためのコーディネータークラスと、入力データを処理して散布図を生成し、構造化データを保存するための関数を提供します。

#### クラス: `CustomProcessingCoordinator`

このクラスは、ファイル読み取り、メタデータ解析、グラフプロット、構造化データ処理などのカスタム処理モジュールを管理するためのコーディネーターです。

##### コンストラクタ <!-- CustomProcessingCoordinator -->

```python
def __init__(self, file_reader: FileReader, meta_parser: MetaParser, graph_plotter: GraphPlotter, structured_processer: StructuredDataProcessor) -> None:
    """Initialize the coordinator with the specified components."""
    self.file_reader = file_reader
    self.meta_parser = meta_parser
    self.graph_plotter = graph_plotter
    self.structured_processer = structured_processer
```

###### 属性　<!-- CustomProcessingCoordinator -->

- `file_reader` (`FileReader`): 入力データを読み取るためのコンポーネント。
- `meta_parser` (`MetaParser`): メタデータを処理するためのコンポーネント。
- `graph_plotter` (`GraphPlotter`): グラフをプロットするためのコンポーネント。
- `structured_processer` (`StructuredDataProcessor`): 構造化データを処理するためのコンポーネント。

#### 関数: `scatterplot_module`

この関数は、入力データを処理して散布図を生成し、構造化データを保存します。

##### 引数　<!-- scatterplot_module -->

- `srcpaths` (`RdeInputDirPaths`): 入力ファイルを含むソースディレクトリへのパス。
- `resource_paths` (`RdeOutputResourcePath`): 処理されたファイルを保存するための出力ディレクトリへのパス。

##### 処理手順　<!-- scatterplot_module -->

1. カスタムコンポーネントを使用して処理モジュールを初期化。
1. インボイスJSONファイルからユーザー定義のグラフオプションを取得。
1. 入力データファイルを読み取り、メタデータとデータを抽出。
1. データをCSVファイルに保存し、ユーザーが指定した列のサブセットも保存。
1. ヘッダー情報をテキストファイルに保存。
1. メタデータ定義JSONファイルに基づいてメタデータを解析して保存。
1. 入力データとユーザー定義のオプションに基づいて散布図画像を生成して保存。

#### 関数: `dataset`

この関数は、構造化処理をラップします。

##### 引数　<!-- dataset -->

- `srcpaths` (`RdeInputDirPaths`): 処理のための入力リソースへのパス。
- `resource_paths` (`RdeOutputResourcePath`): 結果を保存するための出力リソースへのパス。

##### デコレータ　<!-- dataset -->

このデコレータは、データ処理中に発生した例外をキャッチし、指定されたエラーメッセージとエラーコードを出力します。

```python
@catch_exception_with_message(error_message="ERROR: failed in data processing", error_code=50)
```

##### 処理手順 <!-- dataset -->

1. ユーザー固有の処理を定義。(定義されていれば。)
1. scatterplot_module 関数を呼び出して処理を実行。

### ファイルの読み込み: `inputfile_handler.py`

`inputfile_handler.py` は、ファイルの読み取り、解析、およびデータの処理を行うためのクラスと関数を提供します。このモジュールは、特定のフォーマットのテキストファイルを読み取り、その内容を解析してメタデータと測定データを抽出します。

#### クラス: `FileOperator`

- 目的: 指定されたファイルパスからテキストファイルを読み取り、その内容を行ごとのリストとして返します。
- メソッド:
  - `__init__(self, file_path: Path)`: ファイルパスを初期化します。
  - `read(self) -> list[str]`: ファイルの内容を読み取り、行ごとのリストとして返します。

#### 関数: `detect_separator`

- 目的: 指定された行のリストから使用されている区切り文字を検出します。
- 引数:
  - `lines (list[str])`: 区切り文字を検出するための行のリスト。
  - `separators (Sequence[str])`: 検出する可能性のある区切り文字のシーケンス。
- 戻り値: 検出された区切り文字、または見つからなかった場合は `None`。

#### クラス: `HeaderParser`

- 目的: ファイルのヘッダー部分を解析し、キーと値のペアのリストとして返します。
- メソッド:
  - `__init__(self, user_mesurement_start_number: int | None = None)`: 初期化メソッド。
  - `parse(self, data: list[str]) -> list[tuple[str, str]]`: データを解析し、ヘッダーを返します。
  - `split_key_value(self, line: str) -> tuple[str, str]`: 行をキーと値に分割します。
  - `is_mesurement_start(self, line: str) -> bool`: 行が測定の開始かどうかを判定します。

#### クラス: `MeasurementParser`

- 目的: 入力ファイルから測定データを解析し、pandas.DataFrame として返します。
- メソッド:
  - `__init__(self)`: 初期化メソッド。
  - `parse(self, lines: list[str], start_line: int) -> pd.DataFrame`: 指定された行から測定データを解析します。
  - `split_data_line(self, line: str) -> list[int | float] | None`: データ行を分割し、数値のリストとして返します。

#### クラス: `DataParser`

- 目的: ファイル全体を解析し、ヘッダーと測定データを抽出します。
- メソッド:
  - `__init__(self, file_operator: FileOperator, header_parser: HeaderParser, measurement_parser: MeasurementParser)`: 初期化メソッド。
  - `process(self) -> tuple[list[tuple[str, str]], pd.DataFrame]`: ファイルを処理し、ヘッダーと測定データを返します。
  - `get_metadata(self) -> list[tuple[str, str]]`: メタデータを返します。
  - `get_measurements(self) -> pd.DataFrame`: 測定データを返します。

#### クラス: `FileReader`

- 目的: ファイルを読み取り、メタデータと測定データを抽出します。
- メソッド:
  - `read(self, file_path: Path) -> tuple[list[tuple[str, str]], pd.DataFrame]`: ファイルを読み取り、メタデータと測定データを返します。
  - `set_mesurement_start_number(self, invoice_json: Path) -> int | None`: invoice.jsonファイルから測定開始番号を設定します。

##### 使用例 <!-- inputfile_handler.py -->

```python
file_reader = FileReader(Path('file1.txt'))
metadata, measurements = file_reader.read()
```

### メタデータの抽出と保存: `meta_handler.py`

#### MetaParser クラス

`MetaParser` クラスは、事前に取得したメタデータを解析し、ファイルに保存するためのクラスです。このクラスは定数メタデータのみを扱い、繰り返しメタデータはサポートしていません。

##### メソッド: `parse`

指定されたデータ辞書を解析し、定数メタ情報とオプションの繰り返しメタ情報を含むタプルを返します。

- 引数
  - `data` (`list[tuple[str, str]]`): 解析するメタデータのキーと値のペアのリスト。各タプルはメタデータキーとその対応する値で構成されます。
  - `metadata_def_path` (`Path`): `metadata-def.json` ファイルへのパス。このファイルには解析に使用されるメタデータ定義が含まれています。
- 戻り値
  - `tuple[MetaType, RepeatedMetaType | None]`: 定数メタ情報とオプションの繰り返しメタ情報を含むタプル。

##### メソッド: `save_meta`

メタ情報をファイルに保存します。

- 引数
  - `save_path` (`Path`): メタ情報を保存するパス。
  - `metaobj` (`rde2util.Meta`): 保存する情報を含むメタオブジェクト。
  - `const_meta_info` (`Optional[MetaType]`, オプション): 使用する定数メタ情報。デフォルトは `None`。
  - `repeated_meta_info` (`RepeatedMetaType | None`, オプション): 繰り返しメタ情報。デフォルトは `None`。
- 戻り値
  - `rde2util.Meta`: 割り当てられたメタ情報。
- 例外
  - `NotImplementedError`: 繰り返しメタ情報がサポートされていない場合に発生します。

#### 使用例 <!-- meta_handler.py -->

```python
from pathlib import Path
from rdetoolkit import rde2util
from modules.meta_handler import MetaParser

# メタデータの解析
parser = MetaParser()
const_meta_info, repeated_meta_info = parser.parse(data=[("key1", "value1")], metadata_def_path=Path("metadata-def.json"))

# メタデータの保存
metaobj = rde2util.Meta()
parser.save_meta(save_path=Path("output.json"), metaobj=metaobj, const_meta_info=const_meta_info)
```

### 構造化ファイル処理: `structured_handler.py`

`structured_handler.py` ファイルには、構造化データの処理を行うための `StructuredDataProcessor` クラスが定義されています。このクラスは、ヘッダー情報とデータ部分を別々のファイルに保存する機能を提供します。

#### クラス: `StructuredDataProcessor`

`StructuredDataProcessor` クラスは、構造化データのヘッダー情報とデータ部分を処理し、それぞれをCSVファイルとして保存するためのクラスです。

##### メソッド: `to_text`

メタデータをテキストファイルに書き込みます。

- 引数
  - `metadata` (`list[tuple[str, str]]`): 書き込むメタデータのリスト。各タプルはメタデータキーとその対応する値で構成されます。
  - `save_path` (`Path`): テキストファイルを保存するパス。
- 戻り値
  - `None`

##### メソッド: `to_csv`

指定されたデータフレームをCSVファイルとして保存します。

- 引数
  - `dataframe` (`pd.DataFrame`): 保存するデータフレーム。
  - `save_path` (`Path`): CSVファイルを保存するパス。
  - `header` (`Optional[list[str]]`, オプション): CSVファイルのヘッダーとして使用するカラム名のリスト。デフォルトは `None`。
- 戻り値
  - `None`

##### メソッド: `has_explicit_column_headers`

データフレームに明示的なカラムヘッダーがあるかどうかをチェックします。

- 引数
  - `df` (`pd.DataFrame`): チェックするデータフレーム。
- 戻り値
  - `bool`: データフレームに明示的なカラムヘッダーがある場合は `True`、そうでない場合は `False`。

#### 使用例 <!-- structured_handler.py -->

```python
from pathlib import Path
import pandas as pd
from modules.structured_handler import StructuredDataProcessor

# メタデータのテキストファイルへの書き込み
metadata = [("key1", "value1"), ("key2", "value2")]
processor = StructuredDataProcessor()
processor.to_text(metadata, Path("metadata.txt"))

# データフレームのCSVファイルへの保存
data = [[1, 2], [3, 4], [5, 6]]
df = pd.DataFrame(data)
processor.to_csv(df, Path("data.csv"), header=["Column1", "Column2"])
```

### 計測データの可視化: `graph_handler.py`

`graph_handler.py` ファイルには、グラフのオプション設定とプロットを行うための `GraphOptions` クラスと `GraphPlotter` クラスが定義されています。このファイルは、データフレームを使用して散布図を作成し、指定されたパスに保存する機能を提供します。

#### クラス: `GraphOptions`

`GraphOptions` クラスは、グラフのオプション設定を管理するためのクラスです。このクラスは、x軸とy軸のラベル、x軸とy軸のカラム番号を保持します。

- 属性
  - `xlabel` (`str | None`): x軸のラベル。デフォルトは `None`。
  - `ylabel` (`str | None`): y軸のラベル。デフォルトは `None`。
  - `x_col_num` (`int`): x軸に使用するカラム番号。デフォルトは `0`。
  - `y_col_num` (`int`): y軸に使用するカラム番号。デフォルトは `1`。

##### メソッド: `adjust_column_number`

指定されたカラム番号を調整します。カラム番号が0より大きい場合は1減算し、それ以外の場合はそのまま返します。

- 引数
  - `v` (`int`): 調整するカラム番号。
- 戻り値
  - `int`: 調整されたカラム番号。

#### クラス: `GraphPlotter`

`GraphPlotter` クラスは、データフレームを使用して散布図を作成し、指定されたパスに保存するためのクラスです。

##### メソッド: `plot`

データをプロットし、指定されたパスにプロット画像を保存します。

- 引数
  - `data` (`pd.DataFrame`): プロットするデータ。最初のカラムがx軸、2番目のカラムがy軸に使用されます。
  - `save_path` (`Path`): プロット画像を保存するパス。
  - `title` (`str | None`, オプション): プロットのタイトル。デフォルトは `None`。
  - `xlabel` (`str | None`, オプション): x軸のラベル。デフォルトは `None`。
  - `ylabel` (`str | None`, オプション): y軸のラベル。デフォルトは `None`。
  - `select_x_col_num` (`int | None`, オプション): x軸に使用するカラム番号。デフォルトは `None`。
  - `select_y_col_num` (`int | None`, オプション): y軸に使用するカラム番号。デフォルトは `None`。
- 戻り値
  - `None`

##### メソッド: `create_options`

指定されたインボイスJSONファイルに基づいて `GraphOptions` オブジェクトを作成して返します。

- 引数
  - `invoice` (`Path`): インボイスデータを含むJSONファイルへのパス。
- 戻り値
  - `GraphOptions`: グラフの設定オプションを含むオブジェクト。

#### 使用例 <!-- graph_handler.py -->

```python
from pathlib import Path
import pandas as pd
from modules.graph_handler import GraphPlotter, GraphOptions

# グラフオプションの作成
plotter = GraphPlotter()
options = plotter.create_options(Path("invoice.json"))

# データフレームの作成
data = [[1, 2], [3, 4], [5, 6]]
df = pd.DataFrame(data)

# グラフのプロットと保存
plotter.plot(df, Path("scatterplot.png"), xlabel=options.xlabel, ylabel=options.ylabel, select_x_col_num=options.x_col_num, select_y_col_num=options.y_col_num)
```

### モデル: `models.py`

`models.py` ファイルには、メタデータや基本情報、カスタム情報、サンプル情報、インボイス情報を管理するためのデータモデルが定義されています。これらのモデルは、Pydantic を使用してデータのバリデーションとシリアライゼーションを行います。

#### クラス: `Label`

`Label` クラスは、ラベル情報を管理するためのデータモデルです。

- 属性
  - `ja` (`str`): 日本語のラベル。
  - `en` (`str`): 英語のラベル。

#### クラス: `Schema`

`Schema` クラスは、スキーマ情報を管理するためのデータモデルです。

- 属性
  - `type` (`str`): スキーマのタイプ。
  - `format` (`str | None`): スキーマのフォーマット。デフォルトは `None`。

#### クラス: `ChildItem`

`ChildItem` クラスは、子アイテムの情報を管理するためのデータモデルです。

- 属性
  - `name` (`Label`): ラベル情報。
  - `schema_` (`Schema`): スキーマ情報。エイリアス `schema`。
  - `unit` (`str | None`): 単位。デフォルトは `None`。
  - `description` (`str | None`): 説明。デフォルトは `None`。
  - `uri` (`str | None`): URI。デフォルトは `None`。
  - `mode` (`str | None`): モード。デフォルトは `None`。
  - `order` (`str | int`): 順序。
  - `original_name` (`str | None`): 元の名前。エイリアス `originalName`。

### クラス: `MetaDataDef`

`MetaDataDef` クラスは、メタデータ定義を管理するためのデータモデルです。

- 属性
  - `root` (`dict[str, ChildItem]`): 子アイテムの辞書。

### クラス: `Basic`

`Basic` クラスは、基本情報を管理するためのデータモデルです。

- 属性
  - `date_submitted` (`str | None`): 提出日。エイリアス `dateSubmitted`。
  - `data_ownerid` (`str | None`): データ所有者ID。エイリアス `dataOwnerId`。
  - `data_name` (`str | None`): データ名。エイリアス `dataName`。
  - `instrument_id` (`str | None`): 計測器ID。エイリアス `instrumentId`。
  - `experiment_id` (`str | None`): 実験ID。エイリアス `experimentId`。
  - `description` (`str | None`): 説明。

### クラス: `Custom`

`Custom` クラスは、カスタム情報を管理するためのデータモデルです。

- 属性
  - `measurement_data_start_line_number` (`str | int`): 測定データの開始行番号。
  - `x_axis_column_index` (`int | None`): x軸のカラムインデックス。エイリアス `x-axis_column_index`。
  - `y_axis_column_index` (`int | None`): y軸のカラムインデックス。エイリアス `y-axis_column_index`。
  - `xaxis_label_name` (`str | None`): x軸のラベル名。
  - `yaxis_label_name` (`str | None`): y軸のラベル名。
  - `key1` (`str | None`): カスタムキー1。
  - `key2` (`str | None`): カスタムキー2。
  - `key3` (`str | None`): カスタムキー3。
  - `key4` (`str | None`): カスタムキー4。
  - `key5` (`str | None`): カスタムキー5。
  - `key6` (`str | None`): カスタムキー6。
  - `key7` (`str | None`): カスタムキー7。
  - `key8` (`str | None`): カスタムキー8。
  - `key9` (`str | None`): カスタムキー9。
  - `key10` (`str | None`): カスタムキー10。

### クラス: `Sample`

`Sample` クラスは、サンプル情報を管理するためのデータモデルです。

- 属性
  - `sample_id` (`str | None`): サンプルID。エイリアス `sampleId`。
  - `names` (`list[str]`): サンプル名のリスト。
  - `composition` (`str | None`): 構成。
  - `reference_url` (`str | None`): 参照URL。エイリアス `referenceUrl`。
  - `description` (`str | None`): 説明。
  - `general_attributes` (`list[str]`): 一般属性のリスト。エイリアス `generalAttributes`。
  - `owner_id` (`str | None`): 所有者ID。エイリアス `ownerId`。

### クラス: `InvoiceJson`

`InvoiceJson` クラスは、インボイス情報を管理するためのデータモデルです。

- 属性
  - `dataset_id` (`str | None`): データセットID。エイリアス `datasetId`。
  - `basic` (`Basic`): 基本情報。
  - `custom` (`Custom`): カスタム情報。
  - `sample` (`Sample`): サンプル情報。

#### メソッド: `get_xaxis_label_name`

x軸のラベル名を取得します。

- 戻り値
  - `str | None`: x軸のラベル名が設定されている場合はその値、設定されていない場合は `None`。

#### メソッド: `get_yaxis_label_name`

y軸のラベル名を取得します。

- 戻り値
  - `str | None`: y軸のラベル名が設定されている場合はその値、設定されていない場合は `None`。

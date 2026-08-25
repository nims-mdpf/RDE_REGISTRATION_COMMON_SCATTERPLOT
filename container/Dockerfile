## Python Version: 3.12
FROM python:3.12-slim-trixie

# appディレクトリを作成し、作業ディレクトリを指定
WORKDIR /app

# 必要なパッケージをインストール/ フォントキャッシュを更新
RUN apt-get update && apt-get install -y \
    fonts-noto-cjk \
    && rm -rf /var/lib/apt/lists/*
# && fc-cache -fv

COPY pip.conf /etc
COPY requirements.txt /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# プログラムや設定ファイルなどをコピーする
COPY main.py /app
COPY modules/ /app/modules/

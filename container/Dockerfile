# Python Verison: 3.11
# python 3.11.9-slim-bookworm for linux/amd64
FROM python@sha256:aad3c9cb248194ddd1b98860c2bf41ea7239c384ed51829cf38dcb3569deb7f1

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

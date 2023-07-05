# main.py
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql.expression import desc
import pymysql
import pandas as pd
import datetime
import os

# データベース接続情報
URL = "mysql+pymysql://username:password@localhost/db_name"

# テーブル定義
Base = declarative_base()


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    article_date = Column(Date)
    created_at = Column(DateTime, default=func.now())
    url = Column(String(255))


# データベース接続
engine = create_engine(URL)
Base.metadata.create_all(engine)

# セッション生成
Session = sessionmaker(bind=engine)
session = Session()


def insert_data(data_list):
    latest_article_date = session.query(func.max(Article.article_date)).scalar()
    new_data_list = []

    for data in data_list:
        # データ挿入条件
        if latest_article_date is None or data["article_date"] > latest_article_date:
            new_data = Article(
                title=data["title"], article_date=data["article_date"], url=data["url"]
            )
            session.add(new_data)
            new_data_list.append(data)

    session.commit()

    if new_data_list:
        today = datetime.datetime.now().strftime("%Y%m%d")
        csv_file = f"new_data_{today}.csv"
        df = pd.DataFrame(new_data_list)
        df.to_csv(csv_file, index=False)
        print(f"New data saved to {csv_file}")
    else:
        print("No new data found.")


# 辞書型データの例
data_list = [
    {
        "title": "Example Title 1",
        "article_date": datetime.date(2023, 7, 5),
        "url": "https://example.com/article1",
    },
    {
        "title": "Example Title 2",
        "article_date": datetime.date(2023, 7, 4),
        "url": "https://example.com/article2",
    },
]

if __name__ == "__main__":
    insert_data(data_list)

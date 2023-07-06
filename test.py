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



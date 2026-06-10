import csv
import datetime
import os
import sys

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mysql.connector
from mysql.connector import Error

matplotlib.use('Agg')


# 설정 상수
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'mars_db'

CSV_FILE_PATH = 'mars_weathers_data.CSV'
OUTPUT_PNG_PATH = 'mars_weather_summary.png'

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS mars_weather (
    weather_id  INT          NOT NULL AUTO_INCREMENT,
    mars_date   DATETIME     NOT NULL,
    temp        INT,
    storm       INT,
    PRIMARY KEY (weather_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

INSERT_SQL = (
    'INSERT INTO mars_weather (mars_date, temp, storm) '
    'VALUES (%s, %s, %s)'
)


# 데이터베이스 유틸리티
def create_connection(host, port, user, password, database=None):
    # MySQL 연결 객체를 반환
    try:
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
        )
        print(f'[DB] 연결 성공: {host}:{port}')
        return conn
    except Error as exc:
        print(f'[DB] 연결 실패: {exc}')
        sys.exit(1)


def ensure_database(host, port, user, password, db_name):
    # 데이터베이스가 없으면 생성한 뒤 연결 객체를 반환
    conn = create_connection(host, port, user, password)
    cursor = conn.cursor()
    cursor.execute(
        f'CREATE DATABASE IF NOT EXISTS `{db_name}` '
        'CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f'[DB] 데이터베이스 확인/생성: {db_name}')
    return create_connection(host, port, user, password, db_name)


def create_table(conn):
    # mars_weather 테이블 생성
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    cursor.close()
    print('[DB] 테이블 확인/생성: mars_weather')


def insert_rows(conn, rows):
    # 행 목록을 mars_weather 테이블에 삽입
    cursor = conn.cursor()
    inserted = 0
    for row in rows:
        cursor.execute(INSERT_SQL, row)
        inserted += 1
    conn.commit()
    cursor.close()
    print(f'[DB] 삽입 완료: {inserted}건')


def fetch_monthly_stats(conn):
    # 월별 평균 기온과 평균 폭풍 강도를 조회하여 반환
    sql = """
        SELECT
            DATE_FORMAT(mars_date, '%Y-%m') AS month,
            AVG(temp)                       AS avg_temp,
            AVG(storm)                      AS avg_storm
        FROM mars_weather
        GROUP BY month
        ORDER BY month
    """
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    cursor.close()
    return results


# CSV 유틸리티
def read_csv(file_path):
    # CSV 파일을 읽어 헤더와 행 목록을 반환
    if not os.path.isfile(file_path):
        print(f'[CSV] 파일을 찾을 수 없습니다: {file_path}')
        sys.exit(1)

    rows = []
    with open(file_path, newline='', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        header = reader.fieldnames
        print(f'[CSV] 헤더: {header}')
        for line in reader:
            rows.append(line)

    print(f'[CSV] 읽은 행 수: {len(rows)}')
    print('[CSV] 첫 번째 행 샘플:', rows[0] if rows else '없음')
    return header, rows


def convert_rows_for_insert(csv_rows):
    # CSV 행을 INSERT용 튜플 목록으로 변환
    # CSV 헤더의 'stom' 오타를 storm으로 처리, temp는 float -> int로 변환
    result = []
    for row in csv_rows:
        # 헤더 오타 'stom' 대응
        storm_val = row.get('storm') or row.get('stom', '0')
        mars_date = datetime.datetime.strptime(row['mars_date'], '%Y-%m-%d')
        temp_val = int(round(float(row['temp'])))
        storm_int = int(storm_val)
        result.append((mars_date, temp_val, storm_int))
    return result


# 시각화
def save_chart(monthly_stats, output_path):
    # 월별 평균 기온 및 폭풍 강도를 PNG 파일로 저장
    months = [row[0] for row in monthly_stats]
    avg_temps = [float(row[1]) for row in monthly_stats]
    avg_storms = [float(row[2]) for row in monthly_stats]

    x_idx = range(len(months))

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
    fig.suptitle('Mars Weather Summary (2050–2052)', fontsize=16, fontweight='bold')

    # --- 평균 기온 ---
    ax1.plot(x_idx, avg_temps, color='#E8503A', linewidth=1.8, marker='o',
             markersize=3, label='Avg Temp (°C)')
    ax1.fill_between(x_idx, avg_temps, alpha=0.15, color='#E8503A')
    ax1.set_ylabel('Avg Temperature (°C)', fontsize=11)
    ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax1.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
    ax1.legend(loc='upper right', fontsize=10)

    # --- 평균 폭풍 강도 ---
    ax2.bar(x_idx, avg_storms, color='#5B8DB8', alpha=0.85, label='Avg Storm')
    ax2.set_ylabel('Avg Storm Intensity', fontsize=11)
    ax2.set_xticks(list(x_idx))
    ax2.set_xticklabels(months, rotation=45, ha='right', fontsize=7)
    ax2.yaxis.set_minor_locator(ticker.AutoMinorLocator())
    ax2.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.6)
    ax2.legend(loc='upper right', fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'[Chart] 이미지 저장 완료: {output_path}')


# 메인
def main():
    # 1. CSV 읽기
    header, csv_rows = read_csv(CSV_FILE_PATH)

    # 2. INSERT용 튜플로 변환
    insert_data = convert_rows_for_insert(csv_rows)

    # 3. DB 연결 및 테이블 생성
    conn = ensure_database(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME)
    create_table(conn)

    # 4. 데이터 삽입
    insert_rows(conn, insert_data)

    # 5. 월별 통계 조회
    monthly_stats = fetch_monthly_stats(conn)
    print(f'[DB] 월별 통계 행 수: {len(monthly_stats)}')

    conn.close()

    # 6. 차트 저장
    save_chart(monthly_stats, OUTPUT_PNG_PATH)


if __name__ == '__main__':
    main()

import yfinance as yf
import pandas as pd
from datetime import datetime
import schedule
import time
import os

def collect_g7_financial_data():
    print(f"작업 시작 시간: {datetime.now()}")

    # 1. 수집 대상 설정 (국가별 주가지수 및 원화대비 환율 티커)
    # 독일, 프랑스, 이탈리아는 유로(EUR)를 사용합니다.
    g7_conf = {
        '미국': {'index': '^GSPC', 'fx': 'USDKRW=X'},     # S&P 500
        '일본': {'index': '^N225', 'fx': 'JPYKRW=X'},   # Nikkei 225
        '영국': {'index': '^FTSE', 'fx': 'GBPKRW=X'},      # FTSE 100
        '캐나다': {'index': '^GSPTSE', 'fx': 'CADKRW=X'}, # S&P/TSX
        '독일': {'index': '^GDAXI', 'fx': 'EURKRW=X'}, # DAX
        '프랑스': {'index': '^FCHI', 'fx': 'EURKRW=X'},  # CAC 40
        '이탈리아': {'index': 'FTSEMIB.MI', 'fx': 'EURKRW=X'} # FTSE MIB
    }

    data_list = []

    # 2. 데이터 수집 루프
    for country, tickers in g7_conf.items():
        try:
            # 지수와 환율 데이터 가져오기 (최근 1일치)
            idx = yf.Ticker(tickers['index']).history(period='1d')['Close'].iloc[-1]
            fx = yf.Ticker(tickers['fx']).history(period='1d')['Close'].iloc[-1]
            
            data_list.append({
                '날짜': datetime.now().strftime('%Y-%m-%d'),
                '국가': country,
                '주가지수': round(idx, 2),
                '환율(KRW)': round(fx, 2)
            })
        except Exception as e:
            print(f"{country} 데이터 수집 중 오류: {e}")

    # 3. 데이터프레임 변환 (행과 열 구성)
    df_new = pd.DataFrame(data_list)

    # 4. 엑셀 파일 저장 (누적 기록 방식)
    file_name = 'G7_Economic_Data.xlsx'
    
    if not os.path.exists(file_name):
        df_new.to_excel(file_name, index=False)
    else:
        # 기존 데이터 로드 후 합치기
        df_existing = pd.read_excel(file_name)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_excel(file_name, index=False)

    print(f"데이터 저장 완료: {file_name}")

# 5. 스케줄러 설정: 매일 09:00 실행
schedule.every().day.at("09:00").do(collect_g7_financial_data)

# 실행 상태 유지
print("자동 수집 프로그램이 가동 중입니다... (매일 아침 9시 실행)")
while True:
    schedule.run_pending()
    time.sleep(60)

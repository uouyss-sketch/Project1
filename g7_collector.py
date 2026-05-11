import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def collect_g7_financial_data():
    print(f"작업 시작 시간: {datetime.now()}")

    # 1. 수집 대상 설정
    g7_conf = {
        '미국': {'index': '^GSPC', 'fx': 'USDKRW=X'},
        '일본': {'index': '^N225', 'fx': 'JPYKRW=X'},
        '영국': {'index': '^FTSE', 'fx': 'GBPKRW=X'},
        '캐나다': {'index': '^GSPTSE', 'fx': 'CADKRW=X'},
        '독일': {'index': '^GDAXI', 'fx': 'EURKRW=X'},
        '프랑스': {'index': '^FCHI', 'fx': 'EURKRW=X'},
        '이탈리아': {'index': 'FTSEMIB.MI', 'fx': 'EURKRW=X'}
    }

    data_list = []

    # 2. 데이터 수집 루프
    for country, tickers in g7_conf.items():
        try:
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

    # 3. 데이터프레임 변환
    df_new = pd.DataFrame(data_list)
    file_name = 'G7_Economic_Data.xlsx'
    
    # 4. 엑셀 파일 저장
    if not os.path.exists(file_name):
        df_new.to_excel(file_name, index=False)
    else:
        df_existing = pd.read_excel(file_name)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
        df_final.to_excel(file_name, index=False)

    print(f"데이터 저장 완료: {file_name}")

# 단일 실행 (깃허브 액션이 호출할 때 딱 한 번만 실행하고 꺼짐)
collect_g7_financial_data()

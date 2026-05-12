import yfinance as yf
import pandas as pd
from datetime import datetime
import os

def get_financial_data():
    # 1. 수집 대상 설정 (G7 국가 지수 및 원화 대비 환율)
    # 지수: S&P500(미), Nikkei225(일), DAX(독), FTSE100(영), CAC40(프), FTSEMIB(이), S&P/TSX(캐)
    symbols = {
        'US_Index': '^GSPC', 'US_Ex': 'USDKRW=X',
        'JP_Index': '^N225', 'JP_Ex': 'JPYKRW=X',
        'DE_Index': '^GDAXI', 'DE_Ex': 'EURKRW=X',
        'UK_Index': '^FTSE', 'UK_Ex': 'GBPKRW=X',
        'FR_Index': '^FCHI',
        'IT_Index': 'FTSEMIB.MI',
        'CA_Index': '^GSPTSE', 'CA_Ex': 'CADKRW=X'
    }

    # 현재 시간 (한국 시간 기준 출력을 위해 데이터프레임에 기록)
    today = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    data_row = {'Date': today}

    # 2. 데이터 추출
    for name, sym in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            # 최신 1일치 데이터 가져오기
            hist = ticker.history(period='1d')
            if not hist.empty:
                # 종가(Close) 기준 저장
                data_row[name] = round(hist['Close'].iloc[-1], 2)
            else:
                data_row[name] = None
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            data_row[name] = None

    return data_row

def save_to_excel(new_data, filename='g7_market_data.xlsx'):
    new_df = pd.DataFrame([new_data])

    # 3. 파일 저장 로직 (기존 파일이 있으면 병합)
    if os.path.exists(filename):
        try:
            old_df = pd.read_excel(filename)
            final_df = pd.concat([old_df, new_df], ignore_index=True)
            print(f"기존 파일에 데이터를 추가합니다.")
        except Exception as e:
            print(f"파일 읽기 오류, 새로 생성합니다: {e}")
            final_df = new_df
    else:
        final_df = new_df
        print(f"새로운 파일을 생성합니다.")

    # 엑셀 파일로 저장 (엔진은 openpyxl 사용)
    final_df.to_excel(filename, index=False, engine='openpyxl')
    print(f"저장 완료: {filename}")

if __name__ == "__main__":
    market_data = get_financial_data()
    save_to_excel(market_data)

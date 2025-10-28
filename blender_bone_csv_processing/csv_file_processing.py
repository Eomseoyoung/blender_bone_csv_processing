import pandas as pd




# 1. '_Y'로 끝나는 모든 열 이름(헤더) 찾기
# regex='_Y$'는 정규 표현식으로, '$'는 문자열의 끝을 의미합니다.

def columns_to_drop(df):
    columns_to_drop = df.filter(regex='_Y$').columns

    # 2. 해당 열들을 DataFrame에서 삭제
    # axis=1: 열(column)을 삭제함을 지정
    # inplace=True: 원본 DataFrame을 바로 수정
    df.drop(columns=columns_to_drop, inplace=True) 
    # 또는 df = df.drop(columns=columns_to_drop)

    print("삭제된 열:", columns_to_drop.tolist())
    print(df.head())
    
    
    
    
# 헤더문자열 끝부분이 _Z인 컬럼들만 추출   
#columns=df.filter(regex='_Z$').columns


def header_change(df):


    # 1. 변경할 헤더 딕셔너리 생성
    # (리스트 컴프리헨션으로 '기존 이름': '새 이름' 딕셔너리 자동 생성)
    rename_dict = {
        col: col.replace('_Z', '_Y') 
        for col in df.columns 
        if col.endswith('_Z')
    }

    # 결과 딕셔너리 예시: {'Name_Y': 'Name_Final', 'Score_Y': 'Score_Final'}
    print("변경할 헤더:", rename_dict)

    # 2. .rename() 함수로 열 이름 변경 적용
    # axis='columns' 또는 axis=1: 열(헤더)을 변경함을 지정
    # inplace=True: 원본 DataFrame을 바로 수정
    df.rename(columns=rename_dict, inplace=True)

    print("\n변경 후 헤더:", df.columns.tolist())
    print(df.head())


def main():
    df=pd.read_csv("data/Getting up_spine4.csv")
    
    columns_to_drop(df)
    header_change(df)
    df.to_csv('Getting up.csv')
    
main()
    

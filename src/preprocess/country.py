import re


class Country:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def country(self, df):
        """나라 컬럼 생성"""

        # 담당 자사 법인 맵핑
        df["response_corporate2"] = df["response_corporate"].map(self.response_corporate)

        df["customer_country"] = df["customer_country"].str.lower().str.strip()
        df["response_corporate2"] = df["response_corporate2"].str.lower().str.strip()

        # 정규표현식으로 나라만 거르기
        df.loc[:, "country"] = df["customer_country"].str.extract(r"/([^/]+)$")[0]
        df["country"] = df["country"].str.strip()
        
        # country를 기준으로 채움
        country_val = df['country'].values
        country_unique = df['response_corporate2'].unique()
        
        for idx, country in enumerate(country_val):
            if country not in country_unique: # 전처리 된 컬럼의 요소가 정해진 나라 범주에 없으면
                df.loc[idx,'country'] = df.loc[idx,'response_corporate2'] # 해당 나라 범주로 채움
        # 컬럼 드롭
        df.drop(['response_corporate2'],axis = 1, inplace = True)
        return df
        
    def continent(self,df):
        """대륙 컬럼 생성"""
        df['continent'] = df['country'].map(self.country_continent)
        return df

    def apply(self, df, module_list=None):
        
        df = self.country(df)
        df = self.continent(df)
        return df

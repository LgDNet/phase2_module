import re


class Country:
    def __init__(self, **pkl):
        self.area = {
            "anguilla": "united kingdom",
            "br": "none",
            "a": "none",
            "nd": "none",
            "ny": "none",
            "rj": "none",
            "us": "united states",
            "ca": "none",
            "kerela": "india",
            "pune": "india",
            "colombia - cartagena": "colombia",
            "country": "none",
        }
        self.pkl = pkl

    def country(self, df):
        """나라 컬럼 생성"""

        # 담당 자사 법인 맵핑
        df["response_corporate2"] = df["response_corporate"].map(self.pkl)

        df["customer_country"] = df["customer_country"].str.lower().str.strip()
        df["response_corporate2"] = df["response_corporate2"].str.lower().str.strip()

        # 정규표현식으로 나라만 거르기
        df.loc[:, "country"] = df["customer_country"].str.extract(r"/([^/]+)$")[0]
        df["country"] = df["country"].str.strip()

        # 숫자 포함 -> none으로 변경 및 결측치 채우기
        df["country"] = df["country"].apply(
            lambda x: "none" if re.search(r"\d", str(x)) else x
        )
        df["country"].fillna("none", axis=0, inplace=True)

        # 이상한 수치 채우기
        for i, j in self.area.items():
            idx = df[df["country"] == i].index
            if len(idx):
                df.loc[idx, "country"] = j
        # none 결측치 채우기
        cond = df["country"] == "none"
        df.loc[cond, "country"] = df[cond]["response_corporate2"]
        return df

    def city(self, df):
        # 도시만 뽑기
        df["city"] = df["customer_country"].str.split("/").str[-2]
        df["city"] = df["city"].str.strip()

        # others 처리
        cond = df["city"] == ""
        df.loc[cond, "city"] = "others"

        # 결측치 채우기
        df["city"].fillna("others", axis=0, inplace=True)

        return df

    def apply(self, df, module_list):
        if not module_list:
            raise ValueError("Not used modules")

        if not isinstance(module_list, list):
            module_list = [module_list]

        for module in module_list:
            method = getattr(self, module)

            df = method(df)

        return df

import numpy as np
import pandas as pd


class ProductCategory:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def label_rows(self, df):
        if (
            df["product_modelname"] is np.nan
            and df["product_subcategory"] is np.nan
            and df["product_category"] is np.nan
        ):
            return 8
        elif df["product_modelname"] is np.nan and df["product_subcategory"] is np.nan:
            return 7
        elif df["product_modelname"] is np.nan and df["product_category"] is np.nan:
            return 6
        elif df["product_subcategory"] is np.nan and df["product_category"] is np.nan:
            return 5
        elif df["product_modelname"] is np.nan:
            return 4
        elif df["product_subcategory"] is np.nan:
            return 3
        elif df["product_category"] is np.nan:
            return 2
        else:
            return 1

    def apply(self, df, module_list: list):
        df["customer_interest"] = df.apply(lambda row: self.label_rows(row), axis=1)
        df[["product_modelname", "product_subcategory", "product_category"]] = df[
            ["product_modelname", "product_subcategory", "product_category"]
        ].fillna(
            "Unknown"
        )  # 그 후 널값 채우기

        df["product_category"] = df["product_category"].str.lower().str.strip()

        # washing machine 추가
        mask = df["product_category"] == "commercial tv,projector"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "projector"
        # 원본 데이터 프레임에 데이터 추가
        df = pd.concat([df, copy_df])

        # dryer 추가
        mask = df["product_category"] == "commercial tv,projector"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "commercial tv"
        df = pd.concat([df, copy_df])

        # 원본데이터 삭제.
        df = df[df["product_category"] != "commercial tv,projector"]

        # washing machine 추가
        mask = df["product_category"] == "washing machine,dryer"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "washing machine"
        # 원본 데이터 프레임에 데이터 추가
        df = pd.concat([df, copy_df])

        # dryer 추가
        mask = df["product_category"] == "washing machine,dryer"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "dryer"
        df = pd.concat([df, copy_df])

        # 원본데이터 삭제.
        df = df[df["product_category"] != "washing machine,dryer"]

        df["product_category"] = (
            df["product_category"]
            .replace(self.replacement_dict)
            .str.replace("solar,", "")
        )

        df["mapped"] = df["product_category"].apply(
            lambda x: next((v for k, v in self.filter1.items() if k in x), x)
        )

        category_counts = df["mapped"].value_counts()
        categories_to_replace = category_counts[
            category_counts < 6
        ].index.tolist()  # 6개 미만 index 찾기
        # 데이터 변환
        df["product_category"] = df["mapped"].apply(
            lambda x: "others" if x in categories_to_replace else x
        )

        df["category_1"] = df["product_category"].map(self.cate_dict)
        df["category_1"] = df["category_1"].map(self.cate_num_dict)
        df["category_2"] = df["product_category"].map(self.subcate_dict)
        df["category_3"] = df["product_category"].map(self.subsubcate_dict)
        df["cate_is_nan"] = (
            df[["category_1", "category_2", "category_3"]].isna().any(axis=1)
        )

        return df

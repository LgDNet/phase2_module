import numpy as np
import pandas as pd


class ProductCategory:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def get_subcategory_dict(self, dictionary):
        cate1_dict, cate2_dict, cate3_dict = {},{},{}
        # mapping
        for key, value in dictionary.items():
            cate1_dict[key] = value[0]
            cate2_dict[key] = value[1]
            cate3_dict[key] = value[2]
        return(cate1_dict, cate2_dict, cate3_dict)
    
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
        # commercial tv와 projector 분류
        mask = df["product_category"] == "commercial tv,projector"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "projector"
        df = pd.concat([df, copy_df])
        mask = df["product_category"] == "commercial tv,projector"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "commercial tv"
        df = pd.concat([df, copy_df])
        # 원본데이터 삭제.
        df = df[df["product_category"] != "commercial tv,projector"]

        # washing machine와 dryer 분류
        mask = df["product_category"] == "washing machine,dryer"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "washing machine"
        df = pd.concat([df, copy_df])
        mask = df["product_category"] == "washing machine,dryer"
        copy_df = df[mask].copy()
        copy_df["product_category"] = "dryer"
        df = pd.concat([df, copy_df])
        # 원본데이터 삭제.
        df = df[df["product_category"] != "washing machine,dryer"]
        
        # product_category
        data = df[['product_category','product_subcategory', 'product_modelname','customer_interest']].copy()
        data["product_category"] = data["product_category"].replace(self.replacement_dict).str.replace("solar,", "")
        data["mapped"] = data["product_category"].apply(
            lambda x: next((v for k, v in self.filter1.items() if k in x), x)
        )
        category_counts = data["mapped"].value_counts()
        categories_to_replace = category_counts[
            category_counts < 6
        ].index.tolist()  # 6개 미만 index 찾기
        data['mapped'] = data['mapped'].apply(lambda x: 'others' if x in categories_to_replace else x)
        data["category_1"] = data["mapped"].map(self.cate_dict)
        data["category_1"] = data["category_1"].map(self.cate_num_dict)
        data["category_2"] = data["mapped"].map(self.subcate_dict)
        data["category_3"] = data["mapped"].map(self.subsubcate_dict)
        # 7번 진행.
        cond7 = (data['customer_interest'] == 7)
        data.loc[cond7, ['category_1','category_2', 'category_3']] = data.loc[cond7, ['category_1', 'category_2', 'category_3']].fillna('all')
        data["cate_is_nan_all"] = (data[["category_1", "category_2", "category_3"]].isna().any(axis=1)) | (data[["category_1", "category_2", "category_3"]].apply(lambda row: 'all' in row.values, axis=1))
        # 8번 진행.
        cond8 = (data['customer_interest'] == 8)
        data.loc[cond8, ['category_1','category_2', 'category_3']] = data.loc[cond8, ['category_1', 'category_2', 'category_3']].fillna('unknown')
        data["cate_is_nan_all"] = (data[["category_1", "category_2", "category_3"]].isna().any(axis=1)) | (data[["category_1", "category_2", "category_3"]].apply(lambda row: 'all' in row.values, axis=1))
        # 1, 2번, 4번, 6번 진행
        cond4 = (((data['customer_interest'] == 1) | (data['customer_interest'] ==2) | (data['customer_interest'] == 4) | (data['customer_interest'] == 6)) & data['cate_is_nan_all'] == True)
        data.loc[cond4, "mapped"] = data.loc[cond4, "product_subcategory"].replace(self.six_replace_dict)
        data.loc[cond4, "mapped"] = data.loc[cond4, "mapped"].apply(
            lambda x: next((v for k, v in self.six_contain_dict.items() if k in x), x)
        )
        sub_cate_dict, sub_subcate_dict, sub_subsubcate_dict = self.get_subcategory_dict(self.six_cate_dict)
        data.loc[cond4, "category_1"] = data.loc[cond4, "mapped"].map(sub_cate_dict)
        data.loc[cond4, "category_2"] = data.loc[cond4, "mapped"].map(sub_subcate_dict)
        data.loc[cond4, "category_3"] = data.loc[cond4, "mapped"].map(sub_subsubcate_dict)
        data["cate_is_nan_all"] = (data[["category_1", "category_2", "category_3"]].isna().any(axis=1)) | (data[["category_1", "category_2", "category_3"]].apply(lambda row: 'all' in row.values, axis=1))
        
        # 1, 2, 3, 5 진행.
        cond3 = (((data['customer_interest'] == 1) | (data['customer_interest'] == 2)| (data['customer_interest'] == 3) | (data['customer_interest'] == 5))& data['cate_is_nan_all'] == True)
        data.loc[cond3, "mapped"] = data.loc[cond3, "product_modelname"].apply(
            lambda x: next((v for k, v in self.model_contain_dict.items() if k in x), x)
        )
        data.loc[cond3, "category_1"] = data.loc[cond3, "mapped"].map(sub_cate_dict)
        data.loc[cond3, "category_2"] = data.loc[cond3, "mapped"].map(sub_subcate_dict)
        data.loc[cond3, "category_3"] = data.loc[cond3, "mapped"].map(sub_subsubcate_dict)
        # 예외처리
        data["cate_is_nan"] = (data[["category_1", "category_2", "category_3"]].isna().any(axis=1))
        cond1 = data["cate_is_nan"] == True
        data["mapped"] = data["product_category"].apply(
            lambda x: next((v for k, v in self.filter1.items() if k in x), x)
        )
        data.loc[cond1,["category_1"]] = data.loc[cond1,"mapped"].map(self.ate_dict)
        data.loc[cond1,["category_1"]]= data.loc[cond1,"category_1"].map(self.cate_num_dict)
        data.loc[cond1,["category_2"]] = data.loc[cond1,"mapped"].map(self.subcate_dict)
        data.loc[cond1,["category_3"]] = data.loc[cond1,"mapped"].map(self.subsubcate_dict)
        data["cate_is_nan"] = (data[["category_1", "category_2", "category_3"]].isna().any(axis=1))
        cond1 = data["cate_is_nan"] == True
        data.loc[cond1, "mapped"] = data.loc[cond1, "product_subcategory"].replace(self.six_replace_dict)
        data.loc[cond1, "mapped"] = data.loc[cond1, "mapped"].apply(
                    lambda x: next((v for k, v in self.six_contain_dict.items() if k in x), x)
                )
        sub_cate_dict, sub_subcate_dict, sub_subsubcate_dict = self.get_subcategory_dict(self.ix_cate_dict)
        data.loc[cond1, "category_1"] = data.loc[cond1, "mapped"].map(sub_cate_dict)
        data.loc[cond1, "category_2"] = data.loc[cond1, "mapped"].map(sub_subcate_dict)
        data.loc[cond1, "category_3"] = data.loc[cond1, "mapped"].map(sub_subsubcate_dict)
        # reset_index 진행.
        df[['category_1', 'category_2', 'category_3']] = data[['category_1', 'category_2', 'category_3']]
        df.reset_index(drop = True, inplace = True)
        return df

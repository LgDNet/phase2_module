import pandas as pd
import re

class Customer:
    def __init__(self, **kwargs):
        # Load pickle file
        for key, value in kwargs.items():
            setattr(self, key, value)

    def complementary(
        self, df:pd.DataFrame, target_col:list, derivated_col:str, dictionary:dict, comple_list:list, default_value="etc"
    )-> pd.DataFrame:
    
        """ 결측값을 상호보완하여 채워주는 함수"""
        
        df[target_col] = df[target_col].applymap(
            lambda x: re.sub("(&|-|/|:)", "", x.lower().replace(" ", ""))
            if isinstance(x, str)
            else x
        )
        df[derivated_col] = None
    
        for col in comple_list:
            for key, value in dictionary.items():
                for val in value:
                    true_list = []
                    val = re.sub("(&|-|/|:)", "", val).replace(" ", "").lower()
    
                    true_list = list(
                        df.loc[
                            df[col].str.contains(val, na=False)
                        ].index
                    )
                    df.loc[
                        (df[derivated_col].isnull())&(df.index.isin(true_list)), derivated_col,
                    ] = key
    
        comple_col = comple_list[0]
        
        df.loc[
            (df[comple_col].notnull()) & (df[derivated_col].isnull()),
            derivated_col,
        ] = "etc"
    
        # df[derivated_col].fillna("Unknown", inplace=True)
        return df


    def apply(self, df, pkl):
        """실행 함수"""
        customer_type2 = self.customer_type2
        job_function = self.job_function
        seniority_level = self.seniority_level

        customer_col=["customer_type", "customer_job", "customer_position"]

        df = self.complementary(
            df,
            customer_col,
            "customer_type2",
            customer_type2,
            ["customer_type", "customer_job", "customer_position"],
        )
        df = self.complementary(
            df,
            customer_col,
            "job_function",
            job_function,
            ["customer_job", "customer_type", "customer_position"],
        )
        df = self.complementary(
            df,
            customer_col,
            "seniority_level",
            seniority_level,
            ["customer_position", "customer_type", "customer_job"],
        )
        return df

  
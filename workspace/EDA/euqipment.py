import pickle
import pandas as pd

class Enquipment:
    def __init__(self, df):
        self.df = df

    def dataframe(self):
        return self.df

    def raw_df(self):
        """기존 데이터를 반환하는 함수"""
        
        raw_col = [
            "bant_submit",
            "customer_country",
            "business_unit",
            "customer_idx",
            "customer_type","enterprise",
            "historical_existing_cnt",
            "customer_job",
            "lead_desc_length",
            "inquiry_type", 
            "product_category", 
            "product_subcategory",
            "product_modelname", 
            "customer_country.1", 
            "customer_position", 
            "response_corporate",
            "expected_timeline",
            "business_area",
            "business_subarea", 
            "lead_owner",
            "is_converted"
        ]
        
        raw_df = self.df[raw_col]
    
        return raw_df
    
    def derivated_df(self, df):
        """파생 데이터를 반환하는 함수"""
        
        raw_col = set(self.raw_df(Data.train).columns)
        all_col = set(Data.train.columns)
    
        derivated_col = all_col.difference(raw_col)
    
        derivated_col = list(derivated_col)
        derivated_df = df[derivated_col]
    
        return derivated_df
        
    def value_counts(self, *args):
        """ Show Value_counts """
        for col in args:
            print(f"############# {col} ################")
            print(self.df[col].value_counts())
            print(len(self.df[col].value_counts()))
            print("\n")
    
    def is_na(self, *args):
        """" Show Missing Value """
        col_list=[]
        null_list=[]
        for col in args:
            col_list.append(col)
            null_list.append(self.df[col].isnull().sum())
    
        df = pd.DataFrame(data=[null_list], index=['null'], columns=col_list).T.sort_index()
        return df

    def describe_columns(self, *args):
        """ Description of Columns """
        
        with open('phase2_module/workspace/EDA/dictionary/description_columns.pickle', 'rb') as fr:

            description_columns = pickle.load(fr)
        
        for column in args:
            if column in description_columns:
                print(f"{column}: {description_columns[column]}")
            else:
                print(f"{column}: No description available")
                
    def importance(self):
        """ Show Importance of Columns"""
        importance_df = pd.read_csv("phase2_module/workspace/EDA/dictionary/importance_df.csv")
        return importance_df


    def missing_columns(self, null_cols:list, not_null_cols:list)-> list:
        null_cols = set(null_cols).difference(set(not_null_cols))

        return null_cols

    
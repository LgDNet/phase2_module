import pandas as pd
import numpy as np
class Convert_ratio:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
            
    def make_ratio_to_dict(self,df,col_name):
        """ 전환율 딕셔너리 저장 """
        # from phase2_module.src.utils.manage_pkl_files import PickleManager as pkl_manager
        dict_ ={}
        flag = df.groupby(col_name)['is_converted'].agg(['sum','count'])
        for idx, plus, counts in zip(flag.index,flag['sum'],flag['count']):
            cond =  df[col_name] == idx
            ratio = (plus / counts) * 100
            df.loc[cond,f'{col_name}_converted_ratio'] = round(ratio,2)
            dict_[idx] = ratio
        # save
        # pkl_manager.save(f"{col_name}",f"{col_name}_converted_ratio",dict_)
        return dict_
        
    def lead_owner_customer_idx_means(self,df):
        """ 실적 별 회사 전환율 평균 """
        # 범주화
        bin = [0.0001,10.0001,20.0001,30.0001,40.0001,50.0001,60.0001,70.0001,80.0001,90.0001,100.00,100.001]
        df.loc[:,'lead_owner_customer_idx_mean'] = pd.cut(df['lead_owner_converted_ratio'], bins=bin, right = False,labels= False)
        df['lead_owner_customer_idx_mean'] = df['lead_owner_customer_idx_mean']+1
        df['lead_owner_customer_idx_mean'].fillna(0.0,axis = 0, inplace  = True)
        # 매핑
        df['lead_owner_customer_idx_mean'] = df['lead_owner_customer_idx_mean'].map(self.lead_owner_customer_idx_mean)
        return df    

    def ratio_preprocessing(self,df, col_name, ratio_dict):
        """ 해당 컬럼 전환율 변환 """
        for i in np.sort(df[col_name].unique()):
            if i not in ratio_dict.keys(): # 없으면 추가
                ratio_dict[i] = 0.0
        df[f'{col_name}_converted_ratio'] = df[col_name].map(ratio_dict)
        return df
        
    def conert_all_trues(self,df, col_name, ratio_dict):
        """ 해당 컬럼 전환율 변환 """
        for i in np.sort(df[col_name].unique()):
            if i not in ratio_dict.keys(): # 없으면 추가
                ratio_dict[i] = 0.0
        df[f'convert_all_true'] = df[col_name].map(ratio_dict)
        return df
        
    def lead_owner(self,df):
        return self.ratio_preprocessing(df, 'lead_owner', self.lead_owner_converted_ratio)
        
    def customer_idx(self,df):
        return self.ratio_preprocessing(df, 'customer_idx', self.customer_idx_converted_ratio)
        
    def convert_all_true(self,df):
        return self.conert_all_trues(df, 'customer_idx', self.all_true)
    
    def apply(self, df, module_list):
        if not module_list:
            raise ValueError("Not used modules")

        if not isinstance(module_list, list):
            module_list = [module_list]

        for module in module_list:
            method = getattr(self, module)

            df = method(df)
        return df
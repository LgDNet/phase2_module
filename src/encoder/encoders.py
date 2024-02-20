import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from collections import defaultdict

# ENCODERS = {"label": [], "onehot": []}
ENCODERS = defaultdict(list)


class Encode:
    def __init__(self):
        pass

    def label_encoder(self, df, columns):
        if not ENCODERS["label"]:
            for col in columns:  # NOTE: train
                encoder = LabelEncoder()
                try:
                    df.loc[:, col] = encoder.fit_transform(df[col])
                except Exception as e:
                    print(e)
                    print(col)
                # 인코더 저장
                ENCODERS["label"].append(encoder)
        else:  # NOTE: test
            for idx, col in enumerate(columns):
                encoder = ENCODERS["label"][idx]

                for label in np.sort(df[col].unique()):
                    if label not in encoder.classes_:
                        encoder.classes_ = np.append(encoder.classes_, label)
                df.loc[:, col] = encoder.transform(df[col])
        return df

    def convert_dataframe(self, df, onehot_arr, category_list, col_):
        col_list = np.concatenate([i.flatten() for i in category_list])
        onehot_df = pd.DataFrame(
            onehot_arr, columns=[f"OneHot_{col_name}" for col_name in col_list]
        )
        df = pd.concat([df, onehot_df], axis=1)
        df.drop(col_, axis=1, inplace=True)
        return df

    def onehot_encoder(self, df, columns, sparse):
        if not ENCODERS["onehot"]:
            encoder = OneHotEncoder(sparse=sparse)
            try:
                onehot_arr = encoder.fit_transform(df[columns])
                df = self.convert_dataframe(
                    df, onehot_arr, encoder.categories_, columns
                )
            except Exception as e:
                print(e)
            # 인코더 저장
            ENCODERS["onehot"].append(encoder)
        else:
            encoder = ENCODERS["onehot"][0]
            onehot_arr = encoder.transform(df[columns])
            df = self.convert_dataframe(df, onehot_arr, encoder.categories_, columns)
        return df

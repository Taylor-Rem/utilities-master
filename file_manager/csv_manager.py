import pandas as pd
import numpy as np

class CsvManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path, header=None)

    def replace_unit_columns(self, ranges):
        values = np.concatenate([np.arange(_range['start'], _range['end'] + 1) for _range in ranges])
        num_rows = min(len(self.df), len(values))
        self.df.iloc[:num_rows, 1] = values[:num_rows]

    def delete_empty_rows(self):
        self.df = self.df[self.df.iloc[:, 4] != "00/00/0000"].reset_index(drop=True)
        
    def save_csv(self):
        self.df.to_csv(self.file_path, index=False, header=False)

    def convert_units(self):
        self.df.iloc[:, 1] = pd.to_numeric(self.df.iloc[:, 1], errors='coerce').fillna(0).astype(int)

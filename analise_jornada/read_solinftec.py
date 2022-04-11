import pandas as pd

def solinftec_extractor(file):
    df = pd.read_excel('dados/'+file)
    print(df)

file = 'solinftec.xlsx'
if __name__ == '__main__':
    solinftec_extractor(file)
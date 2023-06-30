from main import prepare_data_ar1
import pandas as pd
df_f = pd.read_csv('df_fraud.csv')
prepare_data_ar1('Krzysztof Kaniewski', '', df_f, 'Krzysztof', 'Kaniewski', '777 888 999', 'email')
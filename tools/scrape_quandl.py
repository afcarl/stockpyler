import quandl
import os
import csv

quandl.ApiConfig.api_key = os.environ.get('QUANDL_API_KEY')

def get_all_from(quandl_database_code, metadata_path, out_dir):
    with open(metadata_path,'r') as in_f:
        reader = csv.DictReader(in_f)
        for line in reader:
            code = quandl_database_code + '/' + line['code']
            out_path = os.path.join(out_dir, code.replace('/', '_') + '.csv')
            if os.path.isfile(out_path):
                continue
            df = quandl.get(code)
            df.to_csv(out_path,float_format='%g')
            print(code)

get_all_from('MALTASE','/home/forrest/Downloads/MALTASE_metadata.csv', '/home/forrest/quandl')
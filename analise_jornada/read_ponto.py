import re
import pandas as pd

def ponto_file_extractor(file):
    raw_df = pd.read_excel('dados\\'+ file,header = [8], usecols='A:D')
    text = raw_df.to_string()

    name_pattern = re.compile(r'\w+ \w+ \w+ \w* \w*')
    code_pattern = re.compile(r'\d{6}')
    date_pattern = re.compile(r'\d{4}-\d{2}-\d{2}')

    code_matches = code_pattern.finditer(text)

    end = 0
    data = []
    for code_match in code_matches:
        start = code_match.start()
        next_code_match = code_pattern.search(text, code_match.end())
        try:
            end = next_code_match.start()
        except AttributeError:
            pass
        name_match = name_pattern.search(text,start,end)
        try:
            operador = '{} - {}'.format(code_match.group(), name_match.group())
        except AttributeError:
            pass

        date_matches = date_pattern.finditer(text,start,end)
        for date_match in date_matches:
            date_end = date_match.end()
            time_match = text[date_end+45:date_end+69]
            corrected_date = date_match.group().replace('1901','2022')

            jornada = []
            previous_time = pd.Timestamp(year=1901, month=1, day=1)
            for time in time_match.split():
                if 'NaN' not in time:
                    time = pd.to_datetime(corrected_date + ' ' + time, format='%Y-%m-%d %H:%M')
                    if time < previous_time:
                        time += pd.Timedelta(1, unit='day')
                    else:
                        pass
                    jornada.append(time)
                else:
                    pass
                previous_time = time
            users_info = (operador,corrected_date) + tuple(jornada)
            data.append(users_info)
    for user in data:
        print(user)
file = 'ponto.xlsx'
if __name__ == '__main__':
    ponto_file_extractor(file)

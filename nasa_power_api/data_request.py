import os
import json
import requests
import pandas as pd

def data_request(locations, start, end, parameters="T2M,T2M_MAX,T2M_MIN,RAIN,ALLSKY_SFC_SW_DWN", data_output = 'json'):

    data_output_formats = ('json', 'dataframe', 'excel')
    if data_output not in data_output_formats:
        raise TypeError(f'Informed data_output is not one of the outputs , try: {data_output_formats}')

    output = r""
    base_url = r"https://power.larc.nasa.gov/api/temporal/daily/point?parameters={parameters}&community=RE&longitude={longitude}&latitude={latitude}&start={start}&end={end}&format=JSON"

    for latitude, longitude in locations:
        api_request_url = base_url.format(longitude=longitude,
                                          latitude=latitude,
                                          start=start,
                                          end=end,
                                          parameters=parameters
                                          )

        response = requests.get(url=api_request_url, verify=True, timeout=30.00)

        content = json.loads(response.content.decode('utf-8'))
        filename = response.headers['content-disposition'].split('filename=')[1]
        filepath = os.path.join(output, filename)

        if data_output == 'json':
            with open(filepath, 'w') as file_object:
                json.dump(content, file_object, indent=4)

        elif data_output == 'dataframe':
            data = content['properties']['parameter']
            df = pd.DataFrame(data)
            return df

        elif data_output == 'excel':
            filename = filepath.split('.json')[0]
            data = content['properties']['parameter']
            pd.DataFrame(data).to_excel(f'{filename}.xlsx')


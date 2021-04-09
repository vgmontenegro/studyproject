import urllib.request
import time 

def get_price():
    page = urllib.request.urlopen('https://www.cepea.esalq.usp.br/br/indicador/milho.aspx')
    text = page.read().decode('utf8')
    where = text.find('</td>') + 5
    start = text.find('<td>', where) + 4
    end = text.find('</td>', where) 
    preço = float(text[start:end].replace(',','.'))
    return(preço)

ver_preço = input('Consultar preço? Sim/Não: ')
if ver_preço.lower() == 'sim':
    print('Consultando preço...')
    time.sleep(3)
    preço = get_price()
    print('Milho: R$ {}/sc\n'.format(preço))
else:
    preço = get_price()
    while True:
        if preço != get_price():
            preço = get_price()
            print('O preço da saca de milho está R$ {}'.format(preço))
        else:
            pass
            
        time.sleep(5)

        









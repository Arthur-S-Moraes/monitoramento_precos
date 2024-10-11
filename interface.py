import PySimpleGUI as sg
from banco_dados import *
from time import sleep
from threading import Thread
from sites import monitoramento_precos
import schedule

running = True
def iniciar_schedule(window, url, intervalo):
    intervalo = int(intervalo)
    schedule.every(intervalo).minutes.do(monitoramento_precos, window, url)
    while running:
        schedule.run_pending()
        sleep(1)


conexao = criar_sql()



def janela_principal():
    layout = [
        [sg.Text('verificar o site depois de quanto tempo')],
        [sg.Push(),sg.Slider((1,60), orientation='horizontal', key='intervalo'), sg.Push()],
        [sg.Button('Iniciar', size=15, ),sg.Button('Encerrar processo', size=15, disabled=True)],
        [sg.Button('Adicionar URLS', size=15), sg.Button('Deletar URLS', size=15)],
        [sg.Output((37,10))]
    ]
    return sg.Window('Janela Principal', layout, finalize=True)

def adicionar_urls():
    layout = [
        [sg.Output(size=(50,15),key='exibir_urls')],
        [sg.Text('Adicionar URL (Mercado Livre, Kabum, Amazon)')],
        [sg.Input(key='url')],
        [sg.Text('Nome do produto')],
        [sg.Input(key='nome_produto')],
        [sg.Button('adicionar'), sg.Button('voltar')]
    ]
    return sg.Window('Adicionar URLS', layout, finalize=True)

def excluir_urls():
    layout = [
        [sg.Output(size=(50,15),key='exibir_urls')],
        [sg.Text('digite o numero da URL que deseja deletar')],
        [sg.Input(key='id_deletar')],
        [sg.Button('confirmar'), sg.Button('voltar')]
    ]
    return sg.Window('Excluir URLS', layout, finalize=True)

janela_principal_, adicionar_urls_, excluir_urls_ = janela_principal(), None, None



while True:
    window, event, values = sg.read_all_windows()
    if event == sg.WIN_CLOSED:
        break
    if window == janela_principal_:
        if event == 'Adicionar URLS':
            janela_principal_.hide()
            adicionar_urls_ = adicionar_urls()
            visualizar(conexao)

        if event == 'Deletar URLS':
            janela_principal_.hide()
            excluir_urls_ = excluir_urls()
            visualizar(conexao)

        
        if event == 'Iniciar':
            urls = pegar_url(conexao)
            intervalo = values['intervalo']
            Thread(target=monitoramento_precos, args=(window, urls), daemon=True).start()
            Thread(target=iniciar_schedule, args=(window, urls, intervalo), daemon=True).start()
            window['Iniciar'].update(disabled=True)
            window['Encerrar processo'].update(disabled=False)
            print(f'próximo monitoramento em {intervalo} minutos')

        elif event == 'Encerrar processo':
            running = False
            window['Iniciar'].update(disabled=False)
            window['Encerrar processo'].update(disabled=True)

            
    if window == adicionar_urls_:
        if event == 'adicionar':
            site = values['url']
            produto = values['nome_produto']
            if len(site) == 0:
                sg.popup('o site não pode ficar em branco')
            else:
                window['url'].update('')
                window['url'].update('')
                sg.popup(f'pagina {site} adicionada com sucesso')
                adicionar_dados(conexao, site, produto)
                window['nome_produto'].update('')
                visualizar(conexao)
                
        
        elif event == 'voltar':
            adicionar_urls_.close()
            janela_principal_ = janela_principal()
    
    
    if window == excluir_urls_:
        if event == 'voltar':
            excluir_urls_.close()
            janela_principal_ = janela_principal()

        elif event == 'confirmar':
            id_deletar = values['id_deletar']
            resultado = sg.popup_ok_cancel(f'deseja tirar o ID de numero{id_deletar}?')
            if resultado == 'OK':
                excluir(conexao, id=id_deletar)
                window['exibir_urls'].update('')
                visualizar(conexao)
    

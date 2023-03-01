from datetime import date
from re import compile
from time import sleep
from urllib import parse
from webbrowser import open as webopen

import streamlit as st
from pyperclip import copy
from requests import get

today = date.today().strftime('%Y.%m.%d')


title = '・ Torrent Tracker Adder'
logo_url = 'https://raw.githubusercontent.com/Henrique-Coder/torrent-tracker-adder/main/web-version/assets/tta-logo.png'

st.set_page_config(page_title=title, page_icon='assets/tta-logo.png', layout='centered', initial_sidebar_state='auto')

st.markdown(
    '''
    <style>
    .container {
        display: flex;
        align-items: center;
    }
    .logo {
        height: 50px;
        margin-right: 10px;
    }
    .title {
        font-size: 36px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)

st.write(
    f'''
    <div class='container'>
        <img class='logo' src='{logo_url}' alt='Logo'>
        <h1 class='title'>{title}</h1>
    </div>
    ''',
    unsafe_allow_html=True
)

magnet_url = st.text_input('Insira o link magnético do torrent:')

warn = st.empty()

if not magnet_url:
    warn.warning('O campo de texto está vazio')
    st.stop()

else:
    # Verifica se o link magnetico e valido
    magnet_pattern = compile(r'magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{32}')

    if not magnet_pattern.match(magnet_url):
        warn.error('O url magnético inserido é inválido')
        st.stop()

# Obter o hash do magnet link
magnet_hash = parse.parse_qs(parse.urlsplit(magnet_url).query)['xt'][0].split(':')[-1]

warn.info('Fazendo o download das listas de rastreadores mais recentes...')

# Baixar as listas de trackers e salva-las em variaveis
trackers_ngosang = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
trackers_xiu2 = 'https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt'

warn.info('Juntando as listas de rastreadores e removendo rastreadores repetidos...')

# Juntar as duas listas de trackers e remover trackers repetidos
trackers = list(set(get(trackers_ngosang).text.split('\n') + get(trackers_xiu2).text.split('\n')))
trackers_count = len(trackers)

warn.info('Adicionando os rastreadores ao link magnético...')

# Adicionar os trackers ao url magnetico corrigindo a formatacao
magnet_dict = parse.parse_qs(parse.urlsplit(magnet_url).query)
magnet_dict['tr'] = trackers
updated_magnet_url = 'magnet:?xt=' + magnet_dict['xt'][0] + '&' + '&'.join('tr=' + t for t in trackers)

warn.success(f'・ **{trackers_count}** rastreadores foram adicionados ao link magnético')

# Criar botoes para copiar o link magnetico, abrir o link magnetico no cliente torrent e baixar a lista de trackers
col1, col2, col3 = st.columns(3)

if col1.button('**Copiar o link magnético para área de transferência**'):
    copy(updated_magnet_url)

    warn.info('・ O link magnético foi copiado para a área de transferência')
    sleep(1)
    warn.success(f'・ **{trackers_count}** rastreadores foram adicionados ao link magnético')

if col2.button('**Abrir o link magnético em seu cliente torrent padrão**'):
    webopen(updated_magnet_url, new=1)

    warn.info('・ O link magnético está sendo aberto em seu cliente torrent padrão')
    sleep(1)
    warn.success(f'・ **{trackers_count}** rastreadores foram adicionados ao link magnético')

if col3.download_button(
        label='**Baixar a lista dos melhores rastreadores para torrent**',
        data='\n\n'.join(trackers).strip(),
        file_name=f'tta-besttrackers-{today}.txt',
        mime='text/plain'
):
    warn.info('・ A lista de rastreadores está sendo enviada para você')
    sleep(1)
    warn.success(f'・ **{trackers_count}** rastreadores foram adicionados ao link magnético')

st.markdown('---')

# Criar um caixa de texto bonita para mostrar o link magnetico
st.text_area('Link magnético atualizado:', value=f'{updated_magnet_url}', height=268, disabled=True)

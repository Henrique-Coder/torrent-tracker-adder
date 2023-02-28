from asyncio import sleep
from os import system as cmd
from re import compile
from urllib import parse

from colorama import init as colorama_init
from pyperclip import copy
from requests import get
from termcolor import cprint, colored


# Habilitar o uso de cores no terminal
colorama_init()

# Funcao para limpar a tela
def cs():
    cmd('cls||clear')

# Variaveis universais
c = colored
b = 'bold'

warning_msg = c('   AVISO', 'yellow', attrs=[b])
sucess_msg = c('   SUCESSO', 'green', attrs=[b])
error_msg = c('   ERRO', 'red', attrs=[b])


# Exibir o titulo do programa e seu criador
an1 = c(r" _____                    _     _____            _               _      _    _         ", 'blue', attrs=[b])
an2 = c(r"|_   _|__ _ _ _ _ ___ _ _| |_  |_   _| _ __ _ __| |_____ _ _    /_\  __| |__| |___ _ _ ", 'blue', attrs=[b])
an3 = c(r"  | |/ _ \ '_| '_/ -_) ' \  _|   | || '_/ _` / _| / / -_) '_|  / _ \/ _` / _` / -_) '_|", 'blue', attrs=[b])
an4 = c(r"  |_|\___/_| |_| \___|_||_\__|   |_||_| \__,_\__|_\_\___|_|   /_/ \_\__,_\__,_\___|_|  ", 'blue', attrs=[b])

ac1 = c(r".       .___.  ..__ .__", 'light_magenta', attrs=[b])
ac2 = c(r"|_   .  [__ |__||  \[__)", 'light_magenta', attrs=[b])
ac3 = c(r"[_)\_|  |   |  ||__/|   ", 'light_magenta', attrs=[b])
ac4 = c("                                                                                     ._|\n\n", 'light_magenta',
        attrs=[b])

initial_screen = fr'''
   {an1}
   {an2}   {ac1}
   {an3}   {ac2}
   {an4}   {ac3}
           {ac4}
'''

print(initial_screen)

# Obter o link magnetico do usuario
magnet_url = input(c('   </>  ・ Magnet URL ➝ ', 'light_grey', attrs=[b]))

# Verifica se o link magnetico e valido
magnet_pattern = compile(r'magnet:\?xt=urn:[a-z0-9]+:[a-zA-Z0-9]{32}')

if not magnet_pattern.match(magnet_url):
    cs()

    print(initial_screen)

    cprint('O url magnético inserido é inválido!\n', 'red', attrs=[b])
    cprint(magnet_url, 'gray')

    sleep(3)
    exit()

# Baixar as listas de trackers e salva-las em variaveis
trackers_ngosang = 'https://raw.githubusercontent.com/ngosang/trackerslist/master/trackers_all.txt'
trackers_xiu2 = 'https://raw.githubusercontent.com/XIU2/TrackersListCollection/master/all.txt'

# Juntar as duas listas de trackers e remover trackers repetidos
trackers = list(set(get(trackers_ngosang).text.split('\n') + get(trackers_xiu2).text.split('\n')))
trackers_count = len(trackers)

# Adicionar os trackers ao url magnetico corrigindo a formatacao
magnet_dict = parse.parse_qs(parse.urlsplit(magnet_url).query)
magnet_dict['tr'] = trackers
updated_magnet_url = 'magnet:?xt=' + magnet_dict['xt'][0] + '&' + '&'.join('tr=' + t for t in trackers)

# Copiar o link magnetico atualizado para a area de transferencia
copy(updated_magnet_url)

# Exibir o link magnetico atualizado
cs()

print(initial_screen)

print(sucess_msg, c(f'  ・ {trackers_count} trackers foram adicionados ao seu url magnético para acelerar o download!',
                    'light_green',
                    attrs=[b]))
print(warning_msg, c('    ・ O url magnético atualizado foi copiado para a área de transferência.\n', 'light_yellow',
                     attrs=[b]))

cprint(updated_magnet_url, 'light_cyan', attrs=[b])

input(c('\n   Pressione qualquer tecla para sair...', 'light_grey', attrs=[b]))

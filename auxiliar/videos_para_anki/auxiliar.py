import yt_dlp
import os
import requests
import json

class Aux:
    @staticmethod
    def Menu():
        resp = input('''
=========================================
|               MENU                    |
=========================================
[ 1 ] - Configurações prévias
[ 2 ] - Download
[ 3 ] - Editar o vídeo
[ 4 ] - Abrir o vídeo
[ 5 ] - Testar e mandar pro anki
[ 6 ] - Sair

escolha: ''')
        return resp

    @staticmethod
    def download(dest):
        """metodo que baixa um vídeo em um determinado lugar

        Args:
            dest (str): destino onde o vídeo será baixado
        """        
        url = input('insira a url do vídeo: ')

        ydl_opts = {
            'format': 'bv[ext=mp4]',  # "best video" com extensão mp4
            'outtmpl': os.path.join(dest, '%(title)s.%(ext)s'),
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

        return info.get('title')  # Retorna o título do vídeo
    
    @staticmethod
    def pacotes():
        """
        Purpose: metodo que serve para baixar programas necessários
        """
        os.system('dnf install firefox python3 vlc')
        os.system('flatpak install net.ankiweb.Anki com.vscodium.codium')
    # end def
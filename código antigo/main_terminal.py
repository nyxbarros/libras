import os
import requests
import time
import json
from auxiliar import Aux
from video import Video
from anki import Anki

# 
#  palavras especificas:
#     cores:
#         bege
#     meses:
#
#         abril
#         junho
#         agosto
#         setembro
#         outubro
#

with open("input.json", 'r') as file:
    entrada = json.load(file)

    print(entrada)

def main():
    response = None
    video = '~/Vídeos/Libras/auxiliar/Design sem nome'
    while True:
        escolha = Aux.Menu()
    
        if escolha == '1':
            Aux.pacotes()

        elif escolha == '2':
            entrada['video_baixado'] = Aux.download('~/Vídeos/Libras/auxiliar/')

        elif escolha == '3':
            os.system('firefox -new-window https://www.canva.com/video-editor/')
            os.system('nautilus ../')

            while True:
                if input('já baixou? ').lower().strip()[0] == 's':
                    os.system('mv "~/Downloads/Design sem nome.mp4" ../')
                    break

        elif escolha == '4':
            os.system('flatpak run com.vscodium.codium input.json &')
            os.system(f'vlc "../{entrada['video_baixado']}.mp4"')


        elif escolha == '5':

            os.system('flatpak run net.ankiweb.Anki &')

            time.sleep(10)

            url = "http://localhost:8765"
            
            videos = [Video(video, *corte) for corte in entrada['cortes']]

            for video in videos:
                video.cortar()

            Anki.validarDeck('teste')
            for video in videos:
                video.mover()
                
                response = requests.post(url, json=Anki.cartao(f'<video src="{video.nome}.mp4" controls></video>', video.nome, 'teste'))

            while True:
                manter = input('gostou do resultado [S/N]? ').strip()[0].lower()
                if manter == 'n':
                    for video in videos:
                        print(f'rm "{video.lugar}/{video.nome}.mp4"')
                        os.system(f'rm "{video.lugar}/{video.nome}.mp4"')
                    Anki.deletarDeck('teste')
                    break
                if manter == 's':
                    Anki.deletarDeck('teste')

                    Anki.validarDeck(entrada['deck'])
                    
                    for video in videos:
                        response = requests.post(url, json=Anki.cartao(video.nome, f'<video src="{video.nome}.mp4" controls></video>', entrada['deck']))
                        response = requests.post(url, json=Anki.cartao(f'<video src="{video.nome}.mp4" controls></video>', video.nome, entrada['deck']))
                    
                    break
        
        elif escolha == '6':
            print(entrada)
            with open("input.json", "w") as f:
                json.dump(entrada, f, indent=4)
            os.system('pkill anki')
            break

        else:
            print('opção inválida')


if __name__ == "__main__":
    main()

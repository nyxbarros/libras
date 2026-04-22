import os

class Video:
    def __init__(self, videoBase, nome, inicio, fim):
        """Classe sendo representante de cada recorte menor do vídeo base

        Args:
            videoBase (str): nome do arquivo base .mp4 (sem extenção do arquivo)
            nome (str): nome do recorte do vídeo (sem extenção do arquivo)
            inicio (str): minutagem que começa o trecho (formato: hh:mm:ss)
            fim (str): minutagem que termina o trecho (formato: hh:mm:ss)
        """        
        self.videoBase = os.path.expanduser(videoBase)
        self.nome = nome
        self.inicio = inicio
        self.fim = fim
        self.lugar = None

        self.cortar()

    def cortar(self):
        os.system(f'ffmpeg -ss {self.inicio} -to {self.fim} -i "{self.videoBase}.mp4" -c copy "{self.nome}.mp4" -y')
        self.lugar = os.path.expanduser(f'{self.nome}.mp4')

    def mover(self, dest = '/home/capivara/.var/app/net.ankiweb.Anki/data/Anki2/Usuário 1/collection.media'):
        os.system(f'mv "{self.lugar}" "{dest}"')
        self.lugar = dest
        
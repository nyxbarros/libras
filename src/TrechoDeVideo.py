
import Palavra
import subprocess
from pathlib import Path
import os
import requests
from moviepy import VideoFileClip

class TrechoDeVideo:
    url = "http://localhost:8765"

    def __init__(self, deck, palavra):
        self.caminho = None
        self.deck = deck
        self.palavra = palavra

    def cortar(self, video):
        # Formata [minuto, segundo] para MM:SS
        inicio = f"{int(self.palavra.inicio[0]):02d}:{int(self.palavra.inicio[1]):02d}"
        fim = f"{int(self.palavra.fim[0]):02d}:{int(self.palavra.fim[1]):02d}"

        # Define o caminho de saída em libras/videos/
        pasta_videos = Path(__file__).parent / '..' / "videos"
        pasta_videos.mkdir(parents=True, exist_ok=True)

        # Salva o caminho na instância
        self.caminho = str(pasta_videos / f"{self.palavra.nome}.mp4")

        # Executa o corte com FFmpeg
        subprocess.run([
            "ffmpeg", "-ss", inicio, "-i", video, "-to", fim,
            "-c", "copy", "-y", self.caminho
        ], check=True)

    def salvar(self):
        self.enviar_revisao_entendimento()
        self.enviar_revisao_expressao()

    def enviar_revisao_entendimento(self):
        requests.post(TrechoDeVideo.url, json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": f"{self.deck} - entender",
                    "modelName": "Basic",
                    "fields": {
                        "Front": self.caminho,
                        "Back": self.palavra.nome
                    }
                }
            }
        })

    def enviar_revisao_expressao(self):
        requests.post(TrechoDeVideo.url, json={
            "action": "addNote",
            "version": 6,
            "params": {
                "note": {
                    "deckName": f"{self.deck} - expressar",
                    "modelName": "Basic",
                    "fields": {
                        "Front": self.palavra.nome,
                        "Back": self.caminho
                    }
                }
            }
        })
from yt_dlp import YoutubeDL
from pathlib import Path


class  Utils:
    @staticmethod
    def download_youtube(url):
        # pasta onde está o script
        PASTA_SCRIPT = Path(__file__).parent

        # cria pasta downloads dentro dela
        pasta_downloads = PASTA_SCRIPT / '..' / "videos"
        pasta_downloads.mkdir(exist_ok=True)

        ydl_opts = {
            'outtmpl': str(pasta_downloads / '%(title)s.%(ext)s'),
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return pasta_downloads.resolve()

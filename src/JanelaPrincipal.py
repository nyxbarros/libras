import os
import tkinter as tk
from pathlib import Path
from time import sleep
from tkinter import ttk
import TrechoDeVideo
from FormPalavra import FormPalavra  # Importa a nova janela
from TrechoDeVideo import TrechoDeVideo
from src.Utils import Utils
import subprocess

# videos/video_base.webm
class JanelaPrincipal(tk.Tk):
    def __init__(self):
        super().__init__()

        subprocess.Popen(["anki"])
        sleep(5)

        self.item_selecionado = None
        self.palavras = []

        self.title("Gerador de cards anki a partir de vídeos")
        self.grid_columnconfigure(0, weight=3, uniform="grupo1")
        self.grid_columnconfigure(1, weight=1, uniform="grupo1")
        self.grid_columnconfigure(2, weight=8, uniform="grupo1")

        self.idioma = tk.StringVar()
        self.idioma.set('Libras')
        self.idioma_label = tk.Label(self, text="Idioma")
        self.idioma_label.grid(row=0, column=0, columnspan=2, padx=8, pady=10)
        self.idioma_input = tk.Entry(self, textvariable=self.idioma)
        self.idioma_input.grid(row=0, column=2, columnspan=1, padx=8, pady=10, sticky=tk.W+tk.E)

        self.video_label = tk.Label(self, text="O vídeo para ser cortado")
        self.video_label.grid(row=1, column=0, columnspan=2, padx=8, pady=10)
        self.video_input = tk.Entry(self)
        self.video_input.grid(row=1, column=2, columnspan=1, padx=8, pady=10, sticky=tk.W+tk.E)


        self.botao_atualizar_tabela = tk.Button(self, text="Atualizar\nTabela", command=self.atualizar_tabela, font=("Ariel", 6, "bold"))
        self.botao_atualizar_tabela.grid(row=2, column=0, pady=(10, 20))
        self.botao_adicionar_palavra = tk.Button(self, text="Adicionar Palavra", command=self.criar_card)
        self.botao_adicionar_palavra.grid(row=2, column=1, columnspan=2, pady=(10, 20))

        self.tabela = ttk.Treeview(self, columns=("nome", "inicio", "fim"), show="headings")

        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("inicio", text="Início")
        self.tabela.heading("fim", text="Fim")

        self.tabela.grid(row=3, column=0, columnspan=3, sticky="nsew")

        # menu de contexto
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Editar", command=self.editar_card)
        self.menu.add_command(label="Remover", command=self.remover_card)

        self.botao_atualizar_tabela = tk.Button(self, text="Enviar cards para o Anki", command=self.enviar_para_anki)
        self.botao_atualizar_tabela.grid(row=5, column=0, columnspan=3, pady=(20, 20))

        # bind botão direito
        self.tabela.bind("<Button-3>", self.abrir_menu)

    def enviar_para_anki(self):
        video = self.video_input.get()
        if 'youtube.com/' in video or 'youtu.be/' in video:
            Utils.download_youtube(video)
        else:
            os.system(f'cp \"{video}\" \"{(Path(__file__).parent / ".." / "videos" / video.split("/")[-1]).resolve()}\"')


        video = (Path(__file__).parent / '..' / 'videos' / video.split('/')[-1]).resolve()

        for palavra in self.palavras:
            trecho = TrechoDeVideo(self.idioma_input.get(), palavra)
            trecho.cortar(video)
            trecho.salvar()
            print('salvo' + palavra.nome)


    def abrir_menu(self, event):
        # identifica item clicado
        self.item_selecionado = self.tabela.identify_row(event.y)

        if self.item_selecionado:
            self.tabela.selection_set(self.item_selecionado)
            self.menu.post(event.x_root, event.y_root)

    def receber_cartao(self, cartao):
        self.tabela.insert("", "end", values=(cartao.nome, f'{cartao.inicio[0]}:{cartao.inicio[1]}', f'{cartao.fim[0]}:{cartao.fim[1]}'))
        self.palavras.append(cartao)

    def remover_card(self):
        self.palavras.remove(self.tabela.item(self.item_selecionado, "values"))
        self.tabela.delete(self.item_selecionado)

    def criar_card(self):
        FormPalavra(self, self.receber_cartao, self.palavras)

    def editar_card(self):
        cartao = self.tabela.item(self.item_selecionado, "values")
        FormPalavra(self, self.receber_cartao, self.palavras, cartao)
        self.tabela.delete(self.item_selecionado)

    def atualizar_tabela(self):
        self.tabela.delete(*self.tabela.get_children())
        for cartao in sorted(self.palavras):
            self.tabela.insert("", "end", values=(cartao.nome, f'{cartao.inicio[0]}:{cartao.inicio[1]}', f'{cartao.fim[0]}:{cartao.fim[1]}'))



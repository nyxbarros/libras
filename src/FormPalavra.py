import tkinter as tk

from Palavra import Palavra

class FormPalavra(tk.Toplevel):
    def __init__(self, pai, callback, lista, selecionado = None):
        # Inicializa o construtor do tk.Toplevel passando a janela principal como pai
        super().__init__(pai)
        self.callback = callback
        self.lista = lista

        # Configurações da nova janela
        if selecionado is None:
            self.title("adicionar palavra")
        else:
            self.title("editar palavra")
        # self.geometry("412x150")

        # Torna a janela secundária "modal" (bloqueia cliques na janela principal até fechar)
        self.grab_set()

        # Formulário
        self.nome_label = tk.Label(self, text="A palavra: ")
        self.nome_label.grid(row=0, column=0, sticky='e')
        self.nome_input = tk.Entry(self)
        self.nome_input.insert(0, '' if selecionado is None else selecionado[0])
        self.nome_input.grid(row=0, column=1, columnspan=3, sticky='w')

        self.var_minuto_inicio, self.var_segundo_inicio, self.var_minuto_fim, self.var_segundo_fim = tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()

        if selecionado is not None:
            selecionado = list(selecionado)

            selecionado[1] = selecionado[1].split(':')

            selecionado[2] = selecionado[2].split(':')

        self.horario_inicial_label = tk.Label(self, text="Minutagem inicial da palavra: ")
        self.horario_inicial_label.grid(row=1, column=0, sticky='e')
        self.horario_inicial_minuto_input = tk.Spinbox(self, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Arial", 12), textvariable=self.var_minuto_inicio)
        self.var_minuto_inicio.set("00" if selecionado is None else selecionado[1][0])
        self.horario_inicial_minuto_input.grid(row=1, column=1)
        label_separador = tk.Label(self, text=":", font=("Arial", 12))
        label_separador.grid(row=1, column=2)
        self.horario_inicial_segundo_input = tk.Spinbox(self, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Arial", 12))
        self.var_segundo_inicio.set("00" if selecionado is None else selecionado[1][1])
        self.horario_inicial_segundo_input.grid(row=1, column=3)

        self.horario_final_label = tk.Label(self, text="Minutagem final da palavra: ")
        self.horario_final_label.grid(row=2, column=0, sticky='e')
        self.horario_final_minuto_input = tk.Spinbox(self, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Arial", 12))
        self.var_minuto_fim.set("00" if selecionado is None else selecionado[2][0])
        self.horario_final_minuto_input.grid(row=2, column=1)
        label_separador = tk.Label(self, text=":", font=("Arial", 12))
        label_separador.grid(row=2, column=2)
        self.horario_final_segundo_input = tk.Spinbox(self, from_=0, to=59, format="%02.0f", width=3, wrap=True, font=("Arial", 12))
        self.var_segundo_fim.set("00" if selecionado is None else selecionado[2][1])
        self.horario_final_segundo_input.grid(row=2, column=3)


        self.aviso = tk.Label(self, font=("Arial", 12), fg="red")
        self.aviso.grid(row=3, column=0, columnspan=5)

        # Botão para fechar a janela atual

        self.botao_salvar = tk.Button(self, text="Salvar", command=self.salvar_palavra)
        self.botao_salvar.grid(row=5, column=0, columnspan=5)

    def salvar_palavra(self):
        nome = self.nome_input.get()
        minuto_inicio = self.horario_inicial_minuto_input.get()
        segundo_inicio = self.horario_inicial_segundo_input.get()
        minuto_final = self.horario_final_minuto_input.get()
        segundo_final = self.horario_final_segundo_input.get()

        if nome == '':
            self.aviso.config(text = 'o campo "A palavra" não pode ser vazio')
        elif nome in self.lista:
            self.aviso.config(text = 'não é permitido palavra repetida')
        elif (minuto_inicio > minuto_final) or (minuto_inicio == minuto_final and segundo_inicio > segundo_final):
            self.aviso.config(text = 'a minutagem inicial não pode ser maior que a final')
        else:
            cartao = Palavra(nome, [minuto_inicio, segundo_inicio], [minuto_final, segundo_final])
            self.callback(cartao)
            self.destroy()
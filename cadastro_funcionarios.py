import tkinter as tk
import json
import tkinter.ttk as ttk
import perceptron_employee_performance as pep


class Aplicacao:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastro de Funcionário")
        self.janela.geometry("400x300")  # Defina o tamanho da janela aqui

        # Labels
        tk.Label(janela, text="Nome:").grid(row=0, column=0)
        tk.Label(janela, text="Tarefas Concluídas:").grid(row=1, column=0)
        tk.Label(janela, text="Erros Cometidos:").grid(row=2, column=0)

        # Entradas de texto
        self.nome_entry = tk.Entry(janela)
        self.tarefas_entry = tk.Entry(janela)
        self.erros_entry = tk.Entry(janela)

        self.nome_entry.grid(row=0, column=1)
        self.tarefas_entry.grid(row=1, column=1)
        self.erros_entry.grid(row=2, column=1)

        # Botão para salvar
        self.salvar_botao = tk.Button(janela, text="Salvar", command=self.salvar_dados)
        self.salvar_botao.grid(row=3, column=0, columnspan=2)

        # Botão para abrir a segunda janela
        self.abrir_janela_botao = tk.Button(janela, text="Abrir Segunda Janela", command=self.abrir_segunda_janela)
        self.abrir_janela_botao.grid(row=4, column=0, columnspan=2)

    def salvar_dados(self):
        nome = self.nome_entry.get()
        tarefas_concluidas = int(self.tarefas_entry.get())
        erros_cometidos = int(self.erros_entry.get())

        # Criar um dicionário com os dados
        dados = {
            "Nome": nome,
            "Tarefas Concluídas": tarefas_concluidas,
            "Erros Cometidos": erros_cometidos
        }

        # Abrir o arquivo JSON para adicionar os dados
        try:
            with open("dados_funcionarios.json", "r") as arquivo:
                funcionarios = json.load(arquivo)
        except FileNotFoundError:
            funcionarios = []

        funcionarios.append(dados)

        # Salvar os dados de volta no arquivo JSON
        with open("dados_funcionarios.json", "w") as arquivo:
            json.dump(funcionarios, arquivo, indent=4)

        # Limpar as entradas de texto
        self.nome_entry.delete(0, tk.END)
        self.tarefas_entry.delete(0, tk.END)
        self.erros_entry.delete(0, tk.END)

        print("Dados salvos com sucesso!")

        # Atualize a lista de funcionários na segunda janela
        self.atualizar_lista_funcionarios_segunda_janela()

    def abrir_segunda_janela(self):
        self.segunda_janela = tk.Toplevel()
        self.segunda_janela.title("Cálculo de Eficiência")

        # Label para selecionar um funcionário
        tk.Label(self.segunda_janela, text="Selecione um funcionário:").pack()

        # Lista de nomes de funcionários
        self.var_nome_selecionado = tk.StringVar()
        self.dropdown = tk.OptionMenu(self.segunda_janela, self.var_nome_selecionado, "")
        self.dropdown.pack()

        # Botão para calcular eficiência e classificar
        calcular_botao = tk.Button(self.segunda_janela, text="Calcular Eficiência e Classificar", command=self.calcular_eficiencia)
        calcular_botao.pack()

        # Label para mostrar a eficiência calculada
        self.label_eficiencia = tk.Label(self.segunda_janela, text="")
        self.label_eficiencia.pack()

        # Label para mostrar a classificação
        self.label_classificacao = tk.Label(self.segunda_janela, text="")
        self.label_classificacao.pack()

        # Atualize a lista de funcionários na segunda janela
        self.atualizar_lista_funcionarios_segunda_janela()

    def atualizar_lista_funcionarios_segunda_janela(self):
        # Carregar dados dos funcionários do arquivo JSON
        with open("dados_funcionarios.json", "r") as arquivo:
            dados = json.load(arquivo)

        # Obtenha a lista de nomes de funcionários
        nomes_funcionarios = [funcionario["Nome"] for funcionario in dados]

        # Atualize a lista de opções do dropdown na segunda janela
        self.var_nome_selecionado.set(nomes_funcionarios[0])
        menu = self.dropdown["menu"]
        menu.delete(0, "end")
        for nome in nomes_funcionarios:
            menu.add_command(label=nome, command=lambda nome=nome: self.var_nome_selecionado.set(nome))

    def calcular_eficiencia(self):
        nome_selecionado = self.var_nome_selecionado.get()
        dados_funcionarios = self.carregar_dados_funcionarios()

        for funcionario in dados_funcionarios:
            if funcionario["Nome"] == nome_selecionado:
                tarefas_concluidas = funcionario["Tarefas Concluídas"]
                erros_cometidos = funcionario["Erros Cometidos"]
                eficiencia = tarefas_concluidas / (tarefas_concluidas + erros_cometidos) * 100
                self.label_eficiencia.config(text=f"Eficiência de {nome_selecionado}: {eficiencia:.2f}%")

                # Classificar o funcionário
                funcionario_obj = pep.Funcionario(nome_selecionado, tarefas_concluidas, erros_cometidos)
                classificacao = self.classificar_funcionario(funcionario_obj)
                if classificacao == 1:
                    self.label_classificacao.config(text=f"Com base no treinamento da IA:\n {nome_selecionado} é classificado como Eficiente.")
                else:
                    self.label_classificacao.config(text=f"Com base no treinamento da IA:\n {nome_selecionado} é classificado como Ineficiente.")
    
    def carregar_dados_funcionarios(self):
        # Carregar dados dos funcionários do arquivo JSON
        with open("dados_funcionarios.json", "r") as arquivo:
            dados = json.load(arquivo)
        return dados

    def classificar_funcionario(self, funcionario):
        dados_treinamento = pep.DadosTreinamento()
        avaliador = pep.AvaliadorDesempenho(dados_treinamento)
        previsao = avaliador.classificar_funcionario(funcionario)
        return previsao

if __name__ == "__main__":
    janela = tk.Tk()
    Aplicacao(janela)
    janela.mainloop()
import json
from sklearn.linear_model import Perceptron

class Funcionario:
    def __init__(self, nome, tarefas_concluidas, erros_cometidos):
        self.nome = nome
        self.caracteristicas = [tarefas_concluidas, erros_cometidos]

class DadosTreinamento:
    def __init__(self):
        self.X = [[2, 0], [0, 3], [3, 3], [2, 2]]
        self.y = [1, 0, 1, 1]  # 1 para Eficiente, 0 para Ineficiente

    def verificar_dados(self):
        if self.X == [[2, 0], [0, 3], [3, 3], [2, 2]] and self.y == [1, 0, 1, 1]:
            print("\033[92mTreinamento estão corretos\033[0m\n")
        else:
            print("\033[91mTreinamento inválido\033[0m\n")

    def calcular_precisao(self, clf):
        previsoes = clf.predict(self.X)
        corretos = sum(1 for p, r in zip(previsoes, self.y) if p == r)
        total = len(self.y)
        precisao = (corretos / total) * 100
        return precisao

class AvaliadorDesempenho:
    def __init__(self, dados_treinamento):
        self.clf = Perceptron()
        self.treinar_modelo(dados_treinamento)

    def treinar_modelo(self, dados_treinamento):
        self.clf.fit(dados_treinamento.X, dados_treinamento.y)

    def classificar_funcionario(self, funcionario):
        previsao = self.clf.predict([funcionario.caracteristicas])[0]
        return previsao

class Visualizador:
    @staticmethod
    def mostrar_classificacao(funcionario, eficiente):
        if eficiente:
            print(f"\033[92mO funcionario {funcionario.nome} é classificado como Eficiente.\033[0m")
        else:
            print(f"\033[91mO funcionario {funcionario.nome} é classificado como Ineficiente.\033[0m")

def main():
    # Carregar dados dos funcionários do arquivo JSON
    dados_funcionarios = []
    with open("dados_funcionarios.json", "r") as arquivo:
        dados = json.load(arquivo)
        for item in dados:
            funcionario = Funcionario(item["Nome"], item["Tarefas Concluídas"], item["Erros Cometidos"])
            dados_funcionarios.append(funcionario)

    # Dados de treinamento
    dados_treinamento = DadosTreinamento()
    dados_treinamento.verificar_dados()

    # Avaliador de desempenho
    avaliador = AvaliadorDesempenho(dados_treinamento)
    visualizador = Visualizador()

    # Faça previsões para os novos funcionários
    for funcionario in dados_funcionarios:
        previsao = avaliador.classificar_funcionario(funcionario)
        visualizador.mostrar_classificacao(funcionario, previsao == 1)

    # Calcular e imprimir a precisão
    precisao = dados_treinamento.calcular_precisao(avaliador.clf)
    print(f'\nPrecisão do modelo: {precisao:.2f}%\n')

if __name__ == "__main__":
    main()

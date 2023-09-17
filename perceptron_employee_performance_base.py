from sklearn.linear_model import Perceptron

# Dados de treinamento
# Características dos funcionários (número de tarefas concluídas e número de erros cometidos)
X = [[2, 0], [0, 3], [3, 3], [2, 2]]
y = [1, 0, 1, 1]  # 1 para Eficiente, 0 para Ineficiente

# Crie o modelo Perceptron
clf = Perceptron()

# Treine o modelo
clf.fit(X, y)

# Dados dos novos funcionários
dados_novos_funcionarios = [
    ['Silas', [1, 1]],
    ['Thiago', [2, 4]],
    ['Eduarda', [3, 0]]
]

# Faça previsões para os novos funcionários
for funcionario in dados_novos_funcionarios:
    nome = funcionario[0]
    caracteristicas = funcionario[1]
    previsao = clf.predict([caracteristicas])[0]

    if previsao == 1:
        print(f"O funcionário {nome} é classificado como Eficiente.")
    else:
        print(f"O funcionário {nome} é classificado como Ineficiente.")

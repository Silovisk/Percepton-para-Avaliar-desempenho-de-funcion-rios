import cadastro_funcionarios as cf
import perceptron_employee_performance as pep

if __name__ == "__main__":
    # Execute o código em perceptron_employee_performance.py
    pep.main()

    # Execute o código em cadastro_funcionarios.py
    janela = cf.tk.Tk()
    aplicacao = cf.Aplicacao(janela)
    janela.mainloop()


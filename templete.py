from models import *
from views import *
from datetime import datetime
from tabulate import tabulate


class UI:
    """
    Interface do usuário para interação com o sistema bancário.
    """
    
    def start(self):
        """
        Inicia o menu interativo para o usuário.
        """
        while True:
            print('''
            [1] -> Criar conta
            [2] -> Desativar conta
            [3] -> Transferir dinheiro
            [4] -> Movimentar dinheiro
            [5] -> Total contas
            [6] -> Filtrar histórico
            [7] -> Gráfico
            [8] -> Ativar conta
            [9] -> Sair
                  ''')
            
            try:
                choice = int(input('Escolha uma opção: '))
            except ValueError:
                print("Opção inválida! Digite um número.")
                continue

            match choice:
                case 1:
                    self._criar_conta()
                case 2:
                    self._desativar_conta()
                case 3:
                    self._transferir_saldo()
                case 4:
                    self._movimentar_dinheiro()
                case 5:
                    self._total_contas()
                case 6:
                    self._filtrar_movimentacoes()
                case 7:
                    self._criar_grafico()
                case 8:
                    self._ativar_conta()
                case 9:
                    print("Saindo...")
                    break
                case _:
                    print("Opção inválida!")
    
    def _criar_conta(self):
        """
        Solicita os dados ao usuário e cria uma nova conta bancária.
        """
        print('Digite o nome de um dos bancos abaixo:')
        for banco in Bancos:
            print(f'---{banco.value}---')
        
        banco = input().title()
        valor = float(input('Digite o valor inicial da conta: '))

        try:
            conta = Conta(banco=Bancos(banco), valor=valor)
            criar_conta(conta)
            print("Conta criada com sucesso!")
        except ValueError:
            print("Banco inválido! Tente novamente.")

    def _desativar_conta(self):
        """
        Desativa uma conta bancária escolhida pelo usuário.
        """
        print('Escolha a conta que deseja desativar.')
        for i in listar_contas():
            if i.valor == 0:
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor:.2f}')

        id_conta = int(input())

        try:
            desativar_conta(id_conta)
            print('Conta desativada com sucesso.')
        except ValueError:
            print('Essa conta ainda possui saldo. Faça uma transferência antes.')

    def _transferir_saldo(self):
        """
        Realiza a transferência de saldo entre contas.
        """
        print('Escolha a conta para retirar o dinheiro.')
        for i in listar_contas():
            print(f'{i.id} -> {i.banco.value} -> R$ {i.valor:.2f}')

        conta_retirar_id = int(input())

        print('Escolha a conta para enviar dinheiro.')
        for i in listar_contas():
            if i.id != conta_retirar_id:
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor:.2f}')

        conta_enviar_id = int(input())
        valor = float(input('Digite o valor para transferir: '))

        try:
            transferir_saldo(conta_retirar_id, conta_enviar_id, valor)
            print("Transferência realizada com sucesso!")
            self._exibir_historico()
        except ValueError as e:
            print(f"Erro: {e}")

    def _movimentar_dinheiro(self):
        """
        Registra uma movimentação financeira na conta selecionada.
        """
        print('Escolha a conta.')
        for i in listar_contas():
            print(f'{i.id} -> {i.banco.value} -> R$ {i.valor:.2f}')

        conta_id = int(input())
        valor = float(input('Digite o valor movimentado: '))

        print('Selecione o tipo da movimentação:')
        for tipo in Tipos:
            print(f'---{tipo.value}---')
        
        tipo = input().title()
        try:
            historico = Historico(conta_id=conta_id, tipo=Tipos(tipo), valor=valor, data=datetime.today().date())
            movimentar_dinheiro(historico)
            print("Movimentação registrada com sucesso!")
            self._exibir_historico()
        except ValueError as e:
            print(f"Erro: {e}")

    def _total_contas(self):
        """
        Exibe o saldo total de todas as contas.
        """
        print(f'Total disponível em todas as contas: R$ {total_contas():.2f}')

    def _filtrar_movimentacoes(self):
        """
        Filtra e exibe movimentações dentro de um intervalo de datas.
        """
        data_inicio = input('Digite a data de início (dd/mm/yyyy): ')
        data_fim = input('Digite a data final (dd/mm/yyyy): ')

        data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y').date()
        data_fim = datetime.strptime(data_fim, '%d/%m/%Y').date()

        resultados = buscar_historicos_entre_datas(data_inicio, data_fim)
        
        if not resultados:
            print("Nenhuma movimentação encontrada nesse período.")
            return

        dados = [
            [h.id, h.conta_id, h.tipo.value, f"R$ {h.valor:.2f}", h.data.strftime("%d/%m/%Y")]
            for h in resultados
        ]
        print(tabulate(dados, headers=["ID", "Conta", "Tipo", "Valor", "Data"], tablefmt="grid"))

    def _criar_grafico(self):
        """
        Gera um gráfico do saldo das contas ativas.
        """
        criar_grafico_por_conta()

    def _ativar_conta(self):
        """
        Ativa uma conta inativa.
        """
        print('Escolha a conta que deseja ativar.')
        for i in listar_contas():
            if i.status == Status.INATIVO:
                print(f'{i.id} -> {i.banco.value} -> R$ {i.valor:.2f}')

        id_conta = int(input())

        try:
            ativar_conta(id_conta)
            print('Conta ativada com sucesso.')
        except ValueError:
            print('Essa conta já está ativa.')

# Iniciar o programa
if __name__ == "__main__":
    UI().start()

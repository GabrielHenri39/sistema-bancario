from datetime import date
from typing import List, Optional
import matplotlib.pyplot as plt 
from sqlmodel import Session, select
from models import Conta, engine, Status, Historico, Tipos
from sqlmodel.exc import SQLAlchemyError # type: ignore



def criar_conta(conta: Conta) -> Optional[Conta]:
    """
    Cria uma nova conta, garantindo que não haja outra no mesmo banco.
    """
    with Session(engine) as session:
        existe = session.exec(select(Conta).where(Conta.banco == conta.banco)).first()
        if existe:
            raise ValueError("Já existe uma conta nesse banco!")
            
        session.add(conta)
        session.commit()
        return conta

def listar_contas() -> List[Conta]:
    """
    Lista todas as contas cadastradas.
    """
    with Session(engine) as session:
        statement = select(Conta)
        return session.exec(statement).all()

def desativar_conta(conta_id: int) -> None:
    """
    Desativa uma conta se não houver saldo disponível.
    """
    with Session(engine) as session:
        conta = session.exec(select(Conta).where(Conta.id == conta_id)).first()
        if not conta:
            raise ValueError("Conta não encontrada.")
        if conta.valor > 0:
            raise ValueError('Essa conta ainda possui saldo, não é possível desativar.')
        conta.status = Status.INATIVO
        session.commit()

def ativar_conta(conta_id: int) -> None:
    """
    Ativa uma conta caso esteja inativa.
    """
    with Session(engine) as session:
        conta = session.exec(select(Conta).where(Conta.id == conta_id)).first()
        if not conta:
            raise ValueError("Conta não encontrada.")
        if conta.status == Status.ATIVO:
            raise ValueError("Conta já está ativa.")
        conta.status = Status.ATIVO
        session.commit()

def transferir_saldo(id_conta_saida: int, id_conta_entrada: int, valor: float) -> None:
    """
    Transfere saldo entre contas, registrando a movimentação no histórico.
    """
    try:
        with Session(engine) as session:
            contas = session.exec(select(Conta).where(Conta.id.in_([id_conta_saida, id_conta_entrada])).with_for_update()).all()

            conta_saida, conta_entrada = contas if len(contas) == 2 else (None, None)

            if not conta_saida or not conta_entrada:
                raise ValueError("Uma das contas não existe.")
            if conta_saida.valor < valor:
                raise ValueError("Saldo insuficiente.")
            if id_conta_saida == id_conta_entrada:
                raise ValueError("Não é possível transferir para a mesma conta.")

            conta_saida.valor -= valor
            conta_entrada.valor += valor

            session.add(Historico(conta_id=id_conta_saida, tipo=Tipos.SAIDA, valor=valor, data=date.today()))
            session.add(Historico(conta_id=id_conta_entrada, tipo=Tipos.ENTRADA, valor=valor, data=date.today()))
            session.commit()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Erro no banco de dados: {e}")


def movimentar_dinheiro(historico: Historico) -> Historico:
    """
    Realiza uma movimentação financeira em uma conta e registra no histórico.
    """
    with Session(engine) as session:
        conta = session.exec(select(Conta).where(Conta.id == historico.conta_id)).first()
        if not conta:
            raise ValueError("Conta não encontrada.")
        if conta.status == Status.INATIVO:
            raise ValueError('Conta inativa.')
        if historico.tipo == Tipos.SAIDA and conta.valor < historico.valor:
            raise ValueError("Saldo insuficiente.")

        conta.valor += historico.valor if historico.tipo == Tipos.ENTRADA else -historico.valor
        session.add(historico)
        session.commit()
        return historico

def total_contas() -> float:
    """
    Calcula o saldo total de todas as contas.
    """
    with Session(engine) as session:
        return float(sum(conta.valor for conta in session.exec(select(Conta)).all()))

def buscar_historicos_entre_datas(data_inicio: date, data_fim: date) -> List[Historico]:
    """
    Retorna os registros do histórico entre duas datas.
    """
    with Session(engine) as session:
        return session.exec(select(Historico).where(
            (Historico.data >= data_inicio) & (Historico.data <= data_fim)
        )).all()

def criar_grafico_por_conta() -> None:
    """
    Gera um gráfico de barras mostrando os saldos das contas ativas por banco.
    """
    with Session(engine) as session:
        contas = session.exec(select(Conta).where(Conta.status == Status.ATIVO)).all()
        if not contas:
            raise ValueError("Nenhuma conta ativa encontrada.")
            
        bancos = [conta.banco.value for conta in contas]
        totais = [conta.valor for conta in contas]

    plt.bar(bancos, totais)
    plt.xlabel("Bancos")
    plt.ylabel("Saldo")
    plt.title("Saldo das Contas Ativas por Banco")
    plt.show()

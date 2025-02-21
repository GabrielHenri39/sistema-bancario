# Sistema de Gerenciamento Bancário

## Descrição
O **Sistema de Gerenciamento Bancário** é uma aplicação em Python que permite criar e gerenciar contas bancárias, realizar transferências, movimentar dinheiro, consultar históricos de transações e gerar relatórios gráficos. O sistema conta com um banco de dados SQLite para armazenar informações e utiliza uma interface de linha de comando para interação com o usuário.

## Tecnologias Utilizadas
- **Python**
- **SQLModel** (para interação com SQLite)
- **Matplotlib** (para geração de gráficos)
- **Tabulate** (para exibição de dados formatados em tabela)

## Estrutura do Projeto
```
/
├── models.py  # Definição das tabelas e estrutura do banco de dados
├── views.py   # Funções de manipulação do banco de dados e lógica de negócio
├── temple.py  # Interface de linha de comando para interação com o usuário
├── database.db  # Arquivo do banco de dados SQLite (gerado automaticamente)
```

## Instalação e Uso
### Requisitos
Antes de executar o projeto, certifique-se de ter o **Python 3.13+** instalado.

### Passos de Instalação
1. Clone o repositório:
   ```sh
   git clone https://github.com/GabrielHenri39/sistema-bancario.git
   cd sistema-bancario
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```sh
   python -m venv venv
   source venv/bin/activate  # No Windows, use venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Execute a criação do banco de dados:
   ```sh
   python models.py
   ```

4. Inicie o sistema:
   ```sh
   python temple.py
   ```

## Exemplo de Código
O trecho abaixo mostra a função que realiza uma transferência entre contas, garantindo que ambas existam e que haja saldo suficiente:

```python
def transferir_saldo(id_conta_saida: int, id_conta_entrada: int, valor: float) -> None:
    """
    Transfere saldo entre contas, registrando a movimentação no histórico.
    """
    with Session(engine) as session:
        contas = session.exec(select(Conta).where(Conta.id.in_([id_conta_saida, id_conta_entrada]))).all()
        
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
```

Essa função evita erros comuns, como transferências para a mesma conta e transações com saldo insuficiente.

## Como Contribuir
1. Fork este repositório.
2. Crie uma branch para sua nova feature:
   ```sh
   git checkout -b minha-feature
   ```
3. Implemente suas melhorias e faça commit:
   ```sh
   git commit -m "Adiciona nova funcionalidade"
   ```
4. Envie suas alterações:
   ```sh
   git push origin minha-feature
   ```
5. Abra um **Pull Request** no repositório original.



---

Desenvolvido por Gabriel Henrique Alves Dias.


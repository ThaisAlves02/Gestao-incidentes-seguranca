```python
from classBanco import Banco
from datetime import date, datetime

banco = Banco()


def verClientes():
    print("LISTA DE CLIENTES")

    clientes = banco.consultar('''
        SELECT cod_cliente, nome_cliente, cpf_cliente, email_cliente, telefone_cliente
        FROM clientes
        ORDER BY cod_cliente;
    ''')

    if (len(clientes) == 0):
        print("NÃO HÁ CLIENTES CADASTRADOS")
        return

    print("CÓDIGO | NOME | CPF | EMAIL | TELEFONE")
    for cod, nome, cpf, email, telefone in clientes:
        print(f"{cod} | {nome} | {cpf} | {email} | {telefone}")


def escolherCliente():
    verClientes()

    cod_escolhido = input("Digite o código do cliente desejado: ")

    consulta = banco.consultar('''
        SELECT cod_cliente, nome_cliente, cpf_cliente, email_cliente, telefone_cliente
        FROM clientes
        WHERE cod_cliente = %s;
    ''', (cod_escolhido,))

    if (len(consulta) == 0):
        print("cliente não encontrado!")
        return None

    cliente = consulta[0]

    print(f'''
    Ficha do cliente:

    Código: {cliente[0]}
    Nome: {cliente[1]}
    CPF: {cliente[2]}
    Email: {cliente[3]}
    Telefone: {cliente[4]}
    ''')

    return cliente


def cadastrarCliente():
    print("CADASTRO DE NOVO CLIENTE")

    nome = input("Digite o nome: ")
    cpf = input("Digite o cpf: ")
    email = input("Digite o email: ")
    telefone = input("Digite o telefone: ")

    try:
        banco.manipular('''
            INSERT INTO clientes
            VALUES (default, %s, %s, %s, %s);
        ''', (nome, cpf, email, telefone))
        print(" CADASTRADO COM SUCESSO!")
    except Exception as error:
        print(f"ERRO AO CADASTRAR. O erro foi: {error}.")


def alterarCliente():
    print("ATUALIZAÇÃO DE CLIENTE")

    cliente = escolherCliente()

    if (not cliente):
        print("Não é possível alterar o cliente. Cheque o código escolhido...")
        return

    continuar = input("Deseja alterar as informações do cliente? (S/N) ")

    if (continuar != "S"):
        return

    cod, nome, cpf, email, telefone = cliente

    print("ALTERAR DADOS:")
    print("(Deixe vazio para manter o original)")

    novo_nome = input(f"Digite o novo nome ({nome}): ").strip()
    if (novo_nome):
        nome = novo_nome

    novo_cpf = input(f"Digite o novo cpf ({cpf}): ").strip()
    if (novo_cpf):
        cpf = novo_cpf

    novo_email = input(f"Digite o novo email ({email}): ").strip()
    if (novo_email):
        email = novo_email

    novo_telefone = input(f"Digite o novo telefone ({telefone}): ").strip()
    if (novo_telefone):
        telefone = novo_telefone

    try:
        banco.manipular('''
            UPDATE clientes
            SET nome_cliente = %s,
                cpf_cliente = %s,
                email_cliente = %s,
                telefone_cliente = %s
            WHERE cod_cliente = %s;
        ''', (nome, cpf, email, telefone, cod))
        print("CLIENTE ATUALIZADO!")
    except Exception as error:
        print(f"Ocorreu um erro na atualização! O erro foi: {error}")


def removerCliente():
    print("REMOÇÃO DE CLIENTE")

    cliente = escolherCliente()

    if (not cliente):
        print("cliente não encontrado!")
        return

    continuar = input("DESEJA REALMENTE APAGAR ESSE CLIENTE? (S/N) ")

    if (continuar != "S"):
        print("Cancelando operação...")
        return

    try:
        banco.manipular('''
            DELETE FROM clientes
            WHERE cod_cliente = %s;
        ''', (cliente[0],))
        print("cliente removido com sucesso!")
    except Exception as error:
        print(f"Não foi possível remover o cliente! O erro foi: {error}")


def verAnalista():
    print("LISTA DE ANALISTAS")

    analista = banco.consultar('''
        SELECT cod_analista, nome_analista, email_analista
        FROM analista
        ORDER BY cod_analista
    ''')

    if (len(analista) == 0):
        print("NÃO HÁ ANALISTAS CADASTRADOS")
        return

    print("CÓDIGO | NOME | EMAIL")
    for cod, nome, email in analista:
        print(f"{cod} | {nome} | {email}")


def escolherAnalista():
    verAnalista()

    cod_escolhido = input("Digite o código do analista desejado: ")

    consulta = banco.consultar('''
        SELECT cod_analista, nome_analista, email_analista
        FROM analista
        WHERE cod_analista = %s;
    ''', (cod_escolhido,))

    if (len(consulta) == 0):
        print("analista não encontrado!")
        return None

    analista = consulta[0]

    print(f'''
        Ficha do analista:

        Código: {analista[0]}
        Nome: {analista[1]}
        Email: {analista[2]}
        ''')

    return analista


def cadastrarAnalista():
    print("CADASTRO DE NOVO analista")

    nome = input("Digite o nome: ")
    email = input("Digite o email: ")

    try:
        banco.manipular('''
            INSERT INTO analista
            VALUES (default, %s, %s);
        ''', (nome, email))
        print(" CADASTRADO COM SUCESSO!")
    except Exception as error:
        print(f"ERRO AO CADASTRAR. O erro foi: {error}.")


def alterarAnalista():
    print("ATUALIZAÇÃO DE analista")

    analista = escolherAnalista()

    if (not analista):
        print("Não é possível alterar o analista. Cheque o código escolhido...")
        return

    continuar = input("Deseja alterar as informações do analista? (S/N) ")

    if (continuar != "S"):
        return

    cod, nome, email = analista

    print("ALTERAR DADOS:")
    print("(Deixe vazio para manter o original)")

    novo_nome = input(f"Digite o novo nome ({nome}): ").strip()
    if (novo_nome):
        nome = novo_nome

    novo_email = input(f"Digite o novo email ({email}): ").strip()
    if (novo_email):
        email = novo_email

    try:
        banco.manipular('''
            UPDATE analista
            SET nome_analista = %s,
                email_analista = %s
            WHERE cod_analista = %s;
        ''', (nome, email, cod))
        print("analista ATUALIZADO!")
    except Exception as error:
        print(f"Ocorreu um erro na atualização! O erro foi: {error}")


def removerAnalista():
    print("REMOÇÃO DE analista")

    analista = escolherAnalista()

    if (not analista):
        print("analista não encontrado!")
        return

    continuar = input("DESEJA REALMENTE APAGAR ESSE analista? (S/N) ")

    if (continuar != "S"):
        print("Cancelando operação...")
        return

    try:
        banco.manipular('''
            DELETE FROM analista
            WHERE cod_analista = %s;
        ''', (analista[0],))
        print("analista removido com sucesso!")
    except Exception as error:
        print(f"Não foi possível remover o analista! O erro foi: {error}")


def verOcorrencias():
    print("LISTA DE OCORRÊNCIAS")

    ocorrencias = banco.consultar('''
        SELECT o.cod_ocorrencia, o.titulo, o.tipo_incidente,
               o.gravidade, o.status, c.nome_cliente,
               a.nome_analista
        FROM ocorrencia o
        JOIN clientes c
        ON c.cod_cliente = o.cod_cliente
        JOIN analista a
        ON a.cod_analista = o.cod_analista
        ORDER BY o.cod_ocorrencia;
    ''')

    if (len(ocorrencias) == 0):
        print("NÃO HÁ OCORRÊNCIAS CADASTRADAS")
        return

    print("CÓDIGO | TÍTULO | TIPO | GRAVIDADE | STATUS | CLIENTE | ANALISTA")

    for cod, titulo, tipo, gravidade, status, cliente, analista in ocorrencias:
        print(f"{cod} | {titulo} | {tipo} | {gravidade} | {status} | {cliente} | {analista}")


def escolherOcorrencia():
    verOcorrencias()

    cod_escolhido = input("Digite o código da ocorrência desejada: ")

    consulta = banco.consultar('''
        SELECT cod_ocorrencia, titulo, descricao, solucao,
               data_registro, tipo_incidente, gravidade,
               status, cod_cliente, cod_analista
        FROM ocorrencia
        WHERE cod_ocorrencia = %s;
    ''', (cod_escolhido,))

    if (len(consulta) == 0):
        print("OCORRÊNCIA NÃO ENCONTRADA!")
        return None

    ocorrencia = consulta[0]

    print(f'''
    Ficha da ocorrência:

    Código: {ocorrencia[0]}
    Título: {ocorrencia[1]}
    Descrição: {ocorrencia[2]}
    Solução: {ocorrencia[3]}
    Data de registro: {ocorrencia[4]}
    Tipo de incidente: {ocorrencia[5]}
    Gravidade: {ocorrencia[6]}
    Status: {ocorrencia[7]}
    Código do cliente: {ocorrencia[8]}
    Código do analista: {ocorrencia[9]} #código do analista responsável pela ocorrência antes da alteração.
    ''')

    return ocorrencia


def cadastrarOcorrencia():
    print("REGISTRO DE NOVA OCORRÊNCIA")

    titulo = input("Digite o título: ")
    descricao = input("Digite a descrição: ")
    data_registro = input("Digite a data (AAAA-MM-DD): ")
    tipo_incidente = input("Digite o tipo de incidente: ")
    gravidade = input("Digite a gravidade (baixa, média ou crítica): ")
    status = input("Digite o status (aberto, em investigação ou resolvido): ")
    cod_cliente = input("Digite o código do cliente: ")
    cod_analista = input("Digite o código do analista responsável: ")

    solucao = None

    if (status == "resolvido"):
        solucao = input("Descreva a solução aplicada: ")

    try:
        banco.manipular('''
            INSERT INTO ocorrencia
            VALUES (default, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (
            titulo, descricao, solucao, data_registro,
            tipo_incidente, gravidade, status,
            cod_cliente, cod_analista
        ))

        print("OCORRÊNCIA REGISTRADA COM SUCESSO!")

    except Exception as error:
        print(f"ERRO AO REGISTRAR OCORRÊNCIA: {error}")


def alterarOcorrencia():
    print("ATUALIZAÇÃO DE OCORRÊNCIA")

    try:
        cod_analista_logado = int(input("Informe seu código de analista: "))
    except ValueError:
        print("Código inválido. Digite apenas números.")
        return

    ocorrencia = escolherOcorrencia()

    if not ocorrencia:
        return

    if ocorrencia[9] != cod_analista_logado:
        print("Você não é o responsável por esta ocorrência.")
        return

    continuar = input("Deseja alterar as informações da ocorrência? (S/N) ")

    if (continuar != "S"):
        return

    cod, titulo, descricao, solucao, data_registro, tipo, gravidade, status, cod_cliente, cod_analista = ocorrencia

    print("ALTERAR DADOS:")
    print("(Deixe vazio para manter o original)")

    novo_titulo = input(f"Novo título ({titulo}): ").strip()
    if (novo_titulo):
        titulo = novo_titulo

    nova_descricao = input(f"Nova descrição ({descricao}): ").strip()
    if (nova_descricao):
        descricao = nova_descricao

    nova_solucao = input(f"Nova solução ({solucao}): ").strip()
    if (nova_solucao):
        solucao = nova_solucao

    nova_data = input(f"Nova data ({data_registro}): ").strip()
    if (nova_data):
        data_registro = nova_data

    novo_tipo = input(f"Novo tipo de incidente ({tipo}): ").strip()
    if (novo_tipo):
        tipo = novo_tipo

    nova_gravidade = input(f"Nova gravidade ({gravidade}): ").strip()
    if (nova_gravidade):
        gravidade = nova_gravidade

    novo_status = input(f"Novo status ({status}): ").strip()
    if (novo_status):
        status = novo_status

    novo_cod_cliente = input(f"Novo código do cliente ({cod_cliente}): ").strip()
    if (novo_cod_cliente):
        cod_cliente = novo_cod_cliente

    novo_cod_analista = input(f"Novo código do analista ({cod_analista}): ").strip()
    if (novo_cod_analista):
        cod_analista = novo_cod_analista

    if (status == "resolvido" and (not solucao or not solucao.strip())):
        solucao = input("Descreva a solução aplicada para resolver a ocorrência: ")

    try:
        banco.manipular('''
            UPDATE ocorrencia
            SET titulo = %s,
                descricao = %s,
                solucao = %s,
                data_registro = %s,
                tipo_incidente = %s,
                gravidade = %s,
                status = %s,
                cod_cliente = %s,
                cod_analista = %s
            WHERE cod_ocorrencia = %s;
        ''', (
            titulo, descricao, solucao, data_registro,
            tipo, gravidade, status, cod_cliente,
            cod_analista, cod
        ))

        print("OCORRÊNCIA ATUALIZADA!")

        # REGISTRO DAS ALTERAÇÕES NO HISTÓRICO

        data_alter = date.today()
        hora_alter = datetime.now().time()

        alteracoes = [
            ("status", ocorrencia[7], status),
            ("gravidade", ocorrencia[6], gravidade),
            ("cod_analista", str(ocorrencia[9]), str(cod_analista))
        ]

        for campo, valor_antigo, valor_novo in alteracoes:
            if (str(valor_antigo) != str(valor_novo)):
                banco.manipular('''
                    INSERT INTO historico
                    VALUES (default, %s, %s, %s, %s, %s, %s, %s);
                ''', (
                    cod, campo, str(valor_antigo), str(valor_novo),
                    data_alter, hora_alter, cod_analista_logado
                ))

    except Exception as error:
        print(f"ERRO AO ATUALIZAR OCORRÊNCIA: {error}")


def removerOcorrencia():
    print("REMOÇÃO DE OCORRÊNCIA")

    ocorrencia = escolherOcorrencia()

    if (not ocorrencia):
        print("OCORRÊNCIA NÃO ENCONTRADA!")
        return

    continuar = input("DESEJA REALMENTE REMOVER ESSA OCORRÊNCIA? (S/N) ")

    if (continuar != "S"):
        print("CANCELANDO OPERAÇÃO...")
        return

    try:
        banco.manipular('''
            DELETE FROM ocorrencia
            WHERE cod_ocorrencia = %s;
        ''', (ocorrencia[0],))

        print("OCORRÊNCIA REMOVIDA COM SUCESSO!")

    except Exception as error:
        print(f"ERRO AO REMOVER OCORRÊNCIA: {error}")


def consultarHistorico():
    print("CONSULTA DE HISTÓRICO")

    cod_ocorrencia = input("Digite o código da ocorrência: ")

    historico = banco.consultar('''
        SELECT h.cod_historico, h.cod_ocorrencia,
               h.campo_alter, h.valor_antigo, h.valor_novo,
               h.data_alter, h.hora_alter, a.nome_analista
        FROM historico h
        INNER JOIN analista a
            ON h.cod_analista_alter = a.cod_analista
        WHERE h.cod_ocorrencia = %s
        ORDER BY h.cod_historico;
    ''', (cod_ocorrencia,))

    if (len(historico) == 0):
        print("NÃO HÁ HISTÓRICO PARA ESSA OCORRÊNCIA.")
        return

    print("HISTÓRICO DA OCORRÊNCIA")

    for cod, ocorrencia, campo, antigo, novo, data, hora, analista in historico:
        print(f'''
        Código do histórico: {cod}
        Ocorrência: {ocorrencia}
        Campo alterado: {campo}
        Valor anterior: {antigo}
        Novo valor: {novo}
        Data da alteração: {data}
        Hora da alteração: {hora}
        Analista executor: {analista}
        --------------------------------
        ''')


while (True):
    print('''
    GESTÃO DE INCIDENTES DE SEGURANÇA

    1. Ver Clientes          6. Ver Analistas          11. Ver Ocorrências
    2. Escolher Cliente      7. Escolher Analista      12. Escolher Ocorrência
    3. Cadastrar Cliente     8. Cadastrar Analista     13. Cadastrar Ocorrência
    4. Alterar Cliente       9. Alterar Analista       14. Alterar Ocorrência
    5. Remover Cliente      10. Remover Analista      15. Remover Ocorrência

    16. Consultar Histórico

    0. Sair
    ========================================
    ''')

    op = input("DIGITE O NÚMERO DA OPÇÃO DESEJADA: ")

    if (op == "1"):
        verClientes()
    elif (op == "2"):
        escolherCliente()
    elif (op == "3"):
        cadastrarCliente()
    elif (op == "4"):
        alterarCliente()
    elif (op == "5"):
        removerCliente()
    elif op == "6":
        verAnalista()
    elif op == "7":
        escolherAnalista()
    elif op == "8":
        cadastrarAnalista()
    elif op == "9":
        alterarAnalista()
    elif op == "10":
        removerAnalista()
    elif op == "11":
        verOcorrencias()
    elif op == "12":
        escolherOcorrencia()
    elif op == "13":
        cadastrarOcorrencia()
    elif op == "14":
        alterarOcorrencia()
    elif op == "15":
        removerOcorrencia()
    elif op == "16":
        consultarHistorico()
    elif (op == "0"):
        print("Saindo do programa...")
        break
    else:
        print("ESCOLHA UMA OPÇÃO VÁLIDA")

    input("TECLE ENTER PARA CONTINUAR")
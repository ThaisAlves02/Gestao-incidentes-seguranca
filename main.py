from classBanco import Banco

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

    cod_escolhido = int(input("Digite o código do cliente desejado: "))

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
    CPF: {cliente[2]} minutos
    Email: {cliente[3]}
    Telefone: {cliente[3]}
    ''')

    return cliente

def cadastrarCliente():
    print("CADASTRO DE NOVO CLIENTE")

    nome = input("Digite o título do : ")
    cpf = int(input("Digite a duração (minutos): "))
    classificacao = input("Digite a classificação (L, 10, 12, 14, 16 ou 18): ")

    try:
        banco.manipular('''
            INSERT INTO s
            VALUES (default, %s, %s, %s);
        ''', (titulo, duracao, classificacao))
        print(" CADASTRADO COM SUCESSO!")
    except Exception as error:
        print("ERRO AO CADASTRAR ")


while (True):
    print('''
    GESTÃO DE INCIDENTES

    MENU:

    1. Ver clientes
    2. Escolher clientes
    3. Cadastrar clientes
    4. Alterar clientes
    5. Remover clientes

    0. Sair
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
    elif (op == "0"):
        print("Saindo do programa...")
        break
    else:
        print("ESCOLHA UMA OPÇÃO VÁLIDA")

    input("TECLE ENTER PARA CONTINUAR")
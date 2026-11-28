
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

conexao = None
cursor = None

try:
    conexao = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode=os.getenv("DB_SSL"),
    )
    cursor = conexao.cursor()

    cursor.execute("SELECT current_database(), CURRENT_DATE")
    linha = cursor.fetchone()
    print("Conectado! Resposta do banco:", linha)

    # 1. Remover tabelas existentes
    cursor.execute("DROP TABLE IF EXISTS historico")
    cursor.execute("DROP TABLE IF EXISTS ocorrencia")
    cursor.execute("DROP TABLE IF EXISTS analista")
    cursor.execute("DROP TABLE IF EXISTS clientes")

    # 2. Criar tabela clientes
    cursor.execute("""
        CREATE TABLE clientes (
            cod_cliente integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_cliente varchar(150) NOT NULL,
            cpf_cliente char(11) NOT NULL,
            email_cliente varchar(254) NOT NULL,
            telefone_cliente char(11) NOT NULL,
            CONSTRAINT uni_clientes_cpf UNIQUE (cpf_cliente),
            CONSTRAINT uni_clientes_email UNIQUE (email_cliente)
        )
    """)

    # 3. Criar tabela analista
    cursor.execute("""
        CREATE TABLE analista (
            cod_analista integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_analista varchar(150) NOT NULL,
            email_analista varchar(254) NOT NULL,
            CONSTRAINT uni_analista_email UNIQUE (email_analista)
        )
    """)

    # 4. Criar tabela ocorrencia
    cursor.execute("""
        CREATE TABLE ocorrencia (
            cod_ocorrencia integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            titulo varchar(150) NOT NULL,
            descricao varchar(250) NOT NULL,
            solucao varchar(250),
            data_registro date NOT NULL,
            tipo_incidente varchar(100) NOT NULL,
            gravidade varchar(100) NOT NULL,
            status varchar(100) NOT NULL,
            cod_cliente integer NOT NULL,
            cod_analista integer NOT NULL,
            CONSTRAINT fk_ocorrencia_clientes FOREIGN KEY (cod_cliente) REFERENCES clientes (cod_cliente),
            CONSTRAINT fk_ocorrencia_analista FOREIGN KEY (cod_analista) REFERENCES analista (cod_analista),
            CONSTRAINT ck_solucao CHECK (status != 'resolvido' OR (solucao IS NOT NULL AND BTRIM(solucao) != '')),
            CONSTRAINT ck_gravidade CHECK (gravidade IN ('baixa', 'média', 'crítica')),
            CONSTRAINT ck_status CHECK (status IN ('aberto', 'em investigação', 'resolvido'))
        )
    """)

    # 5. Criar tabela historico
    cursor.execute("""
        CREATE TABLE historico (
            cod_historico integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            cod_ocorrencia integer NOT NULL,
            campo_alter varchar(250) NOT NULL,
            valor_antigo varchar(250),
            valor_novo varchar(250),
            data_alter date NOT NULL,
            hora_alter time NOT NULL,
            cod_analista_alter integer NOT NULL,
            CONSTRAINT fk_historico_ocorrencia FOREIGN KEY (cod_ocorrencia) REFERENCES ocorrencia (cod_ocorrencia),
            CONSTRAINT fk_historico_analista FOREIGN KEY (cod_analista_alter) REFERENCES analista (cod_analista)
        )
    """)

    print("Tabelas criadas.")

    # 6. Inserir dados na tabela clientes
    cursor.execute("""
        INSERT INTO clientes
        (nome_cliente, cpf_cliente, email_cliente, telefone_cliente)
        VALUES
        ('Mariana Silva', '12345678901', 'mariana.silva@email.com', '85999887766'),
        ('Carlos Eduardo Santos', '23456789012', 'carlos.santos@email.com', '85988776655'),
        ('Fernanda Oliveira', '34567890123', 'fernanda.oliveira@email.com', '85977665544'),
        ('Pedro Henrique Lima', '45678901234', 'pedro.lima@email.com', '85966554433'),
        ('Beatriz Martins Souza', '56789012345', 'beatriz.souza@email.com', '85955443322')
        RETURNING cod_cliente;
    """)
    cod_clientes = [row[0] for row in cursor.fetchall()]

    # 7. Inserir dados na tabela analista
    cursor.execute("""
        INSERT INTO analista
        (nome_analista, email_analista)
        VALUES
        ('Lucas Ferreira', 'lucas.ferreira@empresa.com'),
        ('Juliana Costa', 'juliana.costa@empresa.com'),
        ('Rafael Almeida', 'rafael.almeida@empresa.com'),
        ('Camila Rodrigues', 'camila.rodrigues@empresa.com'),
        ('André Martins', 'andre.martins@empresa.com')
        RETURNING cod_analista;
    """)
    cod_analistas = [row[0] for row in cursor.fetchall()]

    # 8. Inserir dados na tabela ocorrencia
    cursor.execute("""
        INSERT INTO ocorrencia
        (titulo, descricao, solucao, data_registro, tipo_incidente, gravidade, status, cod_cliente, cod_analista)
        VALUES
        ('Lentidão no sistema de vendas', 'Sistema apresenta demora excessiva ao finalizar pedidos no caixa.', NULL, '2026-11-20', 'Performance', 'média', 'em investigação', %s, %s),

        ('Erro de autenticação no portal', 'Cliente recebe erro 500 ao tentar redefinir a senha de acesso.', NULL, '2026-11-22', 'Acesso', 'baixa', 'em investigação', %s, %s),

        ('Queda total do servidor de banco de dados', 'Banco principal ficou inacessível impedindo todas as operações.', 'Reiniciado o serviço do PostgreSQL e otimizado o pool de conexões.', '2026-11-24', 'Infraestrutura', 'crítica', 'em investigação', %s, %s),

        ('Tentativa de acesso não autorizado', 'Foram identificadas tentativas repetidas de acesso à conta de um cliente.', NULL, '2026-11-26', 'Segurança', 'crítica', 'em investigação', %s, %s),

        ('Falha no envio de notificações', 'O sistema deixou de enviar notificações automáticas aos clientes.', NULL, '2026-11-27', 'Sistema', 'média', 'em investigação', %s, %s)

        RETURNING cod_ocorrencia;
    """, (
        cod_clientes[0], cod_analistas[0],
        cod_clientes[1], cod_analistas[1],
        cod_clientes[2], cod_analistas[2],
        cod_clientes[3], cod_analistas[3],
        cod_clientes[4], cod_analistas[3]
    ))

    cod_ocorrencias = [row[0] for row in cursor.fetchall()]

    # 9. Inserir dados na tabela historico
    cursor.execute("""
        INSERT INTO historico
        (cod_ocorrencia, campo_alter, valor_antigo, valor_novo,
         data_alter, hora_alter, cod_analista_alter)
        VALUES
        (%s, 'status', 'aberto', 'em investigação',
         '2026-11-21', '09:00:00', %s),

        (%s, 'status', 'aberto', 'em investigação',
         '2026-11-23', '10:15:00', %s),

        (%s, 'status', 'aberto', 'em investigação',
         '2026-11-26', '09:30:00', %s),

        (%s, 'gravidade', 'baixa', 'média',
         '2026-11-27', '10:45:00', %s),

        (%s, 'cod_analista', %s, %s,
         '2026-11-27', '11:20:00', %s);
    """, (
        cod_ocorrencias[0], cod_analistas[0],
        cod_ocorrencias[1], cod_analistas[1],
        cod_ocorrencias[3], cod_analistas[3],
        cod_ocorrencias[4], cod_analistas[4],
        cod_ocorrencias[4],
        str(cod_analistas[4]),
        str(cod_analistas[3]),
        cod_analistas[4]
    ))

    print("Dados inseridos.")

    conexao.commit()
    print("Banco Gestão de Incidentes pronto.")

except Exception as error:
    if conexao is not None:
        conexao.rollback()

    print(f"O tipo do erro foi: {type(error).__name__}")
    print(f"Mensagem do erro: {error}")

finally:
    if cursor is not None:
        cursor.close()

    if conexao is not None:
        conexao.close()
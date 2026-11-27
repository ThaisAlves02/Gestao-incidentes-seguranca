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
        sslmode=os.getenv("DB_SSLMODE"),
    )
    cursor = conexao.cursor()

    cursor.execute("SELECT current_database(), CURRENT_DATE")
    linha = cursor.fetchone()
    print("Conectado! Resposta do banco:", linha)

    cursor.execute("DROP TABLE IF EXISTS historico")
    cursor.execute("DROP TABLE IF EXISTS ocorrencia")
    cursor.execute("DROP TABLE IF EXISTS analista")
    cursor.execute("DROP TABLE IF EXISTS clientes")

    cursor.execute("""
        CREATE TABLE clientes (
            cod_cliente integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_cliente varchar(150) NOT NULL,
            cpf_cliente char(11) NOT NULL UNIQUE,
            email_cliente varchar(254) NOT NULL UNIQUE,
            telefone_cliente char(11) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE analista (
            cod_analista integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_analista varchar(150) NOT NULL,
            email_analista varchar(254) NOT NULL UNIQUE
        )
    """)

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

    # 1. Tabela clientes
    cursor.execute("""
        INSERT INTO clientes (nome_cliente, cpf_cliente, email_cliente, telefone_cliente) VALUES
        ('Mariana Silva', '12345678901', 'mariana.silva@email.com', '85999887766'),
        ('Carlos Eduardo Santos', '23456789012', 'carlos.santos@email.com', '85988776655'),
        ('Fernanda Oliveira', '34567890123', 'fernanda.oliveira@email.com', '85977665544')
        RETURNING cod_cliente;
    """)
    cod_clientes = [row[0] for row in cursor.fetchall()]

    # 2. Tabela analista
    cursor.execute("""
        INSERT INTO analista (nome_analista, email_analista) VALUES
        ('Lucas Ferreira', 'lucas.ferreira@empresa.com'),
        ('Juliana Costa', 'juliana.costa@empresa.com'),
        ('Rafael Almeida', 'rafael.almeida@empresa.com')
        RETURNING cod_analista;
    """)
    cod_analistas = [row[0] for row in cursor.fetchall()]

    # 3. Tabela ocorrencia
    cursor.execute("""
        INSERT INTO ocorrencia (titulo, descricao, solucao, data_registro, tipo_incidente, gravidade, status, cod_cliente, cod_analista) VALUES
        ('Lentidão no sistema de vendas', 'Sistema apresenta demora excessiva ao finalizar pedidos no caixa.', NULL, '2026-11-20', 'Performance', 'média', 'aberto', %s, %s),
        ('Erro de autenticação no portal', 'Cliente recebe erro 500 ao tentar redefinir a senha de acesso.', NULL, '2026-11-22', 'Acesso', 'baixa', 'em investigação', %s, %s),
        ('Queda total do servidor de banco de dados', 'Banco principal ficou inacessível impedindo todas as operações.', 'Reiniciado o serviço do PostgreSQL e otimizado o pool de conexões.', '2026-11-24', 'Infraestrutura', 'crítica', 'em investigação', %s, %s)
        RETURNING cod_ocorrencia;
    """, (
        cod_clientes[0], cod_analistas[0],
        cod_clientes[1], cod_analistas[1],
        cod_clientes[2], cod_analistas[2]
    ))
    cod_ocorrencias = [row[0] for row in cursor.fetchall()]

    # 4. Tabela historico
    cursor.execute("""
        INSERT INTO historico (cod_ocorrencia, campo_alter, valor_antigo, valor_novo, data_alter, hora_alter, cod_analista_alter) VALUES
        (%s, 'status', 'aberto', 'em investigação', '2026-11-23', '10:15:00', %s),
        (%s, 'status', 'em investigação', 'resolvido', '2026-11-25', '14:30:00', %s),
        (%s, 'solucao', NULL, 'Reiniciado o serviço do PostgreSQL e otimizado o pool de conexões.', '2026-11-25', '14:30:00', %s);
    """, (
        cod_ocorrencias[1], cod_analistas[1],
        cod_ocorrencias[2], cod_analistas[2],
        cod_ocorrencias[2], cod_analistas[2]
    ))
    print("Dados inseridos.")

    conexao.commit()
    print("Banco Gestão de incidentes pronto.")

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
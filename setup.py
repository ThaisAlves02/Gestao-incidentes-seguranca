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

    cursor.execute("DROP TABLE IF EXISTS historico ")
    cursor.execute("DROP TABLE IF EXISTS ocorrencia ")
    cursor.execute("DROP TABLE IF EXISTS analista ")
    cursor.execute("DROP TABLE IF EXISTS clientes ")

    cursor.execute("""
        CREATE TABLE clientes (
            cod_cliente integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_cliente varchar(150) NOT NULL,
            cpf char(11) NOT NULL UNIQUE,
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
                CONSTRAINT ck_solucao CHECK (status != 'resolvido' OR BTRIM(solucao) != ''),
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

    cursor.execute("""
           INSERT INTO clientes (nome_cliente, cpf, email_cliente, telefone_cliente) VALUES
               ('Mariana Silva', '12345678901', 'mariana.silva@email.com', '85999991111'),
               ('Carlos Eduardo Santos', '98765432100', 'carlos.santos@email.com', '85988882222'),
               ('Fernanda Lima', '45678912309', 'fernanda.lima@email.com', '85977773333');
    """)

    cursor.execute("""
            INSERT INTO analista (nome_analista, email_analista) VALUES
            ('Lucas Almeida', 'lucas.almeida@empresa.com'),
            ('Beatriz Costa', 'beatriz.costa@empresa.com');
    """)

    cursor.execute("""
    INSERT INTO ocorrencia (titulo, descricao, solucao, data_registro, tipo_incidente, gravidade, status, cod_cliente, cod_analista) VALUES
    ('Falha no login do portal', 'Cliente relata erro 500 ao tentar acessar a área restrita.', NULL, '2026-11-20', 'Acesso / Autenticação', 'crítica', 'aberto', 1, 1),
    ('Lentidão na emissão de boletos', 'O sistema demora mais de 30 segundos para gerar o PDF.', NULL, '2026-11-22', 'Performance', 'média', 'em investigação', 2, 2),
    ('Divergência no valor da fatura', 'Cobrança duplicada identificada no fechamento mensal.', 'Estorno realizado e fatura recalculada corretamente.', '2026-11-18', 'Faturamento', 'baixa', 'resolvido', 3, 1);
    """)

    cursor.execute("""
    INSERT INTO historico (cod_ocorrencia, campo_alter, valor_antigo, valor_novo, data_alter, hora_alter, cod_analista_alter) VALUES
    (2, 'status', 'aberto', 'em investigação', '2026-11-23', '10:15:00', 2),
    (3, 'status', 'em investigação', 'resolvido', '2026-11-19', '16:40:00', 1),
    (3, 'solucao', NULL, 'Estorno realizado e fatura recalculada corretamente.', '2026-11-19', '16:40:00', 1);
    """)

except Exception as error:
    print(f"O tipo do erro foi: {type(error).__name__}")
    print(f"Mensagem do erro: {error}")

finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None:
                    conexao.close()
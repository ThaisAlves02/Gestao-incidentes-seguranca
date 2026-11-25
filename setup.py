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

    cursor.execute("DROP TABLE IF EXISTS clientes ")
    cursor.execute("DROP TABLE IF EXISTS analista ")
    cursor.execute("DROP TABLE IF EXISTS ocorrencia ")
    cursor.execute("DROP TABLE IF EXISTS historico ")

    cursor.execute("""
        CREATE TABLE clientes (
            cod_cliente integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_cliente varchar(150) NOT NULL,
            cpf char(11) NOT NULL UNIQUE,
            email_cliente varchar(254) NOT NULL UNIQUE,
            telefone_cliente char(11) NOT NULL,
        )
    """)

    cursor.execute("""
        CREATE TABLE analista (
            cod_analista integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            nome_analista varchar(150) NOT NULL,
            email_analista varchar(254) NOT NULL UNIQUE,
            )
            """)

    cursor.execute("""
            CREATE TABLE ocorrencia (
                cod_ocorrencia integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
                titulo varchar(150) NOT NULL,
                descricao varchar(250) NOT NULL,
                data_registro date NOT NULL,
                tipo_incidente varchar(100) NOT NULL,
                gravidade varchar(100) NOT NULL,
                status varchar(100) NOT NULL,
                cod_cliente integer NOT NULL,
                cod_analista integer NOT NULL,
                CONSTRAINT fk_ocorrencia_clientes FOREIGN KEY (cod_cliente) REFERENCES clientes (cod_cliente),
                CONSTRAINT fk_ocorrencia_analista FOREIGN KEY (cod_analista) REFERENCES analista (cod_analista),
                CONSTRAINT ck_descricao_solucao CHECK (status != 'resolvido' OR BTRIM(descricao_solucao) != '')
                )
            """)

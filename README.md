# Briefing — Gestão de Incidentes de Segurança

## 1. O cenário

O projeto consiste no desenvolvimento de um sistema para uma consultoria de Tecnologia da Informação especializada em Segurança da Informação, que presta serviços para pequenas equipes e empresas.

A consultoria precisa registrar e acompanhar incidentes de segurança relatados por seus clientes. Entretanto, quando essas informações ficam dispersas, torna-se mais difícil organizar os atendimentos, identificar os responsáveis e acompanhar o andamento de cada ocorrência.

## 2. O objetivo

Desenvolver um sistema para centralizar o registro, a organização e o acompanhamento de incidentes de segurança, permitindo que os analistas mantenham as informações dos clientes, registrem ocorrências e acompanhem seu andamento.

O sistema possui funcionamento manual: os incidentes são registrados pelos usuários, sem monitoramento ou detecção automática de ameaças.

## 3. Os usuários

O sistema atende a dois grupos principais:

- **Clientes:** pessoas que solicitam atendimento e possuem ocorrências registradas.
- **Analistas:** profissionais responsáveis por acompanhar e investigar as ocorrências.

## 4. As funcionalidades

O sistema permite:

- Cadastrar, consultar, alterar e remover clientes.
- Cadastrar, consultar, alterar e remover analistas.
- Registrar e acompanhar ocorrências.
- Definir o tipo, a gravidade e o status de cada ocorrência.
- Associar cada ocorrência a um cliente e a um analista responsável.
- Registrar a solução de uma ocorrência.
- Consultar o histórico de alterações realizadas nas ocorrências.
- Consultar ocorrências com os nomes dos clientes e analistas relacionados.

## 5. As regras e restrições

- Cada cliente pode possuir várias ocorrências.
- Cada ocorrência pertence a um único cliente.
- Cada ocorrência possui um analista responsável.
- Um analista pode ser responsável por várias ocorrências.
- O CPF de um cliente não pode se repetir.
- O e-mail de um cliente não pode se repetir.
- O e-mail de um analista não pode se repetir.
- A gravidade pode ser baixa, média ou crítica.
- O status pode ser aberto, em investigação ou resolvido.
- Uma ocorrência só pode ser marcada como resolvida quando possuir uma descrição da solução.

## 6. O histórico

O sistema mantém registros de alterações importantes nas ocorrências, incluindo mudanças de status, gravidade e analista responsável.

Cada registro informa o campo alterado, o valor anterior, o novo valor, a data e o horário da alteração e o analista que realizou a operação.

## 7. A regra de negócio principal

Uma ocorrência não pode ser marcada como resolvida sem que sua solução esteja preenchida.

A validação é realizada tanto no sistema Python quanto no banco de dados PostgreSQL, evitando o encerramento de ocorrências sem uma descrição da solução.

## 8. Limites do projeto

O sistema é uma aplicação acadêmica de gerenciamento e acompanhamento manual de incidentes. Não realiza varredura de redes, monitoramento contínuo, detecção automática de ameaças ou resposta automatizada a ataques.

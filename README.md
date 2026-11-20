# Gestão de Incidentes de Segurança

A empresa fictícia é uma pequena consultoria de Segurança da Informação que presta serviços a clientes individuais, contando com uma equipe de analistas responsável por investigar e acompanhar incidentes de segurança. O sistema deverá armazenar os dados dos clientes (nome, CPF, e-mail e telefone), dos analistas (nome e e-mail) e das ocorrências (título, descrição, data do registro, tipo de incidente, gravidade e status). Cada cliente poderá possuir várias ocorrências, mas cada ocorrência estará vinculada a um único cliente e a um analista responsável. Um analista poderá ser responsável por várias ocorrências.

**Regras do negócio:**

- O CPF do cliente não pode se repetir.
- O e-mail do cliente não pode se repetir.
- O e-mail do analista não pode se repetir.
- A gravidade de uma ocorrência deve ser baixa, média ou crítica.
- O status de uma ocorrência deve ser aberto, em investigação ou resolvido.
- Uma ocorrência só poderá ser resolvida quando possuir uma descrição da solução adotada.

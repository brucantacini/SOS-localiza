# DESAFIO FIAP: EVENTOS EXTREMOS - SOS Localiza

## Contexto

A natureza apresenta eventos climáticos extremos, como tempestades intensas, ventos fortes, inundações e deslizamentos. Com o aumento da ocorrência desses eventos, é fundamental criar soluções tecnológicas que auxiliem na prevenção, orientação e resposta rápida em situações de risco.

Este projeto foi desenvolvido como parte do desafio da FIAP para a disciplina *Building Relational Database*, com foco em uma aplicação Python que interage com um banco de dados Oracle para gerenciar informações sobre eventos climáticos adversos, localizações de risco e envio de alertas.

---

## Objetivo

Desenvolver uma aplicação em Python que implemente um sistema CRUD (Create, Read, Update, Delete) com funcionalidades voltadas para:

- Gerenciamento de localizações cadastradas pelo usuário (endereços de casa, trabalho etc).
- Consulta de previsões climáticas, com alertas de fortes chuvas.
- Visualização de orientações e cuidados para eventos extremos.
- Envio simulado de SMS para Defesa Civil em caso de emergência.
- Exportação de dados filtrados em arquivos JSON para análise.

---

## Requisitos do Sistema e Como foram atendidos

| Requisito                                                                                  | Implementação no projeto                                     |
|--------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| Menu de opções com principais funcionalidades                                              | Menu interativo no terminal com 12 opções disponíveis       |
| Validação das entradas do usuário                                                         | Tratamento de exceções e validações para entradas e tipos   |
| Uso de estruturas de decisão, repetição, listas e dicionários                             | Uso de `if`, `while`, `match-case`, listas e dicionários   |
| Organização em funções com passagem de parâmetros e retorno                               | Funções separadas para cada funcionalidade (CRUD, consultas)|
| Tratamento de exceções nas operações com banco de dados                                   | Uso de blocos `try-except` em todas operações DB            |
| Operações CRUD nas tabelas do banco de dados                                             | Inserir, consultar, alterar, excluir localizações e SMS     |
| Consultas com filtros e exportação para arquivos JSON                                    | Consultas por nome, ID, data com exportação em JSON         |

---

## Funcionalidades Principais

- **Permitir/Negar uso da localização atual**
- **Cadastrar localizações** (nome, rua, número, CEP)
- **Consultar todas as localizações cadastradas**
- **Alterar dados de uma localização existente**
- **Excluir localizações**
- **Verificar previsão do clima para uma cidade** (com alerta para chuvas fortes via API OpenWeatherMap)
- **Visualizar orientações para eventos adversos** (inundação, deslizamento, tempestades)
- **Enviar SMS de emergência (simulado)**
- **Buscar localizações, eventos e SMS com filtros e exportar resultados em JSON**

---

## Tecnologias Utilizadas

- Python 3.x
- Biblioteca `oracledb` para conexão com banco Oracle
- Biblioteca `requests` para consumo da API OpenWeatherMap
- Banco de dados Oracle com tabelas pré-configuradas

---

## Como executar

1. Configure a conexão Oracle no script (usuário, senha, host, porta, service_name).
2. Instale as dependências necessárias:
    ```bash
    pip install oracledb requests
    ```
3. Execute o script Python:
    ```bash
    python sos_localiza.py
    ```
4. Siga as instruções no menu interativo.

---

## Estrutura do Banco de Dados

- `T_SOS_LOCALIZACAO`: dados de locais cadastrados pelo usuário (nome, rua, número, CEP).
- `T_SOS_EVENTOS`: informações e orientações sobre eventos climáticos extremos.
- `T_SOS_SMS_ENVIADO`: registros de mensagens SMS enviadas (mensagem, data).

---

## Exportação JSON

Consultas específicas podem gerar arquivos JSON contendo:

- Localizações por nome (`localizacoes_por_nome.json`)
- Eventos filtrados por ID (`eventos_filtrados.json`)
- SMS enviados em determinada data (`sms_por_data.json`)

---

## Considerações Finais

Este sistema foi desenvolvido para atender aos requisitos do desafio FIAP "Eventos Extremos", combinando funcionalidades de banco de dados relacional com integração a APIs externas para alertas climáticos. O foco é auxiliar na prevenção e resposta rápida em situações de risco, utilizando tecnologia acessível e interativa.

---

## Autor

Bruno Cantacini

---

## Licença

Projeto disponibilizado sob licença MIT.

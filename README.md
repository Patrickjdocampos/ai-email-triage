# Auto-Mail - Assistente de Triagem de E-mails com IA

Projeto de automação para leitura, análise e classificação de e-mails com apoio de inteligência artificial generativa.

## Visão geral

O **Auto-Mail** foi criado para reduzir a sobrecarga de leitura manual da caixa de entrada. A proposta do projeto é conectar-se a uma conta de e-mail via IMAP, extrair o conteúdo das mensagens e utilizar um modelo de IA para gerar:

- uma **categoria**
- um **resumo curto**
- uma base para futuras automações de organização

Este projeto representa uma etapa inicial da minha trilha em Engenharia de IA, unindo automação, integração com serviços externos e classificação orientada por linguagem natural.

## Problema que o projeto resolve

Caixas de entrada acumulam mensagens de diferentes naturezas: cobranças, mensagens pessoais, marketing, spam e comunicações importantes.

Ler tudo manualmente é lento e pouco escalável.

Este projeto busca resolver esse problema por meio de uma rotina automatizada que:

1. acessa os e-mails não lidos
2. extrai o conteúdo textual
3. envia o texto para análise com IA
4. retorna uma categoria e um resumo objetivo

## Objetivos do projeto

- Automatizar a leitura de e-mails não lidos
- Classificar mensagens por tipo
- Resumir o conteúdo em linguagem simples
- Servir como base para futuras evoluções, como:
  - mover mensagens automaticamente entre pastas
  - sugerir respostas
  - criar prioridades de atendimento
  - registrar histórico de análise

## Arquitetura atual

O projeto está estruturado atualmente como um script Python com as seguintes responsabilidades:

- carregamento seguro de credenciais com `.env`
- conexão com a conta de e-mail via IMAP
- leitura das mensagens
- extração do corpo do e-mail
- envio do conteúdo textual para análise com Gemini
- retorno de categoria e resumo em formato JSON

## Stack utilizada

- **Python 3**
- **IMAPClient** para conexão e leitura de e-mails
- **python-dotenv** para gerenciamento de variáveis de ambiente
- **Google Gemini API** para classificação e sumarização
- **JSON** como formato de saída estruturada

## Categorias analisadas

Atualmente, o fluxo de análise considera categorias como:

- `FATURA`
- `PESSOAL`
- `MARKETING`
- `SPAM`
- `IMPORTANTE`

## Estrutura atual do repositório

```bash
Auto-Mail/
├── leitor_mail.py
├── README.md
├── LICENSE
├── .gitignore
└── .gitattributes

Conta de e-mail
   ↓
Leitura de mensagens via IMAP
   ↓
Extração do conteúdo textual
   ↓
Envio para modelo generativo
   ↓
Retorno em JSON com resumo + categoria

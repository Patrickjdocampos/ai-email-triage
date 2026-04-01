import email
from email.header import decode_header
import os
from dotenv import load_dotenv
import google.generativeai as genai
from imapclient import IMAPClient
import json

load_dotenv()

EMAIL = os.getenv('EMAIL')
SENHA = os.getenv('SENHA')
IMAP_SERVER = "imap.gmail.com"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

FOLDER_FINANCAS = 'Finanças'
FOLDER_PESSOAL = 'Pessoal'
FOLDER_SPAM = '[Gmail]/Spam'

genai.configure(api_key=GEMINI_API_KEY)

def get_email_body(msg):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True).decode('utf-8', 'ignore')
    else:
        return msg.get_payload(decode=True).decode('utf-8', 'ignore')

def analyze_email_with_gemini(text):
    """Envia um texto para a API do Gemini e retorna categoria e resumo em formato JSON."""
    if not text or not text.strip():
        return {"categoria": "DESCONHECIDO", "resumo": "Não foi possível extrair conteúdo."}
    
    prompt = f"""
    Analise o seguinte e-mail e retorne sua resposta estritamente no seguinte formato JSON:
    {{"categoria": "SUA_CATEGORIA", "resumo": "SEU_RESUMO"}}

    As categorias possíveis são: FATURA, PESSOAL, MARKETING, SPAM, IMPORTANTE.
    Se o conteúdo parecer um golpe, publicidade agressiva ou alerta de segurança suspeito, use a categoria SPAM.
    Resuma o e-mail em uma única frase concisa.

    E-mail:
    ---
    {text}
    ---
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_response)
    except Exception as e:
        return {"categoria": "ERRO", "resumo": f"Erro ao processar na IA: {e}"}

try:
    with IMAPClient(IMAP_SERVER) as client:
        client.login(EMAIL, SENHA)
        print(f"Login no e-mail {EMAIL} realizado com sucesso!\n")
        
        if not client.folder_exists(FOLDER_FINANCAS):
            client.create_folder(FOLDER_FINANCAS)
        if not client.folder_exists(FOLDER_PESSOAL):
            client.create_folder(FOLDER_PESSOAL)

        client.select_folder('INBOX')
        messages = client.search(['UNSEEN'])
        
        print(f"Encontrados {len(messages)} e-mails não lidos. Iniciando análise...")

        for uid, message_data in client.fetch(messages, 'RFC822').items():
            msg = email.message_from_bytes(message_data[b'RFC822'])
            
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()

            from_ = decode_header(msg.get("From"))[0][0]
            if isinstance(from_, bytes):
                from_ = from_.decode()
            
            body = get_email_body(msg)
            analysis = analyze_email_with_gemini(body)
            
            categoria = analysis.get('categoria', 'DESCONHECIDO')
            resumo = analysis.get('resumo', 'N/A')

            print("-" * 50)
            print(f"De: {from_}")
            print(f"Assunto: {subject}")
            print(f"Categoria IA: {categoria}")
            print(f"Resumo IA: {resumo}")

            try:
                if categoria == 'FATURA':
                    client.move(uid, FOLDER_FINANCAS)
                    print("Status: Movido para Finanças.")
                elif categoria == 'PESSOAL':
                    client.move(uid, FOLDER_PESSOAL)
                    print("Status: Movido para Pessoal.")
                elif categoria == 'SPAM':
                    client.move(uid, FOLDER_SPAM)
                    print("Status: Movido para Spam.")
                else:
                    client.add_flags(uid, [u'\\Seen'])
                    print("Status: Marcado como lido.")
            except Exception as e:
                print(f"Erro ao mover o e-mail: {e}")

except Exception as e:
    print(f"\nOcorreu um erro fatal: {e}")

finally:
    print("\n" + "="*50)
    print("Processo finalizado.")
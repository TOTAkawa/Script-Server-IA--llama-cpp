import os
import sys
import requests
from duckduckgo_search import DDGS
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

# 1. Configurar Conexões na Porta Física Local 8080
Settings.llm = OpenAI(
    model="gpt-4o", 
    api_base="http://127.0.0.1:8080/v1", 
    api_key="fortaleza",
    context_window=8192,
    temperature=0.1
)

Settings.embed_model = OpenAIEmbedding(
    model="text-embedding-3-small",
    api_base="http://127.0.0.1:8080/v1",
    api_key="fortaleza"
)

PERSIST_DIR = os.path.expanduser("~/fortaleza_ia/rag_nativo/indice_storage")
DOCS_DIR = os.path.expanduser("~/fortaleza_ia/rag_nativo/documentos")

def extrair_conteudo_real_url(url):
    """ Imita o Firefox do Arch Linux no cabeçalho para quebrar bloqueios de robôs """
    print(f"[📡] Burlando travas e extraindo dados da fonte real: {url}")
    
    # LINHA DE CÓDIGO CRUCIAL: Injeta a identidade de um navegador humano real
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"
    }
    
    try:
        # Usa a ponte do Jina Reader passando as permissões humanas falsas
        response = requests.get(f"https://jina.ai{url}", headers=headers, timeout=10)
        # Se retornar erro corporativo ou Cloudflare, rejeita para acionar o Fallback
        if response.status_code == 200 and "cloudflare" not in response.text.lower() and "captcha" not in response.text.lower():
            return response.text[:15000] 
    except Exception as e:
        print(f"[-] Bloqueio de rede detectado: {e}")
    return ""

def buscar_na_web_alta_precisao(query):
    print("[📡] Fazendo varredura profunda no DuckDuckGo...")
    try:
        with DDGS() as ddgs:
            resultados = [r for r in ddgs.text(query, max_results=3)]
            contexto_acumulado = ""
            for r in resultados:
                conteudo_bruto = extrair_conteudo_real_url(r['href'])
                
                # MECANISMO DE CONVENIÊNCIA: Se a página bloquear, suga os dados públicos do buscador
                if conteudo_bruto and len(conteudo_bruto.strip()) > 300:
                    contexto_acumulado += f"\n--- FONTE REAL: {r['href']} ---\n{conteudo_bruto}\n"
                else:
                    print(f"[!] Site protegido por Captcha. Extraindo dados públicos via DuckDuckGo: {r['href']}")
                    contexto_acumulado += f"\n--- DADOS PÚBLICOS ENCONTRADOS ({r['href']}) ---\n{r['body']}\n"
            return contexto_acumulado
    except Exception as e:
        return f"Erro na ponte de rede: {str(e)}"

def inicializar_ou_carregar_rag():
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        return load_index_from_storage(storage_context)
    else:
        if not os.listdir(DOCS_DIR):
            with open(os.path.join(DOCS_DIR, "placeholder.txt"), "w") as f:
                f.write("Base local vazia.")
        documents = SimpleDirectoryReader(DOCS_DIR).load_data()
        index = VectorStoreIndex.from_documents(documents)
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        return index

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[-] Erro: Digite uma pergunta.")
        sys.exit(1)
        
    pergunta_operador = " ".join(sys.argv[1:])
    
    if "http://" in pergunta_operador or "https://" in pergunta_operador:
        url_direta = [w for w in pergunta_operador.split() if "http" in w][0]
        dados_reais = extrair_conteudo_real_url(url_direta)
        if not dados_reais:
            print("[-] Erro: Este link específico exige verificação visual manual no Firefox.")
            sys.exit(1)
        prompt_estendido = (
            f"Você é um terminal utilitário offline estéril. Não dê desculpas e não simule nada. "
            f"Analise os dados brutos reais extraídos diretamente desta URL:\n{dados_reais}\n\n"
            f"Ordem do Operador: {pergunta_operador}"
        )
        print("[+] Processando dados extraídos no osso do metal...")
        resposta = Settings.llm.complete(prompt_estendido)
    else:
        palavras_chave_web = ["hoje", "atual", "noticia", "preco", "mercado", "tempo", "quem é", "quem foi", "versão", "custat"]
        usar_web = any(fld in pergunta_operador.lower() for fld in palavras_chave_web)
        
        if usar_web:
            contexto_fresco = buscar_na_web_alta_precisao(pergunta_operador)
            prompt_estendido = (
                f"Você é um terminal utilitário offline estéril. Não dê desculpas e não simule nada. "
                f"Responda à pergunta baseando-se ESTRITAMENTE nos dados brutos reais abaixo:\n"
                f"{contexto_fresco}\n\n"
                f"Pergunta do Operador: {pergunta_operador}"
            )
            print("[+] Processando contexto de alta precisão nos 12 núcleos do Xeon...")
            resposta = Settings.llm.complete(prompt_estendido)
        else:
            index = inicializar_ou_carregar_rag()
            query_engine = index.as_query_engine()
            resposta = query_engine.query(pergunta_operador)
        
    print("\n[🛡️ RESPOSTA SOBERANA]:")
    print(resposta)

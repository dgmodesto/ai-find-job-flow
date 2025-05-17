import datetime
import os
from typing import Optional
import uuid
import warnings
import textwrap
from datetime import date
from google import genai
import requests
from glassdoor_search import CompanyDataResponse, GlassdoorSearch, GlassdoorSearchQuery
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types

from linkedin_search import LinkedInSearch, LinkedInSearchQuery, LinkedInSearchResponse

warnings.filterwarnings("ignore")

# Configuração da API Gemini
GEMINI_API_KEY = os.environ["GOOGLE_API_KEY"]
GEMINI_MODEL = os.environ["MODEL_ID"]

client = genai.Client()

# Função auxiliar que envia uma mensagem para um agente e retorna a resposta final
def call_agent(agent: Agent, message_text: str, user_id: str = "user1", session_id: Optional[str]=None) -> str:
    """
    Executa um agente passando uma mensagem e retorna a resposta final como string.

    Args:
        agent (Agent): O agente configurado com modelo, instrução e nome.
        message_text (str): A mensagem a ser enviada ao agente.
        user_id (str): ID do usuário (opcional, padrão é "user1").
        session_id (str): ID da sessão (opcional, será gerado se não informado).

    Returns:
        str: A resposta final gerada pelo agente.
    """
    session_service = InMemorySessionService()
    session_id = session_id or str(uuid.uuid4())
    session_service.create_session(app_name=agent.name, user_id=user_id, session_id=session_id)

    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = []
    for event in runner.run(user_id=user_id, session_id=session_id, new_message=content):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    final_response.append(part.text.strip())

    return "\n".join(final_response).strip()

# Agente 1: Entrada do título da vaga
def input_agent():
    return input("Enter job title: ")

# Agente 2: Busca de vagas (mock LinkedIn)
def linkedin_agent(job_title):
    job_title = job_title.lower()
    linkedin_searh = LinkedInSearch()
    jobs = linkedin_searh.execute(LinkedInSearchQuery(job_title, 5))
    
    return jobs

# Agente 3: Busca informações da empresa (mock Glassdoor)
def glassdoor_agent(job_listings: list[LinkedInSearchResponse]):

    company_names = [company.company for company in job_listings]
    glassdoor_search = GlassdoorSearch()
    company_infos = glassdoor_search.execute(GlassdoorSearchQuery(company_names=company_names))
    
    return company_infos

def agente_busca_empresa_google(job_listings: list[LinkedInSearchResponse]):
    company_names = [company.company for company in job_listings]
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    resultados: list[CompanyDataResponse]= []
    for company_name in company_names:
      buscador_empresa = Agent(
          name="agente_busca_empresa_google",
          model="gemini-2.0-flash",
          instruction=f"""
          Você é um assistente de pesquisa especializado em encontrar informações atuais sobre empresas.
          Use a ferramenta de busca do Google (google_search) para encontrar as notícias mais relevantes, avaliações e comentários recentes sobre a empresa "{company_name}".
          Foque em resultados recentes, de no máximo um mês antes da data {current_date}.
          Retorne as informações mais importantes, como avaliação geral, pontos positivos e negativos destacados pelas fontes e qualquer notícia ou fato relevante.
          
          Resuma o resultado  até o máximo de 300 caracateres.
          """,
          description=f"Agente que busca informações atuais sobre a empresa {company_name} no Google.",
          tools=[google_search]
      )

      entrada_buscador = f"Empresa: {company_name}\nData de hoje: {current_date}"
      
      agent_result = call_agent(buscador_empresa, entrada_buscador)
      resultados.append(CompanyDataResponse(company_name, agent_result))
    return resultados

# Agente 4: Gera resumo e dicas de entrevista
def agente_gemini_resumo_dicas(job_listings: list[LinkedInSearchResponse], company_data: list[CompanyDataResponse]):
    agente = Agent(
        name="agente_gemini_resumo_dicas",
        model="gemini-2.0-flash",
        instruction="""
            Você é um especialista em carreiras e recursos humanos.
            Seu papel é gerar um resumo breve sobre a empresa e oferecer 3 dicas valiosas de entrevista para candidatos.
            Utilize os dados fornecidos da empresa como base (rating, pontos positivos e negativos) e os dados da vaga.
            Seja claro, útil e objetivo.
        """,
        description="Agente que gera resumos e dicas de entrevista com base na vaga e dados da empresa."
    )

    resultados = []

    for job in job_listings:
        # Encontra os dados da empresa correspondentes à vaga
        dados_empresa = next((c for c in company_data if c.company.lower() == job.company.lower()), None)
        if not dados_empresa:
            continue  # pula se não encontrou dados da empresa

        prompt = f"""
        Empresa: {job.company}
        Info: {dados_empresa.info}
        Vaga: {job.job_title}
        Gere um resumo breve da empresa e ofereça 3 dicas práticas para ir bem em uma entrevista com ela.
        """

        resposta = call_agent(agente, prompt)
        resultados.append(f"--- {job.company} ---\n{resposta}")

    return "\n\n".join(resultados)

# Execução principal
def run_flow():
  
    job_title = input_agent()
    job_listings = linkedin_agent(job_title)
    company_data = agente_busca_empresa_google(job_listings)
    recommendations = agente_gemini_resumo_dicas(job_listings, company_data)

    print("\n\n*** Career Advice Results ***\n")
    print(recommendations)
    
  
if __name__ == "__main__":
    run_flow()

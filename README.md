
# 🤖 Agentes de Oportunidade: Inteligência Artificial para Recolocação Profissional

Este projeto tem como missão **ajudar pessoas em busca de novas oportunidades de carreira** usando uma abordagem inteligente, automatizada e empática. Por meio de múltiplos agentes integrados, conseguimos realizar buscas de vagas, analisar empresas e gerar dicas personalizadas para entrevistas — tudo isso em poucos minutos.

---

## 🚀 Motivação

Em tempos de instabilidade econômica e incerteza profissional, muitas pessoas se veem perdidas na busca por um novo emprego. Falta de tempo, informações desencontradas e entrevistas mal direcionadas são apenas alguns dos obstáculos enfrentados diariamente.

Este projeto nasceu para **reduzir essa fricção** e **democratizar o acesso à informação de qualidade** sobre o mercado de trabalho. Usando **LLMs**, **web scraping com Selenium**, e **agentes coordenados via google.adk**, conseguimos gerar relatórios completos com:

- ✅ Vagas abertas no LinkedIn para uma determinada função
- ✅ Informações públicas atualizadas sobre as empresas
- ✅ Resumo da reputação corporativa baseado em avaliações
- ✅ Dicas personalizadas para se preparar melhor para a entrevista

---

## 🧠 Arquitetura da Solução

A arquitetura é baseada em múltiplos agentes especializados:

1. **Agente Buscador de Vagas (LinkedIn)**: coleta oportunidades com base no cargo desejado.
2. **Agente Analisador de Empresas**: busca notícias relevantes e recentes no Google.
3. **Agente de Reputação Corporativa**: analisa avaliações da empresa com base em sites públicos.
4. **Agente de Preparação para Entrevistas**: sintetiza as informações e gera dicas para a entrevista com base na cultura e desafios atuais da empresa.

Esses agentes interagem em um **grafo inteligente de decisões (LangGraph)**, proporcionando flexibilidade e adaptação a diferentes contextos.

---

## 🛠 Como Executar

### ✅ Pré-requisitos

- Python 3.10+
- Google Chrome + ChromeDriver compatível com sua versão do navegador
- Conta com acesso ao Google Gemini ou OpenAI (via LangChain)
- Variáveis de ambiente configuradas para suas chaves de API

### 🧱 Instalação

```bash
git clone https://github.com/dgmodesto/ai-find-job-flow.git
cd ai-find-job-flow
pip install -r requirements.txt
````

### ▶️ Execução

Para rodar o pipeline principal:

```bash
python app.py
```


### ⚙️ Configurações

Crie um arquivo `.env` com:

```env
OPENAI_API_KEY=xxx
GOOGLE_API_KEY=xxx
GOOGLE_CSE_ID=xxx
```

Certifique-se de ter o `chromedriver` na mesma pasta do script ou no seu `PATH`.

---

## 📄 Exemplo de Resultado

```markdown
## Resumo da Braskem:

A Braskem é uma empresa com histórico de altos e baixos recentes. Apesar de ter revertido prejuízos no último trimestre, enfrenta desafios como a pressão de agências de rating e recomendações de venda de alguns bancos. Por outro lado, a empresa demonstra ser um bom lugar para se trabalhar, sendo reconhecida pelos próprios funcionários.

## 3 Dicas para a Entrevista:

1. **Demonstre Conhecimento do Cenário Atual**  
   Esteja preparado para discutir os desafios e oportunidades da Braskem no contexto do mercado petroquímico.

2. **Destaque Sua Capacidade de Resolução de Problemas**  
   Mostre como suas habilidades podem contribuir para inovação e eficiência.

3. **Enfatize Seus Valores**  
   Demonstre que você valoriza um ambiente colaborativo e positivo.
```

---

## ❤️ Contribuindo

Quer contribuir? Sinta-se à vontade para abrir uma issue ou enviar um PR com melhorias. Feedbacks também são bem-vindos!

---

## 📜 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🙋‍♂️ Autor

Desenvolvido com 💙 por \[Seu Nome] – [LinkedIn](https://linkedin.com/in/seu-perfil) | [GitHub](https://github.com/seu-usuario)

---

## 🌟 Se este projeto te inspirou, dê uma estrela no repositório e compartilhe com alguém que esteja em busca de uma nova oportunidade!

```


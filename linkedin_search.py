from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class LinkedInSearchQuery:
  def __init__(self, job_title: str, delay: int = 5) -> None:
    self.job_title = job_title
    self.delay = delay


class LinkedInSearchResponse:
    def __init__(self, 
                 job_title: str,
                 company: str,
                 location: str,
                 link: str | None,
                 job_description: str = "") -> None:
        self.job_title = job_title
        self.company = company
        self.location = location
        self.link = link
        self.job_description = job_description

    def __repr__(self):
        return (f"{self.job_title} - {self.company} - {self.location} - {self.link}\n"
                f"Description: {self.job_description[:200]}...")  # mostra só os primeiros 200 chars

class LinkedInSearch:
  def __init__(self) -> None:
    # Opcional: Executa o Chrome em modo headless (sem abrir a janela)
    self.chrome_options = Options()
      
  def execute(self, search: LinkedInSearchQuery, delay: int = 5) -> list[LinkedInSearchResponse]:
    chrome_options = Options()
    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={search.job_title.replace(' ', '%20')}"
    driver.get(search_url)
    time.sleep(delay)

    job_elements = driver.find_elements(By.CLASS_NAME, "base-search-card")
    job_list: list[LinkedInSearchResponse] = []

    for job in job_elements:
        try:
            job_title = job.find_element(By.CLASS_NAME, "base-search-card__title").text.strip()
            company = job.find_element(By.CLASS_NAME, "base-search-card__subtitle").text.strip()
            location = job.find_element(By.CLASS_NAME, "job-search-card__location").text.strip()
            link = job.find_element(By.TAG_NAME, "a").get_attribute("href")

            # Pega a descrição da vaga abrindo o link
            job_description = self.get_job_description(driver=driver, job_link=link, delay=search.delay)

            job_obj = LinkedInSearchResponse(
                job_title=job_title,
                company=company,
                location=location,
                link=link,
                job_description=job_description
            )
            job_list.append(job_obj)

        except Exception as e:
            print("Erro ao extrair vaga:", e)

    driver.quit()
    return job_list
  
  def get_job_description(self, driver, job_link: str | None, delay: int = 3) -> str:
      driver.get(job_link)
      time.sleep(delay)

      try:
          # O container da descrição geralmente tem essa classe, mas pode variar conforme o layout do LinkedIn:
          desc_elem = driver.find_element(By.CLASS_NAME, "show-more-less-html__markup")
          return desc_elem.text.strip()
      except Exception as e:
          print(f"Erro ao capturar descrição: {e}")
          return ""
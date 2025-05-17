from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import urllib.parse

class GlassdoorSearchQuery:
    def __init__(self, company_names: list[str]) -> None:
        self.company_names = company_names

class CompanyDataResponse:
    def __init__(self, company: str, info: str = "") -> None:
        self.company = company
        self.info = info

    def __repr__(self):
        return f"{self.company}\n{self.info}"

class GlassdoorSearch:
    def __init__(self) -> None:
        self.chrome_options = Options()

    def execute(self, search: GlassdoorSearchQuery, delay: int = 5) -> list[CompanyDataResponse]:
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # opcional: ativa modo invisível
        driver = webdriver.Chrome(options=chrome_options)
        job_list = []

        for company_name in search.company_names:
            company_encoded = urllib.parse.quote(company_name.replace(" ", "-"))
            url = f"https://www.glassdoor.com/Overview/Working-at-{company_encoded}-EI_IE.htm"
            driver.get(url)
            time.sleep(delay)

            try:
                rating = driver.find_element(By.CLASS_NAME, "v2__EIReviewsRatingsStylesV2__ratingNum").text
                pros = driver.find_element(By.CSS_SELECTOR, "div[data-test='pros']").text
                cons = driver.find_element(By.CSS_SELECTOR, "div[data-test='cons']").text

                info_text = f"Rating: {rating}\nPros: {pros}\nCons: {cons}"

                job_obj = CompanyDataResponse(
                    company=company_name,
                    info=info_text
                )
                job_list.append(job_obj)

            except Exception as e:
                print(f"Erro ao extrair informações no Glassdoor para {company_name}: {e}")
                job_list.append(CompanyDataResponse(company=company_name, info="Informações não encontradas."))

        driver.quit()
        return job_list

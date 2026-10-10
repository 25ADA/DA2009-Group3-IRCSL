# DA2009 - Group Project - IRCSL Ethical Web Scraping
# DA 2009 - Data Collection Methods II | Group 3
#
# Members:
#   Chandrasekaran Sivaneswaran - 25ada147
#   Zainul Abdeen Athif - 25ada023
#   V. K. Rajapakse - 25ada139
#   P. P. M. Subasinsani - 25ada029
#
# Phase 2 - Insurance Companies spider (Scrapy)
# Done by: P. P. M. Subasinsani (25ada029)
# Run with: scrapy runspider ircsl_insurance_spider.py

import json
import time

import scrapy
from scrapy.exceptions import DropItem
from bs4 import BeautifulSoup

USER_AGENT = "DA2009-StudentProject/1.0 (BSc Applied Data Analytics coursework; academic use only)"
DIRECTORY_URL = "https://ircsl.gov.lk/insurance-companies/"


class InsuranceCompanyItem(scrapy.Item):
    company_name = scrapy.Field()
    footnote_marker = scrapy.Field()
    class_of_insurance = scrapy.Field()
    licence_effective_date = scrapy.Field()
    registration_number = scrapy.Field()
    head_office_address = scrapy.Field()
    telephone = scrapy.Field()
    fax = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    principal_officer = scrapy.Field()
    specified_officer = scrapy.Field()
    contact_person = scrapy.Field()
    source_url = scrapy.Field()
    scraped_at = scrapy.Field()


class QuarterlyReturnItem(scrapy.Item):
    company_name = scrapy.Field()
    within_deadline = scrapy.Field()
    after_deadline = scrapy.Field()
    source_url = scrapy.Field()
    scraped_at = scrapy.Field()


class CleanTextPipeline:
    def process_item(self, item, spider=None):
        for field, value in item.items():
            if isinstance(value, str):
                if "&" in value or "<" in value:
                    value = BeautifulSoup(value, "html.parser").get_text(" ")
                value = " ".join(value.split())
                if value in ["", "-"]:
                    value = None
                item[field] = value
        return item


class ValidateAndDedupePipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider=None):
        if not item.get("company_name"):
            raise DropItem("Missing company name")
        key = (type(item).__name__, item["company_name"], item.get("class_of_insurance"))
        if key in self.seen:
            raise DropItem("Duplicate item")
        self.seen.add(key)
        return item


class InsuranceCompaniesSpider(scrapy.Spider):
    name = "insurance_companies"
    allowed_domains = ["ircsl.gov.lk"]
    start_urls = [DIRECTORY_URL]

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "USER_AGENT": USER_AGENT,
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "ITEM_PIPELINES": {CleanTextPipeline: 100, ValidateAndDedupePipeline: 200},
        "FEEDS": {
            "data/processed/insurance_companies.json": {
                "format": "json", "encoding": "utf8", "indent": 2,
                "overwrite": True, "item_classes": [InsuranceCompanyItem],
            },
            "data/processed/quarterly_returns.json": {
                "format": "json", "encoding": "utf8", "indent": 2,
                "overwrite": True, "item_classes": [QuarterlyReturnItem],
            },
        },
        "LOG_LEVEL": "INFO",
    }

    def parse(self, response):
        scraped_at = time.strftime("%Y-%m-%d %H:%M:%S")

        for row in response.css("#company-table tbody tr"):
            name = row.css("td:nth-child(2)").xpath("string(.)").get().strip()

            # hidden details inside the <script> tag of the row
            hidden = [""] * 13
            script = row.css("script::text").get() or ""
            if "new Array(" in script:
                list_text = script.split("new Array(")[1].split(");")[0]
                hidden = json.loads("[" + list_text.replace("img_to_get", '""') + "]")

            # footnote markers such as ***** or + at the end of a name
            clean_name = name.rstrip("*+ ")
            marker = name[len(clean_name):].strip()

            yield InsuranceCompanyItem(
                company_name=clean_name,
                footnote_marker=marker if marker else None,
                class_of_insurance=row.css("td:nth-child(3)").xpath("string(.)").get(),
                licence_effective_date=row.css("td:nth-child(4)").xpath("string(.)").get(),
                registration_number=None,
                head_office_address=hidden[4],
                telephone=hidden[5],
                fax=hidden[6],
                email=hidden[7],
                website=hidden[8],
                principal_officer=hidden[9],
                specified_officer=hidden[10],
                contact_person=hidden[11],
                source_url=response.url,
                scraped_at=scraped_at,
            )

        # follow the link to the Quarterly Returns page
        href = response.xpath(
            '//a[contains(@href, "/insurance-companies/submission-of-quarterly-returns")]/@href'
        ).get()
        if href:
            next_url = response.urljoin(href)
            self.logger.info("Following link: " + next_url)
            yield scrapy.Request(next_url, callback=self.parse_quarterly_returns)

    def parse_quarterly_returns(self, response):
        scraped_at = time.strftime("%Y-%m-%d %H:%M:%S")

        for table in response.css("table"):
            header = table.css("tr")[0].xpath("string(.)").get()
            if "Name of Insurance Company" not in header:
                continue
            for row in table.css("tr")[1:]:
                cells = [c.xpath("string(.)").get().strip() for c in row.css("td")]
                if len(cells) < 4:
                    continue
                yield QuarterlyReturnItem(
                    company_name=cells[1],
                    within_deadline=cells[2],
                    after_deadline=cells[3],
                    source_url=response.url,
                    scraped_at=scraped_at,
                )

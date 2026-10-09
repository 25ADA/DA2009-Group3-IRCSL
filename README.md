# DA2009 - Group Project - IRCSL Ethical Web Scraping

**DA 2009 - Data Collection Methods II | Group 3**

In this project we collect public data from the website of the Insurance Regulatory Commission of Sri Lanka (https://ircsl.gov.lk) using the tools we learned in the lectures. The work is split into four phases, one for each member.

## Group members and phases

| Phase | Notebook | Member | Student ID | Main tools |
|---|---|---|---|---|
| 1 - Ethical setup, site map and static pages | [Phase1_Static_Pages_Vathsala.ipynb](Phase1_Static_Pages_Vathsala.ipynb) | V. K. Rajapakse | 25ada139 | Requests, robots.txt, BeautifulSoup, pd.read_html |
| 2 - Insurance companies | [Phase2_Insurance_Companies_Poojani.ipynb](Phase2_Insurance_Companies_Poojani.ipynb) | P. P. M. Subasinsani | 25ada029 | Scrapy (selectors, Items, pipelines, export) |
| 3 - Brokers and loss adjusters | [Phase3_Intermediaries_Siva.ipynb](Phase3_Intermediaries_Siva.ipynb) | Chandrasekaran Sivaneswaran | 25ada147 | Requests, BeautifulSoup, Selenium, REST API check |
| 4 - PDF documents | [Phase4_Document_Engine_Athif.ipynb](Phase4_Document_Engine_Athif.ipynb) | Zainul Abdeen Athif | 25ada023 | Requests (streaming), PyPDF2, pdfplumber, PyTesseract |

A PDF copy of each notebook (with all outputs) is in the same folder.

## Open in Google Colab

- [Phase 1 in Colab](https://colab.research.google.com/github/DA2009/DA2009-Group3-IRCSL/blob/main/Phase1_Static_Pages_Vathsala.ipynb)
- [Phase 2 in Colab](https://colab.research.google.com/github/DA2009/DA2009-Group3-IRCSL/blob/main/Phase2_Insurance_Companies_Poojani.ipynb)
- [Phase 3 in Colab](https://colab.research.google.com/github/DA2009/DA2009-Group3-IRCSL/blob/main/Phase3_Intermediaries_Siva.ipynb)
- [Phase 4 in Colab](https://colab.research.google.com/github/DA2009/DA2009-Group3-IRCSL/blob/main/Phase4_Document_Engine_Athif.ipynb)

The notebooks are saved with their outputs, so they can be read without running them. Please do not run all of them again many times, because every run sends requests to the IRCSL website.

## Main finding

The brokers and loss adjusters pages look dynamic (paging, search, sorting and ＋ buttons), but the data is static. All the rows and contact details are already in the first HTML response, and JavaScript only changes how they are shown. So Requests and BeautifulSoup were enough, and Selenium was only used to test this.

## What we collected

| Data | Rows | File |
|---|---|---|
| English pages in the sitemap | 90 | data/processed/site_map_pages.csv |
| IRCSL members and staff (About Us) | 27 | data/processed/about_us_team.csv / .json |
| Contact Us directory | 20 | data/processed/contact_us_directory.csv |
| Insurance companies | 29 | data/processed/insurance_companies_clean.csv / .json |
| Insurance brokers | 84 | data/processed/insurance_brokers.csv / .json |
| Loss adjusters | 29 | data/processed/loss_adjusters.csv / .json |
| Documents listed on the website | 111 | data/processed/document_catalogue.csv |
| PDFs downloaded and analysed (sample) | 10 | data/processed/document_summary.csv / .json |
| Tables found inside the PDFs | 27 | data/processed/pdf_tables.xlsx |

Other files:
- `data/raw/` - the raw HTML and sitemap files we saved, so we could parse them again without asking the server again
- `data/text/` - the full text of each downloaded PDF (pdfplumber, or OCR for the scanned circulars)
- `ircsl_insurance_spider.py` - the Scrapy spider written by the Phase 2 notebook

The downloaded PDF files are not uploaded to this repository. They are public IRCSL documents and can be downloaded again from the website with the Phase 4 notebook.

## Ethical rules we followed

- We checked robots.txt before every request (`urllib.robotparser`, and `ROBOTSTXT_OBEY = True` in Scrapy).
- We used a User-Agent that says this is a student project, and waited 3 seconds between requests.
- We only used public pages. We did not log in or bypass anything.
- We only took what we needed, for example 10 of the 111 PDFs.
- Every row keeps `source_url` and `scraped_at`, so the source is always credited.
- The data is only used for this assignment. This is why the repository is private and only shared with the group members and our lecturer.

## Libraries used

requests, beautifulsoup4, lxml, pandas, scrapy, selenium (with Google Chrome), PyPDF2, pdfplumber, pytesseract (with the Tesseract OCR program), openpyxl.

We assume these are already installed on the machine that runs the notebooks.

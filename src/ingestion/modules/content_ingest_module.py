import os
from src.ingestion.modules.content_ingest_http import ingest_http
from src.ingestion.modules.content_ingest_pdf import ingest_pdf


def ingest_text_dataset(config: dict) -> None:
    ingested_content = config["ingested_content"]
    output_dir = config["output_dir"]

    if "http" in ingested_content:
        http_config = ingested_content["http"]
        
        if isinstance(http_config, list):
            http_entries = http_config
        else:
            http_entries = [http_config]
        
        for entry in http_entries:
            base_url = entry["base_url"]
            print(f"Ingesting HTTP: {base_url}")
            ingest_http(base_url = base_url, output_dir = output_dir)

    if "pdf" in ingested_content:
        pdf_config = ingested_content["pdf"]
        base_folder = pdf_config["base_folder"]
        
        for filename in os.listdir(base_folder):
            print(filename)
            if filename.lower().endswith(".pdf"):
                pdf_path = os.path.join(base_folder, filename)
                print(f"Ingesting PDF: {pdf_path}")
                ingest_pdf(pdf_path = pdf_path, output_dir = output_dir)
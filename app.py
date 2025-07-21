
import streamlit as st
import pdfplumber
import pandas as pd
import io
import re

st.set_page_config(page_title="Leitor de Contas de Luz - Flora Energia", layout="wide")
st.title("⚡ Leitor de Contas de Luz - Flora Energia")

uploaded_file = st.file_uploader("Envie a conta de luz em PDF", type="pdf")

def extract_text_from_pdf(file_bytes):
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def identificar_distribuidora(texto):
    if "CPFL PAULISTA" in texto.upper():
        return "CPFL Paulista"
    elif "CPFL PIRATININGA" in texto.upper():
        return "CPFL Piratininga"
    elif "LIGHT" in texto.upper():
        return "Light"
    elif "CEMIG" in texto.upper():
        return "CEMIG"
    elif "ENERGISA" in texto.upper():
        return "Energisa Sul Sudeste"
    elif "ELEKTRO" in texto.upper():
        return "Elektro"
    elif "ENEL" in texto.upper():
        return "ENEL RJ"
    else:
        return "Distribuidora não reconhecida"

def extrair_dados_simples(texto, distribuidora):
    dados = {
        "Distribuidora": distribuidora,
        "Nome": re.search(r"(?i)nome[:\s]*([A-Z\s]+)", texto),
        "CPF/CNPJ": re.search(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto),
        "Instalacao": re.search(r"Instala.{0,10}?(\d{5,})", texto),
        "Mês": re.search(r"\b(0[1-9]|1[0-2])/20\d{2}\b", texto),
        "Ano": re.search(r"\b20\d{2}\b", texto),
        "Consumo (kWh)": re.search(r"(\d{2,5})\s?kWh", texto),
        "Valor Total (R\$)": re.search(r"R\$\s?\d{1,3}(\.\d{3})*,\d{2}", texto),
    }
    return {chave: m.group(1) if m else "" for chave, m in dados.items()}

if uploaded_file:
    texto = extract_text_from_pdf(uploaded_file.read())
    dist = identificar_distribuidora(texto)
    dados_extraidos = extrair_dados_simples(texto, dist)
    df = pd.DataFrame([dados_extraidos])
    st.subheader("📋 Dados extraídos")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", data=csv, file_name="dados_extraidos.csv", mime="text/csv")

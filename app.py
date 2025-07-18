
import streamlit as st
import pdfplumber
import pandas as pd
import io

st.set_page_config(page_title="Leitor de Contas de Luz - MVP", layout="centered")
st.title("🔌 Leitor de Contas de Luz - MVP")
st.markdown("Faça o upload de uma conta de luz em PDF e visualize os dados extraídos.")

uploaded_file = st.file_uploader("📄 Envie a conta de luz (PDF)", type="pdf")

def extrair_dados(pdf_bytes):
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() + "\n"

    # Extrações simuladas
    dados = {
        "Distribuidora": "Detectar com regex",
        "Nome do Cliente": "Detectar com regex",
        "CPF/CNPJ": "Detectar com regex",
        "Instalação/UC": "Detectar com regex",
        "Referência (Mês/Ano)": "Detectar com regex",
        "Data de Emissão": "Detectar com regex",
        "Data de Vencimento": "Detectar com regex",
        "Consumo (kWh)": "Detectar com regex",
        "Valor Total (R$)": "Detectar com regex"
    }
    return dados

if uploaded_file:
    st.success("Arquivo recebido!")
    dados = extrair_dados(uploaded_file.read())
    df = pd.DataFrame([dados])
    st.subheader("📊 Dados extraídos")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Baixar CSV", data=csv, file_name="conta_extraida.csv", mime="text/csv")

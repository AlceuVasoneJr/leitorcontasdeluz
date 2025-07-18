
import streamlit as st

st.title("Leitor de Contas de Luz - MVP")
st.write("Upload de contas em PDF, extração e exportação.")

uploaded_file = st.file_uploader("Envie o PDF da conta de luz", type="pdf")
if uploaded_file:
    st.success("Arquivo recebido! (Extração será implementada aqui)")

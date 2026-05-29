import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Dashboard de RH",
    page_icon="👥",
    layout="wide",
    
)


# Configuração da Barra Lateral
st.sidebar.title("Sobre o Desenvolvedor")
st.sidebar.markdown("""
### **Gustavo Ricarte**
Desenvolvedor Full-Stack focado em Dados.

---
**Contatos:**
- [LinkedIn](https://www.linkedin.com/in/guricarte)
- [GitHub](https://github.com/guricartee)
- [E-mail](mailto:gustavoricarte12271227@gmail.com)

**Tecnologias Usadas:**
- Python (Streamlit)
- Node.js / FastAPI (Backend)
- Replit (Infraestrutura)
""")

st.title("📊 Dashboard de Insights de RH")

st.markdown("""
Este projeto foi desenvolvido para demonstrar a integração de um **Frontend em Streamlit** com uma **API Backend** customizada. Ele apresenta KPIs reais de gestão de pessoas, como rotatividade, faixas salariais e distribuição por departamento.
""")


# ── Dados ──────────────────────────────────────────────────────────────────────

def criar_dataframe():
    data = {
        'Nome': ['Gustavo', 'Reginaldo', 'Murilo', 'Ofélia'],
        'Idade': [24, 49, 29, 36],
        'Salario': [2300, 7800, 6500, 1150],
    }
    return pd.DataFrame(data)

df = criar_dataframe()

# ── Cabeçalho ──────────────────────────────────────────────────────────────────

st.title("Dashboard de RH")
st.caption("Visão geral dos funcionários · dados demonstrativos")

st.divider()

# ── KPIs ───────────────────────────────────────────────────────────────────────

media_idade = df['Idade'].mean()
media_salario = df['Salario'].mean()
soma_salario = df['Salario'].sum()
total_funcionarios = len(df)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de Funcionários", total_funcionarios)
c2.metric("Média de Idade", f"{media_idade:.1f} anos")
c3.metric("Média Salarial", f"R$ {media_salario:,.2f}")
c4.metric("Folha Total", f"R$ {soma_salario:,.2f}")

st.divider()

# ── Tabela de funcionários ──────────────────────────────────────────────────────

st.subheader("Funcionários por Salário")

df_exibir = df.sort_values(by='Salario', ascending=False).reset_index(drop=True)
df_exibir.index += 1
df_exibir['Salario'] = df_exibir['Salario'].map(lambda x: f"R$ {x:,.2f}")
df_exibir['Idade'] = df_exibir['Idade'].map(lambda x: f"{x} anos")
df_exibir.columns = ['Nome', 'Idade', 'Salário']
st.dataframe(df_exibir, use_container_width=True)

st.divider()

# ── Gráficos ───────────────────────────────────────────────────────────────────

col_esq, col_dir = st.columns(2)

# Gráfico de salários
with col_esq:
    st.subheader("Salário dos Funcionários")
    df_sal = df.sort_values(by='Salario', ascending=False)
    cores = ['#4C72B0', '#DD8452', '#55A868', '#C44E52']

    fig1, ax1 = plt.subplots(figsize=(6, 4))
    barras = ax1.bar(df_sal['Nome'], df_sal['Salario'], color=cores)

    linha_media = df['Salario'].mean()
    ax1.axhline(linha_media, color='gray', linestyle='--', linewidth=1.2, label=f'Média: R$ {linha_media:,.0f}')

    for barra in barras:
        altura = barra.get_height()
        ax1.text(
            barra.get_x() + barra.get_width() / 2,
            altura + 80,
            f'R$ {altura:,.0f}',
            ha='center', va='bottom', fontsize=9, fontweight='bold'
        )

    ax1.set_xlabel('Funcionários')
    ax1.set_ylabel('Salário (R$)')
    ax1.set_ylim(0, df['Salario'].max() * 1.2)
    ax1.legend(fontsize=8)
    ax1.spines[['top', 'right']].set_visible(False)
    ax1.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig1)
    plt.close(fig1)

# Gráfico de idades
with col_dir:
    st.subheader("Idade dos Funcionários")
    df_idade = df.sort_values(by='Idade', ascending=False)
    cores_idade = ['#8172B3', '#55A868', '#4C72B0', '#DD8452']

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    barras2 = ax2.barh(df_idade['Nome'], df_idade['Idade'], color=cores_idade)

    media_idade_val = df['Idade'].mean()
    ax2.axvline(media_idade_val, color='gray', linestyle='--', linewidth=1.2, label=f'Média: {media_idade_val:.1f} anos')

    for barra in barras2:
        largura = barra.get_width()
        ax2.text(
            largura + 0.3,
            barra.get_y() + barra.get_height() / 2,
            f'{largura:.0f} anos',
            va='center', fontsize=9, fontweight='bold'
        )

    ax2.set_xlabel('Idade (anos)')
    ax2.set_xlim(0, df['Idade'].max() * 1.25)
    ax2.legend(fontsize=8)
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.grid(axis='x', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig2)
    plt.close(fig2)

st.divider()

# ── Distribuição salarial (pizza) ──────────────────────────────────────────────

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Participação na Folha Salarial")
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    wedges, texts, autotexts = ax3.pie(
        df['Salario'],
        labels=df['Nome'],
        autopct='%1.1f%%',
        colors=cores,
        startangle=140,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    for at in autotexts:
        at.set_fontsize(9)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close(fig3)

with col_b:
    st.subheader("Salário vs Média")
    diff = df['Salario'] - df['Salario'].mean()
    cores_diff = ['#55A868' if v >= 0 else '#C44E52' for v in diff]

    fig4, ax4 = plt.subplots(figsize=(5, 4))
    barras4 = ax4.bar(df['Nome'], diff, color=cores_diff)
    ax4.axhline(0, color='black', linewidth=0.8)

    for barra, val in zip(barras4, diff):
        ax4.text(
            barra.get_x() + barra.get_width() / 2,
            val + (80 if val >= 0 else -200),
            f'R$ {val:+,.0f}',
            ha='center', fontsize=8, fontweight='bold',
            color='#2d6a35' if val >= 0 else '#8b1a1a'
        )

    ax4.set_ylabel('Diferença da média (R$)')
    ax4.set_xlabel('Funcionários')
    ax4.spines[['top', 'right']].set_visible(False)
    ax4.grid(axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close(fig4)

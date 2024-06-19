import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Hustle & Study Hub", page_icon="📚🧠")

# Função para registrar o estudante
def register_student(
    name, email, student_id, sex, state, college, course, job_title, company, image
):
    st.session_state["student"] = {
        "name": name,
        "email": email,
        "student_id": student_id,
        "sex": sex,
        "state": state,
        "college": college,
        "course": course,
        "job_title": job_title,
        "company": company,
        "image": image,
    }
    st.session_state["registered"] = True

# Lista de cursos, universidades e estados
courses = [
    "Administração", "Agronomia", "Arquitetura e Urbanismo", "Ciências Biológicas",
    "Direito", "Engenharia Civil", "Engenharia da Computação", "Engenharia de Pesca",
    "Engenharia de Produção", "Engenharia Mecânica", "Geografia", "História",
    "Letras - Espanhol", "Letras - Inglês", "Medicina", "Medicina Veterinária",
    "Pedagogia", "Química"
]

universities = ["Universidade Estadual do Maranhão"]

states = ["São Bento", "São José do Patos", "São Luis"]

# Página de apresentação
st.header("Bem-vindo ao Hustle & Study Hub!")
st.write("""
Este é um aplicativo projetado para ajudar estudantes que trabalham a gerenciar suas tarefas acadêmicas e profissionais de maneira eficiente.
Aqui você pode registrar suas informações acadêmicas e profissionais, organizar suas tarefas, e visualizar um resumo e análise dos seus progressos.

Vamos começar registrando suas informações abaixo:
""")

# Página de cadastro do estudante
if not st.session_state.get("registered", False):
    name = st.text_input("Nome")
    email = st.text_input("Email")
    student_id = st.text_input("ID do Estudante")
    sex = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    state = st.selectbox("Estado", states)
    college = st.selectbox("Universidade", universities)
    course = st.selectbox("Curso", courses)
    job_title = st.text_input("Título do Trabalho")
    company = st.text_input("Empresa")
    image = st.file_uploader("Upload da Imagem", type=["jpg", "jpeg", "png"])

    if st.button("Registrar"):
        if name and email and student_id and sex and state and college and course and job_title and company and image:
            register_student(name, email, student_id, sex, state, college, course, job_title, company, image)
            st.success("Cadastro realizado com sucesso!")
else:
    # Definindo as abas do aplicativo
    tab1, tab2, tab3, tab4 = st.tabs(
        ["Produtividade", "Sobre Usuários", "Resumo das Tarefas", "Análise de Dados"]
    )

    with tab1:
        # Criação de um DataFrame para armazenar as tarefas
        if "tasks" not in st.session_state:
            st.session_state["tasks"] = pd.DataFrame(
                columns=["Tarefa", "Categoria", "Prazo", "Concluída"]
            )

        # Função para adicionar uma nova tarefa
        def add_task(task, category, deadline):
            new_task = pd.DataFrame(
                {
                    "Tarefa": [task],
                    "Categoria": [category],
                    "Prazo": [deadline],
                    "Concluída": [False],
                }
            )
            st.session_state["tasks"] = pd.concat(
                [st.session_state["tasks"], new_task], ignore_index=True
            )

        # Função para marcar uma tarefa como concluída
        def complete_task(task_index):
            st.session_state["tasks"].loc[task_index, "Concluída"] = True

        # Seção para adicionar novas tarefas
        st.header("Lista de Tarefas")
        task = st.text_input("Tarefa")
        category = st.selectbox("Categoria", ["Estudo", "Trabalho"])
        deadline = st.date_input("Prazo")

        if st.button("Adicionar Tarefa"):
            add_task(task, category, deadline)
            st.success("Tarefa adicionada com sucesso!")

        # Exibição das tarefas pendentes
        st.header("Tarefas Pendentes")
        pending_tasks = st.session_state["tasks"][
            st.session_state["tasks"]["Concluída"] == False
        ]

        for i, task in pending_tasks.iterrows():
            st.write(f"{task['Tarefa']} ({task['Categoria']}) - Prazo: {task['Prazo']}")
            if st.button("Marcar como Concluída", key=f"complete_{i}"):
                complete_task(i)
                st.experimental_rerun()

        # Exibição das tarefas concluídas
        st.header("Tarefas Concluídas")
        completed_tasks = st.session_state["tasks"][
            st.session_state["tasks"]["Concluída"] == True
        ]

        for i, task in completed_tasks.iterrows():
            st.write(f"{task['Tarefa']} ({task['Categoria']}) - Concluída")

    with tab2:
        st.header("Sobre Usuários")
        student_info = st.session_state.get("student", {})
        if student_info:
            st.write(f"**Nome:** {student_info['name']}")
            st.write(f"**Email:** {student_info['email']}")
            st.write(f"**ID do Estudante:** {student_info['student_id']}")
            st.write(f"**Sexo:** {student_info['sex']}")
            st.write(f"**Estado:** {student_info['state']}")
            st.write(f"**Faculdade:** {student_info['college']}")
            st.write(f"**Curso:** {student_info['course']}")
            st.write(f"**Título do Trabalho:** {student_info['job_title']}")
            st.write(f"**Empresa:** {student_info['company']}")
            st.image(
                student_info["image"],
                caption="Foto do Estudante",
                use_column_width=True,
            )
        else:
            st.write("Nenhum usuário registrado.")

    with tab3:
        # Resumo das tarefas
        st.header("Resumo das Tarefas")
        total_tasks = len(st.session_state["tasks"])
        completed_tasks_count = len(
            st.session_state["tasks"][st.session_state["tasks"]["Concluída"] == True]
        )
        pending_tasks_count = len(
            st.session_state["tasks"][st.session_state["tasks"]["Concluída"] == False]
        )

        st.write(f"Total de Tarefas: {total_tasks}")
        st.write(f"Tarefas Concluídas: {completed_tasks_count}")
        st.write(f"Tarefas Pendentes: {pending_tasks_count}")

    with tab4:
        # Análise de dados
        st.header("Análise de Dados")

        if len(st.session_state["tasks"]) > 0:
            # Criar gráfico de barras com Plotly
            tasks_summary = (
                st.session_state["tasks"]
                .groupby(["Categoria", "Concluída"])
                .size()
                .unstack()
                .fillna(0)
            )
            if True not in tasks_summary.columns:
                tasks_summary[True] = 0
            if False not in tasks_summary.columns:
                tasks_summary[False] = 0
            tasks_summary.columns = ["Pendentes", "Concluídas"]

            fig = px.bar(
                tasks_summary,
                x=tasks_summary.index,
                y=["Pendentes", "Concluídas"],
                title="Tarefas Pendentes e Concluídas por Categoria",
                labels={"value": "Número de Tarefas", "Categoria": "Categoria"},
                barmode="group",
            )

            st.plotly_chart(fig)

            # Botão para baixar as informações das tarefas
            if st.button("Baixar Informações das Tarefas"):
                tasks_csv = st.session_state["tasks"].to_csv(index=False)
                st.download_button(
                    label="Baixar CSV",
                    data=tasks_csv,
                    file_name="tarefas.csv",
                    mime="text/csv",
                )
        else:
            st.write("Nenhuma tarefa registrada para análise.")

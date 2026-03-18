"""
BI Data Generator PRO
Gerador de bases de dados no modelo estrela (Star Schema) para projetos de BI.
Compatível com Power BI, Tableau e qualquer ferramenta de análise de dados.
"""

import streamlit as st
import pandas as pd
import numpy as np
import random
import zipfile
import io
from datetime import date, timedelta
from faker import Faker

# ── configuração da página ──────────────────────────────────────────────────
st.set_page_config(
    page_title="BI Data Generator PRO",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

fake = Faker("pt_BR")
rng  = np.random.default_rng()

# ── helpers ─────────────────────────────────────────────────────────────────
def new_ids(n: int, prefix: str = "") -> list[int]:
    return list(range(1, n + 1))

def dcalendario(start: date, end: date) -> pd.DataFrame:
    """Gera dCalendario compatível com o padrão Power Query."""
    days = pd.date_range(start=start, end=end, freq="D")
    df = pd.DataFrame({"Data": days})
    df["Ano"]      = df["Data"].dt.year
    df["Mes"]      = df["Data"].dt.month
    meses_pt = {1:"Jan",2:"Fev",3:"Mar",4:"Abr",5:"Mai",6:"Jun",
                7:"Jul",8:"Ago",9:"Set",10:"Out",11:"Nov",12:"Dez"}
    df["MesAno"]   = df["Mes"].map(meses_pt) + "/" + df["Ano"].astype(str).str[-2:]
    df["IdMesAno"] = df["Ano"] * 100 + df["Mes"]
    df["Data"]     = df["Data"].dt.date
    return df

def rand_dates(start: date, end: date, n: int) -> list[date]:
    delta = (end - start).days
    return [start + timedelta(days=int(d)) for d in rng.integers(0, delta + 1, n)]

def to_zip(tables: dict[str, pd.DataFrame]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, df in tables.items():
            csv_buf = io.StringIO()
            df.to_csv(csv_buf, index=False)
            zf.writestr(f"{name}.csv", csv_buf.getvalue())
    return buf.getvalue()

# ═══════════════════════════════════════════════════════════════════════════
#  GERADORES POR SETOR
# ═══════════════════════════════════════════════════════════════════════════

# ── VAREJO ──────────────────────────────────────────────────────────────────
def gerar_varejo(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_clientes  = min(n, 5000)
    n_produtos  = min(500, n // 5 + 50)
    n_vendedores = 50
    n_filiais   = 10

    estados = ["SP","RJ","MG","RS","PR","SC","BA","CE","PE","GO"]
    regioes = {"SP":"Sudeste","RJ":"Sudeste","MG":"Sudeste","RS":"Sul","PR":"Sul",
               "SC":"Sul","BA":"Nordeste","CE":"Nordeste","PE":"Nordeste","GO":"Centro-Oeste"}

    dim_geo = pd.DataFrame({
        "id_geo":  new_ids(len(estados)),
        "estado":  estados,
        "regiao":  [regioes[e] for e in estados],
    })

    dim_cliente = pd.DataFrame({
        "id_cliente": new_ids(n_clientes),
        "nome":       [fake.name() for _ in range(n_clientes)],
        "cpf":        [fake.cpf()  for _ in range(n_clientes)],
        "email":      [fake.email() for _ in range(n_clientes)],
        "segmento":   random.choices(["Pessoa Física","Pessoa Jurídica","Premium"], k=n_clientes),
        "cidade":     [fake.city() for _ in range(n_clientes)],
        "uf":         random.choices(estados, k=n_clientes),
    })

    categorias = ["Eletrônicos","Vestuário","Alimentos","Móveis","Esporte","Beleza","Brinquedos"]
    dim_produto = pd.DataFrame({
        "id_produto": new_ids(n_produtos),
        "nome":       [f"Produto {fake.word().capitalize()} {i}" for i in range(1, n_produtos+1)],
        "sku":        [f"SKU-{rng.integers(10000,99999)}" for _ in range(n_produtos)],
        "categoria":  random.choices(categorias, k=n_produtos),
        "preco_unit": rng.uniform(10, 2000, n_produtos).round(2),
        "custo_unit": rng.uniform(5,  1000, n_produtos).round(2),
    })

    dim_vendedor = pd.DataFrame({
        "id_vendedor": new_ids(n_vendedores),
        "nome":        [fake.name() for _ in range(n_vendedores)],
        "cpf":         [fake.cpf()  for _ in range(n_vendedores)],
        "regiao":      random.choices(list(regioes.values()), k=n_vendedores),
        "meta_mensal": rng.integers(10000, 80000, n_vendedores),
    })

    dim_filial = pd.DataFrame({
        "id_filial": new_ids(n_filiais),
        "nome":      [f"Filial {fake.city()}" for _ in range(n_filiais)],
        "uf":        random.choices(estados, k=n_filiais),
        "id_geo":    random.choices(dim_geo["id_geo"].tolist(), k=n_filiais),
        "tipo":      random.choices(["Loja Física","E-commerce","Outlet"], k=n_filiais),
    })

    datas    = rand_dates(start, end, n)
    qtds     = rng.integers(1, 20, n)
    produtos = random.choices(dim_produto["id_produto"].tolist(), k=n)
    precos   = [dim_produto.loc[dim_produto["id_produto"]==p, "preco_unit"].values[0] for p in produtos]

    fato = pd.DataFrame({
        "id_venda":   new_ids(n),
        "id_data":    datas,
        "id_cliente": random.choices(dim_cliente["id_cliente"].tolist(), k=n),
        "id_produto": produtos,
        "id_vendedor":random.choices(dim_vendedor["id_vendedor"].tolist(), k=n),
        "id_filial":  random.choices(dim_filial["id_filial"].tolist(), k=n),
        "quantidade": qtds,
        "valor_unit": [round(p, 2) for p in precos],
        "desconto":   rng.uniform(0, 0.3, n).round(3),
        "valor_total":[round(q * p * (1 - d), 2) for q, p, d in zip(qtds, precos, rng.uniform(0, 0.3, n))],
        "canal":      random.choices(["Loja","Online","Telefone"], k=n),
    })

    return {
        "DimCliente":  dim_cliente,
        "DimProduto":  dim_produto,
        "DimVendedor": dim_vendedor,
        "DimFilial":   dim_filial,
        "DimGeografia":dim_geo,
        "FatoVendas":  fato,
        "dCalendario": dcalendario(start, end),
    }

# ── FINANCEIRO ──────────────────────────────────────────────────────────────
def gerar_financeiro(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_contas  = min(n, 3000)
    n_agencias = 30
    n_produtos = 20

    dim_agencia = pd.DataFrame({
        "id_agencia": new_ids(n_agencias),
        "nome":       [f"Agência {fake.city()}" for _ in range(n_agencias)],
        "codigo":     [f"{rng.integers(1000,9999)}-{rng.integers(0,9)}" for _ in range(n_agencias)],
        "uf":         random.choices(["SP","RJ","MG","RS","PR"], k=n_agencias),
        "tipo":       random.choices(["Física","Digital","Express"], k=n_agencias),
    })

    dim_conta = pd.DataFrame({
        "id_conta":   new_ids(n_contas),
        "titular":    [fake.name() for _ in range(n_contas)],
        "cpf_cnpj":   [fake.cpf()  for _ in range(n_contas)],
        "tipo_conta": random.choices(["Corrente","Poupança","Empresarial","Investimento"], k=n_contas),
        "id_agencia": random.choices(dim_agencia["id_agencia"].tolist(), k=n_contas),
        "segmento":   random.choices(["Varejo","Personnalité","Corporate","Private"], k=n_contas),
    })

    dim_produto = pd.DataFrame({
        "id_produto":  new_ids(n_produtos),
        "nome":        ["CDB","LCI","LCA","Tesouro Direto","Fundo DI","Fundo Multimercado",
                        "Cartão Crédito","Cartão Débito","Seguro Vida","Previdência",
                        "Financiamento","Empréstimo Pessoal","Consórcio","Câmbio",
                        "Conta Corrente","Conta Poupança","PIX","TED","DOC","Cheque"],
        "categoria":   ["Investimento"]*6 + ["Cartão"]*2 + ["Seguro","Previdência"] +
                       ["Crédito"]*3 + ["Câmbio"] + ["Conta"]*2 + ["Pagamento"]*4,
        "taxa_juros":  rng.uniform(0.005, 0.15, n_produtos).round(4),
    })

    tipos_transacao = ["Débito","Crédito","TED","DOC","PIX","Saque","Depósito","Investimento"]
    fato = pd.DataFrame({
        "id_transacao": new_ids(n),
        "id_data":      rand_dates(start, end, n),
        "id_conta":     random.choices(dim_conta["id_conta"].tolist(), k=n),
        "id_agencia":   random.choices(dim_agencia["id_agencia"].tolist(), k=n),
        "id_produto":   random.choices(dim_produto["id_produto"].tolist(), k=n),
        "tipo":         random.choices(tipos_transacao, k=n),
        "valor":        rng.uniform(10, 50000, n).round(2),
        "saldo_apos":   rng.uniform(0, 200000, n).round(2),
        "status":       random.choices(["Aprovada","Negada","Pendente"], weights=[85,10,5], k=n),
    })

    return {
        "DimAgencia":    dim_agencia,
        "DimConta":      dim_conta,
        "DimProduto":    dim_produto,
        "FatoTransacao": fato,
        "dCalendario":   dcalendario(start, end),
    }

# ── SAÚDE ────────────────────────────────────────────────────────────────────
def gerar_saude(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_pacientes  = min(n, 3000)
    n_medicos    = 80
    n_proc       = 40
    n_unidades   = 15

    dim_unidade = pd.DataFrame({
        "id_unidade": new_ids(n_unidades),
        "nome":       [f"Unidade {fake.city()}" for _ in range(n_unidades)],
        "tipo":       random.choices(["Hospital","UPA","Clínica","AME","CAPS"], k=n_unidades),
        "uf":         random.choices(["SP","RJ","MG","RS","PR"], k=n_unidades),
        "leitos":     rng.integers(20, 400, n_unidades),
    })

    especialidades = ["Clínica Geral","Cardiologia","Ortopedia","Pediatria","Ginecologia",
                      "Neurologia","Oncologia","Dermatologia","Psiquiatria","Oftalmologia"]
    dim_medico = pd.DataFrame({
        "id_medico":      new_ids(n_medicos),
        "nome":           [f"Dr(a). {fake.name()}" for _ in range(n_medicos)],
        "crm":            [f"CRM/{random.choice(['SP','RJ','MG'])}-{rng.integers(10000,99999)}" for _ in range(n_medicos)],
        "especialidade":  random.choices(especialidades, k=n_medicos),
        "id_unidade":     random.choices(dim_unidade["id_unidade"].tolist(), k=n_medicos),
    })

    cids = [f"J{rng.integers(10,99)}.{rng.integers(0,9)}" for _ in range(n_proc)]
    dim_procedimento = pd.DataFrame({
        "id_proc":   new_ids(n_proc),
        "nome":      [f"Procedimento {fake.word().capitalize()}" for _ in range(n_proc)],
        "cid":       cids,
        "categoria": random.choices(["Consulta","Exame","Cirurgia","Internação","Terapia"], k=n_proc),
        "valor_sus": rng.uniform(20, 5000, n_proc).round(2),
    })

    dim_paciente = pd.DataFrame({
        "id_paciente": new_ids(n_pacientes),
        "nome":        [fake.name() for _ in range(n_pacientes)],
        "cpf":         [fake.cpf()  for _ in range(n_pacientes)],
        "sexo":        random.choices(["M","F"], k=n_pacientes),
        "idade":       rng.integers(0, 100, n_pacientes),
        "convenio":    random.choices(["SUS","Unimed","Bradesco Saúde","Amil","Particular"], k=n_pacientes),
    })

    fato = pd.DataFrame({
        "id_atendimento": new_ids(n),
        "id_data":        rand_dates(start, end, n),
        "id_paciente":    random.choices(dim_paciente["id_paciente"].tolist(), k=n),
        "id_medico":      random.choices(dim_medico["id_medico"].tolist(), k=n),
        "id_proc":        random.choices(dim_procedimento["id_proc"].tolist(), k=n),
        "id_unidade":     random.choices(dim_unidade["id_unidade"].tolist(), k=n),
        "duracao_min":    rng.integers(15, 300, n),
        "valor_cobrado":  rng.uniform(50, 8000, n).round(2),
        "resultado":      random.choices(["Alta","Internado","Em acompanhamento","Óbito"],
                                         weights=[70,15,12,3], k=n),
    })

    return {
        "DimUnidade":      dim_unidade,
        "DimMedico":       dim_medico,
        "DimProcedimento": dim_procedimento,
        "DimPaciente":     dim_paciente,
        "FatoAtendimento": fato,
        "dCalendario":     dcalendario(start, end),
    }

# ── TECNOLOGIA ───────────────────────────────────────────────────────────────
def gerar_tecnologia(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_clientes = min(n, 2000)
    n_produtos = 30
    n_agentes  = 60

    planos = ["Starter","Basic","Pro","Business","Enterprise"]
    dim_produto = pd.DataFrame({
        "id_produto": new_ids(n_produtos),
        "nome":       [f"{fake.word().capitalize()} {p}" for p in random.choices(planos, k=n_produtos)],
        "categoria":  random.choices(["SaaS","Licença","Suporte","Consultoria","Infraestrutura"], k=n_produtos),
        "plano":      random.choices(planos, k=n_produtos),
        "mrr":        rng.uniform(99, 9999, n_produtos).round(2),
    })

    dim_cliente = pd.DataFrame({
        "id_cliente": new_ids(n_clientes),
        "empresa":    [fake.company() for _ in range(n_clientes)],
        "cnpj":       [fake.cnpj() for _ in range(n_clientes)],
        "setor":      random.choices(["Varejo","Indústria","Serviços","Saúde","Financeiro"], k=n_clientes),
        "tamanho":    random.choices(["MEI","ME","EPP","Médio","Grande"], k=n_clientes),
        "uf":         random.choices(["SP","RJ","MG","RS","PR"], k=n_clientes),
    })

    dim_agente = pd.DataFrame({
        "id_agente": new_ids(n_agentes),
        "nome":      [fake.name() for _ in range(n_agentes)],
        "area":      random.choices(["Comercial","CS","Suporte N1","Suporte N2","Implantação"], k=n_agentes),
        "nivel":     random.choices(["Jr","Pl","Sr"], k=n_agentes),
    })

    fato = pd.DataFrame({
        "id_contrato": new_ids(n),
        "id_data":     rand_dates(start, end, n),
        "id_cliente":  random.choices(dim_cliente["id_cliente"].tolist(), k=n),
        "id_produto":  random.choices(dim_produto["id_produto"].tolist(), k=n),
        "id_agente":   random.choices(dim_agente["id_agente"].tolist(), k=n),
        "tipo":        random.choices(["Novo","Renovação","Upgrade","Downgrade","Churn"], k=n),
        "valor_mrr":   rng.uniform(99, 9999, n).round(2),
        "arr":         rng.uniform(1188, 119988, n).round(2),
        "nps":         rng.integers(0, 11, n),
        "status":      random.choices(["Ativo","Cancelado","Trial","Suspenso"], weights=[70,15,10,5], k=n),
    })

    return {
        "DimProduto":  dim_produto,
        "DimCliente":  dim_cliente,
        "DimAgente":   dim_agente,
        "FatoContrato":fato,
        "dCalendario": dcalendario(start, end),
    }

# ── EDUCAÇÃO ─────────────────────────────────────────────────────────────────
def gerar_educacao(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_alunos  = min(n, 5000)
    n_cursos  = 60
    n_instrutores = 40

    dim_curso = pd.DataFrame({
        "id_curso":    new_ids(n_cursos),
        "nome":        [f"Curso de {fake.word().capitalize()}" for _ in range(n_cursos)],
        "modalidade":  random.choices(["EAD","Presencial","Híbrido"], k=n_cursos),
        "area":        random.choices(["TI","Saúde","Gestão","Direito","Engenharia","Design"], k=n_cursos),
        "carga_horas": random.choices([40,60,80,120,200,360,400], k=n_cursos),
        "valor":       rng.uniform(200, 5000, n_cursos).round(2),
    })

    dim_aluno = pd.DataFrame({
        "id_aluno": new_ids(n_alunos),
        "nome":     [fake.name() for _ in range(n_alunos)],
        "cpf":      [fake.cpf()  for _ in range(n_alunos)],
        "email":    [fake.email() for _ in range(n_alunos)],
        "sexo":     random.choices(["M","F","Outro"], weights=[47,50,3], k=n_alunos),
        "uf":       random.choices(["SP","RJ","MG","RS","PR","BA","CE"], k=n_alunos),
        "faixa_etaria": random.choices(["15-17","18-24","25-34","35-44","45+"], k=n_alunos),
    })

    dim_instrutor = pd.DataFrame({
        "id_instrutor": new_ids(n_instrutores),
        "nome":         [fake.name() for _ in range(n_instrutores)],
        "titulacao":    random.choices(["Graduado","Especialista","Mestre","Doutor"], k=n_instrutores),
        "area":         random.choices(["TI","Saúde","Gestão","Direito","Engenharia","Design"], k=n_instrutores),
    })

    fato = pd.DataFrame({
        "id_matricula":  new_ids(n),
        "id_data":       rand_dates(start, end, n),
        "id_aluno":      random.choices(dim_aluno["id_aluno"].tolist(), k=n),
        "id_curso":      random.choices(dim_curso["id_curso"].tolist(), k=n),
        "id_instrutor":  random.choices(dim_instrutor["id_instrutor"].tolist(), k=n),
        "forma_pagamento": random.choices(["Boleto","Cartão","PIX","Financiamento"], k=n),
        "valor_pago":    rng.uniform(200, 5000, n).round(2),
        "nota_final":    rng.uniform(0, 10, n).round(1),
        "concluiu":      random.choices([1, 0], weights=[65, 35], k=n),
        "status":        random.choices(["Ativo","Concluído","Trancado","Cancelado"], weights=[40,35,15,10], k=n),
    })

    return {
        "DimCurso":     dim_curso,
        "DimAluno":     dim_aluno,
        "DimInstrutor": dim_instrutor,
        "FatoMatricula":fato,
        "dCalendario":  dcalendario(start, end),
    }

# ── LOGÍSTICA ────────────────────────────────────────────────────────────────
def gerar_logistica(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_trans    = 20
    n_clientes = min(n, 2000)
    n_rotas    = 50

    ufs = ["SP","RJ","MG","RS","PR","SC","BA","CE","PE","GO"]
    dim_transportadora = pd.DataFrame({
        "id_transportadora": new_ids(n_trans),
        "nome":              [f"Transportadora {fake.last_name()}" for _ in range(n_trans)],
        "cnpj":              [fake.cnpj() for _ in range(n_trans)],
        "tipo":              random.choices(["Rodoviário","Aéreo","Marítimo","Expresso"], k=n_trans),
        "uf_sede":           random.choices(ufs, k=n_trans),
    })

    dim_rota = pd.DataFrame({
        "id_rota":    new_ids(n_rotas),
        "origem_uf":  random.choices(ufs, k=n_rotas),
        "destino_uf": random.choices(ufs, k=n_rotas),
        "distancia_km": rng.integers(50, 4000, n_rotas),
        "prazo_dias":   rng.integers(1, 15, n_rotas),
    })

    dim_cliente = pd.DataFrame({
        "id_cliente": new_ids(n_clientes),
        "empresa":    [fake.company() for _ in range(n_clientes)],
        "cnpj":       [fake.cnpj() for _ in range(n_clientes)],
        "segmento":   random.choices(["Varejo","Indústria","E-commerce","Atacado"], k=n_clientes),
        "uf":         random.choices(ufs, k=n_clientes),
    })

    fato = pd.DataFrame({
        "id_entrega":        new_ids(n),
        "id_data":           rand_dates(start, end, n),
        "id_transportadora": random.choices(dim_transportadora["id_transportadora"].tolist(), k=n),
        "id_rota":           random.choices(dim_rota["id_rota"].tolist(), k=n),
        "id_cliente":        random.choices(dim_cliente["id_cliente"].tolist(), k=n),
        "peso_kg":           rng.uniform(0.1, 2000, n).round(2),
        "volume_m3":         rng.uniform(0.01, 50, n).round(3),
        "valor_frete":       rng.uniform(15, 5000, n).round(2),
        "prazo_acordado":    rng.integers(1, 15, n),
        "dias_entregue":     rng.integers(1, 20, n),
        "status":            random.choices(["Entregue","Em trânsito","Atrasado","Devolvido"],
                                            weights=[65,20,10,5], k=n),
    })

    return {
        "DimTransportadora": dim_transportadora,
        "DimRota":           dim_rota,
        "DimCliente":        dim_cliente,
        "FatoEntrega":       fato,
        "dCalendario":       dcalendario(start, end),
    }

# ── ENERGIA ──────────────────────────────────────────────────────────────────
def gerar_energia(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_consumidores = min(n, 5000)
    n_medidores    = min(n, 5000)
    n_subestacoes  = 20

    dim_subestacao = pd.DataFrame({
        "id_subestacao": new_ids(n_subestacoes),
        "nome":          [f"SE {fake.city()}" for _ in range(n_subestacoes)],
        "tensao_kv":     random.choices([13.8, 34.5, 69, 138, 230, 440], k=n_subestacoes),
        "uf":            random.choices(["SP","MG","RJ","RS","PR"], k=n_subestacoes),
    })

    dim_consumidor = pd.DataFrame({
        "id_consumidor": new_ids(n_consumidores),
        "nome":          [fake.name() for _ in range(n_consumidores)],
        "cpf_cnpj":      [fake.cpf() for _ in range(n_consumidores)],
        "classe":        random.choices(["Residencial","Comercial","Industrial","Rural","Poder Público"],
                                        weights=[55,25,10,5,5], k=n_consumidores),
        "subclasse":     random.choices(["Normal","BT","AT","MT"], k=n_consumidores),
        "uf":            random.choices(["SP","MG","RJ","RS","PR"], k=n_consumidores),
    })

    dim_medidor = pd.DataFrame({
        "id_medidor":    new_ids(n_medidores),
        "serial":        [f"MED{rng.integers(100000,999999)}" for _ in range(n_medidores)],
        "modelo":        random.choices(["LANDIS+GYR","ELSTER","ITRON","SCHNEIDER"], k=n_medidores),
        "id_consumidor": random.choices(dim_consumidor["id_consumidor"].tolist(), k=n_medidores),
        "id_subestacao": random.choices(dim_subestacao["id_subestacao"].tolist(), k=n_medidores),
    })

    consumo = rng.uniform(50, 5000, n).round(2)
    fato = pd.DataFrame({
        "id_leitura":    new_ids(n),
        "id_data":       rand_dates(start, end, n),
        "id_medidor":    random.choices(dim_medidor["id_medidor"].tolist(), k=n),
        "id_consumidor": random.choices(dim_consumidor["id_consumidor"].tolist(), k=n),
        "id_subestacao": random.choices(dim_subestacao["id_subestacao"].tolist(), k=n),
        "consumo_kwh":   consumo,
        "demanda_kw":    rng.uniform(5, 500, n).round(2),
        "tarifa_kwh":    rng.uniform(0.6, 1.5, n).round(4),
        "valor_fatura":  (consumo * rng.uniform(0.6, 1.5, n)).round(2),
        "tensao_v":      rng.uniform(210, 240, n).round(1),
        "fator_potencia":rng.uniform(0.85, 1.0, n).round(3),
    })

    return {
        "DimSubestacao": dim_subestacao,
        "DimConsumidor": dim_consumidor,
        "DimMedidor":    dim_medidor,
        "FatoConsumo":   fato,
        "dCalendario":   dcalendario(start, end),
    }

# ── TELECOM ──────────────────────────────────────────────────────────────────
def gerar_telecom(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_assinantes = min(n, 5000)
    n_planos     = 20
    n_torres     = 50

    dim_plano = pd.DataFrame({
        "id_plano":    new_ids(n_planos),
        "nome":        [f"Plano {p} {d}" for p, d in
                        zip(random.choices(["Básico","Plus","Max","Ultra","Ilimitado"], k=n_planos),
                            random.choices(["Móvel","Fixo","Combo","Empresarial"], k=n_planos))],
        "tipo":        random.choices(["Pré-pago","Pós-pago","Controle","Empresarial"], k=n_planos),
        "dados_gb":    random.choices([5, 10, 15, 20, 30, 50, 100, 0], k=n_planos),
        "valor_mensal":rng.uniform(29.9, 299.9, n_planos).round(2),
    })

    dim_torre = pd.DataFrame({
        "id_torre": new_ids(n_torres),
        "codigo":   [f"ERB-{rng.integers(1000,9999)}" for _ in range(n_torres)],
        "tecnologia":random.choices(["2G","3G","4G","5G"], weights=[5,10,60,25], k=n_torres),
        "uf":       random.choices(["SP","RJ","MG","RS","PR","BA"], k=n_torres),
        "capacidade_canais": rng.integers(50, 500, n_torres),
    })

    dim_assinante = pd.DataFrame({
        "id_assinante": new_ids(n_assinantes),
        "nome":         [fake.name() for _ in range(n_assinantes)],
        "cpf":          [fake.cpf()  for _ in range(n_assinantes)],
        "ddd":          [str(random.choice([11,21,31,41,51,61,71,81,85,91])) for _ in range(n_assinantes)],
        "id_plano":     random.choices(dim_plano["id_plano"].tolist(), k=n_assinantes),
        "uf":           random.choices(["SP","RJ","MG","RS","PR","BA"], k=n_assinantes),
    })

    fato = pd.DataFrame({
        "id_chamada":    new_ids(n),
        "id_data":       rand_dates(start, end, n),
        "id_assinante":  random.choices(dim_assinante["id_assinante"].tolist(), k=n),
        "id_plano":      random.choices(dim_plano["id_plano"].tolist(), k=n),
        "id_torre":      random.choices(dim_torre["id_torre"].tolist(), k=n),
        "tipo":          random.choices(["Voz","SMS","Dados","VoIP","Roaming"], k=n),
        "duracao_seg":   rng.integers(0, 3600, n),
        "dados_mb":      rng.uniform(0, 2000, n).round(2),
        "valor_cobrado": rng.uniform(0, 50, n).round(2),
        "qualidade_dbm": rng.integers(-110, -60, n),
    })

    return {
        "DimPlano":     dim_plano,
        "DimTorre":     dim_torre,
        "DimAssinante": dim_assinante,
        "FatoChamada":  fato,
        "dCalendario":  dcalendario(start, end),
    }

# ── INDÚSTRIA ────────────────────────────────────────────────────────────────
def gerar_industria(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_maquinas = 30
    n_insumos  = 60
    n_produtos = 40
    n_operadores = 50

    dim_maquina = pd.DataFrame({
        "id_maquina": new_ids(n_maquinas),
        "nome":       [f"Máquina {fake.word().upper()}-{i}" for i in range(1, n_maquinas+1)],
        "tipo":       random.choices(["Torno","Fresadora","Prensa","Injetora","CNC","Soldadora","Estampadora"], k=n_maquinas),
        "linha":      random.choices(["Linha A","Linha B","Linha C","Linha D"], k=n_maquinas),
        "capacidade_h":rng.integers(100, 2000, n_maquinas),
        "ano_fab":    rng.integers(2000, 2023, n_maquinas),
    })

    dim_insumo = pd.DataFrame({
        "id_insumo":  new_ids(n_insumos),
        "nome":       [f"Insumo {fake.word().capitalize()}" for _ in range(n_insumos)],
        "tipo":       random.choices(["Matéria-Prima","Embalagem","Componente","Químico","Combustível"], k=n_insumos),
        "unidade":    random.choices(["kg","ton","litro","unidade","metro"], k=n_insumos),
        "custo_unit": rng.uniform(1, 500, n_insumos).round(2),
    })

    dim_produto = pd.DataFrame({
        "id_produto": new_ids(n_produtos),
        "nome":       [f"Produto {fake.word().upper()}-{i}" for i in range(1, n_produtos+1)],
        "familia":    random.choices(["Família A","Família B","Família C"], k=n_produtos),
        "peso_kg":    rng.uniform(0.1, 100, n_produtos).round(2),
        "preco_venda":rng.uniform(50, 10000, n_produtos).round(2),
    })

    dim_operador = pd.DataFrame({
        "id_operador": new_ids(n_operadores),
        "nome":        [fake.name() for _ in range(n_operadores)],
        "turno":       random.choices(["Manhã","Tarde","Noite"], k=n_operadores),
        "nivel":       random.choices(["Operador I","Operador II","Técnico","Supervisor"], k=n_operadores),
    })

    qtd = rng.integers(1, 500, n)
    fato = pd.DataFrame({
        "id_ordem":    new_ids(n),
        "id_data":     rand_dates(start, end, n),
        "id_maquina":  random.choices(dim_maquina["id_maquina"].tolist(), k=n),
        "id_insumo":   random.choices(dim_insumo["id_insumo"].tolist(), k=n),
        "id_produto":  random.choices(dim_produto["id_produto"].tolist(), k=n),
        "id_operador": random.choices(dim_operador["id_operador"].tolist(), k=n),
        "quantidade":  qtd,
        "tempo_ciclo_min": rng.uniform(1, 480, n).round(1),
        "refugo_pct":  rng.uniform(0, 0.15, n).round(4),
        "custo_producao": rng.uniform(100, 50000, n).round(2),
        "oee":         rng.uniform(0.5, 0.98, n).round(3),
        "turno":       random.choices(["Manhã","Tarde","Noite"], k=n),
    })

    return {
        "DimMaquina":  dim_maquina,
        "DimInsumo":   dim_insumo,
        "DimProduto":  dim_produto,
        "DimOperador": dim_operador,
        "FatoProducao":fato,
        "dCalendario": dcalendario(start, end),
    }

# ── AGRONEGÓCIO ──────────────────────────────────────────────────────────────
def gerar_agronegocio(n: int, start: date, end: date) -> dict[str, pd.DataFrame]:
    n_propriedades = min(n // 5 + 50, 500)
    n_culturas     = 20
    n_insumos      = 40
    n_clientes     = min(n, 1000)

    culturas_nomes = ["Soja","Milho","Cana-de-açúcar","Algodão","Café","Trigo",
                      "Arroz","Feijão","Laranja","Eucalipto","Sorgo","Girassol",
                      "Amendoim","Mandioca","Cacau","Mamona","Canola","Aveia","Cevada","Fumo"]
    dim_cultura = pd.DataFrame({
        "id_cultura":   new_ids(n_culturas),
        "nome":         culturas_nomes,
        "tipo":         random.choices(["Grão","Fibra","Fruta","Hortaliça","Energia"], k=n_culturas),
        "ciclo_dias":   rng.integers(60, 365, n_culturas),
        "preco_ton":    rng.uniform(500, 8000, n_culturas).round(2),
    })

    ufs_agro = ["MT","MS","GO","SP","PR","RS","SC","MG","BA","PI"]
    dim_propriedade = pd.DataFrame({
        "id_propriedade": new_ids(n_propriedades),
        "nome":           [f"Fazenda {fake.last_name()}" for _ in range(n_propriedades)],
        "cnpj_cpf":       [fake.cpf() for _ in range(n_propriedades)],
        "area_ha":        rng.uniform(10, 50000, n_propriedades).round(1),
        "uf":             random.choices(ufs_agro, k=n_propriedades),
        "bioma":          random.choices(["Cerrado","Amazônia","Mata Atlântica","Pampa","Pantanal"], k=n_propriedades),
        "tipo":           random.choices(["Familiar","Empresarial","Cooperativa"], k=n_propriedades),
    })

    dim_insumo = pd.DataFrame({
        "id_insumo": new_ids(n_insumos),
        "nome":      [f"Insumo {fake.word().capitalize()}" for _ in range(n_insumos)],
        "tipo":      random.choices(["Fertilizante","Defensivo","Semente","Combustível","Irrigação"], k=n_insumos),
        "unidade":   random.choices(["kg","litro","saco","dose"], k=n_insumos),
        "custo_unit":rng.uniform(10, 2000, n_insumos).round(2),
    })

    area_plantada = rng.uniform(5, 5000, n).round(1)
    prod_por_ha   = rng.uniform(1, 10, n).round(2)
    fato = pd.DataFrame({
        "id_safra":        new_ids(n),
        "id_data":         rand_dates(start, end, n),
        "id_propriedade":  random.choices(dim_propriedade["id_propriedade"].tolist(), k=n),
        "id_cultura":      random.choices(dim_cultura["id_cultura"].tolist(), k=n),
        "id_insumo":       random.choices(dim_insumo["id_insumo"].tolist(), k=n),
        "area_plantada_ha":area_plantada,
        "produtividade_tha":prod_por_ha,
        "producao_ton":    (area_plantada * prod_por_ha).round(2),
        "custo_ha":        rng.uniform(500, 8000, n).round(2),
        "receita":         rng.uniform(1000, 500000, n).round(2),
        "indice_chuva_mm": rng.uniform(0, 300, n).round(1),
        "temperatura_media":rng.uniform(15, 35, n).round(1),
        "status":          random.choices(["Colhida","Em andamento","Planejada","Perdida"],
                                          weights=[50,30,15,5], k=n),
    })

    return {
        "DimCultura":     dim_cultura,
        "DimPropriedade": dim_propriedade,
        "DimInsumo":      dim_insumo,
        "FatoSafra":      fato,
        "dCalendario":    dcalendario(start, end),
    }

# ═══════════════════════════════════════════════════════════════════════════
#  MAPA DE SETORES
# ═══════════════════════════════════════════════════════════════════════════
SETORES = {
    "🛒 Varejo":          gerar_varejo,
    "💰 Financeiro":      gerar_financeiro,
    "🏥 Saúde":           gerar_saude,
    "💻 Tecnologia":      gerar_tecnologia,
    "📚 Educação":        gerar_educacao,
    "🚚 Logística":       gerar_logistica,
    "⚡ Energia":          gerar_energia,
    "📡 Telecom":         gerar_telecom,
    "🏭 Indústria":       gerar_industria,
    "🌾 Agronegócio":     gerar_agronegocio,
}

# ═══════════════════════════════════════════════════════════════════════════
#  INTERFACE STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, .main, [data-testid="stAppViewContainer"] {
    background-color: #0a0e27 !important;
}

[data-testid="stAppViewContainer"] {
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -10%, rgba(139,92,246,0.12) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 80% 60%, rgba(59,130,246,0.08) 0%, transparent 50%);
}

[data-testid="stHeader"] { background: transparent !important; }

.main h1, .main h2, .main h3, .main h4,
.main p, .main a, .main li,
[data-testid="stAppViewContainer"] div:not([data-testid="stSidebar"]) {
    font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stMarkdownContainer"] { width: 100% !important; }
.block-container {
    max-width: 100% !important;
    padding-left: 4rem !important;
    padding-right: 4rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: rgba(10, 14, 39, 0.95) !important;
    border-right: 1px solid rgba(167,139,250,0.15) !important;
}
[data-testid="stSidebar"] * {
    font-family: 'DM Sans', sans-serif !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
}
[data-testid="stSidebar"] .stSlider > div > div > div {
    background: #a78bfa !important;
}

/* ── HERO ── */
.hero-wrapper {
    text-align: center;
    padding: 72px 20px 48px;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-badge {
    display: inline-block;
    font-family: 'Syne', sans-serif !important;
    font-size: 0.70rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #a78bfa;
    border: 1px solid rgba(167,139,250,0.35);
    background: rgba(167,139,250,0.07);
    padding: 6px 18px;
    border-radius: 100px;
    margin-bottom: 26px;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.2rem, 4.5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.08;
    letter-spacing: -1.5px;
    color: #f0f4ff;
    margin: 0 auto 18px;
    max-width: 760px;
    text-align: center;
}
.hero-title .accent {
    background: linear-gradient(135deg, #a78bfa 0%, #7c3aed 50%, #c4b5fd 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-subtitle {
    font-size: 1rem;
    font-weight: 300;
    color: #7b8ba8;
    max-width: 520px;
    margin: 0 auto 44px;
    line-height: 1.75;
    text-align: center;
}
.hero-stats {
    display: flex;
    justify-content: center;
    gap: 48px;
    flex-wrap: wrap;
    margin-bottom: 52px;
}
.hero-stat { text-align: center; }
.hero-stat-number {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem;
    font-weight: 800;
    color: #a78bfa;
    display: block;
    line-height: 1;
}
.hero-stat-label {
    font-size: 0.72rem;
    color: #4a5568;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 6px;
    display: block;
}
.hero-divider {
    width: 100%;
    max-width: 860px;
    margin: 0 auto 52px;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.3), transparent);
}

/* ── SECTION HEADERS ── */
.section-header {
    font-family: 'Syne', sans-serif !important;
    font-size: 1.4rem;
    font-weight: 800;
    color: #f0f4ff;
    margin: 44px 0 24px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(167,139,250,0.2);
    letter-spacing: -0.5px;
    position: relative;
}
.section-header::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 48px;
    height: 2px;
    background: #a78bfa;
}

/* ── STAT CARDS ── */
.stat-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0.2) 100%);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 18px;
    padding: 28px 22px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stat-card:hover {
    transform: translateY(-4px);
    border-color: rgba(167,139,250,0.4);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.stat-card-icon {
    font-size: 1.8rem;
    margin-bottom: 10px;
    display: block;
}
.stat-number {
    font-family: 'Syne', sans-serif !important;
    font-size: 2rem;
    font-weight: 800;
    color: #a78bfa;
    margin-bottom: 6px;
    line-height: 1;
    display: block;
}
.stat-label {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.72rem;
    font-weight: 700;
    color: #e2e8f0;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    display: block;
}
.stat-sublabel {
    font-size: 0.78rem;
    color: #4a5568;
    margin-top: 6px;
    font-weight: 300;
    display: block;
}

/* ── SECTOR CARDS ── */
.sector-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 20px 0;
}
.sector-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0.2) 100%);
    border: 1px solid rgba(167,139,250,0.18);
    border-radius: 14px;
    padding: 16px 14px;
    text-align: center;
    transition: all 0.3s ease;
}
.sector-card:hover {
    border-color: rgba(167,139,250,0.4);
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(0,0,0,0.35);
}
.sector-card-icon { font-size: 1.6rem; display: block; margin-bottom: 8px; }
.sector-card-name {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.8rem;
    font-weight: 700;
    color: #e2e8f0;
}

/* ── STEPS ── */
.steps-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin: 20px 0;
}
.step-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.03) 0%, rgba(0,0,0,0.2) 100%);
    border: 1px solid rgba(167,139,250,0.18);
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: all 0.3s ease;
}
.step-card:hover {
    border-color: rgba(167,139,250,0.4);
    box-shadow: 0 12px 32px rgba(0,0,0,0.3);
}
.step-num {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #a78bfa;
    background: rgba(167,139,250,0.1);
    border: 1px solid rgba(167,139,250,0.2);
    border-radius: 100px;
    padding: 3px 12px;
    display: inline-block;
    margin-bottom: 14px;
}
.step-icon { font-size: 1.8rem; display: block; margin-bottom: 10px; }
.step-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 0.9rem;
    font-weight: 700;
    color: #f0f4ff;
    margin-bottom: 8px;
}
.step-text { font-size: 0.78rem; color: #7b8ba8; line-height: 1.6; font-weight: 300; }

/* ── INFO BOX ── */
.info-box {
    background: linear-gradient(145deg, rgba(167,139,250,0.08) 0%, rgba(124,58,237,0.05) 100%);
    border: 1px solid rgba(167,139,250,0.25);
    border-radius: 14px;
    padding: 18px 22px;
    margin: 20px 0;
    font-size: 0.88rem;
    color: #c4b5fd;
    line-height: 1.7;
}
.info-box strong { color: #a78bfa; }

/* ── SUCCESS BOX ── */
.success-box {
    background: linear-gradient(145deg, rgba(34,197,94,0.08) 0%, rgba(34,197,94,0.04) 100%);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 14px;
    padding: 16px 20px;
    font-size: 0.9rem;
    color: #86efac;
    margin: 16px 0;
}

/* ── INPUTS ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    color: #e2e8f0 !important;
    border-radius: 12px !important;
}
.stDateInput > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    border-radius: 12px !important;
}
hr {
    border: none !important;
    border-top: 1px solid rgba(167,139,250,0.1) !important;
    margin: 36px 0 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid rgba(167,139,250,0.2) !important;
    gap: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #7b8ba8 !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.5px;
    border-radius: 8px 8px 0 0 !important;
    padding: 10px 20px !important;
    transition: color 0.2s, background 0.2s;
}
.stTabs [aria-selected="true"] {
    background: rgba(167,139,250,0.1) !important;
    color: #a78bfa !important;
    border-bottom: 2px solid #a78bfa !important;
}

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid rgba(167,139,250,0.2) !important; border-radius: 12px !important; }

/* ── BOTÃO COLAPSAR SIDEBAR ── */
span[data-testid="stIconMaterial"] {
    text-indent: -9999px !important;
    overflow: hidden !important;
    font-size: 1.4rem !important;
    display: block !important;
    width: 1.4rem !important;
    height: 1.4rem !important;
}
button[data-testid="stBaseButton-headerNoPadding"],
[data-testid="stSidebarCollapsedControl"] button {
    background: rgba(167,139,250,0.08) !important;
    border: 1px solid rgba(167,139,250,0.2) !important;
    border-radius: 8px !important;
}
button[data-testid="stBaseButton-headerNoPadding"]:hover,
[data-testid="stSidebarCollapsedControl"] button:hover {
    background: rgba(167,139,250,0.18) !important;
    border-color: rgba(167,139,250,0.4) !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0e27; }
::-webkit-scrollbar-thumb { background: rgba(167,139,250,0.2); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(167,139,250,0.4); }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 10px 22px !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(124,58,237,0.4) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, #7c3aed, #a78bfa) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    transition: transform 0.2s, box-shadow 0.2s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(124,58,237,0.45) !important;
}
</style>
""", unsafe_allow_html=True)

# ── sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px;">
        <div style="font-family: Syne, sans-serif; font-size: 1.1rem; font-weight: 800;
                    color: #f0f4ff; margin-bottom: 4px;">BI Data Generator</div>
        <div style="font-family: Syne, sans-serif; font-size: 0.65rem; font-weight: 700;
                    letter-spacing: 3px; text-transform: uppercase; color: #a78bfa;
                    background: rgba(167,139,250,0.1); border: 1px solid rgba(167,139,250,0.25);
                    border-radius: 100px; padding: 3px 12px; display: inline-block;">PRO</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px; background: rgba(167,139,250,0.15); margin-bottom:20px;"></div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Syne, sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4a5568; margin-bottom: 10px;">Setor</p>', unsafe_allow_html=True)
    setor = st.selectbox("", list(SETORES.keys()), label_visibility="collapsed")

    st.markdown('<p style="font-family: Syne, sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4a5568; margin: 18px 0 10px;">Período</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input("Início", value=date(2023, 1, 1))
    with col2:
        data_fim = st.date_input("Fim", value=date(2023, 12, 31))

    if data_fim <= data_inicio:
        st.markdown('<div style="background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;padding:10px 14px;font-size:0.8rem;color:#fca5a5;margin-top:8px;">&#9888; Data fim deve ser após a data início.</div>', unsafe_allow_html=True)

    st.markdown('<p style="font-family: Syne, sans-serif; font-size: 0.7rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #4a5568; margin: 18px 0 10px;">Volume de dados</p>', unsafe_allow_html=True)
    n_linhas = st.slider("", min_value=1000, max_value=10000, value=5000, step=500, label_visibility="collapsed")
    st.markdown(f'<p style="font-size:0.75rem;color:#7b8ba8;text-align:center;margin-top:-8px;">{n_linhas:,} linhas na tabela fato</p>', unsafe_allow_html=True)

    st.markdown('<div style="height:1px; background: rgba(167,139,250,0.15); margin: 20px 0;"></div>', unsafe_allow_html=True)
    gerar = st.button("Gerar base agora", use_container_width=True, type="primary")

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-badge">Star Schema · 10 Setores · dCalendario</div>
    <h1 class="hero-title">
        Dados reais para seu projeto de<br><span class="accent">Business Intelligence</span>
    </h1>
    <p class="hero-subtitle">
        Gere bases profissionais no modelo estrela em segundos.
        Tabelas fato, dimensões e dCalendario prontos para Power BI, Tableau e qualquer ferramenta de BI.
    </p>
    <div class="hero-stats">
        <div class="hero-stat">
            <span class="hero-stat-number">10</span>
            <span class="hero-stat-label">Setores</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-number">10k</span>
            <span class="hero-stat-label">Linhas máx.</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-number">.zip</span>
            <span class="hero-stat-label">Download</span>
        </div>
        <div class="hero-stat">
            <span class="hero-stat-number">free</span>
            <span class="hero-stat-label">Sem cadastro</span>
        </div>
    </div>
    <div class="hero-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── geração ──────────────────────────────────────────────────────────────────
if gerar:
    if data_fim <= data_inicio:
        st.error("Corrija as datas antes de gerar.")
        st.stop()

    with st.spinner("Gerando base de dados..."):
        fn   = SETORES[setor]
        nome = setor.split(" ", 1)[1]
        tabelas = fn(n_linhas, data_inicio, data_fim)

    st.markdown(f'<div class="success-box">✅ Base <strong>{nome}</strong> gerada com sucesso! {len(tabelas)} tabelas prontas para download.</div>', unsafe_allow_html=True)

    # ── métricas ─────────────────────────────────────────────────────────────
    st.markdown('<h3 class="section-header">Resumo da base gerada</h3>', unsafe_allow_html=True)

    n_cols = min(len(tabelas), 7)
    cols   = st.columns(n_cols)
    icons  = {"Fato": "📊", "Dim": "📋", "dCal": "📅"}
    for i, (tname, tdf) in enumerate(tabelas.items()):
        icon = "📅" if tname.startswith("dCal") else ("📊" if tname.startswith("Fato") else "📋")
        with cols[i % n_cols]:
            st.markdown(f"""
            <div class="stat-card">
                <span class="stat-card-icon">{icon}</span>
                <span class="stat-number">{len(tdf):,}</span>
                <span class="stat-label">{tname}</span>
                <span class="stat-sublabel">{len(tdf.columns)} colunas</span>
            </div>
            """, unsafe_allow_html=True)

    # ── preview ───────────────────────────────────────────────────────────────
    st.markdown('<h3 class="section-header">Preview das tabelas</h3>', unsafe_allow_html=True)
    tabs = st.tabs(list(tabelas.keys()))
    for tab, (tname, tdf) in zip(tabs, tabelas.items()):
        with tab:
            st.dataframe(tdf.head(20), use_container_width=True)
            st.caption(f"{len(tdf):,} linhas · {len(tdf.columns)} colunas")

    # ── download ──────────────────────────────────────────────────────────────
    st.markdown('<h3 class="section-header">Download</h3>', unsafe_allow_html=True)
    zip_bytes    = to_zip(tabelas)
    nome_arquivo = f"Base_BI_{nome.replace(' ','_')}.zip"
    st.download_button(
        label=f"Baixar {nome_arquivo}",
        data=zip_bytes,
        file_name=nome_arquivo,
        mime="application/zip",
        use_container_width=True,
        type="primary",
    )

    st.markdown("""
    <div class="info-box">
        <strong>Dica Power BI:</strong> Importe os CSVs e crie relações usando as colunas
        <code>id_*</code> (FK) da tabela Fato para as respectivas dimensões.
        Conecte <code>dCalendario[Data]</code> ao campo de data da tabela Fato.
    </div>
    """, unsafe_allow_html=True)

else:
    # ── estado inicial ────────────────────────────────────────────────────────
    st.markdown('<h3 class="section-header">Como usar</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="steps-grid">
        <div class="step-card">
            <span class="step-num">01</span>
            <span class="step-icon">🏭</span>
            <div class="step-title">Escolha o setor</div>
            <div class="step-text">Selecione entre 10 setores com dados contextualmente corretos</div>
        </div>
        <div class="step-card">
            <span class="step-num">02</span>
            <span class="step-icon">📅</span>
            <div class="step-title">Defina o período</div>
            <div class="step-text">Configure as datas — a dCalendario é gerada automaticamente</div>
        </div>
        <div class="step-card">
            <span class="step-num">03</span>
            <span class="step-icon">🚀</span>
            <div class="step-title">Clique em Gerar</div>
            <div class="step-text">A base completa é gerada em segundos com relações íntegras</div>
        </div>
        <div class="step-card">
            <span class="step-num">04</span>
            <span class="step-icon">📦</span>
            <div class="step-title">Baixe o .zip</div>
            <div class="step-text">CSVs prontos para importar no Power BI, Tableau ou Python</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">Setores disponíveis</h3>', unsafe_allow_html=True)
    setores_info = [
        ("🛒", "Varejo"),     ("💰", "Financeiro"), ("🏥", "Saúde"),
        ("💻", "Tecnologia"), ("📚", "Educação"),   ("🚚", "Logística"),
        ("⚡", "Energia"),     ("📡", "Telecom"),    ("🏭", "Indústria"),
        ("🌾", "Agronegócio"),
    ]
    st.markdown('<div class="sector-grid">' + "".join([
        f'<div class="sector-card"><span class="sector-card-icon">{ico}</span>'
        f'<div class="sector-card-name">{nome}</div></div>'
        for ico, nome in setores_info
    ]) + '</div>', unsafe_allow_html=True)

    st.markdown('<h3 class="section-header">Estrutura Star Schema</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
        Cada base inclui <strong>Tabela Fato</strong> com chaves estrangeiras (<code>id_*</code>) e métricas,
        <strong>Tabelas Dimensão</strong> com chaves primárias e atributos descritivos, e
        <strong>dCalendario</strong> com Data, Ano, Mês, MesAno e IdMesAno — compatível com Power Query.
        Tudo exportado em CSVs compactados em um único <code>.zip</code>.
    </div>
    """, unsafe_allow_html=True)

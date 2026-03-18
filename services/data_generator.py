import pandas as pd
import numpy as np
from faker import Faker
from datetime import date, timedelta
import random

fake = Faker("pt_BR")

# ══════════════════════════════════════
#  dCALENDARIO
# ══════════════════════════════════════

def gerar_dcalendario(data_inicio: date, data_fim: date) -> pd.DataFrame:
    datas = pd.date_range(start=data_inicio, end=data_fim, freq="D")
    df = pd.DataFrame({"Data": datas})
    df["Ano"] = df["Data"].dt.year.astype("int64")
    df["Mês"] = df["Data"].dt.month.astype("int64")
    meses_pt = {
        1: "Jan", 2: "Fev", 3: "Mar", 4: "Abr",
        5: "Mai", 6: "Jun", 7: "Jul", 8: "Ago",
        9: "Set", 10: "Out", 11: "Nov", 12: "Dez",
    }
    df["MesAno"] = df["Mês"].map(meses_pt) + "/" + df["Ano"].astype(str).str[-2:]
    df["IdMesAno"] = (df["Ano"] * 100 + df["Mês"]).astype("int64")
    df["Data"] = df["Data"].dt.date
    return df


# ══════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════

def _datas_aleatorias(data_inicio: date, data_fim: date, n: int):
    delta = (data_fim - data_inicio).days
    return [data_inicio + timedelta(days=random.randint(0, delta)) for _ in range(n)]


# ══════════════════════════════════════
#  SETORES
# ══════════════════════════════════════

# ── 1. VAREJO ──────────────────────────
def _gerar_varejo(n: int, data_inicio: date, data_fim: date):
    # DimCliente
    clientes = pd.DataFrame({
        "id_cliente": range(1, n + 1),
        "nome": [fake.name() for _ in range(n)],
        "cpf": [fake.cpf() for _ in range(n)],
        "email": [fake.email() for _ in range(n)],
        "segmento": random.choices(["Pessoa Física", "Pessoa Jurídica", "Premium"], k=n),
        "cidade": [fake.city() for _ in range(n)],
        "estado": [fake.state_abbr() for _ in range(n)],
    })

    # DimProduto
    categorias = ["Eletrônicos", "Vestuário", "Alimentos", "Móveis", "Esportes", "Beleza"]
    np_ = min(500, n)
    produtos = pd.DataFrame({
        "id_produto": range(1, np_ + 1),
        "nome": [f"Produto {fake.word().capitalize()} {i}" for i in range(1, np_ + 1)],
        "sku": [fake.bothify("SKU-####-??").upper() for _ in range(np_)],
        "categoria": random.choices(categorias, k=np_),
        "preco_unitario": np.round(np.random.uniform(10, 2000, np_), 2),
    })

    # DimVendedor
    nv = min(50, n)
    vendedores = pd.DataFrame({
        "id_vendedor": range(1, nv + 1),
        "nome": [fake.name() for _ in range(nv)],
        "regiao": random.choices(["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"], k=nv),
        "meta_mensal": np.round(np.random.uniform(20000, 100000, nv), 2),
    })

    # DimFilial
    nf = min(10, n)
    filiais = pd.DataFrame({
        "id_filial": range(1, nf + 1),
        "nome": [f"Filial {fake.city()}" for _ in range(nf)],
        "uf": [fake.state_abbr() for _ in range(nf)],
        "tipo": random.choices(["Loja Física", "E-commerce", "Quiosque"], k=nf),
    })

    # DimGeografia
    estados = ["AC","AL","AM","AP","BA","CE","DF","ES","GO","MA","MG","MS","MT",
               "PA","PB","PE","PI","PR","RJ","RN","RO","RR","RS","SC","SE","SP","TO"]
    geo = pd.DataFrame({
        "id_geo": range(1, len(estados) + 1),
        "estado": estados,
        "regiao": ["Norte","Nordeste","Norte","Norte","Nordeste","Nordeste","Centro-Oeste",
                   "Sudeste","Centro-Oeste","Nordeste","Sudeste","Centro-Oeste","Centro-Oeste",
                   "Norte","Nordeste","Nordeste","Nordeste","Sul","Sudeste","Nordeste",
                   "Norte","Norte","Sul","Sul","Nordeste","Sudeste","Norte"],
    })

    # FatoVendas
    datas = _datas_aleatorias(data_inicio, data_fim, n)
    qtd = np.random.randint(1, 20, n)
    precos = produtos["preco_unitario"].sample(n, replace=True).values
    fato = pd.DataFrame({
        "id_venda": range(1, n + 1),
        "id_cliente": np.random.randint(1, n + 1, n),
        "id_produto": np.random.randint(1, np_ + 1, n),
        "id_vendedor": np.random.randint(1, nv + 1, n),
        "id_filial": np.random.randint(1, nf + 1, n),
        "id_data": datas,
        "quantidade": qtd,
        "preco_unitario": np.round(precos, 2),
        "desconto_pct": np.round(np.random.uniform(0, 0.3, n), 2),
        "valor_total": np.round(qtd * precos * (1 - np.random.uniform(0, 0.3, n)), 2),
    })

    return {
        "DimCliente": clientes, "DimProduto": produtos,
        "DimVendedor": vendedores, "DimFilial": filiais,
        "DimGeografia": geo, "FatoVendas": fato,
    }


# ── 2. FINANCEIRO ──────────────────────
def _gerar_financeiro(n: int, data_inicio: date, data_fim: date):
    nc = min(500, n)
    contas = pd.DataFrame({
        "id_conta": range(1, nc + 1),
        "titular": [fake.name() for _ in range(nc)],
        "cpf_cnpj": [fake.cpf() for _ in range(nc)],
        "tipo_conta": random.choices(["Corrente", "Poupança", "Investimento", "Salário"], k=nc),
        "saldo_inicial": np.round(np.random.uniform(0, 50000, nc), 2),
    })

    na = min(20, n)
    agencias = pd.DataFrame({
        "id_agencia": range(1, na + 1),
        "nome": [f"Agência {fake.city()}" for _ in range(na)],
        "codigo": [fake.numerify("####-#") for _ in range(na)],
        "uf": [fake.state_abbr() for _ in range(na)],
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    valores = np.round(np.random.uniform(10, 50000, n), 2)
    fato = pd.DataFrame({
        "id_transacao": range(1, n + 1),
        "id_conta": np.random.randint(1, nc + 1, n),
        "id_agencia": np.random.randint(1, na + 1, n),
        "id_data": datas,
        "tipo_transacao": random.choices(["Crédito", "Débito", "Transferência", "PIX", "TED"], k=n),
        "valor": valores,
        "canal": random.choices(["App", "Internet Banking", "Agência", "ATM"], k=n),
    })

    return {"DimConta": contas, "DimAgencia": agencias, "FatoTransacao": fato}


# ── 3. SAÚDE ───────────────────────────
def _gerar_saude(n: int, data_inicio: date, data_fim: date):
    np_ = min(500, n)
    pacientes = pd.DataFrame({
        "id_paciente": range(1, np_ + 1),
        "nome": [fake.name() for _ in range(np_)],
        "cpf": [fake.cpf() for _ in range(np_)],
        "data_nascimento": [fake.date_of_birth(minimum_age=0, maximum_age=95) for _ in range(np_)],
        "sexo": random.choices(["M", "F"], k=np_),
        "plano": random.choices(["Básico", "Intermediário", "Premium", "Particular"], k=np_),
    })

    nm = min(50, n)
    medicos = pd.DataFrame({
        "id_medico": range(1, nm + 1),
        "nome": [f"Dr(a). {fake.name()}" for _ in range(nm)],
        "crm": [fake.numerify("CRM-#####") for _ in range(nm)],
        "especialidade": random.choices(
            ["Clínica Geral", "Cardiologia", "Ortopedia", "Pediatria",
             "Ginecologia", "Neurologia", "Oncologia"], k=nm),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    fato = pd.DataFrame({
        "id_atendimento": range(1, n + 1),
        "id_paciente": np.random.randint(1, np_ + 1, n),
        "id_medico": np.random.randint(1, nm + 1, n),
        "id_data": datas,
        "tipo_atendimento": random.choices(["Consulta", "Exame", "Cirurgia", "Retorno", "Emergência"], k=n),
        "cid": [fake.bothify("?##.#").upper() for _ in range(n)],
        "valor_procedimento": np.round(np.random.uniform(50, 8000, n), 2),
        "duracao_min": np.random.randint(10, 240, n),
    })

    return {"DimPaciente": pacientes, "DimMedico": medicos, "FatoAtendimento": fato}


# ── 4. TECNOLOGIA ──────────────────────
def _gerar_tecnologia(n: int, data_inicio: date, data_fim: date):
    nc = min(300, n)
    clientes = pd.DataFrame({
        "id_cliente": range(1, nc + 1),
        "empresa": [fake.company() for _ in range(nc)],
        "cnpj": [fake.cnpj() for _ in range(nc)],
        "segmento": random.choices(["Startup", "PME", "Enterprise", "Governo"], k=nc),
        "uf": [fake.state_abbr() for _ in range(nc)],
    })

    np_ = min(50, n)
    produtos = pd.DataFrame({
        "id_produto": range(1, np_ + 1),
        "nome": [f"{fake.word().capitalize()} Suite" for _ in range(np_)],
        "tipo": random.choices(["SaaS", "Licença", "Suporte", "Consultoria", "Treinamento"], k=np_),
        "preco_mensal": np.round(np.random.uniform(99, 9999, np_), 2),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    fato = pd.DataFrame({
        "id_contrato": range(1, n + 1),
        "id_cliente": np.random.randint(1, nc + 1, n),
        "id_produto": np.random.randint(1, np_ + 1, n),
        "id_data": datas,
        "duracao_meses": np.random.randint(1, 36, n),
        "valor_total": np.round(np.random.uniform(500, 500000, n), 2),
        "status": random.choices(["Ativo", "Cancelado", "Suspenso", "Renovado"], k=n),
    })

    return {"DimCliente": clientes, "DimProduto": produtos, "FatoContrato": fato}


# ── 5. EDUCAÇÃO ────────────────────────
def _gerar_educacao(n: int, data_inicio: date, data_fim: date):
    na = min(500, n)
    alunos = pd.DataFrame({
        "id_aluno": range(1, na + 1),
        "nome": [fake.name() for _ in range(na)],
        "cpf": [fake.cpf() for _ in range(na)],
        "data_nascimento": [fake.date_of_birth(minimum_age=14, maximum_age=65) for _ in range(na)],
        "modalidade": random.choices(["Presencial", "EAD", "Híbrido"], k=na),
    })

    nc = min(100, n)
    cursos = pd.DataFrame({
        "id_curso": range(1, nc + 1),
        "nome": [f"Curso de {fake.job()}" for _ in range(nc)],
        "area": random.choices(["TI", "Saúde", "Negócios", "Engenharia", "Humanas", "Direito"], k=nc),
        "carga_horaria": np.random.randint(20, 2000, nc),
        "mensalidade": np.round(np.random.uniform(200, 3500, nc), 2),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    fato = pd.DataFrame({
        "id_matricula": range(1, n + 1),
        "id_aluno": np.random.randint(1, na + 1, n),
        "id_curso": np.random.randint(1, nc + 1, n),
        "id_data": datas,
        "status": random.choices(["Ativa", "Trancada", "Concluída", "Cancelada"], k=n),
        "nota_final": np.round(np.random.uniform(0, 10, n), 1),
        "valor_pago": np.round(np.random.uniform(200, 3500, n), 2),
    })

    return {"DimAluno": alunos, "DimCurso": cursos, "FatoMatricula": fato}


# ── 6. LOGÍSTICA ───────────────────────
def _gerar_logistica(n: int, data_inicio: date, data_fim: date):
    nt = min(30, n)
    transportadoras = pd.DataFrame({
        "id_transportadora": range(1, nt + 1),
        "nome": [fake.company() for _ in range(nt)],
        "cnpj": [fake.cnpj() for _ in range(nt)],
        "modal": random.choices(["Rodoviário", "Aéreo", "Ferroviário", "Marítimo"], k=nt),
    })

    nr = min(50, n)
    rotas = pd.DataFrame({
        "id_rota": range(1, nr + 1),
        "origem": [fake.city() for _ in range(nr)],
        "destino": [fake.city() for _ in range(nr)],
        "distancia_km": np.random.randint(50, 5000, nr),
        "prazo_dias": np.random.randint(1, 15, nr),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    fato = pd.DataFrame({
        "id_entrega": range(1, n + 1),
        "id_transportadora": np.random.randint(1, nt + 1, n),
        "id_rota": np.random.randint(1, nr + 1, n),
        "id_data": datas,
        "peso_kg": np.round(np.random.uniform(0.1, 1000, n), 2),
        "valor_frete": np.round(np.random.uniform(15, 5000, n), 2),
        "status": random.choices(["Entregue", "Em trânsito", "Atrasado", "Devolvido"], k=n),
        "prazo_cumprido": random.choices([True, False], weights=[75, 25], k=n),
    })

    return {"DimTransportadora": transportadoras, "DimRota": rotas, "FatoEntrega": fato}


# ── 7. ENERGIA ─────────────────────────
def _gerar_energia(n: int, data_inicio: date, data_fim: date):
    nc = min(500, n)
    consumidores = pd.DataFrame({
        "id_consumidor": range(1, nc + 1),
        "nome": [fake.name() for _ in range(nc)],
        "cpf_cnpj": [fake.cpf() for _ in range(nc)],
        "tipo": random.choices(["Residencial", "Comercial", "Industrial", "Rural"], k=nc),
        "cidade": [fake.city() for _ in range(nc)],
        "uf": [fake.state_abbr() for _ in range(nc)],
    })

    nm = min(500, n)
    medidores = pd.DataFrame({
        "id_medidor": range(1, nm + 1),
        "codigo": [fake.bothify("MED-########") for _ in range(nm)],
        "tensao": random.choices(["110V", "220V", "380V"], k=nm),
        "fase": random.choices(["Monofásico", "Bifásico", "Trifásico"], k=nm),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    kwh = np.round(np.random.uniform(50, 5000, n), 2)
    fato = pd.DataFrame({
        "id_consumo": range(1, n + 1),
        "id_consumidor": np.random.randint(1, nc + 1, n),
        "id_medidor": np.random.randint(1, nm + 1, n),
        "id_data": datas,
        "consumo_kwh": kwh,
        "tarifa_kwh": np.round(np.random.uniform(0.5, 1.2, n), 4),
        "valor_fatura": np.round(kwh * np.random.uniform(0.5, 1.2, n), 2),
    })

    return {"DimConsumidor": consumidores, "DimMedidor": medidores, "FatoConsumo": fato}


# ── 8. TELECOM ─────────────────────────
def _gerar_telecom(n: int, data_inicio: date, data_fim: date):
    na = min(500, n)
    assinantes = pd.DataFrame({
        "id_assinante": range(1, na + 1),
        "nome": [fake.name() for _ in range(na)],
        "cpf": [fake.cpf() for _ in range(na)],
        "telefone": [fake.phone_number() for _ in range(na)],
        "cidade": [fake.city() for _ in range(na)],
    })

    np_ = min(20, n)
    planos = pd.DataFrame({
        "id_plano": range(1, np_ + 1),
        "nome": [f"Plano {fake.word().capitalize()} {i}GB" for i in range(1, np_ + 1)],
        "tipo": random.choices(["Pré-pago", "Pós-pago", "Controle", "Corporativo"], k=np_),
        "franquia_gb": np.random.randint(1, 100, np_),
        "mensalidade": np.round(np.random.uniform(25, 300, np_), 2),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    fato = pd.DataFrame({
        "id_chamada": range(1, n + 1),
        "id_assinante": np.random.randint(1, na + 1, n),
        "id_plano": np.random.randint(1, np_ + 1, n),
        "id_data": datas,
        "tipo": random.choices(["Voz", "SMS", "Dados", "Internacional"], k=n),
        "duracao_seg": np.random.randint(5, 3600, n),
        "consumo_mb": np.round(np.random.uniform(0, 2000, n), 2),
        "valor_cobrado": np.round(np.random.uniform(0, 50, n), 2),
    })

    return {"DimAssinante": assinantes, "DimPlano": planos, "FatoChamada": fato}


# ── 9. INDÚSTRIA ───────────────────────
def _gerar_industria(n: int, data_inicio: date, data_fim: date):
    nm = min(30, n)
    maquinas = pd.DataFrame({
        "id_maquina": range(1, nm + 1),
        "nome": [f"Máquina {fake.bothify('M-###')}" for _ in range(nm)],
        "tipo": random.choices(["Prensa", "Torno", "Extrusora", "Injetora", "Solda"], k=nm),
        "capacidade_hora": np.random.randint(10, 500, nm),
        "linha": random.choices(["Linha A", "Linha B", "Linha C", "Linha D"], k=nm),
    })

    ni = min(100, n)
    insumos = pd.DataFrame({
        "id_insumo": range(1, ni + 1),
        "nome": [f"Insumo {fake.word().capitalize()}" for _ in range(ni)],
        "unidade": random.choices(["kg", "litro", "unidade", "metro", "tonelada"], k=ni),
        "custo_unitario": np.round(np.random.uniform(1, 500, ni), 2),
        "fornecedor": [fake.company() for _ in range(ni)],
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    qtd = np.random.randint(10, 10000, n)
    fato = pd.DataFrame({
        "id_producao": range(1, n + 1),
        "id_maquina": np.random.randint(1, nm + 1, n),
        "id_insumo": np.random.randint(1, ni + 1, n),
        "id_data": datas,
        "quantidade_produzida": qtd,
        "refugo_pct": np.round(np.random.uniform(0, 0.15, n), 4),
        "horas_trabalhadas": np.round(np.random.uniform(1, 24, n), 2),
        "custo_total": np.round(qtd * np.random.uniform(1, 500, n), 2),
    })

    return {"DimMaquina": maquinas, "DimInsumo": insumos, "FatoProducao": fato}


# ── 10. AGRONEGÓCIO ────────────────────
def _gerar_agronegocio(n: int, data_inicio: date, data_fim: date):
    np_ = min(100, n)
    propriedades = pd.DataFrame({
        "id_propriedade": range(1, np_ + 1),
        "nome": [f"Fazenda {fake.last_name()}" for _ in range(np_)],
        "proprietario": [fake.name() for _ in range(np_)],
        "municipio": [fake.city() for _ in range(np_)],
        "uf": [fake.state_abbr() for _ in range(np_)],
        "area_hectares": np.round(np.random.uniform(10, 50000, np_), 2),
    })

    nc = min(20, n)
    culturas = pd.DataFrame({
        "id_cultura": range(1, nc + 1),
        "nome": random.choices(
            ["Soja", "Milho", "Cana-de-açúcar", "Café", "Algodão",
             "Arroz", "Feijão", "Trigo", "Laranja", "Eucalipto"], k=nc),
        "ciclo_dias": np.random.randint(60, 365, nc),
        "preco_tonelada": np.round(np.random.uniform(500, 8000, nc), 2),
    })

    datas = _datas_aleatorias(data_inicio, data_fim, n)
    prod = np.round(np.random.uniform(1, 10000, n), 2)
    fato = pd.DataFrame({
        "id_safra": range(1, n + 1),
        "id_propriedade": np.random.randint(1, np_ + 1, n),
        "id_cultura": np.random.randint(1, nc + 1, n),
        "id_data": datas,
        "producao_toneladas": prod,
        "area_plantada_ha": np.round(np.random.uniform(1, 5000, n), 2),
        "custo_producao": np.round(np.random.uniform(500, 2000000, n), 2),
        "receita_total": np.round(prod * np.random.uniform(500, 8000, n), 2),
    })

    return {"DimPropriedade": propriedades, "DimCultura": culturas, "FatoSafra": fato}


# ══════════════════════════════════════
#  DISPATCHER PRINCIPAL
# ══════════════════════════════════════

SETORES = {
    "Varejo":       _gerar_varejo,
    "Financeiro":   _gerar_financeiro,
    "Saúde":        _gerar_saude,
    "Tecnologia":   _gerar_tecnologia,
    "Educação":     _gerar_educacao,
    "Logística":    _gerar_logistica,
    "Energia":      _gerar_energia,
    "Telecom":      _gerar_telecom,
    "Indústria":    _gerar_industria,
    "Agronegócio":  _gerar_agronegocio,
}


def gerar_base_completa(
    setor: str,
    n_linhas: int = 1000,
    data_inicio: date = date(2023, 1, 1),
    data_fim: date = date(2023, 12, 31),
) -> dict:
    """
    Retorna um dict com todos os DataFrames do setor escolhido
    mais a dCalendario. Chaves = nomes das tabelas (str).

    Exemplo:
        tabelas = gerar_base_completa("Varejo", n_linhas=5000)
        tabelas["FatoVendas"]    # pd.DataFrame
        tabelas["dCalendario"]   # pd.DataFrame
    """
    if setor not in SETORES:
        raise ValueError(f"Setor '{setor}' não encontrado. Disponíveis: {list(SETORES.keys())}")

    tabelas = SETORES[setor](n_linhas, data_inicio, data_fim)
    tabelas["dCalendario"] = gerar_dcalendario(data_inicio, data_fim)
    return tabelas

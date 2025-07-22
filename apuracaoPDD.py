import pandas as pd
from datetime import datetime

filePath = "C:\\Users\\barbara_furquim\\Downloads\\PDD_Fiscal_2025.xlsx"
# Carregar os dados das planilhas
historico_df = pd.read_excel(filePath, sheet_name="Historico_CCBs_Anteriores", engine="openpyxl")
junho_df = pd.read_excel(filePath, sheet_name="Saldos_Negativos_Junho_2025", engine="openpyxl")

# Agrupar os saldos negativos de junho por cliente
saldos_junho = junho_df.set_index("ID_Cliente")["Saldo_Negativo_Junho_2025"].to_dict()

# Adicionar coluna de saldo de junho por cliente
historico_df["Saldo_Negativo_Junho_2025"] = historico_df["ID_Cliente"].map(saldos_junho)

# Etapa 1 e 2: Identificar novas CCBs e quitações
historico_df["Nova_CCB"] = historico_df["Saldo_Negativo_Junho_2025"] < historico_df["Valor_Saldo_Restante_CCB_Maio_2025"]
historico_df["Quitacao"] = historico_df["Saldo_Negativo_Junho_2025"] > historico_df["Valor_Saldo_Restante_CCB_Maio_2025"]

# Etapa 3: Atualizar saldos e calcular dias de atraso com base em 30/06/2025
base_date = datetime(2025, 6, 30)
historico_df["Data_Constituicao_CCB"] = pd.to_datetime(historico_df["Data_Constituicao_CCB"])
historico_df["Dias_Atraso_Junho_2025"] = (base_date - historico_df["Data_Constituicao_CCB"]).dt.days

# Atualizar saldo restante com base no saldo de junho
historico_df["Valor_Saldo_Restante_CCB_Junho_2025"] = historico_df["Saldo_Negativo_Junho_2025"]

# Etapa 4: Aplicar regras fiscais para dedutibilidade
def verificar_dedutibilidade(valor, dias):
    valor_abs = abs(valor)
    if valor_abs <= 15000 and dias > 180:
        return "Dedutível"
    elif 15000 < valor_abs <= 100000 and dias > 365:
        return "Dedutível"
    elif valor_abs > 100000:
        return "Não dedutível"
    return "Não dedutível"

historico_df["PDD_Fiscal"] = historico_df.apply(
    lambda row: verificar_dedutibilidade(row["Valor_Saldo_Restante_CCB_Junho_2025"], row["Dias_Atraso_Junho_2025"]),
    axis=1
)

# Criar planilha de saldos atualizados
saldos_atualizados = historico_df[[
    "ID_Cliente", "ID_CCB", "Data_Constituicao_CCB", "Valor_Original_CCB",
    "Valor_Saldo_Restante_CCB_Maio_2025", "Dias_Atraso_Maio_2025",
    "Valor_Saldo_Restante_CCB_Junho_2025", "Dias_Atraso_Junho_2025", "PDD_Fiscal"
]]

# Etapa 5: Criar planilha de resumo
total_ccbs_ativas = saldos_atualizados.shape[0]
total_dedutivel = saldos_atualizados[saldos_atualizados["PDD_Fiscal"] == "Dedutível"]["Valor_Saldo_Restante_CCB_Junho_2025"].sum()
total_nao_dedutivel = saldos_atualizados[saldos_atualizados["PDD_Fiscal"] == "Não dedutível"]["Valor_Saldo_Restante_CCB_Junho_2025"].sum()

resumo_df = pd.DataFrame({
    "Descrição": [
        "Total de CCBs ativas em Junho/2025",
        "Valor total de PDD Fiscal dedutível",
        "Valor total de PDD Fiscal não dedutível"
    ],
    "Valor": [total_ccbs_ativas, total_dedutivel, total_nao_dedutivel]
})

newFilePath = "C:\\Users\\barbara_furquim\\Downloads\\simulacao_PDD_Fiscal_2025.xlsx"
# Salvar em novo arquivo Excel
with pd.ExcelWriter(newFilePath, engine="openpyxl") as writer:
    historico_df.to_excel(writer, sheet_name="Historico_CCBs_Anteriores", index=False)
    junho_df.to_excel(writer, sheet_name="Saldos_Negativos_Junho_2025", index=False)
    saldos_atualizados.to_excel(writer, sheet_name="saldos_atualizados", index=False)
    resumo_df.to_excel(writer, sheet_name="resumo", index=False)

print("Arquivo 'simulacao_PDD_Fiscal_2025.xlsx' criado com sucesso.")

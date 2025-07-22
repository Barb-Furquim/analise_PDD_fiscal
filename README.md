# 📊 Apuração e Análise de PDD Fiscal

Este projeto em Python automatiza o processamento de dados financeiros de CCBs (Cédulas de Crédito Bancário), atualizando saldos, calculando atrasos e aplicando regras fiscais de dedutibilidade com base em informações de duas planilhas.

## 📁 Estrutura do Projeto

- `PDD_Fiscal_2025.xlsx`: Arquivo original com duas planilhas:
  - `Historico_CCBs_Anteriores`: Dados históricos das CCBs até maio/2025.
  - `Saldos_Negativos_Junho_2025`: Saldos negativos atualizados por cliente em junho/2025.
- `simulacao_PDD_Fiscal_2025.xlsx`: Arquivo gerado com:
  - `saldos_atualizados`: Dados atualizados com dedutibilidade fiscal.
  - `resumo`: Indicadores consolidados.

## ⚙️ Funcionalidades do Script

1. **📥 Importação de Dados**  
   Lê os dados das planilhas originais usando `pandas`.

2. **🔍 Identificação de Novas CCBs e Quitações**  
   - **Nova CCB**: Quando o saldo negativo de junho é maior que o de maio.
   - **Quitação**: Quando o saldo de junho é menor que o de maio.

3. **📆 Cálculo de Dias de Atraso**  
   Calcula os dias de atraso com base na data de constituição da CCB até 30/06/2025.

4. **💰 Atualização de Saldos**  
   Atualiza os saldos restantes com os valores de junho.

5. **📑 Aplicação das Regras Fiscais**  
   Define a dedutibilidade fiscal com base nas regras:
   - Até R$ 15.000: Dedutível se atraso > 180 dias.
   - De R$ 15.000,01 a R$ 100.000: Dedutível se atraso > 365 dias.
   - Acima de R$ 100.000: Não dedutível (exceto com processo judicial, não considerado aqui).

6. **📈 Geração de Relatórios**  
   - Planilha `saldos_atualizados` com todos os dados processados.
   - Planilha `resumo` com:
     - Total de CCBs ativas em junho/2025.
     - Valor total de PDD Fiscal dedutível.
     - Valor total de PDD Fiscal não dedutível.

## 🧪 Tecnologias Utilizadas

- Python 🐍
- Pandas 📊
- OpenPyXL 📄

## 🚀 Como Executar

1. Instale as dependências:
   ```bash
   pip install pandas
   ```
   ```bash
   pip installopenpyxl
   ```

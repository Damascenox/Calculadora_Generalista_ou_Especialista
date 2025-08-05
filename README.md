# 🧠 Sistema de Classificação 

O modelo funciona como um **juiz de perfil** que distribui **pontos** em duas “contas” — Especialista e Generalista — com base em **6 blocos de regras**.  
No final:

* Quem tiver mais pontos como **Especialista** → **Especialista**  
* Quem tiver mais pontos como **Generalista** → **Generalista**  
* Se a disputa for muito apertada → **Ambíguo**

---

## Os 6 Critérios Avaliados

### Função/Área de Atuação  
**Peso: alto (até 3 pts)**

| Função declarada        | Pontos | Lado         |
|-------------------------|--------|--------------|
| Engenharia de Dados     | +2     | Especialista |
| Ciência de Dados        | +2     | Especialista |
| Análise de Dados        | +3     | Generalista  |
| BI                      | +3     | Generalista  |

---

### Cargo Atual (busca por palavras-chave)  
**Peso: médio-alto (até 2,5 pts)**

| Palavras-chave no cargo                                    | Pontos | Lado         |
|------------------------------------------------------------|--------|--------------|
| cientista de dados / data scientist / engenheiro(a) dados … | +1,5   | Especialista |
| professor / pesquisador                                   | +2     | Especialista |
| analista de dados / data analyst / BI / business analyst … | +2,5   | Generalista  |
| product manager / gestor …                                | +2,5   | Generalista  |

> ⚠️ Só a **primeira** palavra-chave encontrada vale pontos.

---

### Quantidade de Atividades Diárias  
**Peso: médio (até 2,5 pts + penalidade)**

| Atividades marcadas | Generalista | Especialista |
|---------------------|-------------|--------------|
| 6 ou +              | +2,5        | **–1**       |
| 4 ou 5              | +1,5        | 0            |
| 2 ou –              | 0           | +1           |

---

### Área de Formação (busca por palavras-chave)  
**Peso: médio (até 2 pts)**

| Área de formação                           | Pontos | Lado         |
|--------------------------------------------|--------|--------------|
| Computação, Engenharia, Estatística, Matemática … | +1,5–2 | Especialista |
| Administração, Economia, Negócios, Marketing …   | +1,5–2 | Generalista  |
| Ciências da Saúde / biológicas              | +0,5   | Ambos (meio) |

---

### Nível de Escolaridade  
**Peso: baixo-médio (até 2 pts)**

| Nível de ensino           | Pontos | Lado         |
|---------------------------|--------|--------------|
| Doutorado / PhD           | +2     | Especialista |
| Mestrado                  | +1,5   | Especialista |
| Pós-graduação lato sensu  | +0,5   | Especialista |
| Estudante de graduação    | +0,5   | Generalista  |

---

### Atuação Específica em Dados  
**Peso: alto (até 2,5 pts)**

| Atuação declarada        | Pontos | Lado         |
|--------------------------|--------|--------------|
| Engenharia de Dados      | +2     | Especialista |
| Ciência de Dados         | +2     | Especialista |
| Análise de Dados         | +2,5   | Generalista  |
| Gestor                   | +2,5   | Generalista  |

---

## Como a Decisão é Tomada

1. Soma tudo:  
   - `pontos_especialista`  
   - `pontos_generalista`

2. Calcula:  
   - **diferença** = |Esp – Gen|  
   - **total**     = Esp + Gen

3. Escolhe a classe de confiança:

| Confiança | Condições                              |
|-----------|----------------------------------------|
| **Alta**  | diferença ≥ 4 **e** total ≥ 4          |
| **Média** | diferença ≥ 2,5 **e** total ≥ 3        |
| **Baixa** | diferença ≥ 1,5 **e** total ≥ 1,5      |
| **Ambíguo**| qualquer outro caso                   |

---

## Exemplos Práticos

### João – Data Engineer Sênior
- Função: Engenharia de Dados → +2 Esp  
- Cargo: Data Engineer → +1,5 Esp  
- Atividades: 2 → +1 Esp  
- Formação: Engenharia → +1,5 Esp  
- Nível: Mestrado → +1,5 Esp  
- Atuação: Engenharia de Dados → +2 Esp  
**Total: Esp = 9,5 | Gen = 0 → Especialista Alta Confiança**

---

### Maria – Analista de BI Pleno
- Função: BI → +3 Gen  
- Cargo: Analista BI → +2,5 Gen  
- Atividades: 6 → +2,5 Gen / –1 Esp  
- Formação: Administração → +2 Gen  
- Nível: Pós → 0  
- Atuação: Análise de Dados → +2,5 Gen  
**Total: Esp = –1 | Gen = 12,5 → Generalista Alta Confiança**

---

### Carlos – Pleno com Perfil Misto
- Função: Análise de Dados → +3 Gen  
- Cargo: Analytics Engineer → +1,5 Esp  
- Atividades: 4 → +1,5 Gen  
- Formação: Sistemas de Informação → +1,5 Esp  
- Nível: Graduação → 0  
- Atuação: Análise de Dados → +2,5 Gen  
**Total: Esp = 3 | Gen = 7 → Generalista Média Confiança**

---

Pronto! O modelo agora avalia cada pessoa nesses seis blocos, soma os dois lados e devolve uma categoria com nível de confiança — ou “Ambíguo” quando a disputa é acirrada demais.
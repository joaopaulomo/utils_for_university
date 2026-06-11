"""
grade_generator.py
Gera grades horárias em HTML para o site UFBA/IGEO no GitHub Pages.
Coloca os arquivos em grades/ (mesma pasta do index.html).
"""

from datetime import datetime, timedelta
from pathlib import Path

COR_FUNDO = "#FFFFFF"
COR_TEXTO = "#000000"
COR_BLOCO = "#F4A316"
COR_LINHA = "#E0E0E0"
COR_CABECALHO = "#F5F5F5"
COR_COL_HORA = "#FAFAFA"


def calcular_horario_fim(horario_inicio_str):
    formato = "%H:%M"
    inicio = datetime.strptime(horario_inicio_str, formato)
    fim = inicio + timedelta(minutes=55)
    return fim.strftime(formato)


def gerar_html_grade(dados_aulas, semestre, horarios_ref, dias_ref, pasta_saida="grades"):
    grade_matrix = {h: {d: None for d in dias_ref} for h in horarios_ref}

    for aula in dados_aulas:
        codigo = aula[0]
        nome = aula[1]
        dia_semana = aula[2]
        horario_inicio = aula[4]
        conteudo_celula = f"{codigo}<br><span style='font-size:0.85em; font-weight:normal'>{nome}</span>"
        if horario_inicio in grade_matrix and dia_semana in grade_matrix[horario_inicio]:
            grade_matrix[horario_inicio][dia_semana] = conteudo_celula

    html = f"""<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Grade {semestre}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: {COR_FUNDO};
      color: {COR_TEXTO};
      font-family: 'Space Grotesk', sans-serif;
      padding: 32px 24px;
    }}
    h1 {{
      text-align: center;
      font-size: 22px;
      font-weight: 600;
      margin-bottom: 4px;
      color: #111;
    }}
    .sub {{
      text-align: center;
      font-size: 13px;
      color: #888;
      margin-bottom: 28px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    th, td {{
      border: 1px solid {COR_LINHA};
      padding: 8px 6px;
      text-align: center;
    }}
    th {{
      background: {COR_CABECALHO};
      font-weight: 600;
      font-size: 11px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: #555;
    }}
    .horario-col {{
      font-weight: 600;
      background: {COR_COL_HORA};
      color: #666;
      font-size: 12px;
      white-space: nowrap;
      width: 80px;
    }}
    .aula-box {{
      background: {COR_BLOCO};
      color: #2a1600;
      font-weight: 600;
      border-radius: 5px;
      padding: 8px 6px;
      font-size: 12px;
      line-height: 1.4;
    }}
    .vazio {{ color: #ddd; font-size: 11px; }}
    footer {{
      margin-top: 24px;
      text-align: center;
      font-size: 11px;
      color: #bbb;
    }}
    a.back {{
      display: inline-block;
      margin-bottom: 20px;
      font-size: 12px;
      color: #888;
      text-decoration: none;
    }}
    a.back:hover {{ color: #444; }}
  </style>
</head>
<body>
  <a class="back" href="../index.html">← Voltar ao site</a>
  <h1>Grade Horária</h1>
  <p class="sub">Semestre {semestre}</p>
  <table>
    <thead>
      <tr>
        <th>Horário</th>
        {''.join([f'<th>{d[:3]}</th>' for d in dias_ref])}
      </tr>
    </thead>
    <tbody>
"""

    for h_inicio in horarios_ref:
        h_fim = calcular_horario_fim(h_inicio)
        linha = f"<tr><td class='horario-col'>{h_inicio}<br><span style='font-size:10px;color:#aaa'>{h_fim}</span></td>"
        for dia in dias_ref:
            conteudo = grade_matrix[h_inicio][dia]
            if conteudo:
                linha += f"<td><div class='aula-box'>{conteudo}</div></td>"
            else:
                linha += "<td class='vazio'>·</td>"
        linha += "</tr>"
        html += linha

    html += f"""
    </tbody>
  </table>
  <footer>Gerado automaticamente · UFBA/IGEO · {semestre}</footer>
</body>
</html>"""

    pasta = Path(pasta_saida)
    pasta.mkdir(exist_ok=True)
    nome_arquivo = pasta / f"grade_visual_{semestre}.html"
    nome_arquivo.write_text(html, encoding="utf-8")
    return nome_arquivo


def main():
    horarios_disponiveis = [
        "07:00", "07:55", "08:50", "09:45", "10:40", "11:35",
        "12:30", "13:00", "13:55", "14:50", "15:45", "16:40",
        "17:35", "18:30",
    ]
    dias_semana = [
        "Segunda-feira", "Terça-feira", "Quarta-feira",
        "Quinta-feira", "Sexta-feira", "Sábado",
    ]

    dados_coletados = []

    print("=" * 50)
    print("GERADOR DE GRADE VISUAL — UFBA/IGEO")
    print("=" * 50)

    semestre = input("Semestre atual (ex: 2025.1): ").strip()
    semestre_safe = semestre.replace("/", "-").replace("\\", "-")
    if not semestre_safe:
        semestre_safe = "indefinido"

    while True:
        print("\n" + "─" * 30)
        print("NOVA MATÉRIA")
        print("─" * 30)

        codigo = input("Código (ou 'sair'): ").strip()
        if codigo.lower() == "sair":
            break

        nome = input("Nome da Matéria: ").strip()

        print("\n─ Horários ─")
        for i, h in enumerate(horarios_disponiveis):
            print(f"[{i+1:02d}] {h}")

        try:
            escolha_inicio = int(input("Início (número): "))
            qtd_aulas = int(input("Qtd de aulas seguidas: "))
        except ValueError:
            print("❌ Entrada inválida.")
            continue

        idx_inicio = escolha_inicio - 1
        if idx_inicio < 0 or (idx_inicio + qtd_aulas) > len(horarios_disponiveis):
            print("❌ Horário inválido.")
            continue

        fim_bloco = calcular_horario_fim(horarios_disponiveis[idx_inicio + qtd_aulas - 1])
        print(f"⏰ {horarios_disponiveis[idx_inicio]} → {fim_bloco}")

        print("\n─ Dias ─")
        for i, dia in enumerate(dias_semana):
            print(f"[{i+1}] {dia}")

        entrada_dias = input("Dias (ex: 1,3): ").strip()
        try:
            indices_dias = [int(x.strip()) for x in entrada_dias.split(",") if x.strip().isdigit()]
        except:
            continue

        for idx_dia in indices_dias:
            if 1 <= idx_dia <= 6:
                dia_nome = dias_semana[idx_dia - 1]
                for i in range(qtd_aulas):
                    h_atual = horarios_disponiveis[idx_inicio + i]
                    h_fim = calcular_horario_fim(h_atual)
                    dados_coletados.append([
                        codigo.upper(), nome, dia_nome,
                        f"{i+1}/{qtd_aulas}", h_atual, h_fim,
                    ])
                print(f"✅ {dia_nome}")

    if dados_coletados:
        arquivo = gerar_html_grade(dados_coletados, semestre_safe, horarios_disponiveis, dias_semana)
        print("\n" + "=" * 50)
        print(f"✅ HTML salvo em: {arquivo}")
        print()
        print("📋 Adicione ao index.html em SEMESTRES:")
        print(f'   {{ id: "{semestre_safe}", label: "{semestre}", arquivo: "grades/grade_visual_{semestre_safe}.html" }},')
        print("=" * 50)
    else:
        print("\nNenhum dado registrado.")


if __name__ == "__main__":
    main()

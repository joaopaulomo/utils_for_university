from datetime import datetime, timedelta

COR_FUNDO = "#FFFFFF"
COR_TEXTO = "#000000"
COR_BLOCO = "#FFA500"
COR_LINHA = "#CCCCCC"
COR_CABECALHO = "#EFEFEF"
COR_COL_HORA = "#F8F8F8"


def calcular_horario_fim(horario_inicio_str):
    formato = "%H:%M"
    inicio = datetime.strptime(horario_inicio_str, formato)
    fim = inicio + timedelta(minutes=55)
    return fim.strftime(formato)


def gerar_html_grade(dados_aulas, semestre, horarios_ref, dias_ref):
    grade_matrix = {h: {d: None for d in dias_ref} for h in horarios_ref}

    for aula in dados_aulas:
        codigo = aula[0]
        nome = aula[1]
        dia_semana = aula[2]
        horario_inicio = aula[4]

        conteudo_celula = f"{codigo}<br><span style='font-size:0.9em; font-weight:normal'>{nome}</span>"

        if (
            horario_inicio in grade_matrix
            and dia_semana in grade_matrix[horario_inicio]
        ):
            grade_matrix[horario_inicio][dia_semana] = conteudo_celula

    html = f"""
    <!DOCTYPE html>
    <html lang="pt-br">
    <head>
        <meta charset="UTF-8">
        <title>Grade Horária {semestre}</title>
        <style>
            body {{
                background-color: {COR_FUNDO};
                color: {COR_TEXTO};
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 20px;
            }}
            h1 {{ text-align: center; margin-bottom: 10px; }}
            h3 {{ text-align: center; color: #555; margin-top: 0; }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            th, td {{
                border: 1px solid {COR_LINHA};
                padding: 8px;
                text-align: center;
                width: 14%;
            }}
            th {{
                background-color: {COR_CABECALHO};
                color: #333;
                font-weight: bold;
                text-transform: uppercase;
                font-size: 0.9em;
            }}
            .horario-col {{
                font-weight: bold;
                background-color: {COR_COL_HORA};
                color: #444;
                font-size: 0.9em;
            }}
            .aula-box {{
                background-color: {COR_BLOCO};
                color: black;
                font-weight: bold;
                border-radius: 4px;
                padding: 10px;
                font-size: 0.95em;
                border: 1px solid #e69500;
            }}
            .vazio {{ color: #ccc; }}
        </style>
    </head>
    <body>
        <h1>Grade Horária</h1>
        <h3>Semestre: {semestre}</h3>
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
        linha_html = f"<tr><td class='horario-col'>{h_inicio} <br><span style='font-size:0.8em; color:#777'>{h_fim}</span></td>"

        for dia in dias_ref:
            conteudo = grade_matrix[h_inicio][dia]
            if conteudo:
                linha_html += f"<td><div class='aula-box'>{conteudo}</div></td>"
            else:
                linha_html += "<td class='vazio'>-</td>"

        linha_html += "</tr>"
        html += linha_html

    html += """
            </tbody>
        </table>
        <br>
        <p style="text-align:center; color: #999; font-size: 0.8em;">Gerado automaticamente via Python - UFBA/IGEO</p>
    </body>
    </html>
    """

    nome_arquivo_html = f"grade_visual_{semestre}.html"
    with open(nome_arquivo_html, "w", encoding="utf-8") as f:
        f.write(html)

    return nome_arquivo_html


def main():
    horarios_disponiveis = [
        "07:00",
        "07:55",
        "08:50",
        "09:45",
        "10:40",
        "11:35",
        "13:00",
        "13:55",
        "14:50",
        "15:45",
        "16:40",
        "17:35",
        "18:30",
    ]

    dias_semana = [
        "Segunda-feira",
        "Terça-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sábado",
    ]

    dados_coletados = []

    print("=" * 50)
    print("GERADOR DE GRADE VISUAL - UFBA (IGEO)")
    print("=" * 50)

    semestre = input("Qual o semestre atual? (ex: 2025.1): ").strip()
    semestre_safe = semestre.replace("/", "-").replace("\\", "-")
    if not semestre_safe:
        semestre_safe = "indefinido"

    while True:
        print("\n" + "-" * 30)
        print("NOVA MATÉRIA")
        print("-" * 30)

        codigo = input("Digite o Código (ou 'sair'): ").strip()
        if codigo.lower() == "sair":
            break

        nome = input("Digite o Nome da Matéria: ").strip()

        print("\n--- Horários ---")
        for i, h in enumerate(horarios_disponiveis):
            print(f"[{i+1:02d}] {h}")

        try:
            escolha_inicio = int(input("Início (número): "))
            qtd_aulas = int(input("Qtd de aulas seguidas: "))
        except ValueError:
            continue

        idx_inicio = escolha_inicio - 1
        if idx_inicio < 0 or (idx_inicio + qtd_aulas) > len(horarios_disponiveis):
            print("❌ Erro: Horário inválido.")
            continue

        fim_bloco = calcular_horario_fim(
            horarios_disponiveis[idx_inicio + qtd_aulas - 1]
        )
        print(
            f"⏰ Horário definido: {horarios_disponiveis[idx_inicio]} até {fim_bloco}"
        )

        print("\n--- Dias ---")
        for i, dia in enumerate(dias_semana):
            print(f"[{i+1}] {dia}")

        entrada_dias = input("Dias (ex: 1,3): ").strip()

        try:
            indices_dias = [
                int(x.strip()) for x in entrada_dias.split(",") if x.strip().isdigit()
            ]
        except:
            continue

        for idx_dia in indices_dias:
            if 1 <= idx_dia <= 6:
                dia_nome = dias_semana[idx_dia - 1]
                for i in range(qtd_aulas):
                    h_atual = horarios_disponiveis[idx_inicio + i]
                    h_fim = calcular_horario_fim(h_atual)

                    dados_coletados.append(
                        [
                            codigo.upper(),
                            nome,
                            dia_nome,
                            f"{i+1}/{qtd_aulas}",
                            h_atual,
                            h_fim,
                        ]
                    )
                print(f"✅ Registrado: {dia_nome}")

    if dados_coletados:
        arquivo_html = gerar_html_grade(
            dados_coletados, semestre_safe, horarios_disponiveis, dias_semana
        )

        print("\n" + "=" * 50)
        print(f"🚀 CONCLUÍDO!")
        print(f"📂 Arquivo HTML gerado: {arquivo_html}")
        print(f"👉 Dê dois cliques no arquivo para ver sua grade!")
        print("=" * 50)
    else:
        print("\nNenhum dado registrado.")


if __name__ == "__main__":
    main()

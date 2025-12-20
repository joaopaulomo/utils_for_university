import pandas as pd
from datetime import datetime, timedelta


def calcular_horario_fim(horario_inicio_str):
    """Adiciona 55 minutos ao horário de início."""
    formato = "%H:%M"
    inicio = datetime.strptime(horario_inicio_str, formato)
    fim = inicio + timedelta(minutes=55)
    return fim.strftime(formato)


def main():
    horarios_disponiveis = [
        "07:00",
        "07:55",
        "08:50",
        "09:45",
        "10:40",
        "11:35",  # Manhã
        "13:00",
        "13:55",
        "14:50",
        "15:45",
        "16:40",
        "17:35",
        "18:30",  # Tarde/Noite
    ]

    dados_planilha = []

    print("=" * 50)
    print("GERADOR DE GRADE HORÁRIA - UFBA (IGEO)")
    print("=" * 50)

    while True:
        print("\n--- Horários Disponíveis ---")
        for i, h in enumerate(horarios_disponiveis):
            print(f"[{i+1:02d}] Início: {h}")
        print("----------------------------")

        codigo = input(
            "\nDigite o Código da Matéria (ex: GEO123) ou 'sair' para encerrar: "
        ).strip()
        if codigo.lower() == "sair":
            break

        nome = input("Digite o Nome da Matéria: ").strip()

        try:
            escolha_inicio = int(input("Qual o número do horário de início? (1-13): "))
            qtd_aulas = int(input("Quantas aulas (de 55min) seguidas serão? "))
        except ValueError:
            print("❌ Erro: Por favor, digite apenas números inteiros.")
            continue

        indice_real = escolha_inicio - 1
        if indice_real < 0 or (indice_real + qtd_aulas) > len(horarios_disponiveis):
            print(
                "❌ Erro: O número de aulas ultrapassa o limite de horários do dia (18:30)."
            )
            continue

        for i in range(qtd_aulas):
            horario_atual_str = horarios_disponiveis[indice_real + i]

            horario_fim_str = calcular_horario_fim(horario_atual_str)

            entrada = {
                "Código": codigo.upper(),
                "Matéria": nome,
                "Aula Nº": f"{i+1}/{qtd_aulas}",
                "Horário Início": horario_atual_str,
                "Horário Fim": horario_fim_str,
            }
            dados_planilha.append(entrada)
            print(f"✅ Adicionado: {nome} ({horario_atual_str} - {horario_fim_str})")

    if dados_planilha:
        df = pd.DataFrame(dados_planilha)

        nome_arquivo = f"grade_horaria_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

        df.to_excel(nome_arquivo, index=False)
        print("\n" + "=" * 50)
        print(f"🚀 Sucesso! Planilha gerada: {nome_arquivo}")
        print("=" * 50)
    else:
        print("\nNenhuma matéria foi adicionada.")


if __name__ == "__main__":
    main()

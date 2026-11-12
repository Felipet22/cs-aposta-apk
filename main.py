import flet as ft
import random
import json
import os
from datetime import datetime
import asyncio

DIRETORIO_DADOS = os.getenv("FLET_APP_STORAGE_DATA") or "."
ARQUIVO_BANCO = os.path.join(DIRETORIO_DADOS, "banco_cs_aposta.json")

# ==========================================
# 1. BANCO DE DADOS E REGRAS
# ==========================================

def carregar_dados():
    if os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, 'r') as arquivo:
            return json.load(arquivo)
    return {}

def salvar_dados(dados):
    with open(ARQUIVO_BANCO, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)

def calcular_idade(data_str):
    try:
        data_nasc = datetime.strptime(data_str, "%d/%m/%Y")
        hoje = datetime.now()
        return hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
    except:
        return -1

PIADAS_DERROTA = [
    "💀 VOCÊ PERDEU!\nO Tigrinho mandou abraços e agradece a doação!",
    "💀 VOCÊ PERDEU!\nFoi por pouco... ou não! 🤡",
    "💀 VOCÊ PERDEU!\nA casa sempre vence, mas você tentou bravamente!",
    "💀 VOCÊ PERDEU!\nMais sorte na próxima encarnação!"
]

PIADAS_BANCA_QUEBRADA = [
    "\n\n💸 BANCA QUEBRADA!\nO Tigrinho levou até suas calças! 🐯👖",
    "\n\n💸 BANCA QUEBRADA!\nJá pode pedir reembolso no SPC/Serasa!",
    "\n\n💸 BANCA QUEBRADA!\nHora de pedir empréstimo com o agiota da esquina!",
    "\n\n💸 BANCA QUEBRADA!\nO importante é a experiência e a emoção! 🤡"
]

PIADAS_PARAR_GANHANDO = [
    "🧠 SABEDORIA PURA!\nVocê parou enquanto estava no lucro. O Tigrinho chora com a sua inteligência! 🤑",
    "💰 SAQUE REALIZADO!\nPegou o dinheiro e correu antes que a sorte acabasse. Visão de mestre!",
    "🎉 PARABÉNS!\nSair do cassino com lucro é para raros mestres. Aproveite o prêmio!"
]

PIADAS_PARAR_PERDENDO = [
    "🏃 CORREU NA HORA CERTA!\nParou antes de perder o que sobrou. Menos mal!",
    "📉 SAQUE DE EMERGÊNCIA!\nSalvou o troco do pão. Amanhã é um novo dia!"
]

SIMBOLOS_TIGRINHO = ["🍎", "💰", "🐯", "💎", "🍀", "🔥"]

# ==========================================
# 2. INTERFACE DO APLICATIVO
# ==========================================

def main(page: ft.Page):
    page.title = "CS Aposta Justa"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    estado = {"chave": "", "saldo": 0.0, "saldo_inicial": 1000.00, "dados_banco": carregar_dados()}

    def mostrar_aviso(mensagem, cor):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, weight="bold", color=ft.Colors.WHITE),
            bgcolor=cor,
            open=True
        )
        page.overlay.append(snack)
        page.update()

    # --- TELA 2: DENTRO DO CASSINO ---
    texto_saldo = ft.Text(size=38, weight="black", color=ft.Colors.GREEN_400)

    cartao_saldo = ft.Container(
        content=ft.Column([
            ft.Text("SEU SALDO ATUAL", size=14, color=ft.Colors.WHITE_70),
            texto_saldo
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.GREY_900,
        padding=15,
        border_radius=15,
        width=350,
        border=ft.Border.all(2, ft.Colors.GREEN_700)
    )

    rolo1_texto = ft.Text("🎰", size=36, weight="black")
    rolo2_texto = ft.Text("🎰", size=36, weight="black")
    rolo3_texto = ft.Text("🎰", size=36, weight="black")

    def criar_caixa_rolo(texto_ctrl):
        return ft.Container(
            content=texto_ctrl,
            width=90,
            height=90,
            bgcolor=ft.Colors.BLACK,
            border_radius=12,
            border=ft.Border.all(2, ft.Colors.AMBER_400),
            alignment=ft.Alignment(0, 0)
        )

    linha_rolos_tigrinho = ft.Row(
        [criar_caixa_rolo(rolo1_texto), criar_caixa_rolo(rolo2_texto), criar_caixa_rolo(rolo3_texto)],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
        visible=False
    )

    numero_girando_texto = ft.Text("00", size=46, weight="black", color=ft.Colors.AMBER_400)
    subtexto_girando = ft.Text("SORTEANDO...", size=14, weight="bold", color=ft.Colors.WHITE_70)

    caixa_numero_girando = ft.Container(
        content=ft.Column([
            numero_girando_texto,
            subtexto_girando
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        width=280,
        height=105,
        bgcolor=ft.Colors.BLACK,
        border_radius=15,
        border=ft.Border.all(2, ft.Colors.AMBER_400),
        alignment=ft.Alignment(0, 0),
        visible=False
    )

    titulo_visor = ft.Text("SORTEANDO...", size=12, weight="bold", color=ft.Colors.AMBER_400)

    visor_roleta = ft.Container(
        content=ft.Column([
            titulo_visor,
            linha_rolos_tigrinho,
            caixa_numero_girando
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
        bgcolor=ft.Colors.GREY_900,
        padding=15,
        border_radius=15,
        width=350,
        border=ft.Border.all(2, ft.Colors.AMBER_700),
        visible=False
    )

    input_escolha = ft.TextField(
        label="Sua Escolha (selecione a modalidade acima)",
        filled=True,
        border_radius=10
    )

    def atualizar_exemplo_escolha(e):
        risco = dropdown_risco.value
        input_escolha.value = ""
        
        if risco == "1":
            input_escolha.label = "Sua Escolha (ex: Par ou Ímpar)"
            input_escolha.visible = True
        elif risco == "2":
            input_escolha.label = "Sua Escolha (ex: 1, 2 ou 3)"
            input_escolha.visible = True
        elif risco == "3":
            input_escolha.label = "Sua Escolha (ex: um número de 1 a 10)"
            input_escolha.visible = True
        elif risco == "4":
            input_escolha.visible = False
            
        input_escolha.update()
        page.update()

    dropdown_risco = ft.Dropdown(
        label="Escolha a modalidade",
        filled=True,
        border_radius=10,
        options=[
            ft.dropdown.Option("1", "Risco Baixo (2x) - Par ou Ímpar"),
            ft.dropdown.Option("2", "Risco Médio (3x) - Escolher 1, 2 ou 3"),
            ft.dropdown.Option("3", "Risco Alto (10x) - Adivinhar 1 a 10"),
            ft.dropdown.Option("4", "Roleta Tigrinho 🐯 (4x a 25x)"),
        ]
    )
    dropdown_risco.on_select = atualizar_exemplo_escolha
    
    input_aposta = ft.TextField(
        label="Valor da Aposta (R$)",
        prefix=ft.Text("R$ "),
        keyboard_type=ft.KeyboardType.NUMBER,
        filled=True,
        border_radius=10
    )

    texto_resultado = ft.Text(size=18, weight="bold", text_align=ft.TextAlign.CENTER)
    
    caixa_resultado = ft.Container(
        content=texto_resultado,
        padding=18,
        border_radius=15,
        visible=False,
        alignment=ft.Alignment(0, 0),
        width=350
    )

    def atualizar_saldo():
        texto_saldo.value = f"R$ {estado['saldo']:.2f}"
        page.update()

    async def processar_aposta(e):
        try:
            aposta = float(input_aposta.value.replace(',', '.'))
        except:
            mostrar_aviso("Digite um valor numérico válido!", ft.Colors.RED_600)
            return

        if aposta < 5 or aposta > estado['saldo']:
            mostrar_aviso("Aposta inválida (Mínimo: R$ 5 | Máximo: Seu Saldo).", ft.Colors.RED_600)
            return

        risco = dropdown_risco.value
        escolha = input_escolha.value.strip().upper()

        if not risco:
            mostrar_aviso("Selecione um jogo primeiro!", ft.Colors.RED_600)
            return

        if risco == '1' and escolha not in ['PAR', 'IMPAR', 'ÍMPAR', 'P', 'I']:
            mostrar_aviso("Digite 'Par' ou 'Ímpar'.", ft.Colors.RED_600)
            return
        elif risco == '2' and escolha not in ['1', '2', '3']:
            mostrar_aviso("Digite 1, 2 ou 3.", ft.Colors.RED_600)
            return
        elif risco == '3' and (not escolha.isdigit() or not (1 <= int(escolha) <= 10)):
            mostrar_aviso("Digite um número de 1 a 10.", ft.Colors.RED_600)
            return

        btn_apostar.disabled = True
        btn_parar.disabled = True
        caixa_resultado.visible = False
        visor_roleta.visible = True

        ganhou = False
        multiplicador = 0
        mensagem_jogo = ""

        if risco in ['1', '2', '3']:
            linha_rolos_tigrinho.visible = False
            caixa_numero_girando.visible = True

            if risco == '1':
                titulo_visor.value = "ROLETA PAR OU ÍMPAR (1 a 100)"
                sorteio_final = random.randint(1, 100)
                e_par = (sorteio_final % 2 == 0)
                apostou_par = escolha in ['PAR', 'P']
                ganhou = (apostou_par and e_par) or (not apostou_par and not e_par)
                multiplicador = 2
                label_final = "PAR" if e_par else "ÍMPAR"
                mensagem_jogo = f"Número sorteado: {sorteio_final} ({label_final})"

                for passo in range(20):
                    if passo < 19:
                        num_temp = random.randint(1, 100)
                        numero_girando_texto.value = str(num_temp)
                        numero_girando_texto.color = ft.Colors.CYAN_400 if num_temp % 2 == 0 else ft.Colors.ORANGE_400
                        subtexto_girando.value = "PAR" if num_temp % 2 == 0 else "ÍMPAR"
                    else:
                        numero_girando_texto.value = str(sorteio_final)
                        numero_girando_texto.color = ft.Colors.GREEN_400 if ganhou else ft.Colors.RED_400
                        subtexto_girando.value = f"DEU {label_final}!"
                    page.update()
                    await asyncio.sleep(0.06 if passo < 13 else 0.14)

            elif risco == '2':
                titulo_visor.value = "SORTEIO RISCO MÉDIO (1, 2 ou 3)"
                sorteio_final = random.randint(1, 3)
                ganhou = (escolha == str(sorteio_final))
                multiplicador = 3
                mensagem_jogo = f"Número sorteado: {sorteio_final}"

                for passo in range(18):
                    if passo < 17:
                        num_temp = (passo % 3) + 1
                        numero_girando_texto.value = str(num_temp)
                        numero_girando_texto.color = ft.Colors.AMBER_400
                        subtexto_girando.value = "GIRANDO..."
                    else:
                        numero_girando_texto.value = str(sorteio_final)
                        numero_girando_texto.color = ft.Colors.GREEN_400 if ganhou else ft.Colors.RED_400
                        subtexto_girando.value = f"NÚMERO {sorteio_final}!"
                    page.update()
                    await asyncio.sleep(0.07 if passo < 12 else 0.15)

            elif risco == '3':
                titulo_visor.value = "SORTEIO RISCO ALTO (1 a 10)"
                sorteio_final = random.randint(1, 10)
                ganhou = (escolha == str(sorteio_final))
                multiplicador = 10
                mensagem_jogo = f"Número sorteado: {sorteio_final}"

                for passo in range(22):
                    if passo < 21:
                        num_temp = random.randint(1, 10)
                        numero_girando_texto.value = str(num_temp)
                        numero_girando_texto.color = ft.Colors.PURPLE_300
                        subtexto_girando.value = "GIRANDO DE 1 A 10..."
                    else:
                        numero_girando_texto.value = str(sorteio_final)
                        numero_girando_texto.color = ft.Colors.GREEN_400 if ganhou else ft.Colors.RED_400
                        subtexto_girando.value = f"SORTEADO: {sorteio_final}!"
                    page.update()
                    await asyncio.sleep(0.06 if passo < 14 else 0.15)

        elif risco == '4':
            caixa_numero_girando.visible = False
            linha_rolos_tigrinho.visible = True
            titulo_visor.value = "ROLETA DO TIGRINHO 🐯"

            sorteio = random.randint(1, 100)
            if sorteio <= 75:
                ganhou = False
                finais_rolos = ["🍎", "💰", "🐯"]
                mensagem_jogo = "Combinação incompleta - Não deu!"
            elif sorteio <= 90:
                ganhou = True
                multiplicador = 4
                finais_rolos = ["🍎", "🍎", "🍎"]
                mensagem_jogo = "4x FRUTAS PREMIADAS!"
            elif sorteio <= 98:
                ganhou = True
                multiplicador = 8
                finais_rolos = ["💰", "💰", "💰"]
                mensagem_jogo = "8x CHUVA DE MOEDAS!"
            else:
                ganhou = True
                multiplicador = 25
                finais_rolos = ["🐯", "🐯", "🐯"]
                mensagem_jogo = "🔥 25x GRANDE PRÊMIO DO TIGRE! 🔥"

            for passo in range(18):
                if passo < 8:
                    rolo1_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                    rolo2_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                    rolo3_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                elif passo < 13:
                    rolo1_texto.value = finais_rolos[0]
                    rolo2_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                    rolo3_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                elif passo < 17:
                    rolo1_texto.value = finais_rolos[0]
                    rolo2_texto.value = finais_rolos[1]
                    rolo3_texto.value = random.choice(SIMBOLOS_TIGRINHO)
                else:
                    rolo1_texto.value = finais_rolos[0]
                    rolo2_texto.value = finais_rolos[1]
                    rolo3_texto.value = finais_rolos[2]

                page.update()
                await asyncio.sleep(0.08 if passo < 12 else 0.14)

        if ganhou:
            lucro = aposta * (multiplicador - 1)
            estado['saldo'] += lucro
            texto_resultado.value = f"{mensagem_jogo}\n\n🎉 VOCÊ GANHOU!\nLucro: +R$ {lucro:.2f}"
            texto_resultado.color = ft.Colors.WHITE
            caixa_resultado.bgcolor = ft.Colors.GREEN_800
        else:
            estado['saldo'] -= aposta
            piada_derrota = random.choice(PIADAS_DERROTA)
            texto_resultado.value = f"{mensagem_jogo}\n\n{piada_derrota}\n-R$ {aposta:.2f}"
            texto_resultado.color = ft.Colors.WHITE
            caixa_resultado.bgcolor = ft.Colors.RED_900

        estado['dados_banco'][estado['chave']] = estado['saldo']
        salvar_dados(estado['dados_banco'])

        if estado['saldo'] <= 0:
            piada_quebra = random.choice(PIADAS_BANCA_QUEBRADA)
            texto_resultado.value += piada_quebra
            btn_apostar.disabled = True
            btn_parar.disabled = False
        else:
            btn_apostar.disabled = False
            btn_parar.disabled = False

        caixa_resultado.visible = True
        atualizar_saldo()

    async def parar_de_jogar(e):
        btn_apostar.disabled = True
        btn_parar.disabled = True
        visor_roleta.visible = False
        
        if estado['saldo'] > estado['saldo_inicial']:
            msg = random.choice(PIADAS_PARAR_GANHANDO)
            caixa_resultado.bgcolor = ft.Colors.BLUE_800
        elif estado['saldo'] > 0:
            msg = random.choice(PIADAS_PARAR_PERDENDO)
            caixa_resultado.bgcolor = ft.Colors.AMBER_900
        else:
            msg = "💸 SAINDO DE MÃOS VAZIAS!\nVolte amanhã para tentar recuperar o prejuízo!"
            caixa_resultado.bgcolor = ft.Colors.GREY_800
            
        texto_resultado.value = f"{msg}\n\nSaldo final guardado: R$ {estado['saldo']:.2f}\n\nVoltando ao início..."
        texto_resultado.color = ft.Colors.WHITE
        caixa_resultado.visible = True
        page.update()

        await asyncio.sleep(3.0)

        input_nome.value = ""
        input_data.value = ""
        input_escolha.value = ""
        input_escolha.visible = True
        input_escolha.label = "Sua Escolha (selecione a modalidade acima)"
        input_aposta.value = ""
        dropdown_risco.value = None
        caixa_resultado.visible = False
        visor_roleta.visible = False
        btn_apostar.disabled = False
        btn_parar.disabled = False

        tela_jogo.visible = False
        tela_login.visible = True
        page.update()

    btn_apostar = ft.FilledButton(
        content=ft.Text("GIRAR A ROLETA"),
        icon=ft.Icons.CASINO,
        on_click=processar_aposta,
        width=350,
        height=55,
        color=ft.Colors.BLACK,
        bgcolor=ft.Colors.AMBER_400,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    btn_parar = ft.FilledButton(
        content=ft.Text("PARAR E SACAR SALDO"),
        icon=ft.Icons.EXIT_TO_APP,
        on_click=parar_de_jogar,
        width=350,
        height=50,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_800,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    tela_jogo = ft.Column(
        controls=[
            ft.Text("🎰 CS APOSTA JUSTA", size=24, weight="black", color=ft.Colors.AMBER_400),
            cartao_saldo,
            visor_roleta,
            dropdown_risco,
            input_escolha,
            input_aposta,
            btn_apostar,
            btn_parar,
            caixa_resultado
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        visible=False
    )

    # --- TELA 1: LOGIN ---
    input_nome = ft.TextField(
        label="Nome Completo", prefix=ft.Icon(ft.Icons.PERSON), filled=True, border_radius=10)
    input_data = ft.TextField(
        label="Nascimento (DD/MM/AAAA)", prefix=ft.Icon(ft.Icons.CALENDAR_MONTH), filled=True, border_radius=10)

    def fazer_login(e):
        nome = input_nome.value.strip().title()
        idade = calcular_idade(input_data.value)

        if not nome:
            mostrar_aviso("Preencha seu nome.", ft.Colors.RED_600)
            return
        if idade == -1:
            mostrar_aviso("Data inválida. Use DD/MM/AAAA.", ft.Colors.RED_600)
            return
        if idade < 18:
            mostrar_aviso("Acesso negado: Apenas para maiores de 18 anos.", ft.Colors.RED_600)
            return

        chave = f"{nome}_{input_data.value.strip()}"
        estado['chave'] = chave

        if chave in estado['dados_banco']:
            estado['saldo'] = estado['dados_banco'][chave]
            estado['saldo_inicial'] = estado['saldo']
        else:
            estado['saldo'] = 1000.00
            estado['saldo_inicial'] = 1000.00
            estado['dados_banco'][chave] = estado['saldo']
            salvar_dados(estado['dados_banco'])

        tela_login.visible = False
        tela_jogo.visible = True
        atualizar_saldo()
        page.update()

    btn_login = ft.FilledButton(
        content=ft.Text("ENTRAR NO CASSINO"),
        on_click=fazer_login,
        width=350,
        height=60,
        bgcolor=ft.Colors.AMBER_400,
        color=ft.Colors.BLACK,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
    )

    tela_login = ft.Column(
        controls=[
            ft.Container(height=60),
            ft.Icon(ft.Icons.MONETIZATION_ON, size=100, color=ft.Colors.AMBER_400),
            ft.Text("BEM-VINDO", size=32, weight="black"),
            ft.Text("Cadastre-se ou faça login para jogar", size=14, color=ft.Colors.WHITE_54),
            ft.Container(height=30),
            input_nome,
            input_data,
            ft.Container(height=20),
            btn_login
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    page.add(tela_login, tela_jogo)

# ==========================================
# 3. INICIALIZAÇÃO DO APLICATIVO
# ==========================================
if __name__ == "__main__":
    ft.run(main)
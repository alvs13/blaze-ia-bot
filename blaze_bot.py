import random
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
import pytz
import os

# Variáveis de ambiente simuladas (substitua isso se usar .env)
TELEGRAM_TOKEN = "7556395706:AAF6eWqQNV2HFv1gr8q2JSoszIrxiOgirXg"
CHAT_ID = "7784221634"

# Inicialização do bot
bot = Bot(token=TELEGRAM_TOKEN)

# Histórico fictício para simulação
historico = []

# Função que simula a cor da próxima jogada
def prever_cor():
    return random.choice(["vermelho", "preto", "branco"])

# Função para calcular a assertividade
def calcular_assertividade(historico, cor_prevista):
    if not historico:
        return 0.0
    acertos = sum(1 for cor in historico if cor == cor_prevista)
    return (acertos / len(historico)) * 100

# Função principal que será agendada
def enviar_mensagem():
    cor = prever_cor()
    historico.append(cor)
    if len(historico) > 10:
        historico.pop(0)
    assertividade = calcular_assertividade(historico, cor)

    mensagem = (
        "🎯 SINAL GERADO: APOSTAR AGORA!\n\n"
        f"🎨 Cor com maior chance: {'🔴 VERMELHO' if cor == 'vermelho' else '⚫ PRETO' if cor == 'preto' else '⚪ BRANCO'}\n"
        f"📈 Assertividade atual: {assertividade:.2f}%\n\n"
        "💡 Entrada recomendada na próxima rodada!"
    )
    bot.send_message(chat_id=CHAT_ID, text=mensagem)

# Agendador
scheduler = BlockingScheduler(timezone=pytz.utc)
scheduler.add_job(enviar_mensagem, 'interval', minutes=1)
print("✅ Robô Blaze com IA iniciado!")
scheduler.start()
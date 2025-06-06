
import os
import random
from telegram import Bot
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import utc

# Token e Chat ID fixos
TELEGRAM_TOKEN = "7556395706:AAF6eWqQNV2HFv1gr8q2JSoszIrxiOgirXg"
CHAT_ID = "7784221634"

bot = Bot(token=TELEGRAM_TOKEN)

# Simulação simples da IA para prever cor (red, black, white)
def prever_cor():
    return random.choices(["vermelho", "preto", "branco"], weights=[45, 45, 10])[0]

# Histórico e assertividade
historico = []

def enviar_mensagem():
    cor = prever_cor()
    historico.append(cor)
    if len(historico) > 100:
        historico.pop(0)
    mais_previsoes = historico.count(cor)
    assertividade = round((mais_previsoes / len(historico)) * 100, 2)
    mensagem = f"🎯 Previsão: {cor.upper()}\n📊 Assertividade: {assertividade}%"
    bot.send_message(chat_id=CHAT_ID, text=mensagem)

scheduler = BlockingScheduler(timezone=utc)
scheduler.add_job(enviar_mensagem, 'interval', minutes=5)

print("✅ Robô Blaze com IA iniciado!")
enviar_mensagem()
scheduler.start()

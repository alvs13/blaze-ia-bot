
import requests
import random
from apscheduler.schedulers.blocking import BlockingScheduler
from telegram import Bot
import pytz
from datetime import datetime

TELEGRAM_TOKEN = "7556395706:AAF6eWqQNV2HFv1gr8q2JSoszIrxiOgirXg"
CHAT_ID = "7784221634"

bot = Bot(token=TELEGRAM_TOKEN)

historico = []

def buscar_resultado_simulado():
    return random.choice(["vermelho", "preto", "branco"])

def prever_cor():
    if len(historico) < 3:
        return random.choice(["vermelho", "preto", "branco"]), 50.0
    ultimas = historico[-3:]
    cor_mais_frequente = max(set(ultimas), key=ultimas.count)
    contagem = ultimas.count(cor_mais_frequente)
    assertividade = (contagem / 3) * 100
    return cor_mais_frequente, assertividade

def enviar_mensagem():
    cor, assertividade = prever_cor()
    if assertividade >= 66.67:  # só envia sinais com boa confiança
        agora = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime('%H:%M')
        mensagem = f"🎯 SINAL DE ENTRADA - {agora}
"
        mensagem += f"🎨 Aposte na cor: {cor.upper()}
"
        mensagem += f"📊 Probabilidade de acerto: {assertividade:.2f}%"
        bot.send_message(chat_id=CHAT_ID, text=mensagem)

    nova_cor = buscar_resultado_simulado()
    historico.append(nova_cor)
    if len(historico) > 100:
        historico.pop(0)

scheduler = BlockingScheduler(timezone=pytz.timezone("America/Sao_Paulo"))
scheduler.add_job(enviar_mensagem, 'interval', minutes=1)
scheduler.start()

import os
from dotenv import load_dotenv

commands_colors = {
  "main": 0x6A0DAD
}

roles = {
  "preto": 1527830072801890404,
  "vermelho": 1527830198311977150,
  "laranja": 1527830559697539183,
  "amarelo": 1527830758524325978,
  "verde": 1527831408670675124,
  "azul": 1527832607012814919,
  "rosa": 1527833388420173985,
  "indigo": 1527836417496191106,
  "roxo": 1527833134702268416,
  "branco": 1527833540853629058
}

prefix = "br."

load_dotenv()
token = os.getenv("TOKEN")
guild_id = int(os.getenv("GUILD_ID"))
owner_role_id = int(os.getenv("OWNER_ROLE_ID"))
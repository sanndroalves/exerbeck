# limpar_dados.py

# Importe o modelo que deseja limpar
from .models import *

# Excluir todos os objetos do modelo
Conversation.objects.all().delete()
ConversationHistory.objects.all().delete()

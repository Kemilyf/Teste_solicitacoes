# ARQUIVO: app.py (Versão com Agendamento)

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime


app = Flask(__name__)

@app.template_filter('dateformat')
def format_date(value, format='%d/%m/%Y'):
    # Se o valor for nulo (sem data), retorna um traço.
    if value is None or value == '':
        return "-"
    # Converte o texto da data para um objeto de data do Python
    date_obj = datetime.strptime(value, '%Y-%m-%d')
    # Formata o objeto de data para o texto no formato (DD/MM/YYYY)
    return date_obj.strftime(format)
# Nosso "banco de dados" agora com o campo 'data_agendamento'
solicitacoes_db = [
    { 
        "id": 1, "endereco": "Rua das Acácias, 123", "descricao": "Vários buracos perigosos na via.", 
        "categoria": "Tapa-buracos", "status": "Pendente", "justificativa": "", "data_agendamento": None
    },
    { 
        "id": 2, "endereco": "Avenida dos Pioneiros, 456", "descricao": "Poste de sinalização de 'PARE' caído.", 
        "categoria": "Sinalização viária", "status": "Em Análise", "justificativa": "", "data_agendamento": None 
    },
    { 
        "id": 3, "endereco": "Travessa dos Girassóis, 789", "descricao": "Tampa de bueiro quebrou, criando um buraco.", 
        "categoria": "Reparo em bueiro", "status": "Agendada", "justificativa": "Equipe C irá ao local.", "data_agendamento": "2025-10-20"
    },
    { 
        "id": 4, "endereco": "Rua Principal, em frente ao nº 1000", "descricao": "Asfalto completamente desgastado.", 
        "categoria": "Recapeamento", "status": "Concluída", "justificativa": "Obra finalizada pela equipe B em 15/10.", "data_agendamento": "2025-10-14" 
    }
]

@app.route("/")
def painel_de_solicitacoes():
    status_filtro = request.args.get('status', '')
  
    if status_filtro:
        dados_filtrados = [s for s in solicitacoes_db if s['status'] == status_filtro]
    else:
        dados_filtrados = solicitacoes_db
    return render_template('painel.html', solicitacoes=dados_filtrados,filtro_ativo=status_filtro)

@app.route("/atualizar/<int:id>")
def pagina_de_atualizacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao:
        return render_template('atualizar.html', solicitacao=solicitacao)
    return "Solicitação não encontrada", 404

# ESTA FUNÇÃO AGORA SALVA A DATA DO AGENDAMENTO
@app.route("/atualizar/<int:id>", methods=['POST'])
def atualizar_solicitacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao:
        solicitacao['status'] = request.form.get('novo_status')
        solicitacao['justificativa'] = request.form.get('justificativa', '')
        # Pega a data do formulário e salva no nosso "banco de dados"
        solicitacao['data_agendamento'] = request.form.get('data_agendamento')
    return redirect(url_for('painel_de_solicitacoes'))

# A função de cancelar continua a mesma
@app.route("/cancelar/<int:id>", methods=['POST'])
def cancelar_solicitacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao and solicitacao['status'] == 'Pendente':
        solicitacoes_db.remove(solicitacao)
    return redirect(url_for('painel_de_solicitacoes'))


if __name__ == "__main__":
    app.run(debug=True, port=5001) # Mudei a porta para 5001 para evitar cache do navegador
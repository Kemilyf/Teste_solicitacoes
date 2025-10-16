# ARQUIVO: app.py (Versão Final e Completa)
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# GARANTINDO QUE A CHAVE É "id", MINÚSCULO
solicitacoes_db = [
    { "id": 1, "endereco": "Rua das Acácias, 123", "descricao": "Muitos buracos na via.", "status": "Recebida" },
    { "id": 2, "endereco": "Avenida dos Pioneiros, 456", "descricao": "Asfalto inexistente.", "status": "Em Análise" }
]

# ... o resto do seu app.py ...
@app.route("/")
def painel_de_solicitacoes():
    return render_template('painel.html', solicitacoes=solicitacoes_db)

@app.route("/atualizar/<int:id>")
def pagina_de_atualizacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao:
        return render_template('atualizar.html', solicitacao=solicitacao)
    return "Solicitação não encontrada", 404

@app.route("/atualizar/<int:id>", methods=['POST'])
def atualizar_solicitacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao:
        solicitacao['status'] = request.form.get('novo_status')
    return redirect(url_for('painel_de_solicitacoes'))

@app.route("/cancelar/<int:id>", methods=['POST'])
def cancelar_solicitacao(id):
    solicitacao = next((s for s in solicitacoes_db if s["id"] == id), None)
    if solicitacao:
        solicitacoes_db.remove(solicitacao)
    return redirect(url_for('painel_de_solicitacoes'))

if __name__ == "__main__":
    app.run(debug=True)
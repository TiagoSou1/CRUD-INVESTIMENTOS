from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import oracledb
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(BASE_DIR, 'templates'))
app = Flask(__name__, template_folder='templates')
CORS(app)


# CONFIGURAÇÃO DO BANCO DE DADOS

def conectar_bd():
    """Estabelece conexão com o banco Oracle"""
    try:
        connection = oracledb.connect(
    user="SEU_USUARIO",
    password="SUA_SENHA",
    dsn="localhost:1521/xe"
)
        return connection
    except Exception as e:
        return None

# ROTAS PRINCIPAIS

@app.route('/api/teste', methods=['POST'])
def teste():
    print("Recebi um POST!")
    return {"status": "ok"}

@app.route('/')
def index():
    return render_template('index.html')

# API - INVESTIMENTOS

@app.route('/api/investimentos', methods=['GET'])
def listar_investimentos_api():
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.investimento_id, i.investimento_codigo, i.investimento_tipo,
                   i.investimento_quantidade, i.investimento_preco_medio,
                   i.investimento_data_compra, c.corretora_nome
            FROM Investimentos i
            JOIN Corretoras c ON i.corretora_id = c.corretora_id
            ORDER BY i.investimento_codigo
        """)
        investimentos = cursor.fetchall()
        
        resultado = []
        for inv in investimentos:
            resultado.append({
                'id': inv[0],
                'codigo': inv[1],
                'tipo': inv[2],
                'quantidade': inv[3],
                'preco_medio': float(inv[4]),
                'data_compra': inv[5].strftime('%d/%m/%Y'),
                'corretora': inv[6]
            })
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/investimentos', methods=['POST'])
def inserir_investimento_api():
    dados = request.json
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        data_obj = datetime.strptime(dados['data_compra'], '%Y-%m-%d')
        
        cursor.execute("""
            INSERT INTO Investimentos (investimento_id, corretora_id, investimento_codigo, 
                                      investimento_tipo, investimento_quantidade, 
                                      investimento_preco_medio, investimento_data_compra)
            VALUES (seq_investimento.NEXTVAL, :1, :2, :3, :4, :5, :6)
        """, (dados['corretora_id'], dados['codigo'], dados['tipo'], 
              dados['quantidade'], dados['preco_medio'], data_obj))
        
        conn.commit()
        return jsonify({'sucesso': True, 'mensagem': 'Investimento inserido com sucesso!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/investimentos/<int:id>', methods=['DELETE'])
def excluir_investimento_api(id):
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Investimentos WHERE investimento_id = :1", (id,))
        conn.commit()
        return jsonify({'sucesso': True, 'mensagem': 'Investimento excluído!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/corretoras', methods=['GET'])
def listar_corretoras_api():
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT corretora_id, corretora_nome, corretora_taxa_corretagem FROM Corretoras ORDER BY corretora_nome")
        corretoras = cursor.fetchall()
        
        resultado = []
        for corr in corretoras:
            resultado.append({
                'id': corr[0],
                'nome': corr[1],
                'taxa': float(corr[2])
            })
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/investimentos/corretora/<int:corretora_id>', methods=['GET'])
def relatorio_por_corretora(corretora_id):
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT i.investimento_codigo, i.investimento_tipo, i.investimento_quantidade,
                   i.investimento_preco_medio
            FROM Investimentos i
            WHERE i.corretora_id = :1
            ORDER BY i.investimento_codigo
        """, (corretora_id,))
        
        investimentos = cursor.fetchall()
        resultado = []
        for inv in investimentos:
            resultado.append({
                'codigo': inv[0],
                'tipo': inv[1],
                'quantidade': inv[2],
                'preco_medio': float(inv[3])
            })
        
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/patrimonio-total', methods=['GET'])
def patrimonio_total():
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        total = cursor.callfunc("fn_patrimonio_total", float)
        return jsonify({'total': total})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/valorizar-ativos', methods=['POST'])
def valorizar_ativos():
    conn = conectar_bd()
    if not conn:
        return jsonify({'erro': 'Erro ao conectar no banco'}), 500
    
    try:
        cursor = conn.cursor()
        cursor.callproc("sp_valorizar_ativos")
        return jsonify({'sucesso': True, 'mensagem': 'Valorização de 5% aplicada!'})
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
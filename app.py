"""Flask API for a small Oracle-backed investment portfolio application."""

from datetime import datetime
import logging
import os
from pathlib import Path

import oracledb
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS


BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__, template_folder=str(BASE_DIR / "templates"))
CORS(app)
app.logger.setLevel(logging.INFO)


def connect_database():
    """Create an Oracle connection from environment variables."""
    user = os.environ.get("ORACLE_USER")
    password = os.environ.get("ORACLE_PASSWORD")
    dsn = os.environ.get("ORACLE_DSN", "localhost:1521/XEPDB1")

    if not user or not password:
        raise RuntimeError("ORACLE_USER and ORACLE_PASSWORD must be configured.")

    return oracledb.connect(user=user, password=password, dsn=dsn)


def database_error(exc: Exception):
    """Log internal details without exposing credentials or DSN data to clients."""
    app.logger.exception("Database operation failed: %s", exc)
    return jsonify({"erro": "Não foi possível concluir a operação no banco."}), 500


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    """Report application health without opening a database connection."""
    configured = bool(
        os.environ.get("ORACLE_USER") and os.environ.get("ORACLE_PASSWORD")
    )
    return jsonify({"status": "ok", "database_configured": configured})


@app.get("/api/investimentos")
def list_investments():
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT i.investimento_id, i.investimento_codigo, i.investimento_tipo,
                   i.investimento_quantidade, i.investimento_preco_medio,
                   i.investimento_data_compra, c.corretora_nome
              FROM Investimentos i
              JOIN Corretoras c ON i.corretora_id = c.corretora_id
             ORDER BY i.investimento_codigo
            """
        )
        result = [
            {
                "id": row[0],
                "codigo": row[1],
                "tipo": row[2],
                "quantidade": row[3],
                "preco_medio": float(row[4]),
                "data_compra": row[5].strftime("%d/%m/%Y"),
                "corretora": row[6],
            }
            for row in cursor.fetchall()
        ]
        return jsonify(result)
    except Exception as exc:  # Oracle errors vary by client version.
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.post("/api/investimentos")
def create_investment():
    connection = cursor = None
    try:
        data = request.get_json(silent=False)
        required = {
            "corretora_id",
            "codigo",
            "tipo",
            "quantidade",
            "preco_medio",
            "data_compra",
        }
        missing = required.difference(data or {})
        if missing:
            return jsonify({"erro": f"Campos ausentes: {', '.join(sorted(missing))}"}), 400

        purchase_date = datetime.strptime(data["data_compra"], "%Y-%m-%d")
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO Investimentos (
                investimento_id, corretora_id, investimento_codigo,
                investimento_tipo, investimento_quantidade,
                investimento_preco_medio, investimento_data_compra
            )
            VALUES (seq_investimento.NEXTVAL, :1, :2, :3, :4, :5, :6)
            """,
            (
                data["corretora_id"],
                data["codigo"],
                data["tipo"],
                data["quantidade"],
                data["preco_medio"],
                purchase_date,
            ),
        )
        connection.commit()
        return jsonify({"sucesso": True, "mensagem": "Investimento inserido."}), 201
    except (TypeError, ValueError) as exc:
        return jsonify({"erro": f"Dados inválidos: {exc}"}), 400
    except Exception as exc:
        if connection is not None:
            connection.rollback()
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.delete("/api/investimentos/<int:investment_id>")
def delete_investment(investment_id: int):
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM Investimentos WHERE investimento_id = :1",
            (investment_id,),
        )
        if cursor.rowcount == 0:
            connection.rollback()
            return jsonify({"erro": "Investimento não encontrado."}), 404
        connection.commit()
        return jsonify({"sucesso": True, "mensagem": "Investimento excluído."})
    except Exception as exc:
        if connection is not None:
            connection.rollback()
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.get("/api/corretoras")
def list_brokers():
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT corretora_id, corretora_nome, corretora_taxa_corretagem
              FROM Corretoras
             ORDER BY corretora_nome
            """
        )
        result = [
            {"id": row[0], "nome": row[1], "taxa": float(row[2])}
            for row in cursor.fetchall()
        ]
        return jsonify(result)
    except Exception as exc:
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.get("/api/investimentos/corretora/<int:broker_id>")
def investments_by_broker(broker_id: int):
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT investimento_codigo, investimento_tipo,
                   investimento_quantidade, investimento_preco_medio
              FROM Investimentos
             WHERE corretora_id = :1
             ORDER BY investimento_codigo
            """,
            (broker_id,),
        )
        result = [
            {
                "codigo": row[0],
                "tipo": row[1],
                "quantidade": row[2],
                "preco_medio": float(row[3]),
            }
            for row in cursor.fetchall()
        ]
        return jsonify(result)
    except Exception as exc:
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.get("/api/patrimonio-total")
def total_equity():
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        total = cursor.callfunc("fn_patrimonio_total", float)
        return jsonify({"total": total})
    except Exception as exc:
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


@app.post("/api/valorizar-ativos")
def appreciate_assets():
    connection = cursor = None
    try:
        connection = connect_database()
        cursor = connection.cursor()
        cursor.callproc("sp_valorizar_ativos")
        connection.commit()
        return jsonify({"sucesso": True, "mensagem": "Valorização de 5% aplicada."})
    except Exception as exc:
        if connection is not None:
            connection.rollback()
        return database_error(exc)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    app.run(
        host=os.environ.get("FLASK_HOST", "127.0.0.1"),
        port=int(os.environ.get("FLASK_PORT", "5000")),
        debug=os.environ.get("FLASK_DEBUG", "0") == "1",
    )

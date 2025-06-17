from flask import Flask, request, jsonify, Response
import build_model
import json


app = Flask(__name__)

# disable CORS for all routes


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    return response

@app.route("/recommendation", methods=["POST"])
def recommendation():
    data = request.get_json()
    queries = data.get("history", [])

    if not queries or not isinstance(queries, list):
        return jsonify({"error": "History must be a list of queries"}), 400

    # Gabungkan semua query menjadi satu kalimat panjang
    combined_query = " ".join(queries)
    
    # Gunakan semantic_search untuk mencari ayat mirip query gabungan
    results = build_model.semantic_search(combined_query, top_n=10)

    return jsonify({
        "recommendations": results.to_dict(orient="records")
    })


@app.route("/semantic_search")
def semantic_search_route():
    query = request.args.get("query", "")
    if not query:
        return {"error": "Query parameter is required"}, 400
    if len(query) < 3:
        return {"error": "Query must be at least 3 characters long"}, 400
    results = build_model.search_by_query(query)
    return {"results": results.to_dict(orient="records")}


# route list surah
@app.route("/list_surah")
def list_surah():
    surah_list = build_model.get_surah_list()
    return jsonify({"surah_list": surah_list.to_dict(orient="records")})


@app.route("/surah_detail/<int:surah_number>")
def surah_detail(surah_number):
    surah_detail = build_model.get_surah_detail(surah_number)
    print(surah_detail['Teks_Arab'])
    if surah_detail.empty:
        return jsonify({"error": "Surah not found"}), 404

    # Convert DataFrame to JSON with proper encoding
    # This ensures that Arabic characters are handled correctly
    json_data = json.dumps(
        {"surah_detail": surah_detail.to_dict(orient="records")},
        ensure_ascii=False,
        indent=2
    )
    return Response(json_data, mimetype='application/json; charset=utf-8')

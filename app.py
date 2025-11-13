from flask import Flask, request, send_file
from weasyprint import HTML
import io

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_html_to_pdf():
    """Convertit HTML en PDF avec WeasyPrint"""
    
    # Récupérer le HTML depuis la requête
    data = request.get_json()
    html_content = data.get('html', '')
    
    if not html_content:
        return {'error': 'No HTML content provided'}, 400
    
    try:
        # Générer le PDF avec WeasyPrint
        pdf_bytes = HTML(string=html_content).write_pdf()
        
        # Créer un buffer en mémoire
        pdf_buffer = io.BytesIO(pdf_bytes)
        pdf_buffer.seek(0)
        
        # Retourner le PDF
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name='devis.pdf'
        )
    
    except Exception as e:
        return {'error': str(e)}, 500

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de santé pour vérifier que le service tourne"""
    return {'status': 'ok'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

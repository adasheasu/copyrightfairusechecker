#!/usr/bin/env python3
"""
Flask Web Server for Copyright Checker
Simple HTML interface for copyright and fair use checking
"""

from flask import Flask, render_template, request, jsonify
import os
from pathlib import Path
from werkzeug.utils import secure_filename
from utils.image_analyzer import ImageAnalyzer
from utils.document_analyzer import DocumentAnalyzer
from utils.copyright_checker import CopyrightChecker
from utils.fair_use_assessor import FairUseAssessor
from utils.alternative_finder import AlternativeFinder

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'data/uploads'

# Ensure upload directory exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'docx', 'doc'}


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Serve the main HTML interface"""
    return render_template('index.html')


@app.route('/check', methods=['POST'])
def check_file():
    """Handle file upload and analysis"""
    try:
        # Check if file was uploaded
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Unsupported file type'}), 400

        # Get form data
        course_type = request.form.get('courseType', 'Online')
        institution = request.form.get('institution', 'Public University')

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Analyze file
        result = analyze_file(filepath, course_type, institution)

        # Clean up
        try:
            os.remove(filepath)
        except:
            pass

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def analyze_file(filepath, course_type, institution):
    """Analyze a file for copyright and fair use"""
    extension = Path(filepath).suffix.lower()
    is_image = extension in ['.jpg', '.jpeg', '.png', '.gif']
    is_document = extension in ['.pdf', '.docx', '.doc']

    # Initialize analyzers
    copyright_checker = CopyrightChecker()
    fair_use_assessor = FairUseAssessor()
    alternative_finder = AlternativeFinder()

    result = {
        'filename': Path(filepath).name,
        'fileType': 'image' if is_image else 'document',
        'sourceInfo': {},
        'copyrightInfo': {},
        'fairUseAssessment': {},
        'alternatives': []
    }

    # Analyze based on file type
    if is_image:
        image_analyzer = ImageAnalyzer()
        source_info = image_analyzer.analyze(filepath)
        copyright_info = copyright_checker.check_image(filepath)
        content_type = 'image'

        result['sourceInfo'] = {
            'dimensions': source_info.get('dimensions'),
            'format': source_info.get('format'),
            'fileSize': source_info.get('file_size')
        }

    else:  # Document
        doc_analyzer = DocumentAnalyzer()
        source_info = doc_analyzer.analyze(filepath)
        copyright_info = copyright_checker.check_document(filepath)
        content_type = 'document'

        result['sourceInfo'] = {
            'author': source_info.get('author'),
            'title': source_info.get('title'),
            'pageCount': source_info.get('page_count')
        }

    # Copyright information
    result['copyrightInfo'] = {
        'licenseType': copyright_info.get('license_type'),
        'copyrightHolder': copyright_info.get('copyright_holder'),
        'year': copyright_info.get('year'),
        'isPublicDomain': copyright_info.get('is_public_domain', False),
        'commercialUseAllowed': copyright_info.get('commercial_use_allowed'),
        'modificationsAllowed': copyright_info.get('modifications_allowed'),
        'attributionRequired': copyright_info.get('attribution_required', False),
        'attributionText': copyright_info.get('attribution_text'),
        'restrictions': copyright_info.get('restrictions', []),
        'confidence': copyright_info.get('confidence', 'Low')
    }

    # Fair use assessment
    fair_use_result = fair_use_assessor.assess(
        copyright_info,
        course_type,
        institution,
        content_type
    )

    result['fairUseAssessment'] = {
        'canUse': fair_use_result.get('can_use'),
        'confidence': fair_use_result.get('confidence'),
        'factors': fair_use_result.get('factors', {}),
        'recommendation': fair_use_result.get('recommendation', ''),
        'bestPractices': fair_use_result.get('best_practices', [])
    }

    # Find alternatives if needed
    if fair_use_result.get('can_use') == False:
        alternatives = alternative_finder.find_alternatives(source_info, copyright_info)
        result['alternatives'] = [
            {
                'source': alt.get('source'),
                'url': alt.get('url'),
                'license': alt.get('license'),
                'description': alt.get('description', '')
            }
            for alt in alternatives[:10]  # Top 10
        ]

    return result


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("  Copyright & Fair Use Checker - Web Interface")
    print("=" * 70)
    print("\n  Starting server...")
    print(f"  Open your browser to: http://localhost:5000")
    print("\n  Press Ctrl+C to stop the server\n")
    print("=" * 70 + "\n")

    app.run(debug=True, port=5000)

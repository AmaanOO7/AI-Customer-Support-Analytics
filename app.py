"""
AI Customer Support Analytics - Main Flask Application
A complete AI-powered customer support analytics platform using IBM Watsonx.ai
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, session, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Import utility modules
from utils.watsonx_client import WatsonxClient
from utils.data_processor import DataProcessor
from utils.ai_analyzer import AIAnalyzer
from utils.pdf_generator import PDFReportGenerator
from utils.export_handler import ExportHandler
from utils.chart_generator import ChartDataGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

analysis_cache = {}

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['EXPORT_FOLDER'] = 'exports'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['EXPORT_FOLDER'], exist_ok=True)

# Initialize components
try:
    watsonx_client = WatsonxClient()
    data_processor = DataProcessor(upload_folder=app.config['UPLOAD_FOLDER'])
    ai_analyzer = AIAnalyzer(watsonx_client=watsonx_client)
    pdf_generator = PDFReportGenerator()
    export_handler = ExportHandler(export_folder=app.config['EXPORT_FOLDER'])
    chart_generator = ChartDataGenerator()
    logger.info("All components initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    watsonx_client = None


# ============================================================================
# ROUTES - Landing Page
# ============================================================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')


# ============================================================================
# ROUTES - File Upload and Analysis
# ============================================================================

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and initial processing"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not data_processor.allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only CSV, XLSX, and XLS files are allowed.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validate file size
        if not data_processor.validate_file_size(filepath):
            os.remove(filepath)
            return jsonify({'error': 'File size exceeds 20 MB limit'}), 400
        
        # Process dataset
        df, profile = data_processor.prepare_for_analysis(filepath)
        
        # Check if dataset is valid
        if not profile.get('is_valid', False):
            return jsonify({
                'error': 'Invalid dataset',
                'warnings': profile.get('warnings', [])
            }), 400
        
        # Store session data
        session['current_file'] = filename
        session['filepath'] = filepath
        
        logger.info(f"File uploaded successfully: {filename}")
        
        return jsonify({
            'success': True,
            'filename': filename,
            'profile': profile,
            'message': 'File uploaded successfully. Starting analysis...'
        })
        
    except Exception as e:
        logger.error(f"Error uploading file: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/analyze', methods=['POST'])
def analyze_dataset():
    """Analyze the uploaded dataset using AI"""
    try:
        # Get filepath from session
        filepath = session.get('filepath')
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'No file uploaded. Please upload a file first.'}), 400
        
        # Get analysis parameters
        data = request.get_json() or {}
        sample_size = data.get('sample_size')
        max_workers = data.get('max_workers', 5)
        
        # Load and prepare dataset
        df, profile = data_processor.prepare_for_analysis(filepath)
        
        # Perform AI analysis
        logger.info(f"Starting AI analysis of {len(df)} tickets")
        analysis_results = ai_analyzer.analyze_dataset(
            df=df,
            max_workers=max_workers,
            sample_size=sample_size
        )
        
        # Generate analytics summary
        analytics_summary = ai_analyzer.generate_analytics_summary(analysis_results)
        
        # Generate business insights
        business_insights = ai_analyzer.generate_business_insights(
            analysis_results=analysis_results,
            analytics_summary=analytics_summary
        )
        
        # Generate chart data
        charts = chart_generator.generate_all_charts(analytics_summary, analysis_results)
        
        # Store results in session
        analysis_cache["latest"] = {
            "analysis_results": analysis_results,
            "analytics_summary": analytics_summary,
            "business_insights": business_insights,
            "charts": charts,
            "dataset_profile": profile}
        
        logger.info("Analysis completed successfully")
        
        return jsonify({
            'success': True,
            'message': 'Analysis completed successfully',
            'redirect': url_for('dashboard')
        })
        
    except Exception as e:
        logger.error(f"Error analyzing dataset: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES - Dashboard
# ============================================================================

@app.route('/dashboard')
def dashboard():

    if "latest" not in analysis_cache:
        return redirect(url_for("index"))

    data = analysis_cache["latest"]

    return render_template(
        "dashboard.html",
        analytics_summary=data["analytics_summary"],
        business_insights=data["business_insights"],
        charts=data["charts"],
        dataset_profile=data["dataset_profile"]
    )


@app.route('/api/tickets')
def get_tickets():
    """API endpoint to get ticket list with pagination and filtering"""
    try:
        analysis_results = analysis_cache.get("latest", {}).get("analysis_results", [])
        
        if not analysis_results:
            return jsonify({'error': 'No analysis results available'}), 404
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Get filter parameters
        filters = {
            'sentiment': request.args.get('sentiment'),
            'emotion': request.args.get('emotion'),
            'priority': request.args.get('priority'),
            'urgency': request.args.get('urgency'),
            'category': request.args.get('category'),
            'agent_name': request.args.get('agent'),
            'keyword': request.args.get('keyword')
        }
        
        # Remove None values
        filters = {k: v for k, v in filters.items() if v}
        
        # Apply filters
        filtered_results = analysis_results
        
        if filters:
            filtered_results = []
            for result in analysis_results:
                match = True
                for key, value in filters.items():
                    if key == 'keyword':
                        # Search in customer message and complaint summary
                        keyword_lower = value.lower()
                        customer_msg = str(result.get('customer_message', '')).lower()
                        summary = str(result.get('complaint_summary', '')).lower()
                        if keyword_lower not in customer_msg and keyword_lower not in summary:
                            match = False
                            break
                    else:
                        if str(result.get(key, '')).lower() != value.lower():
                            match = False
                            break
                
                if match:
                    filtered_results.append(result)
        
        # Pagination
        total = len(filtered_results)
        start = (page - 1) * per_page
        end = start + per_page
        paginated_results = filtered_results[start:end]
        
        return jsonify({
            'tickets': paginated_results,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page
        })
        
    except Exception as e:
        logger.error(f"Error getting tickets: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/ticket/<ticket_id>')
def get_ticket_detail(ticket_id):
    try:
        analysis_results = analysis_cache.get("latest", {}).get("analysis_results", [])

        print("\n========== DEBUG ==========")
        print("Requested Ticket ID:", repr(ticket_id))
        print("Total tickets:", len(analysis_results))

        for i, r in enumerate(analysis_results[:10]):
            print(i, "Stored:", repr(r.get("ticket_id")))

        ticket_detail = ai_analyzer.get_ticket_details(analysis_results, ticket_id)

        print("Found:", ticket_detail is not None)
        print("===========================\n")

        if not ticket_detail:
            return jsonify({"error": "Ticket not found"}), 404

        return jsonify(ticket_detail)

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.route('/api/filters')
def get_filter_options():
    """API endpoint to get available filter options"""
    try:
        analysis_results = analysis_cache.get("latest", {}).get("analysis_results", [])
        
        if not analysis_results:
            return jsonify({'error': 'No analysis results available'}), 404
        
        # Extract unique values for each filter
        sentiments = sorted(set(r.get('sentiment', '') for r in analysis_results if r.get('sentiment')))
        emotions = sorted(set(r.get('emotion', '') for r in analysis_results if r.get('emotion')))
        priorities = sorted(set(r.get('priority', '') for r in analysis_results if r.get('priority')))
        urgencies = sorted(set(r.get('urgency', '') for r in analysis_results if r.get('urgency')))
        categories = sorted(set(r.get('issue_category', '') for r in analysis_results if r.get('issue_category')))
        agents = sorted(set(r.get('agent_name', '') for r in analysis_results if r.get('agent_name')))
        
        return jsonify({
            'sentiments': sentiments,
            'emotions': emotions,
            'priorities': priorities,
            'urgencies': urgencies,
            'categories': categories,
            'agents': agents
        })
        
    except Exception as e:
        logger.error(f"Error getting filter options: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES - Export Functions
# ============================================================================

@app.route('/export/pdf')
def export_pdf():
    """Export analytics report as PDF"""
    try:
        latest = analysis_cache.get("latest", {})

        data = {
            'analysis_results': latest.get('analysis_results', []),
            'analytics_summary': latest.get('analytics_summary', {}),
            'business_insights': latest.get('business_insights', {}),
            'dataset_profile': latest.get('dataset_profile', {})
}
        
        # Generate PDF
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"customer_support_analytics_{timestamp}.pdf"
        output_path = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        pdf_generator.generate_report(output_path, data)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        logger.error(f"Error exporting PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/export/excel')
def export_excel():
    """Export analytics data as Excel"""
    try:
        latest = analysis_cache.get("latest", {})
        # Prepare data for Excel
        data = {
            'analysis_results': latest.get('analysis_results', []),
            'analytics_summary': latest.get('analytics_summary', {}),
            'business_insights': latest.get('business_insights', {})
        }
        
        # Generate Excel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"customer_support_analytics_{timestamp}.xlsx"
        output_path = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        export_handler.export_to_excel(data, output_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        logger.error(f"Error exporting Excel: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/export/csv')
def export_csv():
    """Export ticket analysis as CSV"""
    try:
        analysis_results = analysis_cache.get("latest", {}).get("analysis_results", [])
        
        # Generate CSV
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ticket_analysis_{timestamp}.csv"
        output_path = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        export_handler.export_to_csv(analysis_results, output_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='text/csv'
        )
        
    except Exception as e:
        logger.error(f"Error exporting CSV: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/export/json')
def export_json():
    """Export complete analytics as JSON"""
    try:
        latest = analysis_cache.get("latest", {})

    # Prepare complete data
        data = {
            'analysis_results': latest.get('analysis_results', []),
            'analytics_summary': latest.get('analytics_summary', {}),
            'business_insights': latest.get('business_insights', {}),
            'dataset_profile': latest.get('dataset_profile', {}),
            'charts': latest.get('charts', {})
}
        
        # Generate JSON
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"customer_support_analytics_{timestamp}.json"
        output_path = os.path.join(app.config['EXPORT_FOLDER'], filename)
        
        export_handler.export_to_json(data, output_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
        
    except Exception as e:
        logger.error(f"Error exporting JSON: {str(e)}")
        return jsonify({'error': str(e)}), 500


# ============================================================================
# ROUTES - Utility
# ============================================================================

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    try:
        watsonx_status = watsonx_client.test_connection() if watsonx_client else False
        
        return jsonify({
            'status': 'healthy',
            'watsonx_connected': watsonx_status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@app.route('/clear')
def clear_session():
    session.clear()
    analysis_cache.clear()
    return redirect(url_for('index'))


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Resource not found'}), 404
    return render_template('404.html'), 404


@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors"""
    return jsonify({'error': 'File size exceeds 20 MB limit'}), 413


@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(error)}")
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error'}), 500
    return render_template('500.html'), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    # Check if Watsonx credentials are configured
    if not watsonx_client:
        logger.warning("Watsonx client not initialized. Please check your .env configuration.")
    
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    
    logger.info(f"Starting AI Customer Support Analytics on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)

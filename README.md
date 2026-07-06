# AI Customer Support Analytics

A complete, production-ready AI-powered web application for analyzing customer support conversations and generating comprehensive business insights using IBM Watsonx.ai Granite models.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)
![IBM Watsonx](https://img.shields.io/badge/IBM-Watsonx.ai-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌟 Features

### AI-Powered Analysis
- **Sentiment Analysis**: Positive, Neutral, Negative, Very Negative
- **Emotion Detection**: Angry, Frustrated, Satisfied, Happy, Confused, Disappointed, Excited
- **Intent Recognition**: 12+ intent categories including refund requests, technical issues, billing problems
- **Issue Categorization**: Automatic classification into 12+ categories
- **Priority & Urgency Prediction**: AI-driven prioritization (Low, Medium, High, Critical)
- **Customer Satisfaction Scoring**: 0-100 satisfaction prediction
- **Churn Risk Assessment**: Low, Medium, High risk classification
- **Escalation Detection**: Automatic identification of tickets requiring escalation
- **Root Cause Analysis**: AI-generated root cause identification
- **Keyword Extraction**: Automatic extraction of key terms

### Agent Performance Evaluation
- **Professionalism Score**: 0-100 rating
- **Empathy Score**: Emotional intelligence assessment
- **Grammar Score**: Writing quality evaluation
- **Clarity Score**: Communication effectiveness
- **Resolution Quality Score**: Solution effectiveness
- **Friendliness Score**: Customer service warmth
- **Overall Agent Score**: Composite performance metric
- **Strengths & Weaknesses**: Detailed feedback
- **Improvement Suggestions**: Actionable recommendations
- **AI-Improved Responses**: Enhanced response generation

### Business Intelligence
- **Executive Summary**: Comprehensive overview of support performance
- **Top Complaint Categories**: Most common issues
- **Customer Sentiment Overview**: Sentiment trends and patterns
- **Business Risks**: Identified operational risks
- **Operational Bottlenecks**: Process inefficiencies
- **Monthly & Weekly Trends**: Time-based analysis
- **Agent Performance Rankings**: Top and low performers
- **Actionable Recommendations**: 5-10 strategic recommendations

### Interactive Dashboard
- **KPI Cards**: 8 animated KPI metrics
- **Interactive Charts**: 8+ Chart.js visualizations
  - Sentiment Pie Chart
  - Emotion Distribution Bar Chart
  - Issue Category Horizontal Bar Chart
  - Priority Doughnut Chart
  - Urgency Doughnut Chart
  - Customer Satisfaction Distribution
  - Agent Performance Chart
  - Churn Risk Pie Chart
- **Advanced Filtering**: Filter by sentiment, emotion, priority, urgency, category, agent, keyword
- **Ticket Management**: Paginated ticket list with detailed views
- **Search Functionality**: Full-text search across messages
- **Dark Mode**: Toggle between light and dark themes

### Export Capabilities
- **PDF Reports**: Professional multi-page reports with charts and insights
- **Excel Reports**: Multi-sheet workbooks with analytics and raw data
- **CSV Export**: Ticket-level analysis data
- **JSON Export**: Complete analytics data structure

### Data Processing
- **File Support**: CSV, XLSX, XLS formats
- **Automatic Validation**: File type and size validation (20 MB limit)
- **Column Normalization**: Flexible column name matching
- **Data Cleaning**: Duplicate removal, missing value handling
- **Dataset Profiling**: Comprehensive statistics and quality metrics

## 📁 Project Structure

```
ai-customer-support-analytics/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── README.md                       # This file
├── AGENT_INSTRUCTIONS.md           # AI agent customization guide
├── sample_customer_support_dataset.csv  # Sample dataset
├── utils/                          # Utility modules
│   ├── __init__.py
│   ├── watsonx_client.py          # IBM Watsonx.ai integration
│   ├── data_processor.py          # Dataset processing
│   ├── ai_analyzer.py             # AI analysis orchestration
│   ├── pdf_generator.py           # PDF report generation
│   ├── export_handler.py          # Export functionality
│   └── chart_generator.py         # Chart data preparation
├── templates/                      # HTML templates
│   ├── index.html                 # Landing page
│   ├── dashboard.html             # Analytics dashboard
│   ├── 404.html                   # 404 error page
│   └── 500.html                   # 500 error page
├── static/                         # Static assets
│   ├── css/
│   │   └── style.css              # Custom styles
│   └── js/
│       ├── main.js                # Main JavaScript
│       └── dashboard.js           # Dashboard interactions
├── uploads/                        # Uploaded files (auto-created)
└── exports/                        # Generated exports (auto-created)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- IBM Cloud account with Watsonx.ai access
- pip (Python package manager)

### Installation

1. **Clone or download the project**
   ```bash
   cd ai-customer-support-analytics
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your IBM Cloud credentials:
   ```env
   IBM_CLOUD_API_KEY=your_api_key_here
   WATSONX_PROJECT_ID=your_project_id_here
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   MODEL_ID=ibm/granite-13b-chat-v2
   SECRET_KEY=your_secret_key_here
   ```

### IBM Cloud Setup

1. **Create IBM Cloud Account**
   - Visit [IBM Cloud](https://cloud.ibm.com/)
   - Sign up for a free account or log in

2. **Access Watsonx.ai**
   - Navigate to the Watsonx.ai service
   - Create a new project or use an existing one
   - Note your Project ID

3. **Get API Key**
   - Go to [IBM Cloud API Keys](https://cloud.ibm.com/iam/apikeys)
   - Create a new API key
   - Copy and save the key securely

4. **Configure the Application**
   - Add your API key to `.env` as `IBM_CLOUD_API_KEY`
   - Add your Project ID to `.env` as `WATSONX_PROJECT_ID`

### Running the Application

1. **Start the Flask server**
   ```bash
   python app.py
   ```

2. **Open your browser**
   ```
   http://localhost:5000
   ```

3. **Upload a dataset**
   - Use the provided `sample_customer_support_dataset.csv` or your own
   - Supported formats: CSV, XLSX, XLS
   - Maximum file size: 20 MB

4. **View analytics**
   - Wait for AI analysis to complete
   - Explore the interactive dashboard
   - Filter and search tickets
   - Export reports

## 📊 Sample Dataset

A sample customer support dataset is included: `sample_customer_support_dataset.csv`

### Expected Columns

The application intelligently handles various column names. Recommended columns:

- **Ticket ID**: Unique identifier
- **Customer Message**: Customer's message or complaint
- **Agent Response**: Agent's reply (optional)
- **Agent Name**: Support agent name (optional)
- **Customer Name**: Customer name (optional)
- **Date**: Ticket creation date (optional)
- **Product**: Product or service name (optional)
- **Category**: Issue category (optional)
- **Resolution Time**: Time to resolve in hours (optional)
- **Status**: Ticket status (optional)
- **Customer Rating**: Customer satisfaction rating (optional)

**Note**: Only Customer Message is required. The application will work with partial data and skip unavailable analyses.

## 🎨 Features in Detail

### Landing Page
- Modern hero section with gradient background
- Drag-and-drop file upload
- Feature showcase
- How it works section
- Responsive design

### Analytics Dashboard
- 8 animated KPI cards
- 8+ interactive Chart.js visualizations
- Executive summary with AI insights
- Business recommendations
- Risk identification
- Agent performance rankings

### Ticket Management
- Paginated ticket list (20 per page)
- Advanced filtering system
- Keyword search
- Detailed ticket view modal
- Complete AI analysis for each ticket

### Export Options
- **PDF**: Professional multi-page report with charts
- **Excel**: Multi-sheet workbook with analytics
- **CSV**: Raw ticket analysis data
- **JSON**: Complete data structure

## 🔧 Customization

### AI Agent Behavior
Edit `AGENT_INSTRUCTIONS.md` to customize:
- Analysis criteria
- Scoring thresholds
- Business terminology
- Industry-specific rules
- Output formats

### Styling
Edit `static/css/style.css` to customize:
- Color scheme
- Typography
- Layout
- Animations
- Dark mode colors

### Analysis Parameters
In `app.py`, adjust:
- `max_workers`: Parallel processing threads (default: 5)
- `sample_size`: Limit analysis to N tickets (default: all)

## 🐛 Troubleshooting

### Common Issues

**1. Import Error: ibm_watson_machine_learning**
```bash
pip install ibm-watson-machine-learning
```

**2. Watsonx Connection Failed**
- Verify your API key is correct
- Check your Project ID
- Ensure you have Watsonx.ai access in IBM Cloud
- Verify the Watsonx URL matches your region

**3. File Upload Fails**
- Check file size (max 20 MB)
- Verify file format (CSV, XLSX, XLS only)
- Ensure file has customer message column

**4. Analysis Takes Too Long**
- Reduce `max_workers` in app.py
- Use `sample_size` parameter to analyze subset
- Check your internet connection

**5. Charts Not Displaying**
- Check browser console for JavaScript errors
- Ensure Chart.js CDN is accessible
- Verify chartData is properly passed to template

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**
   - Use strong SECRET_KEY
   - Set FLASK_ENV=production
   - Secure API credentials

2. **Web Server**
   - Use Gunicorn or uWSGI
   - Configure reverse proxy (Nginx/Apache)
   - Enable HTTPS

3. **Database** (Optional Enhancement)
   - Add PostgreSQL/MySQL for persistent storage
   - Store analysis results
   - Enable user authentication

4. **Scaling**
   - Use Redis for session management
   - Implement job queue (Celery) for long analyses
   - Add caching layer

### Deployment Platforms

- **IBM Cloud**: Native integration with Watsonx.ai
- **Heroku**: Easy deployment with Procfile
- **AWS**: EC2, Elastic Beanstalk, or Lambda
- **Google Cloud**: App Engine or Cloud Run
- **Azure**: App Service

## 📈 Future Enhancements

- [ ] User authentication and multi-tenancy
- [ ] Database integration for persistent storage
- [ ] Real-time analysis with WebSockets
- [ ] Email notifications for critical tickets
- [ ] API endpoints for integration
- [ ] Scheduled reports
- [ ] Multi-language support
- [ ] Advanced analytics (cohort analysis, trends)
- [ ] Custom dashboard builder
- [ ] Integration with ticketing systems (Zendesk, Freshdesk)

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- **IBM Watsonx.ai**: AI-powered analysis using Granite models
- **Flask**: Web framework
- **Chart.js**: Interactive visualizations
- **Bootstrap 5**: UI components
- **Font Awesome**: Icons
- **ReportLab**: PDF generation

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review IBM Watsonx.ai documentation

## 🔐 Security

- Never commit `.env` file
- Keep API keys secure
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement rate limiting
- Validate all user inputs

---

**Built with ❤️ using IBM Watsonx.ai Granite Models**

*Last Updated: July 4, 2026*

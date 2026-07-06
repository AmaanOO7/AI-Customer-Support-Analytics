"""
PDF Report Generator Module
Creates professional PDF reports using ReportLab
"""

import os
import logging
from typing import Dict, Any, List
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """Generates professional PDF reports for customer support analytics"""
    
    def __init__(self):
        """Initialize PDF generator"""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading3'],
            fontSize=14,
            textColor=colors.HexColor('#2980B9'),
            spaceAfter=10,
            spaceBefore=15,
            fontName='Helvetica-Bold'
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=8,
            alignment=TA_LEFT
        ))
        
        # KPI style
        self.styles.add(ParagraphStyle(
            name='KPIValue',
            parent=self.styles['Normal'],
            fontSize=20,
            textColor=colors.HexColor('#2980B9'),
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # KPI label style
        self.styles.add(ParagraphStyle(
            name='KPILabel',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#7F8C8D'),
            alignment=TA_CENTER
        ))
    
    def generate_report(self, output_path: str, data: Dict[str, Any]) -> str:
        """
        Generate comprehensive PDF report
        
        Args:
            output_path: Path to save the PDF
            data: Dictionary containing all report data
            
        Returns:
            Path to generated PDF file
        """
        try:
            # Create PDF document
            doc = SimpleDocTemplate(
                output_path,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            # Build content
            story = []
            
            # Title page
            story.extend(self._create_title_page(data))
            story.append(PageBreak())
            
            # Executive summary
            story.extend(self._create_executive_summary(data))
            story.append(Spacer(1, 0.3*inch))
            
            # KPI Dashboard
            story.extend(self._create_kpi_section(data))
            story.append(Spacer(1, 0.3*inch))
            
            # Analytics overview
            story.extend(self._create_analytics_overview(data))
            story.append(PageBreak())
            
            # Customer insights
            story.extend(self._create_customer_insights(data))
            story.append(Spacer(1, 0.3*inch))
            
            # Agent performance
            story.extend(self._create_agent_performance(data))
            story.append(PageBreak())
            
            # Business recommendations
            story.extend(self._create_recommendations(data))
            
            # Build PDF
            doc.build(story)
            
            logger.info(f"PDF report generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating PDF report: {str(e)}")
            raise
    
    def _create_title_page(self, data: Dict[str, Any]) -> List:
        """Create title page"""
        elements = []
        
        # Add spacing
        elements.append(Spacer(1, 2*inch))
        
        # Title
        title = Paragraph("Customer Support Analytics Report", self.styles['CustomTitle'])
        elements.append(title)
        elements.append(Spacer(1, 0.5*inch))
        
        # Date
        date_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
        date_para = Paragraph(date_text, self.styles['CustomBody'])
        elements.append(date_para)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary stats
        summary = data.get('analytics_summary', {})
        total_tickets = summary.get('total_tickets', 0)
        summary_text = f"Analysis of {total_tickets} customer support tickets"
        summary_para = Paragraph(summary_text, self.styles['CustomBody'])
        elements.append(summary_para)
        
        return elements
    
    def _create_executive_summary(self, data: Dict[str, Any]) -> List:
        """Create executive summary section"""
        elements = []
        
        # Section header
        header = Paragraph("Executive Summary", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get insights
        insights = data.get('business_insights', {})
        exec_summary = insights.get('executive_summary', 'No executive summary available.')
        
        # Add summary text
        summary_para = Paragraph(exec_summary, self.styles['CustomBody'])
        elements.append(summary_para)
        
        return elements
    
    def _create_kpi_section(self, data: Dict[str, Any]) -> List:
        """Create KPI dashboard section"""
        elements = []
        
        # Section header
        header = Paragraph("Key Performance Indicators", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        # Get summary data
        summary = data.get('analytics_summary', {})
        
        # Create KPI table
        kpi_data = [
            ['Total Tickets', 'Total Customers', 'Avg Satisfaction', 'Avg Agent Score'],
            [
                str(summary.get('total_tickets', 0)),
                str(summary.get('total_customers', 0)),
                f"{summary.get('avg_customer_satisfaction', 0):.1f}%",
                f"{summary.get('avg_agent_score', 0):.1f}%"
            ],
            ['Positive Tickets', 'Negative Tickets', 'Critical Tickets', 'Escalated'],
            [
                str(summary.get('positive_tickets', 0)),
                str(summary.get('negative_tickets', 0)),
                str(summary.get('critical_tickets', 0)),
                str(summary.get('escalation_stats', {}).get('yes', 0))
            ]
        ]
        
        kpi_table = Table(kpi_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        kpi_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980B9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ECF0F1')),
            ('FONTSIZE', (0, 1), (-1, 1), 14),
            ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 1), (-1, 1), colors.HexColor('#2980B9')),
            ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#2980B9')),
            ('TEXTCOLOR', (0, 2), (-1, 2), colors.whitesmoke),
            ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 2), (-1, 2), 11),
            ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#ECF0F1')),
            ('FONTSIZE', (0, 3), (-1, 3), 14),
            ('FONTNAME', (0, 3), (-1, 3), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0, 3), (-1, 3), colors.HexColor('#2980B9')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        
        elements.append(kpi_table)
        
        return elements
    
    def _create_analytics_overview(self, data: Dict[str, Any]) -> List:
        """Create analytics overview section"""
        elements = []
        
        # Section header
        header = Paragraph("Analytics Overview", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        summary = data.get('analytics_summary', {})
        
        # Sentiment distribution
        elements.append(Paragraph("Sentiment Distribution", self.styles['SectionHeader']))
        sentiment_dist = summary.get('sentiment_distribution', {})
        if sentiment_dist:
            sentiment_data = [['Sentiment', 'Count', 'Percentage']]
            total = sum(sentiment_dist.values())
            for sentiment, count in sorted(sentiment_dist.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / total * 100) if total > 0 else 0
                sentiment_data.append([sentiment, str(count), f"{percentage:.1f}%"])
            
            sentiment_table = Table(sentiment_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            sentiment_table.setStyle(self._get_table_style())
            elements.append(sentiment_table)
            elements.append(Spacer(1, 0.2*inch))
        
        # Top complaint categories
        elements.append(Paragraph("Top Complaint Categories", self.styles['SectionHeader']))
        category_dist = summary.get('category_distribution', {})
        if category_dist:
            category_data = [['Category', 'Count', 'Percentage']]
            total = sum(category_dist.values())
            sorted_categories = sorted(category_dist.items(), key=lambda x: x[1], reverse=True)[:5]
            for category, count in sorted_categories:
                percentage = (count / total * 100) if total > 0 else 0
                category_data.append([category, str(count), f"{percentage:.1f}%"])
            
            category_table = Table(category_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            category_table.setStyle(self._get_table_style())
            elements.append(category_table)
        
        return elements
    
    def _create_customer_insights(self, data: Dict[str, Any]) -> List:
        """Create customer insights section"""
        elements = []
        
        # Section header
        header = Paragraph("Customer Insights", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        insights = data.get('business_insights', {})
        summary = data.get('analytics_summary', {})
        
        # Customer sentiment overview
        sentiment_overview = insights.get('sentiment_overview', 'No sentiment overview available.')
        elements.append(Paragraph("Sentiment Overview", self.styles['SectionHeader']))
        elements.append(Paragraph(sentiment_overview, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Churn risk analysis
        elements.append(Paragraph("Customer Churn Risk", self.styles['SectionHeader']))
        churn_dist = summary.get('churn_risk_distribution', {})
        if churn_dist:
            churn_data = [['Risk Level', 'Count']]
            for risk, count in sorted(churn_dist.items()):
                churn_data.append([risk, str(count)])
            
            churn_table = Table(churn_data, colWidths=[2.5*inch, 2*inch])
            churn_table.setStyle(self._get_table_style())
            elements.append(churn_table)
        
        return elements
    
    def _create_agent_performance(self, data: Dict[str, Any]) -> List:
        """Create agent performance section"""
        elements = []
        
        # Section header
        header = Paragraph("Agent Performance Analysis", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        summary = data.get('analytics_summary', {})
        insights = data.get('business_insights', {})
        
        # Average agent score
        avg_score = summary.get('avg_agent_score', 0)
        score_text = f"Average Agent Performance Score: {avg_score:.1f}%"
        elements.append(Paragraph(score_text, self.styles['CustomBody']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Top performing agents
        top_agents = insights.get('top_performing_agents', [])
        if top_agents:
            elements.append(Paragraph("Top Performing Agents", self.styles['SectionHeader']))
            for i, agent in enumerate(top_agents[:5], 1):
                agent_text = f"{i}. {agent}"
                elements.append(Paragraph(agent_text, self.styles['CustomBody']))
            elements.append(Spacer(1, 0.15*inch))
        
        # Low performing agents
        low_agents = insights.get('low_performing_agents', [])
        if low_agents:
            elements.append(Paragraph("Agents Needing Support", self.styles['SectionHeader']))
            for i, agent in enumerate(low_agents, 1):
                agent_text = f"{i}. {agent}"
                elements.append(Paragraph(agent_text, self.styles['CustomBody']))
        
        return elements
    
    def _create_recommendations(self, data: Dict[str, Any]) -> List:
        """Create recommendations section"""
        elements = []
        
        # Section header
        header = Paragraph("Actionable Business Recommendations", self.styles['CustomSubtitle'])
        elements.append(header)
        elements.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#2980B9')))
        elements.append(Spacer(1, 0.2*inch))
        
        insights = data.get('business_insights', {})
        recommendations = insights.get('actionable_recommendations', [])
        
        if recommendations:
            for i, recommendation in enumerate(recommendations, 1):
                rec_text = f"{i}. {recommendation}"
                elements.append(Paragraph(rec_text, self.styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))
        else:
            elements.append(Paragraph("No recommendations available.", self.styles['CustomBody']))
        
        # Business risks
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("Identified Business Risks", self.styles['SectionHeader']))
        risks = insights.get('business_risks', [])
        if risks:
            for i, risk in enumerate(risks, 1):
                risk_text = f"{i}. {risk}"
                elements.append(Paragraph(risk_text, self.styles['CustomBody']))
                elements.append(Spacer(1, 0.1*inch))
        else:
            elements.append(Paragraph("No significant risks identified.", self.styles['CustomBody']))
        
        return elements
    
    def _get_table_style(self) -> TableStyle:
        """Get standard table style"""
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2980B9')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#ECF0F1')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ])

"""
AI-Powered Analysis Module
Orchestrates comprehensive customer support analysis using IBM Watsonx
"""

import logging
from typing import Dict, Any, List, Optional
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from .watsonx_client import WatsonxClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Orchestrates AI-powered analysis of customer support data"""
    
    def __init__(self, watsonx_client: Optional[WatsonxClient] = None):
        """
        Initialize AI Analyzer
        
        Args:
            watsonx_client: Optional WatsonxClient instance
        """
        self.watsonx = watsonx_client or WatsonxClient()
    
    def analyze_single_ticket(self, row: pd.Series) -> Dict[str, Any]:
        """
        Analyze a single customer support ticket
        
        Args:
            row: DataFrame row containing ticket data
            
        Returns:
            Dictionary containing comprehensive analysis
        """
        try:
            # Extract data from row
            customer_message = str(row.get('customer_message', ''))
            agent_response = str(row.get('agent_response', ''))
            
            if not customer_message or customer_message == 'nan':
                return {'error': 'No customer message found'}
            
            # Analyze customer message
            customer_analysis = self.watsonx.analyze_customer_message(
                customer_message=customer_message,
                agent_response=agent_response if agent_response != 'nan' else ''
            )
            
            # Analyze agent response if available
            agent_analysis = {}
            if agent_response and agent_response != 'nan':
                try:
                    agent_analysis = self.watsonx.analyze_agent_response(
                        customer_message=customer_message,
                        agent_response=agent_response
                    )
                except Exception as e:
                    logger.warning(f"Agent analysis failed: {str(e)}")
                    agent_analysis = {'error': str(e)}
            
            # Combine analyses
            result = {
                'ticket_id': row.get('ticket_id', ''),
                'customer_name': row.get('customer_name', ''),
                'agent_name': row.get('agent_name', ''),
                'date': str(row.get('date', '')),
                'product': row.get('product', ''),
                'category': row.get('category', ''),
                'status': row.get('status', ''),
                'customer_message': customer_message,
                'agent_response': agent_response if agent_response != 'nan' else '',
                **customer_analysis,
                'agent_analysis': agent_analysis
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing ticket: {str(e)}")
            return {
                "ticket_id": row.get("ticket_id", ""),
                "customer_name": row.get("customer_name", ""),
                "agent_name": row.get("agent_name", ""),
                "customer_message": str(row.get("customer_message", "")),
                "agent_response": str(row.get("agent_response", "")),

                "complaint_summary": "",

                "sentiment": "Unknown",
                "emotion": "Unknown",
                "intent": "Unknown",
                "issue_category": "Unknown",

                "priority": "Unknown",
                "urgency": "Unknown",

                "customer_satisfaction_score": 0,

                "churn_risk": "Unknown",

                "escalation_needed": "No",
                "escalation_reason": "",
                "root_cause": "",

                "keywords": [],

                "agent_analysis": {},

                "error": str(e)
            }
    
    def analyze_dataset(self, df: pd.DataFrame, max_workers: int = 5, sample_size: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Analyze entire dataset with parallel processing
        
        Args:
            df: DataFrame containing customer support data
            max_workers: Maximum number of parallel workers
            sample_size: Optional limit on number of tickets to analyze
            
        Returns:
            List of analysis results
        """
        logger.info(f"Starting analysis of {len(df)} tickets")
        
        # Sample dataset if requested
        if sample_size and sample_size < len(df):
            df = df.sample(n=sample_size, random_state=42)
            logger.info(f"Analyzing sample of {sample_size} tickets")
        
        results = []
        
        # Process tickets in parallel
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.analyze_single_ticket, row): idx 
                      for idx, row in df.iterrows()}
            
            completed = 0
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    completed += 1
                    
                    if completed % 10 == 0:
                        logger.info(f"Analyzed {completed}/{len(df)} tickets")
                        
                except Exception as e:
                    logger.error(f"Error processing ticket: {str(e)}")
        
        logger.info(f"Analysis complete: {len(results)} tickets processed")
        return results
    
    def generate_analytics_summary(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics from analysis results
        
        Args:
            analysis_results: List of ticket analysis results
            
        Returns:
            Dictionary containing summary analytics
        """
        # Filter out error results
        valid_results = [r for r in analysis_results if 'error' not in r]
        
        if not valid_results:
            return {
                "total_tickets": 0,
                "total_customers": 0,

                "sentiment_distribution": {},
                "emotion_distribution": {},
                "intent_distribution": {},
                "category_distribution": {},
                "priority_distribution": {},
                "urgency_distribution": {},
                "churn_risk_distribution": {},

                "escalation_stats": {
                    "yes": 0,
                    "no": 0,
                    "percentage": 0
                },

                "avg_customer_satisfaction": 0,
                "avg_agent_score": 0,

                "agent_performance": {},
                "top_performing_agents": [],
                "low_performing_agents": [],

                "positive_tickets": 0,
                "negative_tickets": 0,
                "critical_tickets": 0,

                "error": "No valid AI analysis available"
            }
        
        # Sentiment distribution
        sentiment_counts = {}
        for result in valid_results:
            sentiment = result.get('sentiment', 'Unknown')
            sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
        
        # Emotion distribution
        emotion_counts = {}
        for result in valid_results:
            emotion = result.get('emotion', 'Unknown')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Intent distribution
        intent_counts = {}
        for result in valid_results:
            intent = result.get('intent', 'Unknown')
            intent_counts[intent] = intent_counts.get(intent, 0) + 1
        
        # Issue category distribution
        category_counts = {}
        for result in valid_results:
            category = result.get('issue_category', 'Unknown')
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Priority distribution
        priority_counts = {}
        for result in valid_results:
            priority = result.get('priority', 'Unknown')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Urgency distribution
        urgency_counts = {}
        for result in valid_results:
            urgency = result.get('urgency', 'Unknown')
            urgency_counts[urgency] = urgency_counts.get(urgency, 0) + 1
        
        # Churn risk distribution
        churn_counts = {}
        for result in valid_results:
            churn = result.get('churn_risk', 'Unknown')
            churn_counts[churn] = churn_counts.get(churn, 0) + 1
        
        # Escalation statistics
        escalation_yes = sum(1 for r in valid_results if r.get('escalation_needed') == 'Yes')
        escalation_no = sum(1 for r in valid_results if r.get('escalation_needed') == 'No')
        
        # Customer satisfaction statistics
        satisfaction_scores = [r.get('customer_satisfaction_score', 0) for r in valid_results 
                              if isinstance(r.get('customer_satisfaction_score'), (int, float))]
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
        
        # Agent performance statistics
        agent_scores = []
        for result in valid_results:
            agent_analysis = result.get('agent_analysis', {})
            if 'overall_score' in agent_analysis:
                agent_scores.append(agent_analysis['overall_score'])
        
        avg_agent_score = sum(agent_scores) / len(agent_scores) if agent_scores else 0
        
        # Agent performance by name
        agent_performance = {}
        for result in valid_results:
            agent_name = result.get('agent_name', 'Unknown')
            agent_analysis = result.get('agent_analysis', {})
            
            if agent_name and agent_name != 'Unknown' and 'overall_score' in agent_analysis:
                if agent_name not in agent_performance:
                    agent_performance[agent_name] = []
                agent_performance[agent_name].append(agent_analysis['overall_score'])
        
        # Calculate average score per agent
        agent_avg_scores = {
            agent: sum(scores) / len(scores) 
            for agent, scores in agent_performance.items()
        }
        
        # Top and low performing agents
        sorted_agents = sorted(agent_avg_scores.items(), key=lambda x: x[1], reverse=True)
        top_agents = [agent for agent, score in sorted_agents[:5]]
        low_agents = [agent for agent, score in sorted_agents[-3:]] if len(sorted_agents) > 3 else []
        
        # Compile summary
        summary = {
            'total_tickets': len(valid_results),
            'total_customers': len(set(r.get('customer_name', '') for r in valid_results if r.get('customer_name'))),
            'sentiment_distribution': sentiment_counts,
            'emotion_distribution': emotion_counts,
            'intent_distribution': intent_counts,
            'category_distribution': category_counts,
            'priority_distribution': priority_counts,
            'urgency_distribution': urgency_counts,
            'churn_risk_distribution': churn_counts,
            'escalation_stats': {
                'yes': escalation_yes,
                'no': escalation_no,
                'percentage': round((escalation_yes / len(valid_results)) * 100, 2) if valid_results else 0
            },
            'avg_customer_satisfaction': round(avg_satisfaction, 2),
            'avg_agent_score': round(avg_agent_score, 2),
            'agent_performance': agent_avg_scores,
            'top_performing_agents': top_agents,
            'low_performing_agents': low_agents,
            'positive_tickets': sentiment_counts.get('Positive', 0),
            'negative_tickets': sentiment_counts.get('Negative', 0) + sentiment_counts.get('Very Negative', 0),
            'critical_tickets': priority_counts.get('Critical', 0)
        }
        
        return summary
    
    def generate_business_insights(self, analysis_results: List[Dict[str, Any]], 
                                   analytics_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive business insights using AI
        
        Args:
            analysis_results: List of ticket analysis results
            analytics_summary: Summary analytics
            
        Returns:
            Dictionary containing business insights
        """
        try:
            # Prepare data for AI analysis
            insights_data = {
                'total_tickets': analytics_summary.get('total_tickets', 0),
                'sentiment_distribution': analytics_summary.get('sentiment_distribution', {}),
                'top_categories': dict(sorted(
                    analytics_summary.get('category_distribution', {}).items(),
                    key=lambda x: x[1],
                    reverse=True
                )[:5]),
                'escalation_rate': analytics_summary.get('escalation_stats', {}).get('percentage', 0),
                'avg_satisfaction': analytics_summary.get('avg_customer_satisfaction', 0),
                'avg_agent_score': analytics_summary.get('avg_agent_score', 0),
                'churn_risk': analytics_summary.get('churn_risk_distribution', {}),
                'top_agents': analytics_summary.get('top_performing_agents', []),
                'low_agents': analytics_summary.get('low_performing_agents', [])
            }
            
            # Generate insights using AI
            insights = self.watsonx.generate_business_insights(insights_data)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating business insights: {str(e)}")
            return {
                'error': str(e),
                'executive_summary': 'Unable to generate insights due to an error.',
                'actionable_recommendations': []
            }
    
    def get_ticket_details(self, analysis_results: List[Dict[str, Any]], 
                          ticket_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed analysis for a specific ticket
        
        Args:
            analysis_results: List of all analysis results
            ticket_id: ID of the ticket to retrieve
            
        Returns:
            Ticket analysis details or None
        """
        for result in analysis_results:
            if str(result.get('ticket_id', '')) == str(ticket_id):
                return result
        return None
    
    def get_time_series_data(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate time series data for trends analysis
        
        Args:
            analysis_results: List of ticket analysis results
            
        Returns:
            Dictionary containing time series data
        """
        try:
            # Convert to DataFrame for easier processing
            df = pd.DataFrame(analysis_results)
            
            if 'date' not in df.columns or df['date'].isna().all():
                return {'error': 'No date information available'}
            
            # Parse dates
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            df = df.dropna(subset=['date'])
            
            # Monthly trends
            df['month'] = df['date'].dt.to_period('M')
            monthly_counts = df.groupby('month').size().to_dict()
            monthly_counts = {str(k): v for k, v in monthly_counts.items()}
            
            # Weekly trends
            df['week'] = df['date'].dt.to_period('W')
            weekly_counts = df.groupby('week').size().to_dict()
            weekly_counts = {str(k): v for k, v in weekly_counts.items()}
            
            # Sentiment trends over time
            sentiment_trends = df.groupby(['month', 'sentiment']).size().unstack(fill_value=0).to_dict()
            
            return {
                'monthly_trends': monthly_counts,
                'weekly_trends': weekly_counts,
                'sentiment_trends': sentiment_trends
            }
            
        except Exception as e:
            logger.error(f"Error generating time series data: {str(e)}")
            return {'error': str(e)}

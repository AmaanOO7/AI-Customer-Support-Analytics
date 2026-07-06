"""
IBM Watsonx.ai Client for AI-powered analysis using Granite models
"""

import os
import json
import logging
from typing import Dict, Any, Optional
import requests
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WatsonxClient:
    """Client for interacting with IBM Watsonx.ai Granite models"""
    
    def __init__(self):
        """Initialize Watsonx client with credentials from environment"""
        self.api_key = os.getenv('IBM_CLOUD_API_KEY')
        self.project_id = os.getenv('WATSONX_PROJECT_ID')
        self.url = os.getenv('WATSONX_URL', 'https://us-south.ml.cloud.ibm.com')
        self.model_id = os.getenv('MODEL_ID', 'bm/granite-4-h-small')
        
        if not self.api_key or not self.project_id:
            raise ValueError("IBM_CLOUD_API_KEY and WATSONX_PROJECT_ID must be set in environment")
        
        self.credentials = Credentials(
            url=self.url,
            api_key=self.api_key
            )
        
        self.model_params = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 2000,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TEMPERATURE: 0.7,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1,
            GenParams.REPETITION_PENALTY: 1.1
        }
        
        logger.info(f"Watsonx client initialized with model: {self.model_id}")
    
    def _create_model(self) -> Model:
        """Create a new model instance"""
        return ModelInference(
            model_id=self.model_id,
            params=self.model_params,
            credentials=self.credentials,
            project_id=self.project_id
        )
    
    def generate_text(self, prompt: str, max_tokens: int = 2000) -> str:
        """
        Generate text using IBM Granite model
        
        Args:
            prompt: Input prompt for the model
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        try:
            params = self.model_params.copy()
            params[GenParams.MAX_NEW_TOKENS] = max_tokens
            
            model = ModelInference(
                model_id=self.model_id,
                params=params,
                credentials=self.credentials,
                project_id=self.project_id
            )
            
            response = model.generate(prompt=prompt)
                return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating text: {str(e)}")
            raise
    
    def generate_json_response(self, prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Generate JSON response using IBM Granite model
        
        Args:
            prompt: Input prompt requesting JSON output
            max_tokens: Maximum tokens to generate
            
        Returns:
            Parsed JSON response as dictionary
        """
        try:
            response_text = self.generate_text(prompt, max_tokens)
            
            # Extract JSON from response (handle markdown code blocks)
            json_text = response_text
            if "```json" in response_text:
                json_text = response_text.split("```json")[1].split("```")[0].strip()
            elif "```" in response_text:
                json_text = response_text.split("```")[1].split("```")[0].strip()
            
            # Try to parse JSON
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                # If direct parsing fails, try to find JSON object in text
                start_idx = json_text.find('{')
                end_idx = json_text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    json_text = json_text[start_idx:end_idx+1]
                    return json.loads(json_text)
                raise
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            logger.error(f"Response text: {response_text}")
            raise ValueError(f"Invalid JSON response from model: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating JSON response: {str(e)}")
            raise
    
    def analyze_customer_message(self, customer_message: str, agent_response: str = "") -> Dict[str, Any]:
        """
        Analyze customer support message using AI

        Args:
            customer_message: Customer's message/complaint
            agent_response: Agent's response (optional)

        Returns:
            Dictionary containing comprehensive analysis
        """

        agent_section = ""

        if agent_response:
            agent_section = "Agent Response:\n" + agent_response + "\n"

        prompt = f"""You are an expert customer support analyst. Analyze the following customer support conversation and provide a comprehensive analysis in strict JSON format.

Customer Message:
{customer_message}

{agent_section}

Provide your analysis in the following JSON structure (respond ONLY with valid JSON, no additional text):

{{
  "complaint_summary": "Brief summary of the customer's issue",
  "sentiment": "Positive|Neutral|Negative|Very Negative",
  "emotion": "Angry|Frustrated|Satisfied|Happy|Confused|Disappointed|Excited",
  "intent": "Refund Request|Order Status|Complaint|Technical Issue|Billing Issue|Subscription|Cancellation|Feature Request|Product Inquiry|Payment Issue|Account Issue|General Inquiry",
  "issue_category": "Shipping|Delivery|Billing|Payment|Website|Mobile App|Technical|Account|Product Quality|Refund|Subscription|Other",
  "priority": "Low|Medium|High|Critical",
  "urgency": "Low|Medium|High|Critical",
  "customer_satisfaction_score": 75,
  "churn_risk": "Low|Medium|High",
  "escalation_needed": "Yes|No",
  "escalation_reason": "Reason if escalation is needed, otherwise empty string",
  "root_cause": "Identified root cause of the issue",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Respond with ONLY the JSON object, no markdown formatting or additional text."""

        return self.generate_json_response(prompt, max_tokens=1500)
    
    def analyze_agent_response(self, customer_message: str, agent_response: str) -> Dict[str, Any]:
        """
        Analyze agent's response quality
        
        Args:
            customer_message: Customer's message
            agent_response: Agent's response
            
        Returns:
            Dictionary containing agent performance analysis
        """
        prompt = f"""You are an expert in customer service quality assessment. Analyze the agent's response to the customer and provide detailed feedback in strict JSON format.

Customer Message:
{customer_message}

Agent Response:
{agent_response}

Evaluate the agent's response and provide your analysis in the following JSON structure (respond ONLY with valid JSON, no additional text):

{{
  "professionalism_score": 85,
  "empathy_score": 80,
  "grammar_score": 90,
  "clarity_score": 85,
  "resolution_quality_score": 75,
  "friendliness_score": 88,
  "overall_score": 84,
  "strengths": ["strength1", "strength2", "strength3"],
  "weaknesses": ["weakness1", "weakness2"],
  "improvements": ["improvement1", "improvement2"],
  "improved_response": "A professionally improved version of the agent's response that addresses all weaknesses while maintaining the core message"
}}

All scores should be between 0-100. Respond with ONLY the JSON object, no markdown formatting or additional text."""

        return self.generate_json_response(prompt, max_tokens=1500)
    
    def generate_business_insights(self, analytics_summary: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive business insights from analytics data
        
        Args:
            analytics_summary: Summary of all analytics data
            
        Returns:
            Dictionary containing business insights and recommendations
        """
        prompt = f"""You are a senior business analyst specializing in customer support operations. Based on the following customer support analytics data, provide comprehensive business insights and actionable recommendations in strict JSON format.

Analytics Summary:
{json.dumps(analytics_summary, indent=2)}

Provide your analysis in the following JSON structure (respond ONLY with valid JSON, no additional text):

{{
  "executive_summary": "Comprehensive executive summary of the customer support performance and key findings",
  "top_complaint_categories": ["category1", "category2", "category3"],
  "most_common_issues": ["issue1", "issue2", "issue3"],
  "sentiment_overview": "Overall sentiment analysis and trends",
  "business_risks": ["risk1", "risk2", "risk3"],
  "operational_bottlenecks": ["bottleneck1", "bottleneck2"],
  "top_performing_agents": ["agent1", "agent2", "agent3"],
  "low_performing_agents": ["agent1", "agent2"],
  "actionable_recommendations": [
    "recommendation1",
    "recommendation2",
    "recommendation3",
    "recommendation4",
    "recommendation5"
  ],
  "monthly_trends": "Analysis of monthly trends",
  "weekly_trends": "Analysis of weekly trends",
  "customer_satisfaction_trends": "Analysis of customer satisfaction trends",
  "escalation_trends": "Analysis of escalation patterns",
  "resolution_performance": "Analysis of resolution time and quality"
}}

Respond with ONLY the JSON object, no markdown formatting or additional text."""

        return self.generate_json_response(prompt, max_tokens=2000)
    
    def test_connection(self) -> bool:
        """
        Test connection to Watsonx.ai
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.generate_text("Hello, this is a test.", max_tokens=50)
            logger.info("Watsonx connection test successful")
            return True
        except Exception as e:
            logger.error(f"Watsonx connection test failed: {str(e)}")
            return False

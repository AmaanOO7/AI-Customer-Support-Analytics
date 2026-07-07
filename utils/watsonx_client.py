"""
IBM Watsonx.ai Client
Compatible with ibm-watsonx-ai==1.1.20
"""

import os
import json
import logging
from typing import Dict, Any

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WatsonxClient:

    def __init__(self):

        self.api_key = os.getenv("IBM_CLOUD_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.url = os.getenv(
            "WATSONX_URL",
            "https://us-south.ml.cloud.ibm.com"
        )

        self.model_id = os.getenv(
            "MODEL_ID",
            "ibm/granite-4-h-small"
        )

        if not self.api_key:
            raise ValueError("IBM_CLOUD_API_KEY not found")

        if not self.project_id:
            raise ValueError("WATSONX_PROJECT_ID not found")

        self.credentials = Credentials(
            url=self.url,
            api_key=self.api_key
        )

        self.params = {
            GenParams.DECODING_METHOD: "greedy",
            GenParams.MAX_NEW_TOKENS: 1500,
            GenParams.MIN_NEW_TOKENS: 1,
            GenParams.TEMPERATURE: 0.5,
            GenParams.TOP_K: 50,
            GenParams.TOP_P: 1,
            GenParams.REPETITION_PENALTY: 1.1
        }

        logger.info("Watsonx initialized successfully")

    def _model(self):

        return ModelInference(
            model_id=self.model_id,
            credentials=self.credentials,
            project_id=self.project_id,
            params=self.params
        )

    def generate_text(self, prompt: str, max_tokens: int = 1500) -> str:

        params = self.params.copy()
        params[GenParams.MAX_NEW_TOKENS] = max_tokens

        model = ModelInference(
            model_id=self.model_id,
            credentials=self.credentials,
            project_id=self.project_id,
            params=params
        )

        response = model.generate(prompt=prompt)

        return response["results"][0]["generated_text"].strip()

    def generate_json_response(
        self,
        prompt: str,
        max_tokens: int = 1500
    ) -> Dict[str, Any]:

        response = self.generate_text(prompt, max_tokens)

        if "```json" in response:
            response = response.split("```json")[1].split("```")[0]

        elif "```" in response:
            response = response.split("```")[1].split("```")[0]

        response = response.strip()

        try:
            return json.loads(response)

        except Exception:

            start = response.find("{")
            end = response.rfind("}")

            if start != -1 and end != -1:
                return json.loads(response[start:end + 1])

            raise

    def analyze_customer_message(
        self,
        customer_message: str,
        agent_response: str = ""
    ) -> Dict[str, Any]:

        prompt = f"""
You are an expert customer support analyst.

Customer Message:
{customer_message}

Agent Response:
{agent_response}

Return ONLY valid JSON.

{{
"complaint_summary":"",
"sentiment":"",
"emotion":"",
"intent":"",
"issue_category":"",
"priority":"",
"urgency":"",
"customer_satisfaction_score":80,
"churn_risk":"",
"escalation_needed":"",
"escalation_reason":"",
"root_cause":"",
"keywords":[]
}}
"""

        return self.generate_json_response(prompt)

    def analyze_agent_response(
        self,
        customer_message: str,
        agent_response: str
    ) -> Dict[str, Any]:

        prompt = f"""
Customer:
{customer_message}

Agent:
{agent_response}

Return ONLY JSON.

{{
"professionalism_score":0,
"empathy_score":0,
"grammar_score":0,
"clarity_score":0,
"resolution_quality_score":0,
"friendliness_score":0,
"overall_score":0,
"strengths":[],
"weaknesses":[],
"improvements":[],
"improved_response":""
}}
"""

        return self.generate_json_response(prompt)

    def generate_business_insights(
        self,
        analytics_summary: Dict[str, Any]
    ) -> Dict[str, Any]:

        prompt = f"""
Analytics

{json.dumps(analytics_summary)}

Return ONLY JSON.

{{
"executive_summary":"",
"top_complaint_categories":[],
"most_common_issues":[],
"sentiment_overview":"",
"business_risks":[],
"operational_bottlenecks":[],
"top_performing_agents":[],
"low_performing_agents":[],
"actionable_recommendations":[],
"monthly_trends":"",
"weekly_trends":"",
"customer_satisfaction_trends":"",
"escalation_trends":"",
"resolution_performance":""
}}
"""

        return self.generate_json_response(prompt)

    def test_connection(self):

        try:

            text = self.generate_text("Say Hello")

            logger.info(text)

            return True

        except Exception as e:

            logger.error(e)

            return False

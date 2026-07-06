"""
Chart Data Generator Module
Prepares data for Chart.js visualizations
"""

import logging
from typing import Dict, Any, List
from collections import Counter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChartDataGenerator:
    """Generates data structures for Chart.js visualizations"""
    
    @staticmethod
    def generate_sentiment_chart(sentiment_distribution: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate pie chart data for sentiment distribution
        
        Args:
            sentiment_distribution: Dictionary of sentiment counts
            
        Returns:
            Chart.js compatible data structure
        """
        labels = list(sentiment_distribution.keys())
        data = list(sentiment_distribution.values())
        
        # Color mapping for sentiments
        color_map = {
            'Positive': '#27AE60',
            'Neutral': '#3498DB',
            'Negative': '#E67E22',
            'Very Negative': '#E74C3C'
        }
        
        colors = [color_map.get(label, '#95A5A6') for label in labels]
        
        return {
            'type': 'pie',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': colors,
                    'borderWidth': 2,
                    'borderColor': '#FFFFFF'
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom',
                        'labels': {
                            'padding': 15,
                            'font': {
                                'size': 12
                            }
                        }
                    },
                    'title': {
                        'display': True,
                        'text': 'Customer Sentiment Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_emotion_chart(emotion_distribution: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate bar chart data for emotion distribution
        
        Args:
            emotion_distribution: Dictionary of emotion counts
            
        Returns:
            Chart.js compatible data structure
        """
        # Sort by count descending
        sorted_emotions = sorted(emotion_distribution.items(), key=lambda x: x[1], reverse=True)
        labels = [item[0] for item in sorted_emotions]
        data = [item[1] for item in sorted_emotions]
        
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Number of Tickets',
                    'data': data,
                    'backgroundColor': '#9B59B6',
                    'borderColor': '#8E44AD',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'display': False
                    },
                    'title': {
                        'display': True,
                        'text': 'Customer Emotion Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_category_chart(category_distribution: Dict[str, int], top_n: int = 10) -> Dict[str, Any]:
        """
        Generate horizontal bar chart for issue categories
        
        Args:
            category_distribution: Dictionary of category counts
            top_n: Number of top categories to display
            
        Returns:
            Chart.js compatible data structure
        """
        # Sort and get top N
        sorted_categories = sorted(category_distribution.items(), key=lambda x: x[1], reverse=True)[:top_n]
        labels = [item[0] for item in sorted_categories]
        data = [item[1] for item in sorted_categories]
        
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Number of Tickets',
                    'data': data,
                    'backgroundColor': '#3498DB',
                    'borderColor': '#2980B9',
                    'borderWidth': 1
                }]
            },
            'options': {
                'indexAxis': 'y',
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'display': False
                    },
                    'title': {
                        'display': True,
                        'text': f'Top {len(labels)} Issue Categories',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                },
                'scales': {
                    'x': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_priority_chart(priority_distribution: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate doughnut chart for priority distribution
        
        Args:
            priority_distribution: Dictionary of priority counts
            
        Returns:
            Chart.js compatible data structure
        """
        # Define priority order
        priority_order = ['Low', 'Medium', 'High', 'Critical']
        labels = []
        data = []
        
        for priority in priority_order:
            if priority in priority_distribution:
                labels.append(priority)
                data.append(priority_distribution[priority])
        
        colors = {
            'Low': '#27AE60',
            'Medium': '#F39C12',
            'High': '#E67E22',
            'Critical': '#E74C3C'
        }
        
        background_colors = [colors.get(label, '#95A5A6') for label in labels]
        
        return {
            'type': 'doughnut',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': background_colors,
                    'borderWidth': 2,
                    'borderColor': '#FFFFFF'
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom',
                        'labels': {
                            'padding': 15,
                            'font': {
                                'size': 12
                            }
                        }
                    },
                    'title': {
                        'display': True,
                        'text': 'Priority Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_urgency_chart(urgency_distribution: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate doughnut chart for urgency distribution
        
        Args:
            urgency_distribution: Dictionary of urgency counts
            
        Returns:
            Chart.js compatible data structure
        """
        urgency_order = ['Low', 'Medium', 'High', 'Critical']
        labels = []
        data = []
        
        for urgency in urgency_order:
            if urgency in urgency_distribution:
                labels.append(urgency)
                data.append(urgency_distribution[urgency])
        
        colors = {
            'Low': '#3498DB',
            'Medium': '#9B59B6',
            'High': '#E67E22',
            'Critical': '#C0392B'
        }
        
        background_colors = [colors.get(label, '#95A5A6') for label in labels]
        
        return {
            'type': 'doughnut',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': background_colors,
                    'borderWidth': 2,
                    'borderColor': '#FFFFFF'
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom',
                        'labels': {
                            'padding': 15,
                            'font': {
                                'size': 12
                            }
                        }
                    },
                    'title': {
                        'display': True,
                        'text': 'Urgency Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_satisfaction_chart(analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate line chart for customer satisfaction scores
        
        Args:
            analysis_results: List of ticket analysis results
            
        Returns:
            Chart.js compatible data structure
        """
        # Extract satisfaction scores
        scores = []
        for result in analysis_results:
            score = result.get('customer_satisfaction_score')
            if isinstance(score, (int, float)):
                scores.append(score)
        
        if not scores:
            return {'error': 'No satisfaction data available'}
        
        # Create bins for histogram
        bins = [0, 20, 40, 60, 80, 100]
        bin_labels = ['0-20', '21-40', '41-60', '61-80', '81-100']
        bin_counts = [0] * len(bin_labels)
        
        for score in scores:
            for i, bin_max in enumerate(bins[1:]):
                if score <= bin_max:
                    bin_counts[i] += 1
                    break
        
        return {
            'type': 'bar',
            'data': {
                'labels': bin_labels,
                'datasets': [{
                    'label': 'Number of Tickets',
                    'data': bin_counts,
                    'backgroundColor': '#1ABC9C',
                    'borderColor': '#16A085',
                    'borderWidth': 1
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'display': False
                    },
                    'title': {
                        'display': True,
                        'text': 'Customer Satisfaction Score Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                },
                'scales': {
                    'y': {
                        'beginAtZero': True,
                        'ticks': {
                            'stepSize': 1
                        }
                    },
                    'x': {
                        'title': {
                            'display': True,
                            'text': 'Satisfaction Score Range'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_agent_performance_chart(agent_performance: Dict[str, float], top_n: int = 10) -> Dict[str, Any]:
        """
        Generate bar chart for agent performance
        
        Args:
            agent_performance: Dictionary of agent names and scores
            top_n: Number of top agents to display
            
        Returns:
            Chart.js compatible data structure
        """
        # Sort by score descending
        sorted_agents = sorted(agent_performance.items(), key=lambda x: x[1], reverse=True)[:top_n]
        labels = [item[0] for item in sorted_agents]
        data = [round(item[1], 2) for item in sorted_agents]
        
        # Color based on performance
        colors = []
        for score in data:
            if score >= 80:
                colors.append('#27AE60')
            elif score >= 60:
                colors.append('#F39C12')
            else:
                colors.append('#E74C3C')
        
        return {
            'type': 'bar',
            'data': {
                'labels': labels,
                'datasets': [{
                    'label': 'Performance Score',
                    'data': data,
                    'backgroundColor': colors,
                    'borderWidth': 1
                }]
            },
            'options': {
                'indexAxis': 'y',
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'display': False
                    },
                    'title': {
                        'display': True,
                        'text': f'Top {len(labels)} Agent Performance',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                },
                'scales': {
                    'x': {
                        'beginAtZero': True,
                        'max': 100,
                        'title': {
                            'display': True,
                            'text': 'Performance Score'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_churn_risk_chart(churn_distribution: Dict[str, int]) -> Dict[str, Any]:
        """
        Generate pie chart for churn risk distribution
        
        Args:
            churn_distribution: Dictionary of churn risk counts
            
        Returns:
            Chart.js compatible data structure
        """
        risk_order = ['Low', 'Medium', 'High']
        labels = []
        data = []
        
        for risk in risk_order:
            if risk in churn_distribution:
                labels.append(risk)
                data.append(churn_distribution[risk])
        
        colors = {
            'Low': '#27AE60',
            'Medium': '#F39C12',
            'High': '#E74C3C'
        }
        
        background_colors = [colors.get(label, '#95A5A6') for label in labels]
        
        return {
            'type': 'pie',
            'data': {
                'labels': labels,
                'datasets': [{
                    'data': data,
                    'backgroundColor': background_colors,
                    'borderWidth': 2,
                    'borderColor': '#FFFFFF'
                }]
            },
            'options': {
                'responsive': True,
                'maintainAspectRatio': False,
                'plugins': {
                    'legend': {
                        'position': 'bottom',
                        'labels': {
                            'padding': 15,
                            'font': {
                                'size': 12
                            }
                        }
                    },
                    'title': {
                        'display': True,
                        'text': 'Customer Churn Risk Distribution',
                        'font': {
                            'size': 16,
                            'weight': 'bold'
                        }
                    }
                }
            }
        }
    
    @staticmethod
    def generate_all_charts(analytics_summary: Dict[str, Any], analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate all chart data at once
        
        Args:
            analytics_summary: Summary analytics data
            analysis_results: List of ticket analysis results
            
        Returns:
            Dictionary containing all chart configurations
        """
        charts = {}
        
        # Sentiment chart
        if 'sentiment_distribution' in analytics_summary:
            charts['sentiment'] = ChartDataGenerator.generate_sentiment_chart(
                analytics_summary['sentiment_distribution']
            )
        
        # Emotion chart
        if 'emotion_distribution' in analytics_summary:
            charts['emotion'] = ChartDataGenerator.generate_emotion_chart(
                analytics_summary['emotion_distribution']
            )
        
        # Category chart
        if 'category_distribution' in analytics_summary:
            charts['category'] = ChartDataGenerator.generate_category_chart(
                analytics_summary['category_distribution']
            )
        
        # Priority chart
        if 'priority_distribution' in analytics_summary:
            charts['priority'] = ChartDataGenerator.generate_priority_chart(
                analytics_summary['priority_distribution']
            )
        
        # Urgency chart
        if 'urgency_distribution' in analytics_summary:
            charts['urgency'] = ChartDataGenerator.generate_urgency_chart(
                analytics_summary['urgency_distribution']
            )
        
        # Satisfaction chart
        if analysis_results:
            charts['satisfaction'] = ChartDataGenerator.generate_satisfaction_chart(
                analysis_results
            )
        
        # Agent performance chart
        if 'agent_performance' in analytics_summary:
            charts['agent_performance'] = ChartDataGenerator.generate_agent_performance_chart(
                analytics_summary['agent_performance']
            )
        
        # Churn risk chart
        if 'churn_risk_distribution' in analytics_summary:
            charts['churn_risk'] = ChartDataGenerator.generate_churn_risk_chart(
                analytics_summary['churn_risk_distribution']
            )
        
        return charts

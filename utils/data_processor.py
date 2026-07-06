"""
Data Processing and Validation Module
Handles dataset loading, validation, preprocessing, and profiling
"""

import os
import logging
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np
from datetime import datetime
from werkzeug.utils import secure_filename

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles all data processing operations for customer support datasets"""
    
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
    MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
    
    # Expected column mappings (flexible matching)
    COLUMN_MAPPINGS = {
        'ticket_id': ['ticket_id', 'ticket id', 'id', 'ticket', 'case_id', 'case id'],
        'customer_message': ['customer_message', 'customer message', 'message', 'customer_text', 'complaint', 'issue', 'description'],
        'agent_response': ['agent_response', 'agent response', 'response', 'agent_message', 'reply', 'agent_reply'],
        'agent_name': ['agent_name', 'agent name', 'agent', 'representative', 'rep_name'],
        'customer_name': ['customer_name', 'customer name', 'customer', 'client_name', 'client'],
        'date': ['date', 'created_date', 'created date', 'timestamp', 'created_at', 'date_created'],
        'product': ['product', 'product_name', 'product name', 'item', 'service'],
        'category': ['category', 'issue_category', 'issue category', 'type', 'issue_type'],
        'resolution_time': ['resolution_time', 'resolution time', 'time_to_resolve', 'resolution_hours', 'response_time'],
        'status': ['status', 'ticket_status', 'ticket status', 'state', 'resolution_status'],
        'customer_rating': ['customer_rating', 'customer rating', 'rating', 'satisfaction', 'score', 'csat']
    }
    
    def __init__(self, upload_folder: str = 'uploads'):
        """
        Initialize DataProcessor
        
        Args:
            upload_folder: Directory for uploaded files
        """
        self.upload_folder = upload_folder
        os.makedirs(upload_folder, exist_ok=True)
    
    @staticmethod
    def allowed_file(filename: str) -> bool:
        """
        Check if file extension is allowed
        
        Args:
            filename: Name of the file
            
        Returns:
            True if file extension is allowed
        """
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in DataProcessor.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file_size(file_path: str) -> bool:
        """
        Validate file size
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if file size is within limit
        """
        file_size = os.path.getsize(file_path)
        return file_size <= DataProcessor.MAX_FILE_SIZE
    
    def load_dataset(self, file_path: str) -> pd.DataFrame:
        """
        Load dataset from file
        
        Args:
            file_path: Path to the dataset file
            
        Returns:
            Pandas DataFrame
        """
        try:
            file_extension = file_path.rsplit('.', 1)[1].lower()
            
            if file_extension == 'csv':
                df = pd.read_csv(file_path, encoding='utf-8')
            elif file_extension in ['xlsx', 'xls']:
                df = pd.read_excel(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
            
            logger.info(f"Dataset loaded successfully: {len(df)} rows, {len(df.columns)} columns")
            return df
            
        except Exception as e:
            logger.error(f"Error loading dataset: {str(e)}")
            raise
    
    def normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize column names to standard format
        
        Args:
            df: Input DataFrame
            
        Returns:
            DataFrame with normalized column names
        """
        normalized_df = df.copy()
        column_mapping = {}
        
        for standard_name, variations in self.COLUMN_MAPPINGS.items():
            for col in normalized_df.columns:
                if col.lower().strip() in variations:
                    column_mapping[col] = standard_name
                    break
        
        if column_mapping:
            normalized_df = normalized_df.rename(columns=column_mapping)
            logger.info(f"Normalized columns: {column_mapping}")
        
        return normalized_df
    
    def profile_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive dataset profile
        
        Args:
            df: Input DataFrame
            
        Returns:
            Dictionary containing dataset statistics and profile
        """
        profile = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'missing_values': {},
            'duplicate_rows': int(df.duplicated().sum()),
            'empty_rows': 0,
            'data_types': {},
            'statistics': {},
            'sample_data': []
        }
        
        # Missing values analysis
        for col in df.columns:
            missing_count = int(df[col].isna().sum())
            if missing_count > 0:
                profile['missing_values'][col] = {
                    'count': missing_count,
                    'percentage': round((missing_count / len(df)) * 100, 2)
                }
        
        # Empty rows (all values are NaN)
        profile['empty_rows'] = int(df.isna().all(axis=1).sum())
        
        # Data types
        for col in df.columns:
            profile['data_types'][col] = str(df[col].dtype)
        
        # Statistics for key columns
        if 'ticket_id' in df.columns:
            profile['statistics']['total_tickets'] = int(df['ticket_id'].nunique())
        
        if 'customer_name' in df.columns:
            profile['statistics']['total_customers'] = int(df['customer_name'].nunique())
        
        if 'resolution_time' in df.columns:
            try:
                avg_resolution = df['resolution_time'].mean()
                if pd.notna(avg_resolution):
                    profile['statistics']['avg_resolution_time'] = round(float(avg_resolution), 2)
            except:
                pass
        
        if 'agent_name' in df.columns:
            profile['statistics']['total_agents'] = int(df['agent_name'].nunique())
        
        if 'status' in df.columns:
            profile['statistics']['status_distribution'] = df['status'].value_counts().to_dict()
        
        # Sample data (first 5 rows)
        profile['sample_data'] = df.head(5).fillna('').to_dict('records')
        
        return profile
    
    def clean_dataset(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess dataset
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        cleaned_df = df.copy()
        
        # Remove completely empty rows
        cleaned_df = cleaned_df.dropna(how='all')
        
        # Remove duplicate rows
        cleaned_df = cleaned_df.drop_duplicates()
        
        # Strip whitespace from string columns
        for col in cleaned_df.select_dtypes(include=['object']).columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            cleaned_df[col] = cleaned_df[col].replace('nan', '')
            cleaned_df[col] = cleaned_df[col].replace('', np.nan)
        
        # Parse date columns
        if 'date' in cleaned_df.columns:
            try:
                cleaned_df['date'] = pd.to_datetime(cleaned_df['date'], errors='coerce')
            except:
                pass
        
        # Convert numeric columns
        if 'resolution_time' in cleaned_df.columns:
            try:
                cleaned_df['resolution_time'] = pd.to_numeric(cleaned_df['resolution_time'], errors='coerce')
            except:
                pass
        
        if 'customer_rating' in cleaned_df.columns:
            try:
                cleaned_df['customer_rating'] = pd.to_numeric(cleaned_df['customer_rating'], errors='coerce')
            except:
                pass
        
        logger.info(f"Dataset cleaned: {len(df)} -> {len(cleaned_df)} rows")
        return cleaned_df
    
    def validate_dataset(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate dataset has minimum required columns
        
        Args:
            df: Input DataFrame
            
        Returns:
            Tuple of (is_valid, list of warnings/errors)
        """
        warnings = []
        
        # Check for customer message column (essential)
        has_customer_message = any(col in df.columns for col in ['customer_message', 'message', 'complaint', 'issue'])
        
        if not has_customer_message:
            warnings.append("Warning: No customer message column found. Analysis may be limited.")
        
        # Check for other important columns
        if 'agent_response' not in df.columns:
            warnings.append("Info: No agent response column found. Agent analysis will be skipped.")
        
        if 'date' not in df.columns:
            warnings.append("Info: No date column found. Time-based analysis will be limited.")
        
        if 'agent_name' not in df.columns:
            warnings.append("Info: No agent name column found. Agent performance analysis will be limited.")
        
        # Dataset must have at least customer messages to be valid
        is_valid = has_customer_message and len(df) > 0
        
        if len(df) == 0:
            warnings.append("Error: Dataset is empty.")
            is_valid = False
        
        return is_valid, warnings
    
    def prepare_for_analysis(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Complete pipeline: load, normalize, clean, profile, and validate dataset
        
        Args:
            file_path: Path to the dataset file
            
        Returns:
            Tuple of (cleaned DataFrame, profile dictionary)
        """
        # Load dataset
        df = self.load_dataset(file_path)
        
        # Normalize column names
        df = self.normalize_columns(df)
        
        # Clean dataset
        df = self.clean_dataset(df)
        
        # Validate dataset
        is_valid, warnings = self.validate_dataset(df)
        
        # Generate profile
        profile = self.profile_dataset(df)
        profile['is_valid'] = is_valid
        profile['warnings'] = warnings
        
        return df, profile
    
    def get_filtered_data(self, df: pd.DataFrame, filters: Dict[str, Any]) -> pd.DataFrame:
        """
        Apply filters to dataset
        
        Args:
            df: Input DataFrame
            filters: Dictionary of filter criteria
            
        Returns:
            Filtered DataFrame
        """
        filtered_df = df.copy()
        
        # Date range filter
        if 'start_date' in filters and 'date' in filtered_df.columns:
            try:
                start_date = pd.to_datetime(filters['start_date'])
                filtered_df = filtered_df[filtered_df['date'] >= start_date]
            except:
                pass
        
        if 'end_date' in filters and 'date' in filtered_df.columns:
            try:
                end_date = pd.to_datetime(filters['end_date'])
                filtered_df = filtered_df[filtered_df['date'] <= end_date]
            except:
                pass
        
        # Categorical filters
        for col in ['sentiment', 'emotion', 'priority', 'urgency', 'category', 'agent_name', 'product', 'customer_name']:
            if col in filters and filters[col] and col in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[col] == filters[col]]
        
        # Keyword search
        if 'keyword' in filters and filters['keyword']:
            keyword = filters['keyword'].lower()
            mask = pd.Series([False] * len(filtered_df))
            
            for col in ['customer_message', 'agent_response', 'complaint_summary']:
                if col in filtered_df.columns:
                    mask |= filtered_df[col].astype(str).str.lower().str.contains(keyword, na=False)
            
            filtered_df = filtered_df[mask]
        
        return filtered_df
    
    def get_unique_values(self, df: pd.DataFrame, column: str) -> List[str]:
        """
        Get unique values from a column
        
        Args:
            df: Input DataFrame
            column: Column name
            
        Returns:
            List of unique values
        """
        if column in df.columns:
            unique_vals = df[column].dropna().unique().tolist()
            return sorted([str(val) for val in unique_vals if val])
        return []

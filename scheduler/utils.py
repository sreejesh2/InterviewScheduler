from datetime import datetime, tzinfo
from typing import List, Tuple, Dict, Any
import pytz
from utils import logger

logger = logger.get_logger("DatetimeUtils")

def format_datetime(dt: datetime, tz: tzinfo, fmt: str) -> str:
    """
    Format a datetime object to a specific timezone and format.

    """
    try:
        formatted_date = dt.astimezone(tz).strftime(fmt)
        logger.info(f"Formatted datetime {dt} to {formatted_date} in timezone {tz} with format {fmt}")
        return formatted_date
    except Exception as e:
        logger.error(f"Error formatting datetime {dt}: {str(e)}")
        raise


def convert_to_utc_and_kolkata(start_utc: datetime, end_utc: datetime) -> Dict[str, List[str]]:
    """
    Convert a datetime range from UTC to both UTC and Kolkata timezones in multiple formats.

    """
    try:
        kolkata_tz = pytz.timezone('Asia/Kolkata')
        
        # Define formats
        format_24 = '%Y-%m-%d %H:%M %Z'
        format_12 = '%Y-%m-%d %I:%M %p %Z'
        
        # Format the datetime objects
        formatted_dates = {
            "utc_24": [format_datetime(start_utc, pytz.utc, format_24), format_datetime(end_utc, pytz.utc, format_24)],
            "kolkata_24": [format_datetime(start_utc, kolkata_tz, format_24), format_datetime(end_utc, kolkata_tz, format_24)],
            "utc_12": [format_datetime(start_utc, pytz.utc, format_12), format_datetime(end_utc, pytz.utc, format_12)],
            "kolkata_12": [format_datetime(start_utc, kolkata_tz, format_12), format_datetime(end_utc, kolkata_tz, format_12)]
        }
        
        logger.info(f"Converted datetime range {start_utc} - {end_utc} to multiple formats")
        return formatted_dates
    except Exception as e:
        logger.error(f"Error converting datetime range {start_utc} - {end_utc}: {str(e)}")
        raise


def convert_to_readable_format(datetime_ranges: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
    """
    Convert a list of datetime ranges from ISO format to readable formats in both UTC and Kolkata timezones.

    """
    try:
        readable_format = [
            convert_to_utc_and_kolkata(datetime.fromisoformat(start_str), datetime.fromisoformat(end_str))
            for start_str, end_str in datetime_ranges
        ]
        
        logger.info(f"Converted datetime ranges to readable format: {datetime_ranges}")
        return readable_format
    except Exception as e:
        logger.error(f"Error converting datetime ranges to readable format: {str(e)}")
        raise

from typing import Optional, Dict
import logging
from dataclasses import dataclass
from datetime import datetime

@dataclass
class OptimizationError:
    error_type: str
    message: str
    timestamp: datetime = datetime.now()
    details: Optional[Dict] = None

class ErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def handle_optimization_error(self, error: Exception, context: Dict) -> OptimizationError:
        """Handle optimization pipeline errors"""
        error_type = error.__class__.__name__
        self.logger.error(f"{error_type}: {str(error)}")
        
        return OptimizationError(
            error_type=error_type,
            message=str(error),
            details=context
        )

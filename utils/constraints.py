# utils/constraints.py
from typing import List, Union
from config.settings import CONSTRAINT_LIMITS
import logging

class ConcreteConstraints:
    @staticmethod
    def check_constraints(individual: List[float]) -> bool:
        """
        Verify if concrete mix design meets engineering constraints
        
        Args:
            individual: [cement, slag, fly_ash, water, superplast, coarse, fine]
        
        Returns:
            bool: True if constraints met
        """
        try:
            cement, slag, fly_ash, water, superplast, coarse, fine = individual
            
            # Water-binder ratio check
            total_binder = cement + slag + fly_ash
            if total_binder == 0:
                logging.warning("Total binder content is zero")
                return False
                
            w_b_ratio = water / total_binder
            if not (CONSTRAINT_LIMITS['W_B_RATIO'][0] <= w_b_ratio <= CONSTRAINT_LIMITS['W_B_RATIO'][1]):
                logging.warning(f"Water-binder ratio {w_b_ratio:.2f} outside limits")
                return False
            
            # Total binder check
            if not (CONSTRAINT_LIMITS['TOTAL_BINDER'][0] <= total_binder <= CONSTRAINT_LIMITS['TOTAL_BINDER'][1]):
                logging.warning(f"Total binder content {total_binder:.1f} outside limits")
                return False
            
            # Minimum cement check
            if cement < CONSTRAINT_LIMITS['MIN_CEMENT']:
                logging.warning(f"Cement content {cement:.1f} below minimum")
                return False
                
            # Fine aggregate ratio check
            total_agg = coarse + fine
            fine_ratio = fine/total_agg
            if not (CONSTRAINT_LIMITS['FINE_AGG_RATIO'][0] <= fine_ratio <= CONSTRAINT_LIMITS['FINE_AGG_RATIO'][1]):
                logging.warning(f"Fine aggregate ratio {fine_ratio:.2f} outside limits")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Error in constraint checking: {e}")
            return False
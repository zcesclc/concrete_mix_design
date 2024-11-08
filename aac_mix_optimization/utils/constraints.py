# utils/constraints.py
from typing import List
import logging
from config.settings import AAC_LIMITS

class AACConstraints:
    @staticmethod
    def check_constraints(individual: List[float]) -> bool:
        """
        Verify if AAC mix design meets material and process constraints
        
        Args:
            individual: [Si/Al, Na/Al, Ca/Si, Activator_binder, Fine_agg_binder, 
                       Coarse_agg_binder, Curing_temp, Curing_age]
        
        Returns:
            bool: True if constraints met
        """
        try:
            si_al, na_al, ca_si, act_bind, fine_bind, coarse_bind, cure_temp, cure_age = individual
            
            # Chemical composition ratios
            if not (AAC_LIMITS['SI_AL_RATIO'][0] <= si_al <= AAC_LIMITS['SI_AL_RATIO'][1]):
                logging.warning(f"Si/Al ratio {si_al:.2f} outside limits")
                return False
                
            if not (AAC_LIMITS['NA_AL_RATIO'][0] <= na_al <= AAC_LIMITS['NA_AL_RATIO'][1]):
                logging.warning(f"Na/Al ratio {na_al:.2f} outside limits")
                return False
                
            if not (AAC_LIMITS['CA_SI_RATIO'][0] <= ca_si <= AAC_LIMITS['CA_SI_RATIO'][1]):
                logging.warning(f"Ca/Si ratio {ca_si:.2f} outside limits")
                return False
            
            # Mix proportion checks
            if not (AAC_LIMITS['ACTIVATOR_BINDER'][0] <= act_bind <= AAC_LIMITS['ACTIVATOR_BINDER'][1]):
                logging.warning(f"Activator/binder ratio {act_bind:.2f} outside limits")
                return False
                
            if not (AAC_LIMITS['FINE_AGG_BINDER'][0] <= fine_bind <= AAC_LIMITS['FINE_AGG_BINDER'][1]):
                logging.warning(f"Fine aggregate/binder ratio {fine_bind:.2f} outside limits")
                return False
                
            if not (AAC_LIMITS['COARSE_AGG_BINDER'][0] <= coarse_bind <= AAC_LIMITS['COARSE_AGG_BINDER'][1]):
                logging.warning(f"Coarse aggregate/binder ratio {coarse_bind:.2f} outside limits")
                return False
            
            # Processing parameters
            if not (AAC_LIMITS['CURING_TEMP'][0] <= cure_temp <= AAC_LIMITS['CURING_TEMP'][1]):
                logging.warning(f"Curing temperature {cure_temp:.1f}°C outside limits")
                return False
                
            if not (AAC_LIMITS['CURING_AGE'][0] <= cure_age <= AAC_LIMITS['CURING_AGE'][1]):
                logging.warning(f"Curing age {cure_age:.1f} days outside limits")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Error in AAC constraint checking: {e}")
            return False

    @staticmethod
    def get_penalty(individual: List[float]) -> float:
        """Calculate constraint violation penalty"""
        if AACConstraints.check_constraints(individual):
            return 0.0
        return 1000.0  # Large penalty for constraint violation
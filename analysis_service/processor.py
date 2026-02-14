"""Physics processing and kinematic calculations"""
import numpy as np
import awkward as ak
from typing import Dict, Any, List

class PhysicsProcessor:
    """Process collision events and calculate physics quantities"""
    
    @staticmethod
    def calculate_kinematics(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate physics quantities from event
        
        Args:
            event: Event dictionary with particles
            
        Returns:
            Dictionary of calculated quantities
        """
        particles = event.get('particles', {})
        
        # Convert to arrays if needed
        if isinstance(particles, dict):
            px = np.array(particles['px'])
            py = np.array(particles['py'])
            pz = np.array(particles['pz'])
            energy = np.array(particles['energy'])
        else:
            px = ak.to_numpy(particles.px)
            py = ak.to_numpy(particles.py)
            pz = ak.to_numpy(particles.pz)
            energy = ak.to_numpy(particles.energy)
        
        # Calculate event-level quantities
        kinematics = {
            'event_id': event['event_id'],
            'invariant_mass': PhysicsProcessor._invariant_mass(px, py, pz, energy),
            'scalar_ht': PhysicsProcessor._scalar_ht(px, py),
            'missing_et': PhysicsProcessor._missing_et(px, py),
            'missing_et_phi': PhysicsProcessor._missing_et_phi(px, py),
        }
        
        # Find jets (simplified: particles with high pT)
        pt = np.sqrt(px**2 + py**2)
        jet_indices = pt > 20.0  # 20 GeV threshold
        
        if np.any(jet_indices):
            jet_pt = pt[jet_indices]
            jet_eta = PhysicsProcessor._pseudorapidity(px[jet_indices], py[jet_indices], pz[jet_indices])
            jet_phi = np.arctan2(py[jet_indices], px[jet_indices])
            
            # Sort by pT
            sorted_indices = np.argsort(jet_pt)[::-1]
            
            kinematics.update({
                'num_jets': len(jet_pt),
                'leading_jet_pt': float(jet_pt[sorted_indices[0]]),
                'leading_jet_eta': float(jet_eta[sorted_indices[0]]),
                'leading_jet_phi': float(jet_phi[sorted_indices[0]]),
            })
        else:
            kinematics.update({
                'num_jets': 0,
                'leading_jet_pt': None,
                'leading_jet_eta': None,
                'leading_jet_phi': None,
            })
        
        # Count leptons (PDG ID 11 or 13)
        if isinstance(particles, dict):
            pdg_ids = np.abs(np.array(particles['pdg_id']))
        else:
            pdg_ids = np.abs(ak.to_numpy(particles.pdg_id))
        
        num_leptons = np.sum((pdg_ids == 11) | (pdg_ids == 13))
        kinematics['num_leptons'] = int(num_leptons)
        
        # Count photons (PDG ID 22)
        num_photons = np.sum(pdg_ids == 22)
        kinematics['num_photons'] = int(num_photons)
        
        return kinematics
    
    @staticmethod
    def _invariant_mass(px: np.ndarray, py: np.ndarray, pz: np.ndarray, energy: np.ndarray) -> float:
        """Calculate invariant mass of all particles"""
        E_total = np.sum(energy)
        px_total = np.sum(px)
        py_total = np.sum(py)
        pz_total = np.sum(pz)
        
        m_squared = E_total**2 - (px_total**2 + py_total**2 + pz_total**2)
        return float(np.sqrt(max(0, m_squared)))
    
    @staticmethod
    def _scalar_ht(px: np.ndarray, py: np.ndarray) -> float:
        """Calculate scalar sum of transverse momentum"""
        pt = np.sqrt(px**2 + py**2)
        return float(np.sum(pt))
    
    @staticmethod
    def _missing_et(px: np.ndarray, py: np.ndarray) -> float:
        """Calculate missing transverse energy"""
        met_x = -np.sum(px)
        met_y = -np.sum(py)
        return float(np.sqrt(met_x**2 + met_y**2))
    
    @staticmethod
    def _missing_et_phi(px: np.ndarray, py: np.ndarray) -> float:
        """Calculate azimuthal angle of missing ET"""
        met_x = -np.sum(px)
        met_y = -np.sum(py)
        return float(np.arctan2(met_y, met_x))
    
    @staticmethod
    def _pseudorapidity(px: np.ndarray, py: np.ndarray, pz: np.ndarray) -> np.ndarray:
        """Calculate pseudorapidity η = -ln(tan(θ/2))"""
        pt = np.sqrt(px**2 + py**2)
        theta = np.arctan2(pt, pz)
        # Avoid division by zero
        eta = -np.log(np.tan(theta / 2.0 + 1e-10))
        return eta
    
    @staticmethod
    def passes_trigger(kinematics: Dict[str, Any], trigger_config: Dict[str, float]) -> bool:
        """
        Check if event passes trigger requirements
        
        Args:
            kinematics: Calculated kinematics
            trigger_config: Trigger thresholds
            
        Returns:
            True if event passes trigger
        """
        # Example trigger: at least one jet above threshold
        if kinematics.get('leading_jet_pt', 0) < trigger_config.get('min_jet_pt', 20.0):
            return False
        
        # Or high missing ET
        if kinematics.get('missing_et', 0) > trigger_config.get('min_met', 100.0):
            return True
        
        # Or leptons above threshold
        if kinematics.get('num_leptons', 0) >= 2:
            return True
        
        return True  # For demo, pass most events

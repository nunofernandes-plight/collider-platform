"""Simple collision event generator"""
import numpy as np
import awkward as ak
from typing import Dict, Any, Tuple
import uuid
from datetime import datetime

class SimpleCollisionGenerator:
    """
    Simplified collision generator for hackathon MVP
    Simulates e+e- -> mu+mu- and simple QCD events
    """
    
    def __init__(self, center_of_mass_energy: float = 13000.0):
        """
        Initialize generator
        
        Args:
            center_of_mass_energy: Center of mass energy in GeV
        """
        self.sqrt_s = center_of_mass_energy
        self.run_number = 1
        self.event_counter = 0
        
        # PDG codes
        self.PDG_ELECTRON = 11
        self.PDG_MUON = 13
        self.PDG_PHOTON = 22
        self.PDG_QUARK_UP = 2
        self.PDG_QUARK_DOWN = 1
        
    def generate_event(self, event_type: str = 'dilepton') -> Dict[str, Any]:
        """
        Generate a single collision event
        
        Args:
            event_type: Type of event ('dilepton', 'qcd', 'random')
            
        Returns:
            Event dictionary with particle data
        """
        self.event_counter += 1
        
        if event_type == 'dilepton':
            particles = self._generate_dilepton()
        elif event_type == 'qcd':
            particles = self._generate_qcd()
        else:
            # Random choice
            event_type = np.random.choice(['dilepton', 'qcd'])
            particles = self._generate_dilepton() if event_type == 'dilepton' else self._generate_qcd()
        
        event = {
            'event_id': str(uuid.uuid4()),
            'run_number': self.run_number,
            'event_number': self.event_counter,
            'timestamp': datetime.utcnow().isoformat(),
            'center_of_mass_energy': self.sqrt_s,
            'event_type': event_type,
            'particles': self._particles_to_awkward(particles),
            'num_particles': len(particles),
        }
        
        return event
    
    def _generate_dilepton(self) -> list:
        """Generate e+e- -> l+l- event (simplified)"""
        particles = []
        
        # Generate Z boson mass with Breit-Wigner
        mZ = 91.2  # GeV
        gammaZ = 2.5  # GeV
        mass = np.random.normal(mZ, gammaZ)
        
        # Decay to mu+mu-
        # Back-to-back in transverse plane (simplified)
        pt = np.random.exponential(30.0)  # GeV
        phi = np.random.uniform(0, 2 * np.pi)
        eta = np.random.normal(0, 2.0)  # pseudorapidity
        
        # Muon+ (positive charge)
        px1 = pt * np.cos(phi)
        py1 = pt * np.sin(phi)
        pz1 = pt * np.sinh(eta)
        E1 = np.sqrt(px1**2 + py1**2 + pz1**2 + 0.106**2)  # muon mass 0.106 GeV
        
        particles.append({
            'pdg_id': -self.PDG_MUON,  # mu+
            'px': px1, 'py': py1, 'pz': pz1, 'energy': E1,
            'charge': 1, 'mass': 0.106
        })
        
        # Muon- (back-to-back)
        px2 = -px1
        py2 = -py1
        pz2 = -pz1 + np.random.normal(0, 10)  # Small boost
        E2 = np.sqrt(px2**2 + py2**2 + pz2**2 + 0.106**2)
        
        particles.append({
            'pdg_id': self.PDG_MUON,  # mu-
            'px': px2, 'py': py2, 'pz': pz2, 'energy': E2,
            'charge': -1, 'mass': 0.106
        })
        
        return particles
    
    def _generate_qcd(self) -> list:
        """Generate simple QCD multi-jet event"""
        particles = []
        
        # Generate 2-6 jets
        num_jets = np.random.randint(2, 7)
        
        for _ in range(num_jets):
            # Jet parameters
            pt = np.random.exponential(50.0) + 20.0  # Min 20 GeV
            eta = np.random.uniform(-2.5, 2.5)
            phi = np.random.uniform(0, 2 * np.pi)
            
            # Approximate as massless
            px = pt * np.cos(phi)
            py = pt * np.sin(phi)
            pz = pt * np.sinh(eta)
            E = np.sqrt(px**2 + py**2 + pz**2)
            
            # Random quark flavor
            pdg = np.random.choice([self.PDG_QUARK_UP, self.PDG_QUARK_DOWN, 
                                   -self.PDG_QUARK_UP, -self.PDG_QUARK_DOWN])
            
            particles.append({
                'pdg_id': pdg,
                'px': px, 'py': py, 'pz': pz, 'energy': E,
                'charge': 2/3 if abs(pdg) == self.PDG_QUARK_UP else -1/3,
                'mass': 0.0
            })
        
        return particles
    
    def _particles_to_awkward(self, particles: list) -> ak.Array:
        """Convert particle list to Awkward Array"""
        return ak.Array({
            'pdg_id': [p['pdg_id'] for p in particles],
            'px': [p['px'] for p in particles],
            'py': [p['py'] for p in particles],
            'pz': [p['pz'] for p in particles],
            'energy': [p['energy'] for p in particles],
            'charge': [p['charge'] for p in particles],
            'mass': [p['mass'] for p in particles],
        })
    
    def generate_batch(self, num_events: int = 10) -> list:
        """Generate a batch of events"""
        return [self.generate_event('random') for _ in range(num_events)]

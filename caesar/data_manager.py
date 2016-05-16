import numpy as np

from .property_getter import ptype_ints, get_particles_for_FOF, get_property

class DataManager(object):
    def __init__(self, obj):
        self.obj = obj
        self.blackholes = False
        self.determine_ptypes()
        self.load_data()
        self.load_gas_data()
        
    def determine_ptypes(self):
        self.ptypes = ['gas','star']
        if 'blackholes' in self.obj._kwargs and self.obj._kwargs['blackholes']:
            self.ptypes.append('bh')
            self.blackholes = True
        self.ptypes.append('dm')            
        
    def load_data(self):
        pdata = get_particles_for_FOF(self.obj, self.ptypes)
        self.pos   = pdata['pos']
        self.vel   = pdata['vel']
        self.mass  = pdata['mass']
        self.ptype = pdata['ptype']
        self.index = pdata['indexes']
        pdata = None
                
        self.glist  = np.where(self.ptype == ptype_ints['gas'])[0]
        self.slist  = np.where(self.ptype == ptype_ints['star'])[0]
        self.dmlist = np.where(self.ptype == ptype_ints['dm'])[0]        
        self.bhlist = np.where(self.ptype == ptype_ints['bh'])[0]

        # move these to obj.simulation?
        self.obj.ngas  = len(self.glist)
        self.obj.nstar = len(self.slist)
        self.obj.ndm   = len(self.dmlist)
        self.obj.nbh   = len(self.bhlist)

    def load_gas_data(self):
        if self.obj.ngas == 0:
            return

        sfr = get_property(self.obj, 'sfr', 'gas').to('%s/%s' % (self.obj.units['mass'], self.obj.units['time']))
        gZ  = get_property(self.obj, 'metallicity', 'gas')
        gT  = get_property(self.obj, 'temperature', 'gas').to(self.obj.units['temperature'])
        
        self.gsfr = sfr
        self.gZ   = gZ
        self.gT   = gT
        
        
        

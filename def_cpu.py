"""
Name:    def_cpu
By:      Ehsan Moravveji
Date:    29 August 2018
Usage:    
Return:  
Purpose: To define the basic cpu class and its relevant machinery
Remarks: + All default string attributes are set to None 
         + All default logical attributes are set to False
         + All default integer attributes are set to zero
         + The name of most attributes are taken from the output of 
           the "pbsnodes" Torque command
         + The int and float attribute names begin with "_" and they
           have dedicated getter methods to carry out the type conversion
"""
import sys, os
import logging

#--------------------------------------
# logger to capture exceptions
logger = logging.getLogger(__name__)
#--------------------------------------

# C L A S S ###########################
class cpu:
  """
  A class that encapsulates the CPU part of the node.
  All attributes are the fields returned from the 
  "status" entry of the "pbsnodes" command. For brevity, 
  only the critical attributes are captured for now; the rest
  can be easily elaborated later. The attribute list is complete.
  """
  #------------------------------------
  def __init__(self):
    self.opsys = None
    self.uname = None
    self.sessions = None
    self._nsessions = 0
    self._loadave = 0.0
#    self.gres = 0
    self.netload = None
    self.state = None
    self.varattr = None
    self.puppethpccode = None
    self.sudo = None
    self.kernel = None
    self.cpuclock = None
    self.macaddr = None
    self.version = None
    self.rectime = None
    self.jobs = None

  #------------------------------------
  @property
  def nsessions(self): return self._nsessions
  @nsessions.setter
  def nsessions(self, val): self._nsessions = int(val)

  @property
  def loadave(self): return self._loadave
  @loadave.setter
  def loadave(self, val): self._loadave = float(val)

  #------------------------------------
  def set(self, attr, val):
    """
    Set the attribute of "attr" to the value "val"
    """
    try: 
      setattr(self, attr, val)
    except AttributeError:
      logging.error(f"Error: set: gpu class does not have this attribute: {attr}")
      sys.exit(1)

  #------------------------------------
  def get(self, attr):
    """
    Retrieve the value of the attribute "attr"
    """
    try:
      return self.__getattribute__(attr)
    except AttributeError: 
      logger.error(r"Error: def_gpu: get: gpu class does not have this attribute {attr}")
      sys.exit(1)

  #------------------------------------


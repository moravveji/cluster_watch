"""
Name:    def_gpu
By:      Ehsan Moravveji
Date:    29 August 2018
Usage:    
Return:  
Purpose: To define the basic gpu class and its relevant machinery
Remarks: + All default string attributes are set to None 
         + All default logical attributes are set to False
         + All default integer attributes are set to zero
         + The name of most attributes are taken from the output of 
           the "pbsnodes" Torque command
         + The int and float attribute names begin with "_" and they
           have dedicated getter methods to carry out the type conversion
"""
import sys
import logging

#--------------------------------------
# logger to capture exceptions
logger = logging.getLogger(__name__)
#--------------------------------------

# C L A S S ###########################
class gpu:
  """
  A class that encapsulates the GPU device properties.
  All attributes are the fields returned from the "gpu_status" 
  entry of the "pbsnodes" command. For brevity, only the critical
  attributes are captured for now; the rest can be easily elaborated
  later. The attribute list is complete.
  """
  #------------------------------------
  def __init__(self):
    self.gpu_id = None
    self._gpu_pci_device_id = 0
    self.gpu_pci_location_id = None
    self.gpu_product_name = None
    self.gpu_memory_total = None
    self._gpu_memory_used = 0
    self.gpu_mode = None
    self.gpu_state = None
    self._gpu_utilization = 0
    self._gpu_memory_utilization = 0
    self.gpu_ecc_mode = None
    self._gpu_single_bit_ecc_errors = 0
    self._gpu_double_bit_ecc_errors = 0
    self.gpu_temperature = None

  #------------------------------------
  @property
  def gpu_pci_device_id(self): return self._gpu_pci_device_id
  @gpu_pci_device_id.setter
  def gpu_pci_device_id(self, val): self._gpu_pci_device_id = int(val)
 
  @property
  def gpu_memory_used(self): return self._gpu_memory_used
  @gpu_memory_used.setter
  def gpu_memory_used(self, val): self._gpu_memory_used = int(val)
 
  @property
  def gpu_utilization(self): return self._gpu_utilization
  @gpu_utilization.setter
  def gpu_utilization(self, val): self._gpu_utilization = int(val)

  @property 
  def gpu_memory_utilization(self): return self._gpu_memory_utilization
  @gpu_memory_utilization.setter
  def gpu_memory_utilization(self, val): self._gpu_memory_utilization = int(val) 

  @property
  def gpu_single_bit_ecc_errors(self): return self._gpu_single_bit_ecc_errors
  @gpu_single_bit_ecc_errors.setter
  def gpu_single_bit_ecc_errors(self, val): self._gpu_single_bit_ecc_errors = int(val)

  @property
  def gpu_double_bit_ecc_errors(self): return self._gpu_double_bit_ecc_errors
  @gpu_double_bit_ecc_errors.setter
  def gpu_double_bit_ecc_errors(self, val): self._gpu_double_bit_ecc_errors = int(val)

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

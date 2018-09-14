"""
Name:    def_node
By:      Ehsan Moravveji
Date:    29 August 2018
Usage:    
Return:  
Purpose: To define the basic node class and its relevant machinery
Remarks: + All default string attributes are set to None 
         + All default logical attributes are set to False
         + All default integer attributes are set to zero
         + The name of most attributes are taken from the output of 
           the "pbsnodes" Torque command
         + The int and float attribute names begin with "_" and they
           have dedicated getter methods to carry out the type conversion
         + An instance of cpu() class is used, and a list of instances of
           the gpu() class can be used for nodes that contain GPU devices
"""
import sys, os
import logging
import subprocess

from def_gpu import *
from def_cpu import *

#--------------------------------------
# logger to capture exceptions
logger = logging.getLogger(__name__)
#--------------------------------------

# C L A S S ###########################
class node:
  """
  A class that encapsulates the nodes properties
  """
  #------------------------------------
  def __init__(self, hostname):
    """
    Instantiate the object
    Most of the attributes are the output entries of the 
    "pbsnodes" command
    """
    self.hostname = hostname
    
    # pbsnodes message captured from ther STDOUT
    self.pbsnodes = None
    
    # Default attributes from "pbsnodes" output
    self.state = None
    self.power_state = None
    self._np = 0
    self.properties = None
    self.ntype = None
    self.jobs = None
    self.status = None
    self._mom_service_port = 0
    self._mom_manager_port = 0
    self._gpus = 0
    self.gpu_status = None
    self._total_sockets = 0
    self._total_numa_nodes = 0
    self._total_cores = 0
    self._total_threads = 0
    self._dedicated_sockets = 0
    self._dedicated_numa_nodes = 0
    self._dedicated_cores = 0
    self._dedicated_threads = 0

    # Extra attributes
    self.cpu  = cpu()
    self.gpu_list = list()

    # Call the pbsnodes command and get the stdout
    self.call_pbsnodes()

    # Parse (process) the self.pbsnodes 
    self.parse_pbsnodes()

    # Parse (process) the self.status for cpu attributes
    self.parse_cpu_status()

    # Parse (process) the self.gpu_status for gpu attributes
    self.parse_gpu_status()

  #------------------------------------
  @property
  def np(self): return self._np
  @np.setter
  def np(self, val): self._np = int(val)

  @property
  def mom_service_port(self): return self._mom_service_port
  @mom_service_port.setter
  def mom_service_port(self, val): self._mom_service_port = int(val)

  @property
  def mom_manager_port(self): return self._mom_manager_port
  @mom_manager_port.setter
  def mom_manager_port(self, val): self._mom_manager_port = int(val)

  @property
  def gpus(self): return self._gpus
  @gpus.setter
  def gpus(self, val): self._gpus = int(val)

  @property
  def total_sockets(self): return self._total_sockets
  @total_sockets.setter
  def total_sockets(self, val): self._total_sockets = int(val)

  @property
  def total_numa_nodes(self): return self._total_numa_nodes
  @total_numa_nodes.setter
  def total_numa_nodes(self, val): self._total_numa_nodes = int(val)

  @property
  def total_cores(self): return self._total_cores
  @total_cores.setter
  def total_cores(self, val): self._total_cores = int(val)

  @property
  def total_threads(self): return self._total_threads
  @total_threads.setter
  def total_threads(self, val): self._total_threads = int(val)

  @property
  def dedicated_sockets(self): return self._dedicated_sockets
  @dedicated_sockets.setter
  def dedicated_sockets(self, val): self._dedicated_sockets = int(val)

  @property
  def dedicated_numa_nodes(self): return self._dedicated_numa_nodes
  @dedicated_numa_nodes.setter
  def dedicated_numa_nodes(self, val): self._dedicated_numa_nodes = int(val)

  @property
  def dedicated_cores(self): return self._dedicated_cores
  @dedicated_cores.setter
  def dedicated_cores(self, val): self._dedicated_cores = int(val)

  @property
  def dedicated_threads(self): return self._dedicated_threads
  @dedicated_threads.setter
  def dedicated_threads(self, val): self._dedicated_threads = int(val)

  #------------------------------------
  def set(self, attr, val):
    """
    Set the attribute of "attr" to the value "val"
    """
    try: 
      setattr(self, attr, val)
    except AttributeError:
      logging.error(f"Error: set: node class does not have this attribute: {attr}")
      sys.exit(1)

  #------------------------------------
  def get(self, attr):
    """
    Retrieve the value of the attribute "attr"
    """
    try:
      return self.__getattribute__(attr)
    except AttributeError: 
      logger.error(f"Error: get: node class does not have this attribute {attr}")
      sys.exit(1)

  #------------------------------------
  def call_pbsnodes(self):
    """
    Let a subprocess call the "pbsnodes <hostname>" and collect the result back
    """
    cmnd = f'pbsnodes {self.hostname}'
    try: 
      call = subprocess.Popen(cmnd, stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, shell=True,
                              universal_newlines=True, encoding='utf-8')
      result, ierr = call.communicate()
      self.pbsnodes = result 
    except:
      logger.error(f'Error: call_pbsnodes failed on {self.hostname}')
      sys.exit(ierr)

  #------------------------------------
  def parse_pbsnodes(self):
    """
    Parse the self.pbsnodes strings into the 'default' attributes of the node class
    """
    pbsnodes = self.pbsnodes.split('\n') # list of lines
    hostname = pbsnodes.pop(0)
    if not hostname == self.hostname: 
      logger.error(f'Error: parse_pbsnodes: conflicting hostnames: {hostname} vs. {self.hostname}')
      sys.exit(1)
    for line in pbsnodes:
      if not line: continue
      if '=' not in line: continue
      line = line.strip()
      (attr, val) = line.split(sep='=', maxsplit=1)
      self.set(attr.strip(), val.strip())
    
  #------------------------------------
  def parse_cpu_status(self):
    """
    Retrieve the self.status and split the key-value fields separated by 
    semi-colon, and assign each field to the correct attribute of the parent
    class cpu
    """
    status = self.status
    items  = status.split(',')
    for item in items:
      if '=' not in item: continue
      attr, val = item.split(sep='=', maxsplit=1)
      try:
        self.cpu.set(attr, val)
      except:
        print(f'Error: parse_cpu_status: failed to set attribute {attr}')
        print(f'{attr}: {val}')
        sys.exit(1)

  #------------------------------------
  def parse_gpu_status(self):
    """
    Retrieve the self.gpu_status and split the key-value fields separated by 
    semi-colon, and assign each field to the correct attribute of the parent
    class gpu
    """
    if self.gpu_status is None: return # non-GPU nodes do not have this entry
    try:
      assert len(self.gpu_list) == 0
    except AssertionError:
      logger.error(f"Error: parse_gpu_status: self.gpu_list is not empty!")
      sys.exit(1)
    status = self.gpu_status

    dev_index = list()  # collects device ids, e.g. 0, 1, 2, 3, ...
    dev_list  = list()  # collects instances of the gpu() class
    junk, messages = status.split(sep='=', maxsplit=1)
    list_messages  = messages.split(',')
    print(list_messages)
    sys.exit(1)

    for i, msg in enumerate(list_messages):
      which_dev, info = msg.split(sep='=', maxsplit=1)
      dev_id = int(which_dev[4])
      dev_index.append(dev_id)
      items  = info.split(';')

      this = gpu()

      for k, item in enumerate(items):
        key, val = item.split('=')
        this.set(key, val)

      dev_list.append(this)

    # invert the dev_list, because originally it is from the last device to the first
    dev_list = dev_list[::-1]

    # set the gpu_list attribute
    self.set('gpu_list', dev_list.copy())

  #------------------------------------
  #------------------------------------


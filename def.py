"""
Name:    gpu_info
By:      Ehsan Moravveji
Date:    14 August 2018
Usage:   $> gpu_info 
Return:  Simplistic screenshot of the resource utilization
Purpose: To have an admin's overview of how busy the cluster is,
         w.r.t. to the available resources (e.g. CPUs, GPUGs etc)
Remarks: + All default string attributes are set to None 
         + All default logical attributes are set to False
         + All default integer attributes are set to zero
         + The name of most attributes are taken from the output of 
           the "pbsnodes" Torque command
         + The int and float attribute names begin with "_" and they
           have dedicated getter methods to carry out the type conversion
         + The data structure tree looks like this (cpu, gpu and node are parents):
           cpu    gpu    node                    nodes 
                         -> cpu                  -> [node_0, ..., node_M]
                         -> [gpu_0, ..., gpu_N]

         + The parent cpu and gpu classes do not have a "set" method, 
           because all the set operations are done bottom-up by calling
           that of "node" class
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
class nodes:
  """
  nodes encapsulates the available information from all nodes
  in the cluster
  """
  def __init__(self, cluster):
#    super().__init__()
    self.cluster = cluster.lower()
    self.check_cluster_name()

    # intrinsic attributes
    self.gpu_hostnames = []
    self.cpu_hostnames = []
    self.hostnames     = []

    # list of instances of the "node" class, one per each hostname
    self.list_hosts    = []

    # Collect the hostnames based on the cluster name
    self.set_hostnames()

    # Gather a list of "node" objects for all physical nodes in the cluster
    self.gather_nodes()

  #------------------------------------
  def set(self, attr, val):
    """
    Set the value of the attribute "attr" to "val"
    """
    try: 
      setattr(self, attr, val)
    except AttributeError:
      logging.warning(f"set: class 'node' does not have this attribute: {attr}")
      return None

  #------------------------------------
  def get(self, attr):
    """
    Get the value of an existing attribute of the class
    """
    try:
      return self.__getattribute__(attr)
    except AttributeError:
      logging.warning(f"get: class 'nodes' does not have this attribute: {attr}")
      return None

  #------------------------------------
  def check_cluster_name(self):
    """
    Assert the cluster name is valid (thinking, genius or breniac)
    """
    try:
      assert self.cluster in ['thinking', 'genius', 'breniac']
    except AssertionError:
      logger.error(f'Error: check_cluster_name: {self.cluster} is invalid')
      sys.exit(1)

  #------------------------------------
  def set_gpu_hostnames(self):
    """
    Set the hostnames of the GPU nodes in "self.gpu_hostnames"
    """
    if self.cluster == 'genius':
      rack22 = [f'r22g{k:02d}' for k in range(35, 42)]
      rack23 = [f'r23g{k:02d}' for k in range(34, 40)]
      rack24 = [f'r24g{k:02d}' for k in range(35, 42)]
      hosts  = rack22 + rack23 + rack24
    elif self.cluster == 'thinking':
      hosts  = []
    elif self.cluster == 'breniac':
      hosts  = []
    self.set('gpu_hostnames', hosts)

  #------------------------------------
  def set_cpu_hostnames(self):
    """
    Set the hostnames of the CPU nodes in "self.cpu_hostnames"
    """
    if self.cluster == 'genius':
      hosts = [f'r{r:02d}i{i:02d}n{n:02d}' for r in (22, 23) for i in (13, 27) for n in range(1, 25)]
    elif self.cluster == 'thinking':
      hosts  = []
    elif self.cluster == 'breniac':
      hosts  = []
    self.set('cpu_hostnames', hosts)

  #------------------------------------
  def set_hostnames(self):
  
    """
    Aggregate the hostnames from GPU and CPU hostnames
    """
    # Collect the hostnames based on the cluster name
    self.set_gpu_hostnames()
    self.set_cpu_hostnames()
    self.hostnames = self.gpu_hostnames + self.cpu_hostnames

  #------------------------------------
  def gather_nodes(self):
    """
    Gather a list of instances of the "node" class which are all well instantiated. 
    Thus, the attributes of each object is allready set to the right value, and this 
    list represents the status of the cluster, collected through a collective call to 
    the "pbsnodes" command in a snapshot.
    """
    if self.list_hosts:
      logger.error('Error: gather_nodes: the class object is not properly initialized')
      sys.exit(1)
    
    for host in self.hostnames: self.list_hosts.append( node(host) )

  #------------------------------------
  #------------------------------------
  #------------------------------------
  #------------------------------------

import os, sys
import logging
import def_node as df

#--------------------------------------
logger = logging.getLogger(__name__)

#--------------------------------------
def test_def_gpu():
  device = df.gpu()
  device.gpu_utilization = '2'
  try: 
    assert isinstance(device.gpu_utilization, int)
  except AssertionError:
    logger.error('Error: test_def_gpu: failed to set an integer attribute')
    sys.exit(1)

  return 0

#--------------------------------------
def test_def_cpu():
  board = df.cpu()
  board.nsessions = '5'
  board.loadave = '12.4'
  try: 
    assert isinstance(board.nsessions, int)
    assert isinstance(board.loadave, float)
  except AssertionError:
    logger.error('Error: test_def_cpu: failed to set an integer/float attribute')
    sys.exit(1)

  return 0 # some comment

#--------------------------------------
def test_def_node(): 
  gnode = df.node(hostname='r23g35')
  print(f"{gnode.hostname} has {gnode.gpus} GPUs onboard")
  cnode = df.node(hostname='r22i13n01')
  print(f"{cnode.hostname} has {cnode.np} processoers on chip")

  return 0

#--------------------------------------
def check_gpu_status():
  gnode = df.node(hostname='r23g34')
  gpus  = gnode.gpus
  try:
    assert gpus == len(gnode.gpu_list)
  except AssertionError:
    print('Error: check_gpu_status failed')
    sys.exit(1)

  print()
  print(f"Jobs on {gnode.hostname}: {gnode.jobs}")
  print('{0:<16s} {1:<6s} {1:<6s} {2:<6s}'.format('Device ID', 'Use', 'Mem', 'Tempr'))
  print('{0:<16s} {1:<6s} {1:<6s} {2:<6s}'.format(' ', '[%]', '[%]', 'C'))
  for i, gpu in enumerate(gnode.gpu_list):
    gid   = gpu.gpu_id
    gutil = gpu.gpu_utilization
    gmem  = gpu.gpu_memory_utilization
    gtemp = gpu.gpu_temperature

    print(f"{gid:<16s} {gutil:<6d} {gmem:<6d} {gtemp:<6d}")
  print()

#--------------------------------------
#--------------------------------------
#--------------------------------------
def main():

  test_def_gpu()

  test_def_cpu()

  test_def_node()

  check_gpu_status()

#  genius = gpi.nodes(cluster='genius')

#--------------------------------------
if __name__ == '__main__':
  sys.exit(main())
#--------------------------------------


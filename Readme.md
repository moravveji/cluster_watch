# cluster_watch: Live Monitoring of a Supercomputer

## Purpose
This `Python` tool provides live graphical monitoring of a cluster (of e.g. hybird CPU and GPU nodes), by providing a list of hostnames. It heavily relies on the output of the `pbsnodes <hostname> ` command. The instant node information is captured from STDOUT, and is parsed to the attributes of the `node`, `cpu` and `gpu` class instances. A cluster is an aglemeration of a pool of `nodes` (i.e. a list of `node` instances). 

## Dependencies
* Python/3.6-intel-2018a
* Python Tkinter

## To Do List
* Allow the `nodes` class initialization to accept the list of hostnames of the cluster from an ASCII file
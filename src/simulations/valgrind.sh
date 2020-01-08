#!/bin/bash
make MODE=debug -C ../ -j8
valgrind --leak-check=full ../src/AeronauticalCommunicationSimulator_dbg -m -u Cmdenv -n .:../src:../../../omnet/inet4/src:../../../omnet/inet4/examples:../../../omnet/inet4/tutorials:../../../omnet/inet4/showcases --image-path=../images:../../../omnet/inet4/images -l ../../../omnet/inet4/src/INET omnetpp.ini

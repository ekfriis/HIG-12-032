#!/bin/bash

# Setup datacard working areas

MASSES="110 115 120 125 130 135 140" 
DCs=$CMSSW_BASE/src/auxiliaries/datacards/

#setup-htt.py -i $DCs -o STANDARD-LIMITS $MASSES --channels="em et mt mm" &
setup-htt.py -i $DCs -o NEW-LIMITS $MASSES --channels="vhtt tt" &
setup-htt.py -i $DCs -o ALL-LIMITS $MASSES --channels="vhtt tt em et mt mm" &

wait

#!/bin/bash

# Make datacard project areas

setup-htt.py -o ALL-LIMITS 115 120 125 130 135 140 --channels="vhtt tt em mt et mm"  -i $CMSSW_BASE/src/auxiliaries/datacards
setup-htt.py -o STANDARD-LIMITS 115 120 125 130 135 140 --channels="em mt et mm"  -i $CMSSW_BASE/src/auxiliaries/datacards
setup-htt.py -o NEW-LIMITS 115 120 125 130 135 140 --channels="vhtt tt"  -i $CMSSW_BASE/src/auxiliaries/datacards

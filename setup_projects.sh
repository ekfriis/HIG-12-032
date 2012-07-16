#!/bin/bash

# Setup datacard working areas

MASSES="110 115 120 125 130 135 140" 

setup-htt.py -o STANDARD-LIMITS $MASSES --channels="em et mt mm"
setup-htt.py -o UPDATE-LIMITS $MASSES --channels="vhtt tt"
setup-htt.py -o ALL-LIMITS $MASSES --channels="vhtt tt em et mt mm"

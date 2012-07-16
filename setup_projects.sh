#!/bin/bash

# Setup datacard working areas

MASSES="110 115 120 125 130 135 140" 
DCs=$CMSSW_BASE/src/auxiliaries/datacards/

setup-htt.py -i $DCs -o STANDARD-LIMITS $MASSES --channels="em et mt mm"
setup-htt.py -i $DCs -o UPDATE-LIMITS $MASSES --channels="vhtt tt"
setup-htt.py -i $DCs -o ALL-LIMITS $MASSES --channels="vhtt tt em et mt mm"

# Make a megacard to extract tables out of
cd UPDATE-LIMITS/cmb/125
#combineC
combineCards.py -S boost=htt_tt_0_8TeV.txt  vbf=htt_tt_1_8TeV.txt  \
  llt7TeV=vhtt_0_7TeV.txt  llt8TeV=vhtt_0_8TeV.txt \
  ZH7TeV=vhtt_1_7TeV.txt  ZH8TeV=vhtt_1_8TeV.txt  \
  ltt7TeV=vhtt_2_7TeV.txt  ltt8TeV=vhtt_2_8TeV.txt > megacard.txt

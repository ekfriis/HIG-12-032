#!/bin/bash

cd NEW-LIMITS
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_tt_layout.py tt
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_llt_layout.py llt
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_4l_layout.py 4l

plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_HIG_12_032_layout.py cmb

cp llt_sm.pdf llt_sm_cls.pdf
cp tt_sm.pdf tt_sm_cls.pdf
cp 4l_sm.pdf 4l_sm_cls.pdf
cp cmb_sm.pdf cmb_sm_cls.pdf

root -b -q '../../HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C+("limits_sm.root", "cmb,tt,4l,llt", true, false, "sm-xsex", 0, 20, false)'

cd ../ALL-LIMITS
echo "Making combined plot"
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_layout.py cmb

cp cmb_sm.pdf cmb_sm_cls.pdf

#!/bin/bash

cd NEW-LIMITS
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_tt_layout.py tt
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_llt_layout.py llt
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_4l_layout.py 4l
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_HIG_12_032_layout.py cmb

root -b -q '../../HiggsAnalysis/HiggsToTauTau/macros/compareLimits.C+("limits_sm.root", "cmb,tt,4l,llt", true, false, "sm-xsex", 0, 20, false)'

cd ../ALL-LIMITS
plot CLs $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_layout.py cmb

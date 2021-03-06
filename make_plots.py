'''

Build plots for HIG-12-032 results.

'''

from rootpy.plotting import views, Legend
import rootpy.io as io
import glob
import ROOT

def add_cms_blurb(sqrts, intlumi, preliminary=True, blurb=''):
    latex = ROOT.TLatex()
    latex.SetNDC();
    latex.SetTextSize(0.04);
    latex.SetTextAlign(31);
    latex.SetTextAlign(11);
    label_text = "CMS"
    if preliminary:
        label_text += " Preliminary"
    label_text += " %s TeV" % sqrts
    label_text += " L=%sfb^{-1}" % (intlumi)
    label_text += " " + blurb
    return latex.DrawLatex(0.18,0.97, label_text);

vh_7TeV = io.open('NEW-LIMITS/cmb/common/vhtt.input_7TeV.root')
vh_8TeV = io.open('NEW-LIMITS/cmb/common/vhtt.input_8TeV.root')

# We only care about 7 + 8 TeV
vh_combined = views.SumView(vh_7TeV, vh_8TeV)

# Now combine sub-channels
llt_combined = views.SumView(*[
    views.SubdirectoryView(vh_combined, x) for x in ['emt', 'mmt', ]])

# We have to get the shape versions of these from a separate root file.
zh_combined = views.SumView(*[
    views.SubdirectoryView(io.open('zh_with_shapes.root'), x) for x in [
        'eeem_zh', 'eeet_zh', 'eemt_zh', 'eett_zh',
        'mmme_zh', 'mmet_zh', 'mmmt_zh', 'mmtt_zh',
    ]])

ltt_combined = views.SumView(*[
    views.SubdirectoryView(vh_combined, x) for x in [ 'ett_sm', 'mtt_sm' ]])

def rebin(histo):
    histo.Rebin(20)
    return histo
ltt_combined = views.FunctorView(ltt_combined, rebin)

# Make views of individual backgrounds
channels = {
    'llt' : {},
    'ltt' : {},
    'zh' : {},
    # tau_h tau_h
    'boost' : {},
    'vbf' : {},
}

# Define styles.  Normally this is done in FSA, but lets keep it static here.
main_irreducible = {
    'legendstyle' : 'f',
    'format' : 'hist',
    # Same as Z+jets
    'fillstyle' : 1001,
    'fillcolor' : '#FFCC66',
    'linecolor' : '#000000',
    'linewidth' : 3,
}
next_irreducible = {
    'legendstyle' : 'f',
    'format' : 'hist',
    # Same as W+jets
    'fillstyle' : 1001,
    'fillcolor' : '#990000',
    'linecolor' : '#000000',
    'linewidth' : 3,
}
third_irreducible = {
    'legendstyle' : 'f',
    'format' : 'hist',
    # Same as ttbar
    'fillstyle' : 1001,
    'fillcolor' : '#9999CC',
    'linecolor' : '#000000',
    'linewidth' : 3,
}
fakes = {
    'legendstyle' : 'f',
    'format' : 'hist',
    # Same as QCD
    'fillcolor' : '#FFCCFF',
    'linecolor' : '#000000',
    'fillstyle' : 1001,
    'linewidth' : 3,
}
signal = {
    'legendstyle' : 'f',
    'format' : 'hist',
    'fillcolor' : 0,
    'fillstyle' : 0,
    'linestyle' : 2,
    'linewidth' : 5,
    'linecolor' : '#1C1C76',
    'name' : "VH",
}
data =  {
    'markerstyle' : 20,
    'markersize' : 3,
    'linewidth' : 2,
    'markercolor' : '#000000',
    'legendstyle' : 'pe',
    'format' : 'pe',
    'name' : "Observed",
}


Style = views.StyleView
Subdir = views.SubdirectoryView
Sum = views.SumView
Title = views.TitleView
ScaleView = views.ScaleView
sigscale = 5

def set_line_width(x):
    x.SetLineWidth(3)
    print "Setting line width"
    return x

# stupid hack to get always get a given histogram no matter what the Get(x) is
def Getter(view, histoname, title=None):
    def doot(x):
        print "doot", histoname
        return histoname

    if title is not None:
        return views.FunctorView(views.TitleView(views.PathModifierView(view, doot), title), set_line_width)
    else:
        return views.FunctorView(views.PathModifierView(view, doot), set_line_width)

signal_label = '(5#times) m_{H}=125 GeV'

channels['llt']['wz'] = Style(Getter(llt_combined, 'wz', 'WZ'), **main_irreducible)
channels['llt']['zz'] = Style(Getter(llt_combined, 'zz', 'ZZ'), **next_irreducible)
channels['llt']['fakes'] = Style(Getter(llt_combined, 'fakes', 'Non-prompt'), **fakes)
channels['llt']['signal'] = Title(ScaleView(Style(
    Sum(
        Getter(llt_combined, 'VH125'),
        Getter(llt_combined, 'VH_hww125'),
    ), **signal), sigscale),
    signal_label)
channels['llt']['obs'] = Style(Getter(llt_combined, 'data_obs', "Observed"), **data)

#channels['ltt']['wz'] = Style(Getter(ltt_combined, 'WZ', 'WZ'), **main_irreducible)
#channels['ltt']['zz'] = Style(Getter(ltt_combined, 'ZZ', 'ZZ'), **next_irreducible)
#channels['ltt']['fakes'] = Style(Getter(ltt_combined, 'FakeRate', 'Non-prompt'), **fakes)
#channels['ltt']['signal'] = Title(ScaleView(
    #Style(Sum(Getter(ltt_combined, 'WH125')), **signal), sigscale),
    #signal_label)

channels['zh']['zz'] = Style(Getter(zh_combined, 'ZZ', 'ZZ'), **next_irreducible)
channels['zh']['fakes'] = Style(Getter(zh_combined, 'Zjets', 'Non-prompt'), **fakes)
channels['zh']['signal'] = Title(ScaleView(Style(
    Sum(
        Getter(zh_combined, 'VH125'),
        Getter(zh_combined, 'VH_hww125'),
    ), **signal), sigscale),
    signal_label)
channels['zh']['obs'] = Style(Getter(zh_combined, 'data_obs', "Observed"), **data)

print "ZH overflow check"
zh_fakes = channels['zh']['fakes'].Get(None)
print zh_fakes.GetBinContent(zh_fakes.GetNbinsX())
print zh_fakes.GetBinContent(0)
print zh_fakes.Integral()

llt_stack = views.StackView(
    *[channels['llt'][x] for x in ['zz', 'wz', 'fakes', 'signal']])

#ltt_stack = views.StackView(
    #*[channels['ltt'][x] for x in ['zz', 'wz', 'fakes', 'signal']])

zh_stack = views.StackView(
    *[channels['zh'][x] for x in ['zz', 'fakes', 'signal']])

canvas = ROOT.TCanvas("asdf", "asdf", 800, 800)

def make_a_legend(entries=5):
    vh_legend = Legend(
        entries, rightmargin=0.26, topmargin=0.05, leftmargin=0.375)
    vh_legend.SetEntrySeparation(0.0)
    vh_legend.SetMargin(0.35)
    vh_legend.SetBorderSize(0)
    return vh_legend

# Draw LLT
vh_legend = make_a_legend()
llt = llt_stack.Get(None)
llt.Draw()
llt.GetHistogram().GetXaxis().SetRangeUser(0, 200)
llt.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
llt.GetHistogram().GetYaxis().SetTitle("Events")
llt_data = channels['llt']['obs'].Get(None)
llt.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % llt_data.GetBinWidth(1))
llt_data.Draw('same, pe')
blurb = add_cms_blurb('7-8', '10', blurb=' ll#tau_{h}')
vh_legend.AddEntry(llt_data)
vh_legend.AddEntry(llt)
vh_legend.Draw()
canvas.Update()
canvas.SaveAs('llt.pdf')

## Draw LTT
#vh_legend = make_a_legend()
#ltt = ltt_stack.Get(None)
#ltt.Draw()
#ltt.Draw()
#ltt.GetHistogram().GetXaxis().SetRangeUser(0, 200)
#ltt.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
#ltt.GetHistogram().GetYaxis().SetTitle("Events")
#blurb = add_cms_blurb('7+8', '10.0')
#vh_legend.AddEntry(ltt)
#vh_legend.Draw()
#canvas.Update()
#canvas.SaveAs('ltt.pdf')

vh_legend = make_a_legend(4)
zh = zh_stack.Get(None)
zh.Draw()
zh.GetHistogram().GetXaxis().SetRangeUser(0, 200)
zh.GetHistogram().GetXaxis().SetTitle("m_{vis} [GeV]")
zh.GetHistogram().GetYaxis().SetTitle("Events")
blurb = add_cms_blurb('7-8', '10', blurb='llLL')
zh_data = channels['zh']['obs'].Get(None)
zh_data.Draw('same, pe')
zh.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % zh_data.GetBinWidth(1))
vh_legend.AddEntry(zh_data)
vh_legend.AddEntry(zh)
vh_legend.Draw()
canvas.Update()
canvas.SaveAs('zh.pdf')

# Make tau_h tau_h plots
tt = io.open('NEW-LIMITS/cmb/common/htt_tt.input_8TeV.root')

#from FinalStateAnalysis.PlotTools.BlindView import BlindView, blind_in_range

#boost = BlindView(Subdir(tt, 'tauTau_boost'), '.*data_obs',
                  #blinding=blind_in_range(100, 140))

#vbf = BlindView(Subdir(tt, 'tauTau_vbf'), '.*data_obs',
                #blinding=blind_in_range(100, 140))

boost = Subdir(tt, 'tauTau_boost')

vbf = Subdir(tt, 'tauTau_vbf')

channels['boost']['ztt'] = Style(Getter(boost, 'ZTT', 'Z #rightarrow #tau#tau'), **main_irreducible)
channels['boost']['data'] = Style(Getter(boost, 'data_obs', 'Observed'), **data)

channels['boost']['ewk'] = Style(Sum(
    Getter(boost, 'ZJ', 'Electroweak'),
    Getter(boost, 'ZL', 'Electroweak'),
    Getter(boost, 'W', 'Electroweak')), **next_irreducible)

channels['boost']['qcd'] = Style(Getter(boost, 'QCD', 'Multijet'), **fakes)
channels['boost']['ttbar'] = Style(Getter(boost, 'TT', 'ttbar'), **third_irreducible)
channels['boost']['signal'] = Style(ScaleView(Sum(
                #blinding=blind_in_range(100, 140))
    Getter(boost, 'ggH125', '(5#times) m_{H}=125 GeV'),
    Getter(boost, 'qqH125', '(5#times) m_{H}=125 GeV'),
    Getter(boost, 'VH125', '(5#times) m_{H}=125 GeV')), 5), **signal)

boost_stack = views.StackView(
    *[channels['boost'][x] for x in ['ttbar', 'ewk', 'qcd', 'ztt', 'signal']])

legend = make_a_legend(6)
boost = boost_stack.Get(None)
boost.Draw()
boost_data = channels['boost']['data'].Get(None)
boost_data.Draw('same,pe')
boost.SetMaximum(1.2*max(boost.GetMaximum(), boost_data.GetMaximum()))
boost.GetHistogram().GetXaxis().SetRangeUser(0, 300)
boost.GetHistogram().GetXaxis().SetTitle("m_{#tau#tau} [GeV]")
boost.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % boost_data.GetBinWidth(1))
blurb = add_cms_blurb('8', '5')
legend.AddEntry(boost_data)
legend.AddEntry(boost)
legend.Draw()
canvas.Update()
canvas.SaveAs('boost.pdf')

channels['vbf']['ztt'] = Style(Getter(vbf, 'ZTT', 'Z #rightarrow #tau#tau'), **main_irreducible)

channels['vbf']['ewk'] = Style(Sum(
    Getter(vbf, 'ZJ', 'Electroweak'),
    Getter(vbf, 'ZL', 'Electroweak'),
    Getter(vbf, 'W', 'Electroweak')), **next_irreducible)
channels['vbf']['data'] = Style(Getter(vbf, 'data_obs', 'Observed'), **data)

channels['vbf']['qcd'] = Style(Getter(vbf, 'QCD', 'Multijet'), **fakes)
channels['vbf']['ttbar'] = Style(Getter(vbf, 'TT', 'ttbar'), **third_irreducible)
channels['vbf']['signal'] = Style(ScaleView(Sum(
    Getter(vbf, 'ggH125', '(5#times) m_{H}=125 GeV'),
    Getter(vbf, 'qqH125', '(5#times) m_{H}=125 GeV'),
    Getter(vbf, 'VH125', '(5#times) m_{H}=125 GeV')), 5), **signal)

vbf_stack = views.StackView(
    *[channels['vbf'][x] for x in ['ttbar', 'ewk', 'qcd', 'ztt', 'signal']])

legend = make_a_legend(6)
vbf = vbf_stack.Get(None)
vbf.Draw()
vbf_data = channels['vbf']['data'].Get(None)
vbf_data.Draw('same,pe')
vbf.GetHistogram().GetYaxis().SetTitle("Events/%i GeV" % vbf_data.GetBinWidth(1))
vbf.GetHistogram().GetXaxis().SetRangeUser(0, 300)
vbf.GetHistogram().GetXaxis().SetTitle("m_{#tau#tau} [GeV]")
blurb = add_cms_blurb('8', '5')
legend.AddEntry(vbf_data)
legend.AddEntry(vbf)
legend.Draw()
canvas.Update()
canvas.SaveAs('vbf.pdf')

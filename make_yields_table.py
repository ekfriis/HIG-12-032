'''

Build yields for HIG-12-032 results table using data card.


'''

from FinalStateAnalysis.StatTools.DataCard import DataCard
import pprint
import string

# Get the combination of all new channels
megacard = DataCard('megacard_125.txt')

# Store yields for various processes
yields = {
    'llt' : {},
    'ltt' : {},
    'zh' : {},
    # tau_h tau_h
    'boost' : {},
    'vbf' : {},
}

# Get LLT yields
llt_exclude = None
#llt_exclude = '*eet*'
yields['llt']['wz'] = megacard.get_rate('llt*', 'wz', excludebin=llt_exclude)
yields['llt']['zz'] = megacard.get_rate('llt*', 'zz', excludebin=llt_exclude)
yields['llt']['fakes'] = megacard.get_rate('llt*', 'fakes', excludebin=llt_exclude)
yields['llt']['VH'] = megacard.get_rate('llt*', 'VH', excludebin=llt_exclude)
yields['llt']['VHww'] = megacard.get_rate('llt*', 'VH_hww', excludebin=llt_exclude)
yields['llt']['total'] = yields['llt']['wz'] + yields['llt']['zz'] + yields['llt']['fakes']
yields['llt']['obs'] = megacard.get_obs('llt*')

#yields['ltt']['wz'] = megacard.get_rate('ltt*', 'wz')
#yields['ltt']['zz'] = megacard.get_rate('ltt*', 'zz')
#yields['ltt']['fakes'] = megacard.get_rate('ltt*', 'fakes')
#yields['ltt']['VH'] = megacard.get_rate('ltt*', 'VH')
#yields['ltt']['VHww'] = 0
#yields['ltt']['total'] = yields['ltt']['wz'] + yields['ltt']['zz'] + yields['ltt']['fakes']

yields['zh']['zz'] = megacard.get_rate('ZH*', 'ZZ')
yields['zh']['fakes'] = megacard.get_rate('ZH*', 'Zjets')
yields['zh']['VH'] = megacard.get_rate('ZH*', 'VH')
yields['zh']['VHww'] = megacard.get_rate('ZH*', 'VH_hww')
yields['zh']['total'] = yields['zh']['zz'] + yields['zh']['fakes']
yields['zh']['obs'] = megacard.get_obs('ZH*')

yields['boost']['fakes'] = megacard.get_rate('boost*', 'QCD')
yields['boost']['ZTT'] = megacard.get_rate('boost*', 'ZTT')
yields['boost']['ZJ'] = megacard.get_rate('boost*', 'ZJ')
yields['boost']['ZL'] = megacard.get_rate('boost*', 'ZL')
yields['boost']['TT'] = megacard.get_rate('boost*', 'TT')
yields['boost']['VV'] = megacard.get_rate('boost*', 'VV')
yields['boost']['W'] = megacard.get_rate('boost*', 'W')
yields['boost']['VH'] = megacard.get_rate('boost*', 'VH')
yields['boost']['ggH'] = megacard.get_rate('boost*', 'ggH')
yields['boost']['qqH'] = megacard.get_rate('boost*', 'qqH')
yields['boost']['total'] = sum(
    yields['boost'][x] for x in ['fakes', 'ZJ', 'ZL', 'TT', 'VV', 'W', 'ZTT'])
yields['boost']['obs'] = megacard.get_obs('boost*')

yields['vbf']['fakes'] = megacard.get_rate('vbf*', 'QCD')
yields['vbf']['ZTT'] = megacard.get_rate('vbf*', 'ZTT')
yields['vbf']['ZJ'] = megacard.get_rate('vbf*', 'ZJ')
yields['vbf']['ZL'] = megacard.get_rate('vbf*', 'ZL')
yields['vbf']['TT'] = megacard.get_rate('vbf*', 'TT')
yields['vbf']['VV'] = megacard.get_rate('vbf*', 'VV')
yields['vbf']['W'] = megacard.get_rate('vbf*', 'W')
yields['vbf']['VH'] = megacard.get_rate('vbf*', 'VH')
yields['vbf']['ggH'] = megacard.get_rate('vbf*', 'ggH')
yields['vbf']['qqH'] = megacard.get_rate('vbf*', 'qqH')
yields['vbf']['total'] = sum(
    yields['vbf'][x] for x in ['fakes', 'ZJ', 'ZL', 'TT', 'VV', 'W', 'ZTT'])
yields['vbf']['obs'] = megacard.get_obs('vbf*')

def render(the_yield):
    if isinstance(the_yield, int):
        return str(the_yield)
    elif isinstance(the_yield, float):
        return "%0.f" % the_yield
    return r'$ %0.2f \pm %0.2f $' % (the_yield.nominal_value,
                                       the_yield.std_dev())

# flatten dictionary and stringify yields
flat = {}
for channel, channel_info in yields.iteritems():
    for process, process_yield in channel_info.iteritems():
        flat[channel + process] = render(process_yield)

vh_template = r'''
    \begin{tabular}{l | c | c}
      Process & $$\ell \ell \tau_h$$  & $$ \ell\ell LL $$ \\
      \hline
      Fakes & $lltfakes & \multirow{2}{*}{$zhfakes} \\
      WZ & $lltwz & \\
      \hline
      ZZ & $lltzz & $zhzz \\
      \hline
      \hline
      Total bkg. &  $llttotal & $zhtotal \\
      \hline
      VH$$\to\tau\tau (m_H=125\GeV)$$ & $lltVH & $zhVH \\
      VH$$\to WW (m_H=125\GeV)$$ & $lltVHww & $zhVHww \\
      \hline
      Observed $lltobs & $zhobs & \\
    \end{tabular}
'''

tt_template = r'''
    \begin{tabular}{l | c | c }
      Process & $$j \tau_h \tau_h$$ & $$jj \tau_h \tau_h$$ \\
      \hline
      Z$$\to\tau\tau$$ & $boostZTT & $vbfZTT \\
      Multijet &  $boostfakes & $vbffakes \\
      W+jets &  $boostW & $vbfW \\
      Z$$\ell\to\tau_h$$ fake &  $boostZL & $vbfZL \\
      Z+jet$$\to\tau_h$$ fake &  $boostZJ & $vbfZJ \\
      $$\ttbar$$ &  $boostTT & $vbfTT \\
      Dibosons &  $boostVV & $vbfVV \\
      \hline
      \hline
      Total bkg. &  $boosttotal & $vbftotal \\
      \hline
      VH$$\to\tau\tau (m_H=125\GeV)$$ & $boostVH & $vbfVH \\
      ggH$$\to\tau\tau (m_H=125\GeV)$$ & $boostggH & $vbfggH \\
      qqH$$\to\tau\tau (m_H=125\GeV)$$ & $boostqqH & $vbfqqH \\
      \hline
      Observed $boostobs & $vbfobs & \\
    \end{tabular}
'''

with open('vh_table.tex', 'w') as vh_file:
    vh_file.write(string.Template(vh_template).substitute(**flat))

with open('tt_table.tex', 'w') as tt_file:
    tt_file.write(string.Template(tt_template).substitute(**flat))

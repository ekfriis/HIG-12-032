
# Task to run a limit
def make_task(directory)
  mass = File.basename(directory)
  output = "#{directory}/higgsCombine-exp.Asymptotic.mH#{mass}.root"
  inputs = Dir.glob("#{directory}/*.txt")
  file output => inputs do |t|
    puts t.investigation
    sh "limit.py --expectedOnly --asymptotic --userOpt '-t -1 --minosAlgo stepping' #{directory}"
  end
  return output
end

masses = Array[115, 120, 125, 130, 135, 140]

multitask :newlimits => []

masses.each do |mass|
  multitask :newlimits => make_task("NEW-LIMITS/cmb/#{mass}")
  #multitask :newlimits => make_task("NEW-LIMITS/ltt/#{mass}")
  multitask :newlimits => make_task("NEW-LIMITS/llt/#{mass}")
  multitask :newlimits => make_task("NEW-LIMITS/4l/#{mass}")
  multitask :newlimits => make_task("NEW-LIMITS/tt/#{mass}")
  multitask :oldlimits => make_task("STANDARD-LIMITS/cmb/#{mass}")
  multitask :megalimits => make_task("ALL-LIMITS/cmb/#{mass}")
end

task :newplots => [] do |t|
  chdir('NEW-LIMITS') do 
    #sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py ltt"
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py llt"
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py cmb"
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py 4l"
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_vhtt_layout.py tt"
  end
end

task :oldplots => [] do |t|
  chdir('STANDARD-LIMITS') do 
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_layout.py cmb"
  end
end

task :megaplots => [] do |t|
  chdir('ALL-LIMITS') do 
    sh "plot asymptotic $CMSSW_BASE/src/HiggsAnalysis/HiggsToTauTau/python/layouts/sm_htt_layout.py cmb"
  end
end

class Task 
  def investigation
    result = "------------------------------\n"
    result << "Investigating #{name}\n" 
    result << "class: #{self.class}\n"
    result <<  "task needed: #{needed?}\n"
    result <<  "timestamp: #{timestamp}\n"
    result << "pre-requisites: \n"
    prereqs = @prerequisites.collect {|name| Task[name]}
    prereqs.sort! {|a,b| a.timestamp <=> b.timestamp}
    prereqs.each do |p|
      result << "--#{p.name} (#{p.timestamp})\n"
    end
    latest_prereq = @prerequisites.collect{|n| Task[n].timestamp}.max
    result <<  "latest-prerequisite time: #{latest_prereq}\n"
    result << "................................\n\n"
    return result
  end
end




# Task to run a limit
def make_task(directory)
  mass = File.basename(directory)
  output_asymp = "#{directory}/higgsCombine-exp.Asymptotic.mH#{mass}.root"
  inputs = Dir.glob("#{directory}/*.txt")
  file output_asymp => inputs do |t|
    puts t.investigation
    #sh "limit.py --expectedOnly --asymptotic --userOpt '-t -1 --minosAlgo stepping' #{directory}"
    sh "limit.py --asymptotic --userOpt '--minosAlgo stepping' #{directory}"
  end

  return output_asymp
end

def make_cls_task(directory)
  mass = File.basename(directory)
  output_cls = "#{directory}/higgsCombineTest.HybridNew.mH#{mass}.root"
  inputs = Dir.glob("#{directory}/*.txt") + Dir.glob("#{directory}/crab*/res/*root")
  file output_cls => inputs do |t|
    puts t.investigation
    #sh "limit.py --expectedOnly --asymptotic --userOpt '-t -1 --minosAlgo stepping' #{directory}"
    sh "limit.py --CLs #{directory}"
  end
  return output_cls
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

multitask :newclslimits=> []

masses.each do |mass|
  multitask :newclslimits=> make_cls_task("NEW-LIMITS/cmb/#{mass}")
  #multitask :newclslimits=> make_cls_task("NEW-LIMITS/ltt/#{mass}")
  multitask :newclslimits=> make_cls_task("NEW-LIMITS/llt/#{mass}")
  multitask :newclslimits=> make_cls_task("NEW-LIMITS/4l/#{mass}")
  multitask :newclslimits=> make_cls_task("NEW-LIMITS/tt/#{mass}")
  multitask :oldclslimits=> make_cls_task("STANDARD-LIMITS/cmb/#{mass}")
  multitask :megaclslimits=> make_cls_task("ALL-LIMITS/cmb/#{mass}")
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



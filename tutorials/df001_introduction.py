import ROOT

def fill_tree(treeName, fileName):
	df = ROOT.RDataFrame(10)
	df.Define("b1", "(double) rdfentry_")\
	   .Define("b2", "(int) rdfentry_ * rdfentry_").Snapshot(treeName, fileName)

	   
fileName = "df001_introduction_py.root"
treeName = "myTree"
fill_tree(treeName, fileName)

d = ROOT.RDataFrame(treeName, fileName)

h = d.Histo1D(("fig", "name", 4, 0, 9), "b1")
h.Draw()
'''
cutb1 = 'b1 <5.'
cutb1b2 = 'b2 % 2 && b1<4'

entries1 = d.Filter(cutb1) \
	    .Filter(cutb1b2) \
	    .Count();
	    
print('{} entries passed all filters'.format(entries1.GetValue()))



# `Min`, `Max` and `Mean` actions
# These actions allow to retrieve statistical information about the entries
# passing the cuts, if any.

b1b2_cut = d.Filter(cutb1b2)
minVal = b1b2_cut.Min('b1')
maxVal = b1b2_cut.Max('b1')
meanVal = b1b2_cut.Mean('b1')
nonDefmeanVal = b1b2_cut.Mean("b2")
print('The mean is always included between the min and the max: {0} <= {1} <= {2}'.format(minVal.GetValue(), meanVal.GetValue(), maxVal.GetValue()))


hist = d.Filter(cutb1).Histo1D('b1')
print('Filled h {0} times, mean: {1}'.format(hist.GetEntries(), hist.GetMean()))


cutb1_result = d.Filter(cutb1)
cutb1b2_result = d.Filter(cutb1b2)
cutb1_cutb1b2_result = cutb1_result.Filter(cutb1b2)

evts_cutb1_result = cutb1_result.Count()
evts_cutb1b2_result = cutb1b2_result.Count()
evts_cutb1_cutb1b2_result = cutb1_cutb1b2_result.Count()

print('Events passing cutb1: {}'.format(evts_cutb1_result.GetValue()))
print('Events passing cutb1b2: {}'.format(evts_cutb1b2_result.GetValue()))
print('Events passing both: {}'.format(evts_cutb1_cutb1b2_result.GetValue()))


entries_sum = d.Define('sum', 'b1 + b2') \
	       .Filter('sum > 4.2') \
	       .Count()
	       
print(entries_sum.GetValue())
'''

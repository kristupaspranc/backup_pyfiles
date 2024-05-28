import ROOT
#import gi
#gi.require_version('Gtk', '2.0')

df = ROOT.RDataFrame(1024)

coordDefineCode = '''ROOT::RVecD {0}(len);
                     std::transform({0}.begin(), {0}.end(), {0}.begin(), [](double){{return gRandom->Uniform(-1.0, 1.0);}});
                     return {0};'''

d = df.Define("len", "gRandom->Uniform(0,16)")\
      .Define("x", coordDefineCode.format("x"))\
      .Define("y", coordDefineCode.format("y"))

d1 = d.Define("r", "sqrt(x*x + y*y)")

ring_h = d1.Define("rInFig", "r > .5 && x*y < 0")\
	   .Define("yFig", "y[rInFig]")\
	   .Define("xFig", "x[rInFig]")\
	   .Histo2D(("fig", "Two quarters of a ring", 64, -1.1, 1.1, 64, -1.1, 1.1), "xFig", "yFig")


cring = ROOT.TCanvas()
ring_h.Draw("Copz")
cring.SaveAs("df016_ring.png")



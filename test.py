import numpy as np
import pandas as pd
import pcreode

file_nm = "data/synthetic.csv"
expression = pd.read_csv( file_nm, skiprows=[0])

data_pca = pcreode.PCA( expression)
data_pca.get_pca()

pca_reduced_data = data_pca.pca_set_components( min( 3, expression.shape[1]))

# calculate density
dens = pcreode.Density( pca_reduced_data)
best_guess = dens.radius_best_guess()
density = dens.get_density( radius=best_guess, mute=True)

# get downsampling parameters
noise, target = pcreode.get_thresholds( pca_reduced_data)

num_runs = 2
file_path = "test/"

# run pCreode
out_graph, out_ids = pcreode.pCreode(
  data=pca_reduced_data,
  density=density,
  noise=noise,
  target=target,
  file_path=file_path,
  num_runs=num_runs,
  mute=True
)

# score graphs, returns a vector of ranks by similarity
graph_ranks = pcreode.pCreode_Scoring( data=pca_reduced_data, file_path=file_path, num_graphs=num_runs, mute=True)
# select most representative graph
gid = graph_ranks[0]

# extract cell graph
analysis = pcreode.Analysis(
  file_path=file_path,
  graph_id=gid,
  data=pca_reduced_data,
  density=density,
  noise=noise
)

print "all good"

import sys
import numpy as np
import actress
import actress.run_actress_notebook as actr
import os

if "CHUNK_ID" in os.environ:
    chunk_id = int(os.environ["CHUNK_ID"])
    n_chunks = int(os.environ["N_CHUNKS"])
else:
    chunk_id = int(sys.argv[1])
    n_chunks = int(sys.argv[2])

print(f"Running chunk {chunk_id} of {n_chunks}")


# load fixed facula distribution
data = np.load("faculae_distribution.npz")
rs = data["rs"]
longs = data["longs"]
lats = data["lats"]

phot_files = [f"test_phot_{i}.txt" for i in range(11)]
fac_files  = [f"test_fac_{i}.txt" for i in range(11)]

# all runs you want
'''
pairs = [
    (0, 3),
    (0, 4), (4, 5), (4, 9),
    (5, 3), (5, 5), (5, 9),
    (9, 3), (9, 5), (9, 9),
]
'''
pairs = [(0,5)]

# split jobs
chunks = np.array_split(pairs, n_chunks)
my_pairs = chunks[chunk_id]

print("Chunk:", chunk_id)
print("Pairs:", my_pairs)

for i, j in my_pairs:

    phot_file = phot_files[i]
    fac_file = fac_files[j]


    
    params = actr.Transitparams()

    params.res = 200 #image resolution (2D prejection)
    params.rp = 0.3808
    params.b = -0.04
    params.N = 100
    params.mode = "faconly"

    params.fac_r = rs
    params.fac_long = longs
    params.fac_lat = lats

    params.fac_band = False
    params.fac_band_low = [40]
    params.fac_band_high = [40]

    params.a = 25.01
    params.T = 4.544
    params.phi = 1.0
    params.ld = "power2"

    #save = f"batch_phot{i+1}_fac{j+1}"

    #print(f"Running {save}")
    print(f"Phot file: {phot_file}")
    print(f"Fac file: {fac_file}")

    res_list = [256, 512, 1024]
    
    for res in res_list:
        params.healpix_res = res #stekkar surface resolutions 3D sphere
    
        save = f"res_test_phot{i+1}_fac{j+1}_healpix{res}"

            
        actr.Transitsim(params).sim_spectrum(
            hd_ld_file=phot_file,
            fac_ld_file=fac_file,
            gif_save=False,
            lightcurve_save=save
        )

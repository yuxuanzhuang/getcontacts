# MDContactNetworks
Library for computing dynamic non-covalent contact networks in proteins throughout MD Simulation/


## File format

MDContactNetworks is compatible with all topology and trajectory file formats readable in VMD.


## Running the Code

### 1. Computing non-covalent contacts in a protein throughout every frame of a MD Simulation fragment
   
   __Input:__ 

	Required Arguments:

	   --topology TOPOLOGY - Path to topology
	   --trajectory TRAJECTORY - Path to simulation trajectory fragment
	   --output_dir OUTPUT_DIRECTORY - Path of output directory
	   --itypes INTERACTION_TYPES - User specifies what type of non-covalent interaction to compute using the following flags. 

		   -sb, Salt bridges
		   -pc, Pi-cation 
		   -ps, Pi-stacking
		   -ts, T-stacking
		   -vdw, Van Der Waals
		   -hb, Hydrogen Bonds
		   -lhb, Ligand Hydrogen Bonds

		   Hydrogen bonds are automatically stratified to following subtypes and written as output.

		   -hbbb, Backbone-backbone hydrogen bonds
		   -hbsb, Backbone-sidechain hydrogen bonds
		   -hbss, Sidechain-sidechain hydrogen bonds
		   -wb, Water-mediated hydrogen bond
		   -wb2, Extended water-mediated hydrogen bond
		   -hlb, Ligand-backbone hydrogen bonds
		   -hls, Ligand-sidechain hydrogen bonds
		   -lwb, Ligand water-mediated hydrogen bond
		   -lwb2, Ligand extended water-mediated hydrogen bond


	Optional Arguments:

		-cores NUM_CORES Number of cpu cores to parallelize computations on, default = 6

		-ligand LIGAND Resname of ligand molecule, default = None

		-sele SELECTION VMD selection query to compute contacts in specified region of protein, default = None

		-solv SOLVENT Solvent identifier in simulation, default = "TIP3"

   
   __Output:__ Tables storing non-covalent contacts. Tab delimited rows are formatted to include 
   frame index, atom labels, and interaction types. 

   __Examples:__

	python dynamic_contact_networks.py --topology TOP.pdb --trajectory TRAJ.nc --cores 12 --solv IP3 --sele "chain A and resid 100 to 160" --ligand EJ4 --itype -sb -hb -lhb

	python dynamic_contact_networks.py --topology TOP.psf --trajectory TRAJ.dcd --cores 6 --itype -pc -ps -vdw


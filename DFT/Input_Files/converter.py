#!/usr/bin/env python3

from pymatgen.io.cif import CifParser
# Use the older pwscf module:
from pymatgen.io.pwscf import PWInput

# 1) Path to your CIF file
cif_file = "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/passing_cifs/qmof-0e64acd.cif"

# 2) Parse the CIF
parser = CifParser(cif_file)
structure = parser.get_structures()[0]

# 3) Define pseudopotential mappings (adjust the paths to your local files)
pseudopotentials = {
    "Al": "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/SSSP_1.3.0_PBE_efficiency/Al.pbe-n-kjpaw_psl.1.0.0.UPF",
    "H":  "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/SSSP_1.3.0_PBE_efficiency/H.pbe-rrkjus_psl.1.0.0.UPF",
    "C":  "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/SSSP_1.3.0_PBE_efficiency/C.pbe-n-kjpaw_psl.1.0.0.UPF",
    "N":  "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/SSSP_1.3.0_PBE_efficiency/N.pbe-n-radius_5.UPF",
    "O":  "/Users/moinkhwaja/Documents/GitHub/HTS_MOF_Hydrogenation /DFT/SSSP_1.3.0_PBE_efficiency/O.pbe-n-kjpaw_psl.0.1.UPF",
}

# 4) CONTROL parameters
control_params = {
    "calculation": "relax",         # 'relax' = atomic position optimization
    # Use 'vc-relax' if also optimizing the cell volume/shape
    "pseudo_dir": ".",              # Not strictly needed since we use full paths
    "outdir": "./out",
    "prefix": "qmof-0e64acd_relax"
}

# 5) SYSTEM parameters
system_params = {
    "ibrav": 0,                     # Read lattice from structure
    "ecutwfc": 50.0,                # Wavefunction cutoff (Ry)
    "ecutrho": 400.0,               # Charge density cutoff (Ry)

    # Spin-polarized:
    "nspin": 2,                     # Spin-polarized
    # If you expect magnetism, you may specify starting_magnetization, e.g.:
    # "starting_magnetization(1)": 0.1,

    # If your system is an insulator, you might use 'occupations': 'fixed'. Otherwise:
    "occupations": "smearing",
    "smearing": "gaussian",
    "degauss": 0.01,                # (Ry) Gaussian smearing width
}

# 6) ELECTRONS parameters
electrons_params = {
    "conv_thr": 1.0e-6,            # SCF convergence threshold (Ry)
    "mixing_beta": 0.3
}

# 7) IONS parameters (for relaxation)
ions_params = {
    "ion_dynamics": "cg",          # Conjugate gradient
    "forc_conv_thr": 1.0e-3,       # (Ry/Bohr) Force convergence threshold
}

# 8) (Optional) CELL parameters if you're doing 'vc-relax'. Omit for 'relax'.
# cell_params = {
#     "cell_dynamics": "bfgs",
#     "press_conv_thr": 0.5
# }

# 9) Create the PWInput object using the older pwscf interface:
pw_input = PWInput(
    structure=structure,
    pseudo=pseudopotentials,
    control=control_params,
    system=system_params,
    electrons=electrons_params,
    ions=ions_params,
    # cell=cell_params,            # Uncomment if using vc-relax
    # For a large MOF, Gamma-only k-point is common:
    kpoints_mode="gamma"
)

# 10) Write the QE input file
output_file = "qmof-0e64acd_relax.in"
pw_input.write_file(output_file)

print(f"QE input file '{output_file}' generated using pymatgen.io.pwscf.")



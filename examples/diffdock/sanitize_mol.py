"""Get rid of kekulization errors. Assign formal charge based on valence."""
# https://depth-first.com/articles/2020/02/10/a-comprehensive-treatment-of-aromaticity-in-the-smiles-language/
# Beware of issues with shutil.copy https://docs.python.org/3/library/shutil.html
import argparse
from pathlib import Path
import shutil
from typing import Type

import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem
from openbabel import openbabel

parser = argparse.ArgumentParser()
parser.add_argument('--ligand_path', type=str, help='Ligand file path')
args = parser.parse_args()
ligand = Path(args.ligand_path).name
molname = 'clean_' + ligand

def adjust_formal_charges(molecule: Type[Chem.SDMolSupplier]) -> Type[Chem.SDMolSupplier]:
    """ Sometimes input structures do not have correct formal charges corresponding 
    to bond order topology. So choose to trust bond orders assigned and generate formal 
    charges based on that.
    Explicit valence determined what the formal charge should be from dictionary of valence 
    to formal charge for that atomic number. Special case if atom == carbon or nitrogen 
    and if neighbors contain nitrogen, oyxgen or sulfur (polarizable atoms) then if carbon 
    and explicit valence only 3, give formal charge of +1 (more stable then -1 case).
    Args:
        molecule: The rdkit molecule object

    Returns:
        retval: Molecule object with adjusted formal charges
    """
    atomicnumtoformalchg={1:{2:1},5:{4:1},6:{3:-1},7:{2:-1,4:1},8:{1:-1,3:1},15:{4:1},\
                16:{1:-1,3:1,5:-1},17:{0:-1,4:3},9:{0:-1},35:{0:-1},53:{0:-1}}
    for atom in molecule.GetAtoms():
        atomnum=atom.GetAtomicNum()
        val=atom.GetExplicitValence()
        valtochg=atomicnumtoformalchg[atomnum]
        if val not in valtochg.keys(): # then assume chg=0
            chg=0
        else:
            chg=valtochg[val]
        polneighb=False
        if atomnum == 6 or atomnum == 7:
            for natom in atom.GetNeighbors():
                natomicnum=natom.GetAtomicNum()
                if natomicnum == 7 or natomicnum == 8 or natomicnum == 16:
                    polneighb=True
            if polneighb and val == 3 and atomnum == 6:
                chg=1

        atom.SetFormalCharge(chg)
    return molecule

def babel_remove_aromatic_bonds(molname_ins: str) -> None:
    """ Openbabel seems to be able to remove aromatic bonds (shows up as bond order 4 in SDF)
    Need to remove this before rdkit can read the molecule. Openbabel attempts to assign 
    a kekule form automatically. Strange cases can happen such as if indole ring nitrogen 
    is missing a hydrogen, then the kekule form you would expect for indole ring is not 
    assigned and one of the carbons in between both rings will be assigned formal charge of -1 
    (since three bonds all single bond order).
    Args:
        molname_ins: The molname of new output SDF file
    """
    ob_conversion = openbabel.OBConversion()
    mol = openbabel.OBMol()
    in_format = ob_conversion.FormatFromExt(molname_ins)
    ob_conversion.SetInFormat(in_format)
    ob_conversion.ReadFile(mol, molname_ins)
    ob_conversion.SetOutFormat(in_format)
    ob_conversion.WriteFile(mol,molname_ins)

def sanitize_mol(molecule: Type[Chem.SDMolSupplier], molname_ins: str) -> None:
    """ Catch exception for Kekulization error and Sanitzation error then fix
    Args:
        molecule: The rdkit molecule object
        molname_ins: The molname of new output SDF file
    """
    molecule = adjust_formal_charges(molecule)
    writer = Chem.SDWriter(molname_ins)
    writer.write(molecule)
    writer.close()

r = Chem.SDMolSupplier(ligand, sanitize=False, removeHs=False)
m: Type[Chem.SDMolSupplier] = r[0]

try:
    Chem.SanitizeMol(m) # kekulization error need remove aromatic bonds
    # can also be explicit valence error (i.e.) formal charge not consistent with bond topology
    # choose to trust bond topology around atom and add formal charge based on that
    shutil.copy(ligand, molname)
except rdkit.Chem.rdchem.KekulizeException as e:
    babel_remove_aromatic_bonds(ligand)
    r = Chem.SDMolSupplier(ligand, sanitize=False, removeHs=False)
    new_m: Type[Chem.SDMolSupplier] = r[0]
    sanitize_mol(new_m, molname)
except rdkit.Chem.rdchem.MolSanitizeException as e:
    sanitize_mol(m, molname)

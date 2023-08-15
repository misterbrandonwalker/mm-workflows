"""Get rid of kekulization errors"""
import argparse
from pathlib import Path

from openbabel import openbabel

parser = argparse.ArgumentParser()
parser.add_argument('--ligand_path', type=str, help='Ligand file path')
args = parser.parse_args()
ligand = Path(args.ligand_path).name
obConversion = openbabel.OBConversion()
inFormat = obConversion.FormatFromExt(ligand)
obConversion.SetInFormat(inFormat)
obConversion.SetOutFormat(inFormat)
ligmol = openbabel.OBMol()
obConversion.ReadFile(ligmol, ligand)
molname = 'clean_' + ligand
obConversion.WriteFile(ligmol, molname)

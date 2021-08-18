import sys

if sys.version_info[0] >= 3:
    unicode = str
import pandas as pd

print("This generates a python dataframe and .CSV file for the Common Garden data...", "\n")

inv_data = pd.read_csv(r'2021 Common Garden Data Working Copy.csv', header=0)
print(inv_data)

# This dataframe has the following variables ... not all of which are going to be useful.
# year - year the plots were censused
# census - year and season the plots were censused, e.g. 2008 summer
# pop - population the family originated from (nested within cont_orig).
# cont_orig	- the continent (Europe/NorthAmerica where the population originated
# cont_dest	- the continent the plant was planted in
# site- the site (CA, VA, CH, UK) the plants are planted in, nested within continent (nested within cont_dest)
# treatment	- Treated with fungicide or herbicide (FI) versus controls (CN)
# block	- This was a split plot design, so one replicate of each family, treatment etc,
#           was in each block. The design is laid our clearly in Dex's thesis.
#           The abbreviation here is the site [e.g. CH] and the plot within [e.g. CH04]
# plant_ID - unique plant identifier
# sex- male of female or unknown (missing value)
# survival - A or D depending on whether the plant was alive or dead at that census
# longevity	- This is a strange one. It is the number of census periods this plant eventually lived.
#           As a result, it is the same data for all the census perions. There are other versions of the
#           data where longevity is recorded up to that point, rather than overall.
# basal_lvs - The number of leaves on the basal rosette of the plant. Plants that are alive have either
#           basal leaves or stem leaves or both. Right now a correction is needed, basal leaves should
#           be a zero rather than a missing value for live plants.
# stem_lvs	- the number of leaves on the stem or bolt. Plants that are alive have either
#             basal leaves or stem leaves or both. Right now a correction is needed, stem leaves should
#             be a zero rather than a missing value for live plants.
# total_lvs	- basal_leaves + stem leaves
# bolt_ht - this is the height of all bolts summed. If there are zero bolts, I think it is OK to have this
#            as a missing value.
# bolt_num - number of bolts. Plants that are alive should have zero bolts, not missing values.
# status - reproductive status, V [vegetative], B [bolting], FL [flowering], FR [fruiting].
#           Males can't be FR.
# rep_spd - Number of censuses until the first reproduction. This variable is like longevity in that it is
#           a cumulative measure reported the same data in each census. For example, at the first
#           census, you can see reproductive speeds of 3,4 or 5. Dead plants can have a non-zero
#           reproductive speed because they may have reproduced then died. Plants that died without
#           reproducing currently have a missing value.
# flwr_num - flower number in the current census.
# frt_num - fruit number in the current census. Males have mising values for fruit number.
# frt_hadena - hadena damaged fruits in the current census. Males have missing values.
# reproduced - I have no idea what this variable is.
# smut - Healthy (H) or diseased (S). Change these to ones and zeroes?
# num_smutted_fl - When diseased, how many flowers displayed disease
# leaf_herb	- an index (0-3) for the severity of leaf herbivory
# gen_ENMY - an index (0-3) for the severity of damage by generalist enemies. Rarely a 3.
# spec_ENMY - an index (0-3) for the severity of damage by specialist enemies, smut and hadena. Values
#           never exceeded 1.

DNA_data = pd.read_csv(r'Structure_assignments.csv', header=0)
print(DNA_data)

# This dataframe has the following variables ... not all of which are going to be useful.
# plant_ID - a unique identifier that corresponds to the plant IDs in the common garden data.
# ID - a useless variable that seems to correspond to row number
# sire - male parent used to generate F1s, all crosses were within populations
# dam - female parent used to generate F1s, all crosses were within populations
# subpop - looks like full sibships. These are the ~58 full sib families referred to in the dissertation
# sire.pop - population of origin of the sire, somewhere we should be able to connect this to
#           actual names of families and pops.
# dam.pop - will always be the same as sire.pop
# structure region - demes assigned by structure.


# Since we generated only one family per pop, the full sib families and pops can
#        be used to identify each other.
# Therefore, Merge the common garden and molecular results. Use the common garden data to assign
#           pop names in the molecular results. Then go back and assign molecular data to each
#           common garden plant.
# First, generate a streamlined common garden dataset that simply gives us plant numbers and
#            associated population names, then we can assign population names to the plant numbers
#            in the molecular data. Eventually we can use the pop names to merge the molecular data
#            into the common garden data.
# I needed to create these tempindex variables because what I did below created variable names that
#           were also in the index. Anyway, I am not good enough at python to figure out the best way
#           to resolve this, so I created these temporary variables in inv_data that I will delete later.
# with all that, the following takes the pop names from the large dataset and merges them into the DNA
#           data. We retain only the population and plant_ID.
inv_data['tempindex1'] = inv_data['pop']
inv_data['tempindex2'] = inv_data['plant_ID']
family_ID = inv_data.groupby(['tempindex1', 'tempindex2']).agg({'pop': 'first', 'plant_ID': 'first'})
family_ID = family_ID.merge(DNA_data)

# rename subpop to sibship
family_ID = family_ID.rename(columns={"subpop": "sibship"})
# do this thing with the temporary index again
family_ID['tempindex1'] = family_ID['pop']
# reduce the DNA data down to a single row per population so that can get merged with the common garden
family_ID = family_ID.groupby(['tempindex1']).agg({'pop': 'first', 'sire': 'first', 'dam': 'first', 'sibship': 'first',
                                                   'sire.pop': 'first', 'dam.pop': 'first',
                                                   'Structure_region': 'first'})
print(family_ID)

# now merge the molecular data back (family_ID) into the larger dataset using pop as the key/index.

inv_data = inv_data.merge(family_ID[['sire', 'dam', 'sibship', 'sire.pop', 'dam.pop', 'Structure_region']],
                        on=['tempindex1', 'tempindex1'], how='right', indicator=False)
inv_data = inv_data.drop(columns=['tempindex1', 'tempindex2'])
print(inv_data)

# There are some question marks in the molecular data, replace with missing values.
inv_data=inv_data.replace('?', '')

# uncomment the line below to get a copy of the original common garden data merged with the structure results.
inv_data.to_csv(r'raw garden data with deme assignments.csv', index=False)

# From here, we are going to take a major direction. We have data from ~7 census dates. Rather than
# try to analyze those using something like repeated measures, or aster, we will create summary
# variables. For example, lifetime fitness for females might be the sum of fruit production across
# all census dates.

# In addition, we will transform the data to make it appropriate for parametric statistics

# Later, we can standardize the data for selection analyses.





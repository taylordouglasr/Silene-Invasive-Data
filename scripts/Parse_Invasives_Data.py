import sys

if sys.version_info[0] >= 3:
    unicode = str
import pandas as pd
import numpy as np


# function to get alist of the unique values from a list, handy when looking for weird values
# in the data. The second function reports the number of unique elements, also handy for fixing up the data.
def unique(list1):
    x = np.array(list1)
    y = np.unique(x)
    return y


def len_unique(list1):
    x = np.array(list1)
    y = np.unique(x)
    z = len(y)
    return z


print("This generates a python dataframe and .CSV file for the Common Garden data...", "\n")

# These is the raw data used to generate the results from Dexter's thesis.
inv_data = pd.read_csv(r'2021 Common Garden Data Working Copy.csv', header=0)
# This dataframe has the following variables ... not all of which are going to be useful.
# year - year the plots were censused
# census - year and season the plots were censused, e.g. 2008summer
# pop - population the family originated from (nested within cont_orig).
# cont_orig	- the continent (Europe/NorthAmerica where the population originated (Europe, NorthAmerica)
# cont_dest	- the continent the plant was planted in  (Europe, NorthAmerica)
# site- the site (CA, VA, CH, UK) the plants are planted in, nested within continent (nested within cont_dest)
# treatment	- Treated with fungicide or herbicide (FI) versus controls (CN)
# block	- This was a split plot design, so one replicate of each family, treatment etc,
#           was in each block. The design is laid our clearly in Dex's thesis.
#           The abbreviation here is the site [e.g. CH] and the plot within [e.g. CH04]
# plant_ID - unique plant identifier
# sex- male or female or unknown (missing value)...sex is a variable that has a lot of complications.
#            There are ambiguous genders, and when we get to data analysis, we have to decide how
#            to treat the genders differently. For example, males have no fruits. Is it possible to
#            do a selection analysis on both genders if the variable we define as fitness is not the same?
#            If we do a selection analysis on the two genders separately, do we just omit plants that
#             never flowered?
# survival - A or D depending on whether the plant was alive or dead at that census, later we will
#           switch this to 1s and 0s.
# longevity	- This is a strange one. It is the number of census periods this plant eventually lived.
#           As a result, the same value was copied for all the census periods.
# basal_lvs - The number of leaves on the basal rosette of the plant. Plants that are alive have either
#           basal leaves or stem leaves or both. A correction is needed, basal leaves should
#           be a zero rather than a missing value for live plants. In fact, for all phenotypic traits
#           on living plants, missing values should be replaced with zero. Missing values on dead plants
#           is fine.
# stem_lvs	- the number of leaves on the stem or bolt. Plants that are alive have either
#             basal leaves or stem leaves or both. Right now a correction is needed, stem leaves should
#             be a zero rather than a missing value for live plants.
# total_lvs	- basal_leaves + stem leaves
# bolt_ht - this is the height of all bolts summed. If there are zero bolts, I am not sure whether to have this
#            as a missing value or a zero, but lean toward a zero.
# bolt_num - number of bolts. Plants that are alive should not have missing values.
# status - reproductive status, V [vegetative], B [bolting], FL [flowering], FR [fruiting].
#           Males can't be FR, so we need to be careful with respect to sex if we analyze this.
# rep_spd - Number of censuses until the first reproduction. This variable is like longevity in that it is
#           a cumulative measure reported the same data in each census. For example, at the first
#           census, you can see reproductive speeds of 3,4 or 5. Dead plants can have a non-zero
#           reproductive speed because they may have reproduced then died. Plants that died without
#           ever reproducing currently have a missing value.
# flwr_num - flower number in the current census.
# frt_num - fruit number in the current census. Males have missing values for fruit number.
# frt_hadena - hadena damaged fruits in the current census. Males have missing values.
# reproduced - This is a yes (1) if there is evidence that Hadena bored its way out of the capsule. males=missing value
# smut - Healthy (H) or diseased (S). Change these to ones and zeroes?
# num_smutted_fl - When diseased, how many flowers displayed disease
# leaf_herb	- an index (0-3) for the severity of leaf herbivory
# gen_ENMY - an index (0-3) for the severity of damage by generalist enemies. Rarely a 3.
# spec_ENMY - an index (0-3) for the severity of damage by specialist enemies, smut and hadena. Values
#           never exceeded 1.

# These data are the results of analysing common garden families with STRUCTURE.
DNA_data = pd.read_csv(r'Structure_assignments.csv', header=0)

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
# print(family_ID)

# now merge the molecular data back (family_ID) into the larger dataset using pop as the key/index.
inv_data = inv_data.merge(family_ID[['sire', 'dam', 'sibship', 'sire.pop', 'dam.pop', 'Structure_region']],
                          on=['tempindex1', 'tempindex1'], how='right', indicator=False)
inv_data = inv_data.drop(columns=['tempindex1', 'tempindex2'])

# There are many issues with the data that need to be tidied up
# There are some question marks in the molecular data, replace with missing values.
inv_data = inv_data.replace('?', '')
# There is a strange entry for survival, 'DUG' which is a description of how the plant died. Replace with D
inv_data = inv_data.replace('DUG', 'D')

# Sex is messed up ... there are values other than M, F and missing data...
# This function generates a list of the values in a variable, in this case it was
# ['F' 'M' 'MF' 'S' 'nan'], and the number of elements in that list. I used them to diagnose strange
# values in the data.
#       sex_list = inv_data['sex'].tolist()
#       unique(sex_list)
#       print(len_unique(sex_list))
# So, in this case some plants that were infected with the fungus had a sex=S, for smutted
# As it turns out, we had no M/F data on these prior to infection, so we do not know their gender.
# Therefore, I replaced S with missing value. Whether plants are smutted or not is recorded in another variable.
for i in range(len(inv_data)):
    if inv_data.loc[i, "sex"] == "S":
        inv_data.at[i, 'sex'] = np.nan
# Next there are plants where the gender was ambiguous, MF. I went through the data and if fruits were
# produced it has to be female (plant_ID = 65, 270, 663, 693, 2611). One plant flowered a lot and never
# had fruits, therefore plantID= 2694 was deemed male.
for i in range(len(inv_data)):
    if inv_data.loc[i, "sex"] == "MF":
        inv_data.at[i, 'sex'] = "F"
        if inv_data.loc[i, "plant_ID"] == 2694:
            inv_data.at[i, 'sex'] = "M"
#        print(inv_data.loc[i, "sex"], inv_data.loc[i, "plant_ID"])

# Also, with respect to sex, there are some that have an M, or F from some census times, but missing
# values for other census times. We don't want that, so the following takes plant_IDs that have more
# than one entry for sex, and makes them have just have the one correct one.
# first thing to do is to create a temporary dataset with a list of unique plant_IDs.
# it is helpful to turn survival into a number, A=1, D=0
inv_data['survival'] = inv_data['survival'].replace({'A': 1, 'D': 0})
IDs = inv_data.groupby('plant_ID').agg({'survival': 'max'}).reset_index()
IDs['sex'] = ""
# print(IDs)

# so for each unique plant_ID, I generate a list of genders those IDs had in different censuses.
# If that list contains even one M, or F,  along with missing values, then I want to fill in the
# missing vales for that plant as either M or F. This takes each plant_ID, and generates a list of
# genders recorded for the plant. If that list has an M, it is male, if it has an F it is female,
# otherwise it is a missing value. The result is a list of plant_IDs with a single correct gender.
for i in range(len(IDs)):
    temp = inv_data.loc[inv_data['plant_ID'] == IDs.at[i, 'plant_ID']]
    sex_list = temp['sex'].tolist()
    if 'M' in sex_list:
        IDs.at[i, 'sex'] = 'M'
    #        print(IDs.at[i, 'sex'], IDs.at[i, 'plant_ID'], unique(sex_list), len_unique(sex_list))
    elif 'F' in sex_list:
        IDs.at[i, 'sex'] = 'F'
#        print(IDs.at[i, 'sex'], IDs.at[i, 'plant_ID'], unique(sex_list), len_unique(sex_list))
# Then we merge the newly generated list if plant genders and merge that into the full dataset.
inv_data = inv_data.merge(IDs[['plant_ID', 'sex']], on=['plant_ID'])
inv_data['sex_x'] = inv_data['sex_y']
inv_data = inv_data.rename(columns={"sex_x": "sex"})
inv_data = inv_data.drop(columns=['sex_y'])
# This works great but we still have a problem. There are plants that were alive for one or more census
# times, but had no M or F or anything recorded because they were vegetative. This is a lot of plants.
# Also, we are not interested in calling a plant vegetative if it was never alive. Plus, since many live
# plants had M or F genders in a previous census some did not. So we have to revise the assignments
# and merge the data with Vs, into the merged data with Ms an Fs.
for i in range(len(IDs)):
    temp = inv_data.loc[inv_data['plant_ID'] == IDs.at[i, 'plant_ID']]
    sex_list = temp['sex'].tolist()
    if 'M' in sex_list:
        IDs.at[i, 'sex'] = 'M'
    #        print(IDs.at[i, 'sex'], IDs.at[i, 'plant_ID'], unique(sex_list), len_unique(sex_list))
    elif 'F' in sex_list:
        IDs.at[i, 'sex'] = 'F'
    elif IDs.at[i, 'survival'] > 0:
        IDs.at[i, 'sex'] = 'V'
#        print(IDs.at[i, 'sex'], IDs.at[i, 'plant_ID'], unique(sex_list), len_unique(sex_list))
# Then we re-merge the list of plant genders, with vegetatives, into the full dataset.
inv_data = inv_data.merge(IDs[['plant_ID', 'sex']], on=['plant_ID'])
inv_data['sex_x'] = inv_data['sex_y']
inv_data = inv_data.rename(columns={"sex_x": "sex"})
inv_data = inv_data.drop(columns=['sex_y'])
# Works likes a charm! We now have M, F and if the plant has seen alive but no gender recorder, it is a
# V. If the plant has never been seen alive, sex is a missing value, which is OK b/c we'll delete them.


# Eventually we are going to sum most of these variables to get a lifetime measure, of say, flower
# production. In general therefore, we should convert text categories, e.g. alive (A) or dead (D) to
# numeric categories so the sums or means or whatever might have some meaning.
# survival, A=1, D=0. We did this above for technical reasons.
# inv_data['survival'] = inv_data['survival'].replace({'A': 1, 'D': 0})

# status should represent a numerical stage in development V-B-FL-FR -> 1-2-3-4
status_list = inv_data['status'].tolist()
unique(status_list)
print(unique(status_list))

inv_data['status'] = inv_data['status'].replace({'V': 1, 'V,R': 1, 'B': 2, ' B': 2, 'B,R': 2, 'FL': 3, 'FR': 4})
# reproduced, Y=1, N=0
inv_data['reproduced'] = inv_data['reproduced'].replace({'Y': 1, 'N': 0})
# smut, H=0, S=1
inv_data['smut'] = inv_data['smut'].replace({'S': 1, 'H': 0})

# Missing values is always something to talk about. Right now we have too many missing values. For
# example a live plant with 20+ basal leaves might have a missing value for stem leaves. That should
# be a zero. In fact, I am going to suggest that any phenotypic measurement on a live plant should
# have almost no missing values. If the plant is alive and healthy, there are zero smutted flowers, for
# example. This makes it easy to just stick in zeroes for all missing values for all phenotypic measures
# provided the plant was alive so the zeroes were observed.

inv_data[
    ['stem_lvs', 'bolt_ht', 'bolt_num', 'flwr_num', 'frt_num', 'frt_hadena', 'reproduced', 'num_smutted_fl']] = \
    inv_data.query('survival == 1')[[
        'stem_lvs', 'bolt_ht', 'bolt_num', 'flwr_num', 'frt_num', 'frt_hadena', 'reproduced',
        'num_smutted_fl']].fillna(0)

# this generated a new problem that needs to be corrected...For all living males, make any data
# regarding fruits as missing values.
inv_data['frt_num'] = np.where(inv_data['sex'] == 'M', '', inv_data['frt_num'])
inv_data['reproduced'] = np.where(inv_data['sex'] == 'M', '', inv_data['reproduced'])
inv_data['frt_hadena'] = np.where(inv_data['sex'] == 'M', '', inv_data['frt_hadena'])

# not seeing any reason to keep the dead plants ...
inv_data = inv_data.loc[inv_data['survival'] == 1]

# with all these adjustments, the data_types are a mess ...
inv_data = inv_data.replace({'': np.nan})
print(inv_data.dtypes)
inv_data = inv_data.astype({'frt_num': 'float64', 'frt_hadena': 'float64', 'reproduced': 'float64',
                            'sire.pop': 'float64', 'dam.pop': 'float64', 'Structure_region': 'float64'})

# Which gives us the Parsed Data
inv_data.to_csv(r'Parsed garden data with deme assignments.csv', index=False)

# From here, we are going to take a major direction. We have data from ~7 census dates. Rather than
# try to analyze those using something like aster, we will create summary variables.
# For example, lifetime fitness for females might be the sum of fruit production across
# all census dates.

# the following keeps the dataframe variables, but sums phenotypic traits across all censsus dates/years
df_sumdata = inv_data.groupby(['plant_ID']).agg(
     {'pop': 'first', 'cont_orig': 'first', 'cont_dest': 'first',
      'site': 'first', 'treatment': 'first', 'block': 'first', 'plant_ID': 'first', 'sex': 'first',
      'longevity': 'first', 'basal_lvs': 'sum', 'stem_lvs': 'sum', 'total_lvs': 'sum', 'status': 'sum',
      'rep_spd': 'sum', 'flwr_num': 'sum', 'frt_num': 'sum', 'frt_hadena': 'sum',
      'reproduced': 'sum', 'smut': 'sum', 'num_smutted_fl': 'sum', 'leaf_herb': 'sum',
      'gen_ENMY': 'sum', 'spec_ENMY': 'sum', 'sire': 'first', 'dam': 'first',
      'sibship': 'first', 'sire.pop': 'first', 'dam.pop': 'first', 'Structure_region': 'first'})

print(df_sumdata)
df_sumdata.to_csv(r'Garden data summed across censuses.csv', index=False)

# _________________________________________________________________________________________
# Here is a summary of the variables generated in 'Parsed garden data with deme assignments.csv'
# year - year the plots were censused
# census - year and season the plots were censused, e.g. 2008summer
# pop - population the family originated from (nested within cont_orig).
# cont_orig	- the continent where the population originated (Europe, NorthAmerica)
# cont_dest	- the continent the plant was planted in  (Europe, NorthAmerica)
# site- the site (CA, VA, CH, UK) the plants are planted in (nested within cont_dest)
# treatment	- Treated with fungicide or herbicide (FI) versus controls (CN)
# block	- replicate blocks contain all families within site.
#           The abbreviation here is the site [e.g. CH] and the plot within [e.g. CH04]
# plant_ID - unique plant identifier
# sex- male, female or vegetative (M, F, V) or missing value for plants that were dead from the start.
# survival - A (1) or D (0) at each census. In the end I just deleted empty rows for dead plants.
# longevity	- The number of census periods this plant eventually lived.
# basal_lvs - The number of leaves on the basal rosette of the plant. No missing values on live plants.
# stem_lvs	- the number of leaves on the stem or bolt. No missing values on live plants.
# total_lvs	- basal_leaves + stem leaves
# bolt_ht - The height of all bolts summed. No missing values on live plants.
# # total_lvs	- basal_leaves + stem leaves
# bolt_num - number of bolts. No missing values on live plants.
# status - reproductive status, Vegetative [1], Bolting [2], Flowering [3], Fruiting [4].
#           Males never have a value of 4.
# rep_spd - Number of censuses until the first reproduction. Plants that died without
#           ever reproducing currently have a missing value.
# flwr_num - flower number in the current census.
# frt_num - fruit number in the current census. Males have missing values for fruit number.
# frt_hadena - hadena damaged fruits in the current census. Males have missing values.
# reproduced - This is a yes (1) if there is evidence that Hadena bored its way out of the capsule.
#       males have a missing value
# smut - Healthy (0) or diseased (1).
# num_smutted_fl - When diseased, how many flowers displayed disease
# leaf_herb	- an index (0-3) for the severity of leaf herbivory
# gen_ENMY - an index (0-3) for the severity of damage by generalist enemies. Rarely a 3.
# spec_ENMY - an index (0-3) for the severity of damage by specialist enemies, smut and hadena. Values
#           never exceeded 1.
# sire - male parent used to generate F1s, all crosses were within populations
# dam - female parent used to generate F1s, all crosses were within populations
# sibship - full sibship. There is one sibship per pop so the two are the same variable.
# sire.pop - population of origin of the sire.
# dam.pop - will always be the same as sire.pop. These are useless.
# Structure region - demes assigned by structure.

# _________________________________________________________________________________________
# Here is a summary of the variables generated in 'Garden data summed across censuses.csv'

# In general, all the same variables as above, except ...
# the variables year, census, survival became unnecessary or redundant, and were omitted.
# The variables, 'basal_lvs', 'stem_lvs', 'total_lvs', 'status', 'rep_spd', 'flwr_num', 'frt_num',
#       'frt_hadena', 'reproduced', 'smut', 'num_smutted_fl', 'leaf_herb', 'gen_ENMY', 'spec_ENMY'
#       are now sums for each plant across years.


# Later,will transform the data to make it appropriate for parametric statistics
# Later, we will standardize the data for selection analyses.

# complexities of gender

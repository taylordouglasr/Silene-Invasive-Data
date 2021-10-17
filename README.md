# Silene-Invasive-Data

This repository is for those that would like to access our experiments on the invasiveness of Silene latifolia during its invasion into North America. If you would like to collaborate, or notice errors or omissions, please contact Doug Taylor at drt3b@virginia.edu.

Briefly, ~30 full sib families originating in Europe and ~30 full sib families originating in North America were planted in 4 common gardens, two in Europe and two in North America. So it is essentially a reciprocal transplant experiment. There are a lot of details of the experimental design that motivate the analyses below.

The raw data are located in the CSV, "2021 Common Garden Data Working Copy.csv"

Another data set summarizes molecular data and includes the deme assignments of the full sib families using the program Structure.

The results of the Structure analysis are in the CSV, "Structure_assignments.csv"

The script, "Parse Invasives Data,py" cleans up and merges these two data sets, resulting in "Parsed garden data with deme assignments.csv". There was a LOT of tidying up to do. The script is heavily commented at each step so we can see and agree/disagree with what was done. Detailed decriptions of each variable are also commented in the script. 

In addition, "Parse Invasives Data,py" summarizes the data for each plant across the 7 census periods, and generates "Garden data summed across censuses.csv". The variable names are almost all the same in the two files. In the former, 'flwr_num' gives the number of flowers observed on each plant in each census, whereas 'flwr_num' in the summed data set gives the number of flowers observed for each plant across all census periods, etc. In the past, we have used the summed data rather than deal with the times series data, so I consider this our working data.

The only data yet to be incorprated is the weather data...but I think we can leave that until/if we need it.

It is worth noting that males have missing values for all fruit-related traits, and paradoxially, the vegetative plants ('sex' = V) have zeroes for the fruit traits, so that is a remaining oddity which will come up. After contemplating how these gender categories affect our analysis ...

Jupyter notebooks from Peter Fields and Doug Taylor in the analysis folder show the data will resist being normalized and offer a PCA of the data (excluding fruit traits) if we choose to analyze things that way. 

Analyses to be done.
- GLM models to study variation in trait means.
  * See [here](https://bbolker.github.io/mixedmodels-misc/glmmFAQ.html) and [here](https://ase.tufts.edu/bugs/guide/assets/mixed_model_guide.html) for resourceds on coding GLMs in R
- Selection analyses on traits
- FST/QST
- G matrix estiamtion, and degree of change.
- Can phenotypic evolution be explained entirely by the change in frenquency of ancetral demes? (ad hoc analysis)
- Can G-matrix evolution be explained entirely by the change in frenquency of ancetral demes? (ad hoc analysis)
- How do different ancetral molecular demes experience selection and how does their phenotypic divergence translate to fitness in NA? Are we thinking shifts in frequency are founder effect, or selection among lineages post-invasion.

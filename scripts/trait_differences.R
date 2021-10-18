#clear workspace
rm(list=ls())

ls()

# load required packages
library(tidyverse)
library(ggplot2)
library(cowplot)
library(lme4)
library(car)
library(MASS)

# load data and change number to character asignment of Structure_region
data <- read_csv("~/Desktop/github/Silene-Invasive-Data/data/Parsed garden data with deme assignments.csv")
data$Structure_region <- as.character(data$Structure_region)

# check distribution of values for ttl_lvs
qqp(data$total_lvs, "norm")
qqp(data$total_lvs, "lnorm")

# log transformation looks okay

# create base model
PQL <- glmmPQL(total_lvs ~ cont_orig + treatment, random=list(site = ~1,block = ~1), family = gaussian(link = "log"), 
               data = data1, verbose = FALSE,start=c(3,3,3))
summary(PQL)


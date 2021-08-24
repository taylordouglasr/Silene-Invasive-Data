## Load required packages
                 
library("ggplot2")
theme_set(theme_bw())
library("sf")                

library("rnaturalearth")
library("rnaturalearthdata")

## Import data

EU <- read.csv("~/Desktop/Silene_sampling_locations_EU.csv")
G <- read.csv("~/Desktop/Silene_sampling_locations_G.csv")
NoA <- read.csv("~/Desktop/Silene_sampling_locations_NA.csv")
  
worldmap <- ne_countries(scale = 'medium', type = 'map_units',
                         returnclass = 'sf')

ggplot(data = world) +
  geom_sf()

ggplot() + geom_sf(data = worldmap) +
  geom_point(data = G, aes(x = Longitude, y = Latitude), shape = 21, size = 4, fill = "red") +
  geom_point(data = EU, aes(x = Longitude, y = Latitude), size = 2) +
  coord_sf(xlim = c(-20, 35), ylim = c(35, 58), expand = FALSE) +
  theme_bw()

ggplot() + geom_sf(data = worldmap) +
  geom_point(data = G, aes(x = Longitude, y = Latitude), shape = 21, size = 4, fill = "red") +
  geom_point(data = NoA, aes(x = Longitude, y = Latitude), size = 2) +
  coord_sf(xlim = c(-115, -50), ylim = c(30, 60), expand = FALSE) +
  theme_bw()





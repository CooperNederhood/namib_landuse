# Project: "Assessement of Underutilized Public Land for Infill Housing Operations in Windhoek, Namibia"
*Namibian University of Science and Technology, ILMI Seed Grant Project 2020*
### Overview
The main objective of this project is to develop a concrete policy proposal for the realization of urban-
infill housing on currently under-utilized publically-owned land in Windhoek. In other words, if a plot of public land has nothing on it, then new housing can be built on it. But, that new housing needs to be connected to the current infrastructure, and that is easier if the area ***around*** the available land is already built up. Those are the ideal spots for housing development, and that is what we are seeking to identify.

By utilizing a dataset of building footprints across the city, we hope to identify, at-scale, land across the city that is underutilized. We define underutilized land as exhibiting two main properties:
1. Open, non-built-up, public land
2. But surrounded by otherwise built-up land

By weighing both of these criteria, we hope to identify parcels that have available space while still being comparatively efficient to integrate with existing infrastructure. 

Computationally identifying target sites can then inform on-the-ground verification of these sites. Importantly, we do not have immediate access to zoning data to determine if land is public or private. We also lack data on flooding and topography to determine if the site is indeed viable. By first verifying identified sites against satellite imagery, we can do an initial verification of the sites before investing resources in having on-the-ground surveys. 

This repository houses the code and related materials for the computational part of these efforts. 

An example of potential target sites is below:
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc5.png)

### Current computational approach
We have an initial application where a user can select city blocks from Windhoek per specified criteria and then visualize the satellite imagery of those areas for further visual inspection.

As shown below, when you start the application, all of the blocks in Windhoek are selected (so selections are highlighted in red):
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc1.png)

Then, you can filter the selections to those with some level of ***building density***, suggesting the block is developed in some way and may have a degree of infrastructure already. As you might suggest, this tends to select blocks near the city center (red is selected, bule is not). We illustrate this below:
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc2.png)

Instead of selecting blocks with some building density, you can select blocks that have above some amount of ***continuous open space***, indicating there is unused land. Rather than selecting blocks in the center, this tends to select blocks in the periphery. We illustrate this below:
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc3.png)

Now, to identify blocks with both some existing buildings but also unused land, we can use both filters simultaneously to get the intersection. As shown below, we are now selecting a much smaller number of blocks around the center and near periphery:
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc4.png)

This map is fully zoomable, so you can zoom in and inspect areas. Overlaying the satellite helps verify if we are getting the sorts of areas we want. Below, we've zoomed into one specific block from the red highlighted areas above. 
![GitHub Logo](https://github.com/CooperNederhood/namib_landuse/blob/master/pics/sc5.png)


### Next steps following initial identification

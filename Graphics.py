#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 14:57:14 2020

@author: benrobbins

This is a program to generate the graphics to represent the sentimate of michigan
given dates and the senimate of the tweets.
"""
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.patches as mpatches

'''
This function creates and saves a colored map of michigan based on the given 
average sentiment. 
aveSentiment: A double ranging from -1 to 1 representing the average sentiment
file_name: This is the title of the map and the name of the saved file.
'''
def michiganSentimateGraph(aveSentiment, file_name):
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())
    
    ax.set_extent([-92, -80, 40, 48], ccrs.Geodetic())
    
    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',
                                         category='cultural', name=shapename)
    
    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    
    ax.set_title(file_name)
    
    #for state in shpreader.Reader(states_shp).geometries():
    for state in shpreader.Reader(states_shp).records():
        if (aveSentiment < -0.76):
            facecolor = 'red'
        elif (aveSentiment < -0.74):
            facecolor = '#FF7E00'
        elif (aveSentiment < -0.72):
            facecolor = "lightyellow"
        elif (aveSentiment < -0.70):
            facecolor = "lightblue"
        else:
            facecolor = "#0000FF"
    
        if state.attributes['name'] == 'Michigan':
            ax.add_geometries([state.geometry], ccrs.PlateCarree(),
                          facecolor=facecolor, edgecolor='black')
    # make two proxy artists to add to a legend
    teer1 = mpatches.Rectangle((0, 0), 1, 1, facecolor="red")
    teer2 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#FF7E00")
    teer3 = mpatches.Rectangle((0, 0), 1, 1, facecolor="lightyellow")
    teer4 = mpatches.Rectangle((0, 0), 1, 1, facecolor="lightblue")
    teer5 = mpatches.Rectangle((0, 0), 1, 1, facecolor="#0000FF")
    labels = ['<-0.76', '-0.76 ≤ and < -0.74', '-0.74 ≤ and < -0.72', 
              '-0.72 ≤ and < -0.70', '≥ -.070']
    plt.legend([teer1, teer2, teer3, teer4, teer5], labels,
               loc='lower left', bbox_to_anchor=(0.025, -0.1), fancybox=True)
    
    plt.savefig(file_name + '.png', bbox_inches='tight')
    plt.show()
    
# all of the average sentiments
aveSentiment = [-41/54.0, -34/43.0, -37/43.0, -5/7.0, -128/172.0, -230/307.0, 
                -29/49.0, -58/79.0]
# the dates that the seentiments were collected.
dates = ['11-27-2020', '11-28-2020', '11-30-2020', '12-03-2020', '12-08-2020',
         '12-09-2020', '12-10-2020', '12-11-2020']

# make and save the images
for i in range(len(dates)):
    michiganSentimateGraph(aveSentiment[i], (dates[i] + "- Michigan Sentiment"))

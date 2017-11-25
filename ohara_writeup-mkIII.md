##### Screen Resolution = 1024x768, Quality = Good, Windowed = True
##### Student: Christopher Ohara, RoboND
#
---
## Project: Search and Sample Return
#

### Writeup Template: You can use this file as a template for your writeup if you want to submit it as a markdown file, but feel free to use some other method and submit a pdf if you prefer.

---


**The goals / steps of this project are the following:**  

**Training / Calibration**  

* Download the simulator and take data in "Training Mode"
* Test out the functions in the Jupyter Notebook provided
* Add functions to detect obstacles and samples of interest (golden rocks)
* Fill in the `process_image()` function with the appropriate image processing steps (perspective transform, color threshold etc.) to get from raw images to a map.  The `output_image` you create in this step should demonstrate that your mapping pipeline works.
* Use `moviepy` to process the images in your saved dataset with the `process_image()` function.  Include the video you produce as part of your submission.

**Autonomous Navigation / Mapping**

* Fill in the `perception_step()` function within the `perception.py` script with the appropriate image processing functions to create a map and update `Rover()` data (similar to what you did with `process_image()` in the notebook). 
* Fill in the `decision_step()` function within the `decision.py` script with conditional statements that take into consideration the outputs of the `perception_step()` in deciding how to issue throttle, brake and steering commands. 
* Iterate on your perception and decision function until your rover does a reasonable (need to define metric) job of navigating and mapping.  

[//]: # (Image References)

[image1]: ./misc/rover_image.jpg
[image2]: ./calibration_images/example_grid1.jpg
[image3]: ./calibration_images/example_rock1.jpg 

## [Rubric](https://review.udacity.com/#!/rubrics/916/view) Points
### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  You can submit your writeup as markdown or pdf.  

You're reading it!

### Notebook Analysis
#### 1. Run the functions provided in the notebook on test images (first with the test data provided, next on data you have recorded). Add/modify functions to allow for color selection of obstacles and rock samples.
#
##### I added the ability for the rover to distinguish between the ground, obstacles, and rocks. The color selection is completed by "threshing" since the ground, obstacles and rocks all have drastically different colors. This would be more difficult if there was a gradient of colors (spectrum) in which the rocks closely resembled the ground or obstacles. 
#
### 1) Threshing
---
##### The initial task for the rover to identify and distinguish between the environment, obstacles, and rocks. The color values were obtained from a color chart.
#
#### Ground and Obstacles
##### The color_thresh was defined from recommendations from the official slack channel to be in the form of RGB=(160,160,160). The color select decides if the image is above or below these specifications, such that the ground is "above" the threshold and the obstacles are "below" this threshold.
#
##### Obstacles could also have a specified value (low values for dark colors) but the implementation centered around the implemented values operated with nominal results.

#
#### Rocks
##### The color selection was chosen off of a color chart to find the range of the "yellow" colored rocks. This is optimized by giving a high and low range from the color spectrum. This range was chosen to be RGB = (100,100,20), (210,210,55) for low and high respectively. 
#

![alt text][image1]

#### 1. Populate the `process_image()` function with the appropriate analysis steps to map pixels identifying navigable terrain, obstacles and rock samples into a worldmap.  Run `process_image()` on your test data using the `moviepy` functions provided to create video output of your result. 
And another! 

![alt text][image2]
### Process_image()
---
##### The goal of the process image function is to create a video for the Jupyter Notebook. This is achieved by taking the inputs from the perception_step and outputting the data in a manner the DataBucket add-on can interpret.
#
##### Essentially, the requirements in the perception_step take information from test images. The images are warped through a perspective transform and modified with the color threshing as described above. A world map is created and the rover-centric values are utilized. The path the rover takes is dependent on the computer vision information it receives from the angles and distances.  
#
###### Note: Compiling a video proved to be more difficult than I expected. I was able to program the rover on my local machine to operate with my final specifications. However, upon importing the data into the Jupyter Notebook, I had to remove and edit several functions. (e.g. "Rover" needed to be renamed to "data" and other functions had to be fitted to match the DataBucket parameters).




### Autonomous Navigation and Mapping

#### 1. Fill in the `perception_step()` (at the bottom of the `perception.py` script) and `decision_step()` (in `decision.py`) functions in the autonomous mapping scripts and an explanation is provided in the writeup of how and why these functions were modified as they were.
#
#### decision_step()
---
###### This function actually did not require modifications. However, without editing this file, the rover might find itself in a never-ending circular loop that might cause the mapping percentage requirements to not be achievable without temporary user override (not very autonomous, right?).
#
###### To counter this dilemma, I changed the maximum steering angle to +/- 10 degrees instead of the default +/- 15 degrees. This caused the maximum radius of a "circle that could be drawn" to become larger (in most cases) than the open area on the eastern side of the map. 
#
###### The rover operates with the decisions of "forward", "stop" and "obstructed." Under normal conditions, the rover will move forward. If its path becomes obstructed (it is stuck) it will stop, turn and commence moving forward. It loops through these functions to navigate.  
#
###### Note: This change in steering angle can sometimes cause the rover to behave inefficiently since it does not steer out of obstacles and dead-ends in an optimal fashion. This could be corrected by implementing a "reverse and turn around" algorithm. However, since this seldom occurred, it was not designed.
#
#### perception_step()
---
    
##### The perception step specifically had eight areas to complete. The specifications are as follows:
1) ###### Define points for perspective transform
    * ###### Set up the box size
    * ###### Define the source and destination (use data from the course videos)
2) ###### Apply the perspective transform
    * ###### Warp the image based on the image, source and destination
3) ###### Apply color threshold
    * ###### Translate definitions
4) ###### Update the image
    * ###### Using example pseudocode
5) ###### Convert map values to rover-centric coordinates
    * ###### Define the pixels based on the coordinates, position, and yaw
6) ###### Convert pixel values to world coordinates
    * ###### Scale the map to an appropriate size 
    * ###### Acquire the navigable pixel positions to world coordinates
7) ###### Update Worldmap
    * ###### Implemented modified version of given pseudocode
8) ###### Convert rover-centric pixel positions to polar coordinates
    * ###### Implemented modified version of given pseudocode

#



#


#### 2. Launching in autonomous mode your rover can navigate and map autonomously.  Explain your results and how you might improve them in your writeup.  

**Note: running the simulator with different choices of resolution and graphics quality may produce different results, particularly on different machines!  Make a note of your simulator settings (resolution and graphics quality set on launch) and frames per second (FPS output to terminal by `drive_rover.py`) in your writeup when you submit the project so your reviewer can reproduce your results.**


#
#### Results and Discussion
---
###### I was able to meet the required mapping and fidelity percentage by implementing the discussed modifications. As reported in the notes, several adjustments could be made to improve the overall performance. These adjustments include:
1) ###### Adding a "reverse" feature to the decision_step()
2) ###### Being more specific in the color threshing of the obstacles
3) ###### Adjusting the rover speed with a range based on conditional statements
#
###### The biggest change that I implemented had to do with the steering/turning angle for navigation in the "decision_step.py." I found (like other students in the forums) that the rover would often get stuck in an endless circle in the large area on the eastern side of the map. Essentially, the rover was drawing a circle with a radius that was inscribed perfectly within the open areas. To rectify this, I decreased the maximum turn angle incrementally until the rover could balance not getting stuck in a nonterminal looping cycle but still be able to escape from rocks and deadends. 
#
###### One aspect that could be addressed to correct movement problems is to create an algorithm that provides the rover with better navigation. This might best be approached by considering its speed, yaw, and turning angle. However, this is slightly beyond the scope of the class and my (time-related) ability as implementation will result in a primarily recursive trial-and-error approach due to the stochastic environment in which the rover operates. 



![alt text][image3]



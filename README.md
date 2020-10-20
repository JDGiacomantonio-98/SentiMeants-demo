# Sentimeant
We plan to query the Twitter API against a given hashtag to extract a tweet mass on which to perform a sentiment analysis to evaluate people believes about said topic/word. 

* sentiment_analyzer.py: contains the function that takes in input the tweets and outputs it's scores [negative,neutral,positive,compound]
* visualization.py : contains the function visualize takes in input the scores and passes them to the function make_visualization_plots which generates the plots and returns a figure object with all the plots, then the function takes care to generate html code and visualizing the plots 


## INSTALLING NODE.JS, npm, Chart.js, Christ, The Blessed Virgin and Saint Joseph
1. Download the windows node.js installer from : https://nodejs.org/en/download/
2. Install all the packages in the installer
3. Check if node.js and npm are installed by typing in console:
    ~~~~
    node --version
    npm --version
    ~~~~
4. Update npm by typing in console:
    ~~~~
    npm i -g npm@latest
    ~~~~
5. Type in console:
    ~~~~
   npm config list
   ~~~~
    it should output something like:
    ~~~~
    prefix : "C:\\Users\\<user>\\AppData\\Roaming\\npm"
    node bin location = C:\Program Files\nodejs\node.exe 
    ~~~~
   these are respectively where node.js and npm are located
6. The way we use npm is like pip in python,
   go to your project folder where you want your js files to be
   installed (in our case _sentime/app/static/js)
7. open the console that folder and type:
    ~~~~
    npm init
    ~~~~
   it will guide you through the creation of package.json
   which works in a way similar to requirements.txt in python
8. It will ask you to input some information, these don't have
   no function whatsoever so you can write whatever you like
9. At the end a file called "package.json" should have appeared
   in the folder
10.With the console open in the same folder of package.json,
   you can install libraries by typing:
    ~~~~
    npm install <package name> --save
    ~~~~  
   the --save argument is important because it writes in package.json
   the library you are downloading.
   
   Now to install Chart.js:
    ~~~~
    npm install chart.js --save
    ~~~~
11. At the end a folder is created in the directory where you have
    "package.json", with the dowloaded package and inside "package.json"
    there is an entry named "dependencies" with your installed packages
12. To install dependencies form a "package.json" file just head to
    the folder with the file and type into the console:
    ~~~~
    npm install
    ~~~~
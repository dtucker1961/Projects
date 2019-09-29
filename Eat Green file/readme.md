This iOS iphone app gives students the ability to look up a cafeteria food item and to then get a letter grade reflecting the environmental impact of the food. I used information about the top carbon producing foods (cited below) and compared them to the ingredients of the food inputted by the user. To use, just type in the food name in the search bar and hit the button corresponding to what meal the food is in. The program will then direct the user to another page to receive the grade. Also, on the home page, there is a button that will redirect the user to the menu called “Today’s Menu.”

To compile, configure, and use my project, download the free Xcode development environment (https://developer.apple.com/xcode/). You must have mac to download. In XCode, simply build the viewcontroller.swift files.

While it is not essential, I built my app for the iPhone 8 (the type of phone I have). Different generations of iPhones have different screen sizes, and the pictures I inserted into my app fit the iPhone 8 the best, but the functionality is still the same. To run the iPhone 8 simulator, simply select iPhone 8 from the drop down menu in the top left corner.

Since iOS 9, Apple does not allow requests to non-secure websites (http websites). The website I’m gathering information from is non-secure, so you have to access security settings in Xcode to allow requests to non-secure websites.

Tutorial on how to change setting: https://stackoverflow.com/questions/31254725/transport-security-has-blocked-a-cleartext-http

Also, Make sure your computer’s Domain Name Server is
8.8.8.8
8.8.4.4
Otherwise, my program will be unable to open the website.

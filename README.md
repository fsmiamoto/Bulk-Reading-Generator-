# Bulk Reading Generator Plus
An attempt to improve Anki's built-in bulk reading generator with a more intuitive interface.

## Requirements
 * You should have the [Japanese Support](https://ankiweb.net/shared/info/3918629684) installed for using this add-on
 
## Features

* No need to stick to the predfined field names in the Japanese Support Add-on files!
* You can generate readings for multiple fields at a time!

# How to Use

## Single Field

* Once you installed the add-on either by using Anki's built-in downloader or by saving the .py file to your add-on folder, a option called
'Reading Generator' should appear in your tool's menu.

* By clicking on it, a window should pop up. You can select the deck you want and then insert the source and destinations fields (e.g Expression and Reading)

![Interface](https://i.imgur.com/DSvZbiF.png)

* After that, just click OK and it should be done!

![Use example](https://i.imgur.com/hS6BmBB.png)

## Multiple Fields

Let's take an example card where you have the following fields:

![Fields](https://i.imgur.com/TX3DLIh.png)

In this example, suppose you want to generate readings for **both** Expression and Word.
You can then type the fields, just like you would if you only wanted generate for one field, and separate with ";"

![Example Multiple](https://i.imgur.com/7RmeGIO.png)

In this case, the text in Expression would be used to generate the text for Expression Reading and the text in Word would be used to generate the text for Word Reading.

If everything is typed correctly, you can click Ok and it should be done!

![Multiple sucess](https://i.imgur.com/YIlfBP6.png)

# Additional Info

* Be careful with typing mistakes! The text should match **exactly** the field name, including case.
* The add-on only generates readings for the cards that don't already have it, therefore it will not overwrite previous reading generations.
* This add-on is still under development so some bug's / errors can be expected. Any feedback would be **greatly** appreciated.

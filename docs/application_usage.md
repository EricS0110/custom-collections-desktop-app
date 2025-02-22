# Using the Application

## Summary

This desktop application is designed to help you manage a collection of items either stored or intended
to be stored in a MongoDB instance.  The main landing page gives a quick overview of what each tab is
as a reminder, as well as a summary of what Database it is currently connected to as well as all the 
collections within that database and the counts of items saved in each.  I tried to keep this page
informative but brief.  If you have any suggestions for at-a-glance features you'd like to see out on the
Welcome tab, feel free to open an issue to suggest what you're looking for, and I'll see if it's an easy add!

I've added a feature that the app logs operations and events to an `app.log` file located out in the main 
Application folder.  This allows you to track and see what operations were performed or what error might have
been triggered and when.

I've also added a feature where any Excel file you select in the [Add Bulk](#add-bulk) tab will be copied to an
archive folder in the application folder in order to serve as an audit in case you want to check what files loaded
what data later on.

## Settings

This section is effectively a stub, since I wanted to keep the first version of the app simple and only
have to configure it once.  On this page I've only set up a Dark Mode toggle, although it's a bit finicky 
due to how the main UI library this is built on handles Windows default system settings.  You might need
to toggle the switch on and off to get it to control in the intended manner, I'm still looking into if 
this is an easy fix or if this is just Windows not being as developer-friendly as it could be.

## New Collection

This tab is intended to give you a way to create a new collection for items without having any data to enter yet.  It's 
not required, but may help you organize or plan out what you all want to be tracking in the long run.  To use
this tab, you just need to enter a name into the entry field and the click the `Create Collection` button.  If
there are invalid characters in the field the app will let you know what valid characters are, and once you've been
able to successfully add a collection you can click the `Refresh List` button to confirm that it's now in fact there!

## Add One

The Add One tab is a way to add items to a given collection one item at a time.  The user interaction flow for this tab 
is intended as follows:

1. Select the collection you want to add an item to from the dropdown menu at the top of the page
2. The box below the dropdown will automatically update to display the list of currently available fields
in the selected collection.  If there are no items in the collection yet, this box is empty.  **Currently, the best
way to start a new collection** is to use the bulk upload method.  I've got a to-do in my notes to set up a more 
customizable field list, but that's not implemented yet.
3. Once you've entered the data you want in the fields, click on the `Check Item` button.  This will read all the 
provided data and create a summary of fields and entered values in the Preview box.  If all of that data looks good,
click on the `Add Item` button to send this data to the database for storage!

## Add Bulk

The Add Bulk tab is how you can add one or many items to one or many collections.  I've provided an example input file 
for you to use, named `ExampleBulkUpload.xlsx`, found in the `src` folder in the main application folder.  You can use 
this as a template for your own collections and fields.  The main requirements are laid out below:

* Each sheet has a unique name, representing the collection the items will be added to
* The first row of each sheet should have the intended field names for items in that collection
* There should not be any blank rows between rows of data.  I don't *THINK* it would be a problem, but I haven't 
officially tested it so let's just avoid it :)

To use this page, click on the `Select Excel File` button.  Pick a file using the newly-opened file selection window, 
and the app will update to display the number of rows in each sheet that will be uploaded.  If those counts line
up with what you expect, click the `Upload Data` button and the app will work through and upload each item to 
its respective collection.  This is pretty performant, and I've only seen slow-downs in older versions of Python when 
I tried to upload hundreds of items at once, and even then it was only a second or two to run.

## Download

This tab is another stub, but that's because it's performing a very simple task.  Pick a collection you
would like to download a copy of to your computer and then click the `Download` button.  You'll be able
to pick the file name and location for the downloaded file.  Data gets downloaded into a new Excel file
for easy comparison to the upload records.

## Search

The Search tab allows you to search your collection for a given field and criteria.  Similar to the Add One
tab, here's a walkthrough of how to use this tab:

1. Select the collection you want to search from the first dropdown menu
2. Select the field you want to search on within the selected collection in the second dropdown menu
3. Enter a search criteria into the labeled field
4. Click the `Search` button.

Note that if you search without providing criteria all items in the selected collection will be returned
in the Search Results box.  This won't be a problem for formatting, although you might have to scroll a lot
depending on how many items you have in said collection.

## Delete

This tab is probably the most "dangerous", only because it deletes data, but I've put protective measures
in place so that even if you do delete an item you'll at least know what you deleted by checking the logs.

1. Select the collection you want to delete an item from
2. Enter the item `_id` (a field automatically added by MongoDB) for the item you want to delete
3. Click the `Check Item` button.  This will load a preview of the data for that item in the preview box and 
enable the last button.
4. Clicking the `Delete` button will delete the specified item from the MongoDB collection and log that this operation
was performed.

## Conclusion

I've tried to keep this as intuitive as possible, but as the developer it's hard to get a completely fresh view of 
the UI and how natural interactions feel.  If anything in this documentation wasn't clear or the application does not
feel easy to use, please open an issue on GitHub and let me know what can be improved!  Happy Collecting!
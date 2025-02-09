/*
    NAME:          popup.js
    AUTHOR:        Alan Davies (Lecturer Health Data Science)
    EMAIL:         alan.davies-2@manchester.ac.uk
    DATE:          18/12/2019
    INSTITUTION:   University of Manchester (FBMH)
    DESCRIPTION:   JavaScript file for managing display of popup dialoges
*/

function Popup()
{
    var popup = new Object();
    popup.mask = document.getElementById("page-mask");
    popup.entryFormPopup = document.getElementById("creat-calc");
    popup.aboutPopup = document.getElementById("about-box");

    // display the popup mask
    popup.showMask = function()
    {
        this.mask.style.display = "block";
        $('#page-mask').height($(document).height());
    }

    //hide the popup mask
    popup.hideMask = function()
    {
        this.mask.style.display = "none";
    }

    //show the creatinine clearance calculator form dialog
    popup.showCeatCalcFormPopup = function()
    {
        this.showMask();
        this.entryFormPopup.style.display = "block";
        this.positionDialogue(this.entryFormPopup);
        //this.entryFormPopup.style.left = (($(document).width() / 2) - (this.entryFormPopup.offsetWidth / 2)) + "px";
    }

    // hide the creatinine clearance calculator form dialog
    popup.hideCeatCalcFormPopup = function()
    {
        this.hideMask();
        this.entryFormPopup.style.display = "none";
    }


    // Show the BMI calculator form dialog
    popup.showBMICalcFormPopup = function() {
        this.showMask(); // Call the existing method to show the mask
        this.bmiFormPopup = document.getElementById("BMI-calc"); // Reference the BMI calculator element
        this.bmiFormPopup.style.display = "block"; // Make the BMI calculator visible
        this.positionDialogue(this.bmiFormPopup); // Position the dialog box
    };

    // Hide the BMI calculator form dialog
    popup.hideBMICalcFormPopup = function() {
        this.hideMask(); // Call the existing method to hide the mask
        this.bmiFormPopup.style.display = "none"; // Hide the BMI calculator
    };

    // Show the BMI calculator form dialog
    popup.showConvCalcFormPopup = function() {
        this.showMask(); // Call the existing method to show the mask
        this.ConvFormPopup = document.getElementById("conversion-calc"); // Reference the BMI calculator element
        this.ConvFormPopup.style.display = "block"; // Make the BMI calculator visible
        this.positionDialogue(this.ConvFormPopup); // Position the dialog box
    };

    // Hide the BMI calculator form dialog
    popup.hideConvCalcFormPopup = function() {
        this.hideMask(); // Call the existing method to hide the mask
        this.ConvFormPopup.style.display = "none"; // Hide the conversion calculator
    };

    // show the about popup
    popup.showAboutPopup = function()
    {
        this.showMask();
        this.aboutPopup.style.display = "block";
        this.positionDialogue(this.aboutPopup);
    }

    // hide about popup
    popup.hideAboutPopup = function()
    {
        this.hideMask();
        this.aboutPopup.style.display = "none";
    }

    // position dialogue center screen
    popup.positionDialogue = function(popupBox)
    {
        popupBox.style.left = (($(document).width() / 2) - (popupBox.offsetWidth / 2)) + "px";
    }

    return popup;
}
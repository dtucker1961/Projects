//
//  ViewController.swift
//  Eatgreen2
//
//  Created by John Tucker on 12/5/18.
//  Copyright © 2018 John Tucker. All rights reserved.
//

import UIKit
// Global variable I can use in oterh ViewController: text user inserted

var foodname = ""
// Global variable I can use in oterh ViewController: the meal type submitted
var meal = ""

class ViewController: UIViewController {
    
    // Text filed
    @IBOutlet weak var Outlet: UITextField!
    
    // Action if user submits using Breakfast button
    @IBAction func Breakfast(_ sender: Any) {
        // If there is something in the textfield
        if (Outlet.text != ""){
            // Set foodname to what is in the textfield
            foodname = Outlet.text!
            // Set meal to Breakfast
            meal = "Breakfast"
            // Redirect to the secound page
            performSegue(withIdentifier: "SegueBreakfast", sender: self)
        }
    }
    
    // Action if user submits using Lunch button
    @IBAction func Lunch(_ sender: Any) {
        // If there is something in the textfield
        if (Outlet.text != ""){
            // Set foodname to what is in the textfield
            foodname = Outlet.text!
            // Set meal to Lunch
            meal = "Lunch"
            // Redirect to the secound page
            performSegue(withIdentifier: "SegueLunch", sender: self)
        }
    }
    
    // Action if user submits using Dinner button
    @IBAction func Dinner(_ sender: Any) {
        // If there is something in the textfield
        if (Outlet.text != ""){
            // Set foodname to what is in the textfield
            foodname = Outlet.text!
            // Set meal to Lunch
            meal = "Dinner"
            // Redirect to the secound page
            performSegue(withIdentifier: "SegueDinner", sender: self)
        }
    }
    
    // Action if user clicks "Today's Menu" button
    @IBAction func MenuLink(_ sender: Any) {
    // Redirect User to the Harvard's menu website
    UIApplication.shared.openURL(URL(string: "http://www.foodpro.huds.harvard.edu/foodpro/menu_items.asp?type=30&meal=1")!)
    }

    override func viewDidLoad() {
        super.viewDidLoad()
    }
}
// Image Citation: https://www.kisspng.com/png-green-leaf-transparent-png-clip-art-image-52732/

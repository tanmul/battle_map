# D&D Battle Map
#### Created by Tanmay M.

## How to Use

### Initial Setup
* **Add Hero/Playable Character (PC)**

    * Choose Character from dropdown menu
    * Click *Spawn Hero* (Hero sizes are dictated by cell size)
    * The new character can undergo the following changes:
        * Can be moved
        * Can be enlarged/shrunk
        * Can be deleted
    * **NOTE:** Trying to spawn the same character will result in a duplicate character being created.
    This character will have a certain visual change denoting it's difference from the main character.
* **Add Enemy**
    * Choose enemy size from dropdown menu. The implemented sizes are shown in the table below.
    
        |Size Class|Numerical Size|
        |----------|--------------|
        |Tiny| 2.5ft by 2.5ft|
        |Small| 5ft by 5ft|
        |Medium| 5ft by 5ft|
        |Large| 10ft by 10ft|
        |Huge| 15ft by 15ft|
        |Gargantuan| 20ft by 20ft|
        
        _**NOTE:** Each square/cell is **5ft by 5ft**. Sizes of enemies will automatically be computed based on the size of the battlemap and each cell._
    * Click _Spawn Enemy_ (Enemies are shown by a red dot)
* **Check radius for AOE spells/attacks**
    * The Battlemap comes equipped for DMs to check the AOE of spells like Fireball and Lightning
    * Enter the length/radius and width/radius of the spell in their respective text entries
    * **NOTE:** Entering in a non-numerical value or no value at all will result in the battlemap creating a shape with the default value. The default values for each shape is shown in the table below.
        
        |Shape|Default Size|
        |----------|--------------|
        |Rectangle| 5ft by 100ft|
        |Triangle| NULL|
        |Oval| 20ft radius|
    * Choose Shape Type from dropdown menu
    * Click *Check Radius* to spawn shape
    * **ROTATING THE RECTANGLE/TRIANGLE SHAPES**
        * Hold down middle mouse button and drag to rotate the shape
* **Drawing Obstacles**
    * _**Pen Up**_ denotes that drawing is currently DISABLED
    * _**Pen Down**_ denotes that drawing is currently ENABLED
    * **To Erase**: Hold down right click and move the mouse over obstacles
* **Changing the size of characters**
    * Click on the character to enlarge/shrink
    * Press the **UP** key on the keyboard to enlarge the character
    * Press the **DOWN** key on the keyboard to shrink the character
* **Deleting battlemap assets**
    * Right click on any character/enemy/shape to delete it
    

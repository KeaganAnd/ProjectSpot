def returnStyleSheet():
    return("""
[class="header1"] {
       color: white;
       font-size: 50px;
       font-weight: bold;
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       font-family: Times New Roman;
       }  
[class="header3"] {
       color: white;
       font-size: 30px;
       font-weight: bold;
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       font-family: Times New Roman;
       }  
[class="homeButton"] {
       font-family: Times New Roman;
       font-size: 60px;
       font-weight: bold;
       background: none;
       border: none;
       text-align: left;
       padding-left: 10px;
       }
[class="homeButton"]:hover {
       color: #A5D6A7;
       }
[class="boldBody"] {
       font-size: 20px;
       font-weight: bold;    
       }
[id="topBox"] {
       background-image: url('classes/ui/imgs/homebg.png');
       background-repeat: no-repeat;
       background-position: bottom;
       }
QSplitter{
       
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       }  
QVBoxLayout
       {
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       }
QLineEdit
       {
       background-color: #8FBC8F;
       color: #F5F5F5;
       min-height: 50px;
       max-height: 50px;
       font-size: 20px;
       max-width: 1000px;
       border-radius: 20px;
       margin: 0px 0px 0px 0px;
       border: 1px solid white;
       }
QLineEdit:hover
       {
       background-color: #A2D1A2;

       }
QMainWindow{
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       background-color: #8FBC8F;
       }
QWidget{
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       
       }
QGroupBox {
       margin: 0px 0px 0px 0px;
       padding: 0px 0px 0px 0px;
       border: none;
           
       }
[class="header"] {
       background-color: #30343F;
       border-bottom: 3px solid white;
               
       }
[class="locationInfoWidget"] {
       border: 2px solid white;
       border-radius: 10px;
       margin: 5px 5px 5px 5px;
       background-color: #30343F;
       background-image: url(classes/ui/imgs/denim2.png);    
       }
[class2="locationButton"] {
       border: none;
       background-color: none;
       }
[class2="locationButton"]:hover {
       color: #A5D6A7;    
       }
""")
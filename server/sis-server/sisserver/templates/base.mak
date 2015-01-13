<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <link rel="icon" type="image/png" href="static/media/favicon.png">

    <title>SIS - Simple Image Share</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'> 
    
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />
    <link rel="stylesheet" href="static/foundation/css/foundation-datepicker.css" />
    
    <link href='http://fonts.googleapis.com/css?family=Lato' rel='stylesheet' type='text/css'>
    
    <style>

        body {
            background: url("static/media//congruent_outline.png") repeat scroll 0% 0% transparent;
        }

        /*
         *   Foundation Overrides
         */


        


        /*
         *   Site specific stuff
         */

        div.header {
            color: #EEEEEE;
        }

        div.header h2 {
            color: #EEEEEE;
        }

        div.header a {
            font-size: 150% !important;
            margin-right: 20px;
        }

        div.contents-wrapper {
            border-left: 1px solid #888888;
            border-right: 1px solid #888888;
        }

        div.box {
            padding: 15px;
            background: #FFFFFF;
            border: 1px solid #222222;
            border-radius: 5px;
        }

        div.picture-box {
            padding: 15px;
            width: 320px;
            background: #FFFFFF;
            border: 1px solid #222222;
            border-radius: 5px;
        }

        div.small-box {
            max-width: 350px;
        }

        div.login-box {
            margin: auto;
            margin-top: 100px;
        }


    </style>

</head>
<body>

        <script src="static/foundation/js/vendor/jquery.js"></script>
       
        <div class="row">
             <div class="large-12 columns">
                </br>
                ${self.body()}
            </div>
        </div>
        
        <script src="static/foundation/js/foundation/foundation.js"></script>
        
        <script src="static/foundation/js/foundation/foundation.dropdown.js"></script>

        <script src="static/foundation/js/vendor/modernizr.js"></script>

        <script src="static/foundation/js/foundation-datepicker.js"></script>

        <script>
            $(document).foundation({
                /*
                dropdown: {
                    // specify the class used for active dropdowns
                    active_class: 'open'
                }
                */
            });
        </script>
    
        <script>

            // global functions here

        </script>

</body>
</html

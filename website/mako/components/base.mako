<html>
    <head>
        <!-- Google stuff -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-23654340-2"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag() {
                dataLayer.push(arguments);
            }
            gtag('js', new Date());
            gtag('config', 'UA-23654340-2');
        </script>

        <!-- JS, Popper.js, and jQuery -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>

        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>

        <!-- CSS only -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">

        <!-- Page specific includes -->
        <%block name="includes"/>

        <!-- Main CSS for site -->
        <link rel="stylesheet" href="main.css">
    </head>

    <body>
        <!-- Feather icon set -->
        <script src="https://unpkg.com/feather-icons"></script>

        <div class="container main-header">
            <div class="row">
                <div class="col">
                    <div class="main-logo"></div>
                </div>
                <div class="col-8">
                    <div class="container">
                        <div class="row main-title" style="text-align: center">
                            <div class="col">Convert Visual Basic To Python</div>
                        </div>
                        <div class="row"><div class="col"><%include file="main_links.mako"/></div></div>
                    </div>
                </div>
                <div class="col donate-box">
                    <%include file="donate.mako"/>
                </div>
            </div>
        </div>
        <div class="header">
            <%block name="header"/>
        </div>

        <div class="container">
            <div class="row">
                <%block name="content"/>
            </div>
        </div>

        <%block name="raw_content"/>

        <div class="footer">
            <%block name="footer">

            </%block>
        </div>

        <!-- Render Feather icons -->
        <script>
          feather.replace({class: "feather-icon"})
        </script>

    </body>
</html>
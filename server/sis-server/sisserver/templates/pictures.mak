<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="row header">
        <div class="large-12 columns">
            <h2>Pictures</h2>
        </div>
        <div class="large-12 columns">
            <a>Home</a>
            <a>Albums</a>
            %if user_type == 'admin':
                <a>Pictures</a>
            %endif
            <a>About</a>
        </div>
    </div>

    <div class="row">
        % for picture in pictures:
        <div class="large-4 columns">
            <div class="picture-box">
                <center><img src="get_preview.jpg?unique=${picture.unique}" height="320" width="240"></img></center>
            </div>
            <br/>
        </div>
        % endfor
    </div>
    <br/>

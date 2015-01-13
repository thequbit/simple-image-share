<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="row header">
        <div class="large-12 columns">
            <h2>Home</h2>
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

    <br/>

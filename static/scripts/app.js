var app_methods = {};
var page;

$(window).on('load', function() {
	
	// Preloder
	$(".loader").fadeOut();

    // preloder delay
	$("#preloder").delay(400).fadeOut("slow");
});


var app_data = {

    // The panel that is displayed
    panel: 'sign-in',

    // Alerts data
    error_login:'',
    error_newgallery:'',
    error_signup:'',
    success_signup:'',

    // New album data
    album_title:'',
    album_info:'',
    photo_name:'',

    // Signin data
    user_email:'',
    user_password :'',

    // Albums
    albums:'',
    
    // Album photos data
    photo_header:'',
    title:'',
    album_photos:'',
    add_photo_name:'',

    // Signup data
    fullname:'',
    password:'',
    confirm_password:'',
    email:'',

};



// Change panel to target and disable all alerts
app_methods.change_panel = function(target){
    app_data.panel = target;
    app_data.error_newgallery = '';
    app_data.error_login = '';
    app_data.error_signup = '';
    app_data.success_signup = '';
}


//  What to do after click on signout
app_methods.signout = function(target){

    axios.get('/sign-out').then(response => {
        if (response.data=='True')
        {
            $(alert('Logout was successfully'))
            page='sign-in';
            app_data.panel= 'sign-in';
            app_data.user_email= '';
            app_data.user_password= '';
        }   
        app_data.error_newgallery = '';
        app_data.error_login = '';
        app_data.error_signup = '';
        app_data.success_signup = '';
    })
}


app_methods.albumphotos = function(target){
    app_data.title=target[0];
    var data = {     
        'album_title':app_data.title,
    }

    // Post request to get album photos
    axios.post('/albumphotos',data).then(response => {        
        app_data.album_photos= response.data;         
        app_data.panel='album_panel';
    })
}

// Add photo to the album
app_methods.add_photo = function(target){
    var data = {     
        'album_title':app_data.title,
        'photo_name':app_data.add_photo_name
    }
    axios.post('/add_photo_to_album',data).then(response => {
        app_data.album_photos= response.data;         
        app_data.panel='album_panel';
        app_data.add_photo_name = '';
    })
}


// Get albums
app_methods.getalbums = function(){

    app_data.panel='gallery';    
    axios.post('/albums').then(response => {
        app_data.albums= response.data;         
    })
}



// Create new album
app_methods.add_album = function(target){
    var data = {
        'title':app_data.album_title,
        'info':app_data.album_info,
        'photo':app_data.photo_name,
    }

    axios.post('/add-album', data).then(response => {
        if (response.data=='True')
        {
            $(alert('New album created successfully'))

            // Change panel to gallery panel
            page='gallery';
            app_data.panel= 'gallery';
            app_data.album_title='';
            app_data.album_info='';
            app_data.photo_name='';            
            app_methods.getalbums();
        }   
        else {

            // if create panel was not successful getback this error
            app_data.error_newgallery=response.data;            
            app_data.panel= 'new-album';
        }  
    })
}



// Do signin to user
app_methods.signin = function(){
    var data = {
        'email':app_data.user_email,
        'password':app_data.user_password,
    }
    app_data.panel=page;

    axios.post('/signin', data).then(response => {

        if (response.data=='user') {
            //  Login was succesful
            page='gallery';
            app_data.panel= 'gallery';
            app_methods.getalbums();
        }
        // else if (response.data=='logged in') {
        //     app_data.panel= 'gallery';
        //     app_methods.getalbums();
        // } 
        else {
            //  Login was not succesful
            app_data.error_login=response.data;
            app_data.panel= 'sign-in';
        } 
    })
}

// Do signup to user
app_methods.signup = function(target){
    app_data.panel= 'signup';
    var data = {
        'fullname':app_data.fullname,
        'email':app_data.email,
        'password':app_data.password,
        'confirm_password':app_data.confirm_password
    }

    axios.post('/signup', data).then(response => {

        if (response.data=='True')
        {   
            // Signup was successful
            app_data.error_signup = '';         
            app_data.success_signup = response.data;
            app_data.panel= 'signup';
            page='signup';
        }   
        else {
            // Signup was not successful
            app_data.success_signup = '';         
            app_data.error_signup = response.data;
            app_data.panel= 'signup';
            page='signup';
        }           
    })    
}


var app = new Vue({
    el: '#app',
    data: app_data,
    methods: app_methods,

    created: function(){
        axios.get('/signin').then(response => {
            if (response.data=='user1')
            {
                app_methods.getalbums();
                page='gallery';
                app_data.panel= 'gallery';
                app_data.user_email= '';
                app_data.user_password= '';
            }  
            app_data.error_newgallery = '';
            app_data.error_login = '';
            app_data.error_signup = '';
            app_data.success_signup = '';
        })

    }}
);
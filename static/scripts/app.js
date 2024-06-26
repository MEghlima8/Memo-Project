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
    error_login : '',
    error_newgallery : '',
    error_signup : '',
    success_signup : '',
    error_add_photo : '',

    // New album data
    AddNewAlbum : '',
    album_title : '',
    album_info : '',


    // Signin data
    user_email : '',
    user_password : '',

    // Albums
    albums : '',
    
    // Album photos data
    photo_header : '',
    title : '',
    album_photos : '',

    // Signup data
    fullname : '',
    password : '',
    confirm_password : '',
    email : '',

    // Add Photo To Album
    AddPhotoToAlbum : '',
    

};


// Change panel to target and disable all alerts
app_methods.change_panel = function(target){
    app_data.panel = target;
    app_data.error_newgallery = '';
    app_data.error_login = '';
    app_data.error_signup = '';
    app_data.success_signup = '';
    app_data.error_add_photo = '';
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

    const fd = new FormData();
    fd.append('album_title', app_data.title)
    fd.append('AddPhotoToAlbum',this.AddPhotoToAlbum)

    axios.post('/add_photo_to_album',fd).then(response => {
        if (response.data=='fileSize')
        {
            app_data.error_add_photo = 'fileSize';
            app_data.panel= 'add_photo';
        }   
        else {
            app_data.album_photos= response.data;         
            app_data.panel='album_panel';
        }  
    })
}


// Get albums
app_methods.getalbums = function(){

    app_data.panel='gallery';    
    axios.post('/albums').then(response => {
        app_data.albums= response.data;         
    })
}


app_methods.handleAddNewAlbum = function(event){
    app_data.AddNewAlbum = event.target.files[0]
}


// Create new album
app_methods.add_album = function(target){

    const fd = new FormData();
    fd.append('AddNewAlbum', app_data.AddNewAlbum)
    fd.append('title', app_data.album_title)
    fd.append('info', app_data.album_info)

    axios.post('/add-album', fd).then(response => {
        if (response.data=='True')
        {
            $(alert('New album created successfully'))

            // Change panel to gallery panel
            page='gallery';
            app_data.panel= 'gallery';
            app_data.album_title='';
            app_data.album_info='';
            app_methods.getalbums();
        }   
        else {

            // if create panel was not successful getback this error
            app_data.error_newgallery=response.data;            
            app_data.panel= 'new-album';
        }  
    })
}


app_methods.validate_signin = function(){

    var email = app_data.user_email;
    var password = app_data.user_password;

    if (email == "") {
    return 'empty_email';
    }
    
    if (password == "") {
    return 'empty_password';
    }

    if (password.length < 8) {
        return 'password_length';
    }

    // check if email is valid
    var emailRegex = /^\S+@\S+\.\S+$/;
    if (!emailRegex.test(email)) {
        return 'char_email';
    }

    // Check if password contains at least one uppercase letter
    if (!/[A-Z]/.test(password)) {
        return 'char_password';
    }

    // Check if password contains at least one lowercase letter
    if (!/[a-z]/.test(password)) {
        return 'char_password';
    }

    // Check if password contains at least one number
    if (!/\d/.test(password)) {
        return 'char_password';
    }

    // Check if password contains at least one special character
    if (!/[$&+,:;=?@#|'<>.^*()%!-]/.test(password)) {
        return 'char_password';
    }

      return true;
}


app_methods.validate_signup = function(){

    var email = app_data.email;
    var password = app_data.password;
    var fullname =  app_data.fullname;
    var confirm_password = app_data.confirm_password

    if (email == "") {
    return 'empty_email';
    }
    
    // check if email is valid
    var emailRegex = /^\S+@\S+\.\S+$/;
    if (!emailRegex.test(email)) { return 'char_email'; }


    if (password == "") { return 'empty_password'; }

    if (password.length < 8) { return 'password_length'; }

    // Check if password contains at least one uppercase letter
    if (!/[A-Z]/.test(password)) { return 'char_password'; }

    // Check if password contains at least one lowercase letter
    if (!/[a-z]/.test(password)) { return 'char_password'; }

    // Check if password contains at least one number
    if (!/\d/.test(password)) { return 'char_password'; }

    // Check if password contains at least one special character
    if (!/[$&+,:;=?@#|'<>.^*()%!-]/.test(password)) { return 'char_password'; }

    if (password != confirm_password){ return 'no_match_password' }

    const regex = /^[A-Za-z]+([\ A-Za-z]+)*([\.\ A-Za-z]+)*$/;
    if (!regex.test(fullname)){ return 'char_fullname' }

    if(fullname.length > 50) { return 'fullname_length' }

    if (fullname == "") { return 'empty_fullname' }

    return true;
}


// Do signin to user
app_methods.signin = function(){
    var data = {
        'email':app_data.user_email,
        'password':app_data.user_password,
    }
    app_data.panel=page;
        
    var res = app_methods.validate_signin();
    if (res != true){
        app_data.error_login = res;
        app_data.panel= 'sign-in';
        return;
    }    

    axios.post('/signin', data).then(response => {
                

        if (response.data=='user') {            
            //  Login was succesful
            page='gallery';
            app_data.panel= 'gallery';
            app_methods.getalbums();            
        }        
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

    var res = app_methods.validate_signup();
    if (res != true){
        app_data.error_signup = res;
        app_data.panel= 'signup';
        return;
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
            app_data.panel = 'signup';
            page ='signup';
        } 
    })    
}


app_methods.handleAddPhotoToAlbum = function(event){
    app_data.AddPhotoToAlbum = event.target.files[0]
}



var app = new Vue({
    el: '#app',
    data: app_data,
    methods: app_methods,

    created: function(){
        axios.get('/signin').then(response => {
            if (response.data=='user')
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

    }
});
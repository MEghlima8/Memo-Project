var app_methods = {};
var page;

$(window).on('load', function() {
	
	// Preloder
	$(".loader").fadeOut();
	$("#preloder").delay(400).fadeOut("slow");

});



var app_data = {
    panel: 'sign-in',
    error_login:'',
    error_newgallery:'',
    error_signup:'',
    success_signup:'',

    // new album
    album_title:'',
    album_info:'',
    photo_name:'',

    // signin
    user_email:'',
    user_password :'',

    // albums
    albums:'',
    
    // album photos
    photo_header:'',
    title:'',
    album_photos:'',
    add_photo_name:'',

    // signup
    fullname:'',
    password:'',
    confirm_password:'',
    email:'',

};


app_methods.change_panel = function(target){
    app_data.panel = target;
    app_data.error_newgallery = '';
    app_data.error_login = '';
    app_data.error_signup = '';
    app_data.success_signup = '';
}

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
    axios.post('/albumphotos',data).then(response => {        
        app_data.album_photos= response.data;         
        app_data.panel='album_panel';
    })
}


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



app_methods.getalbums = function(){

    app_data.panel='gallery';    
    axios.post('/albums').then(response => {
        app_data.albums= response.data;         
    })
}




app_methods.add_album = function(target){
    var data = {
        'title':app_data.album_title,
        'info':app_data.album_info,
        'photo':app_data.photo_name,
    }
    // app_data.panel=page;

    axios.post('/add-album', data).then(response => {
        if (response.data=='True')
        {
            $(alert('New album created successfully'))
            page='gallery';
            app_data.panel= 'gallery';
            app_data.album_title='';
            app_data.album_info='';
            app_data.photo_name='';            
            app_methods.getalbums();
        }   
        else {
            app_data.error_newgallery=response.data;            
            // page='new-album';
            app_data.panel= 'new-album';
        }  
    })
}




app_methods.signin = function(target){
    var data = {
        'email':app_data.user_email,
        'password':app_data.user_password,
    }
    app_data.panel=page;

    axios.post('/', data).then(response => {
        if (response.data=='user')
        {
            page='gallery';
            app_data.panel= 'gallery';
            app_methods.getalbums();
        }
        else {
            app_data.error_login=response.data;
            app_data.panel= 'sign-in';
        } 
        // else if (response.data=='empty') {
        //     $(alert('fill all labels'))            
        //     page='sign-in';
        //     app_data.panel= 'sign-in';
        // }   
        // else if(response.data=='False'){
        //     $(alert('Email or password is incorrect'))
        //     page='sign-in';
        //     app_data.panel= 'sign-in';
        // }
        // else if (response.data=='noactive'){
        //     $(alert('Activate link sent to your email. open the link to active your account'))
        //     page='sign-in';
        //     app_data.panel= 'sign-in';
        // }
    })
}


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
            app_data.error_signup = '';         
            app_data.success_signup = response.data;
            app_data.panel= 'signup';
            page='signup';
        }   
        else {
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
});
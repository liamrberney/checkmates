var locationVar = document.getElementById("location");

var getLocation = (function() {
    var executed = false;
    return function() {
        if (!executed) {
            executed = true;
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            }
        }
    };
})();

function test(){
    if ((typeof sessionStorage !== 'undefined') &&
        (sessionStorage.getItem('get user location once every session') === null)) {
        getLocation();
        console.log('ok');
        sessionStorage.setItem('get user location once every session', true);
    }
}

function showPosition(position) {
  locationVar.value = position.coords.latitude + 
  ","+ position.coords.longitude;
  document.locateUsr.submit();
}
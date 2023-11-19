window.onload = function() {
    updateDateTime();
};

function updateDateTime() {
    setInterval(function(){
        var now = new Date();
        document.getElementById('datetime').innerHTML = now.toLocaleString();
    }, 1000);
}


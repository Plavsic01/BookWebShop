var span = document.getElementById('kolicina');

if (sessionStorage.getItem('kolicina') != null){
    var proizvodi = JSON.parse(sessionStorage.getItem('kolicina'));
    span.innerText = proizvodi['kolicina'];
}

function reset_kolicina(){
    sessionStorage.setItem('kolicina',JSON.stringify({'kolicina':0}));  
}
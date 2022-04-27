function izbrisi_iz_korpe(prod_naziv){
    fetch('/ocisti-kosaricu/' + prod_naziv,
    {method:'POST'}
    )
    .then(response => response.json())
    .then(data => {
        var span = document.getElementById('kolicina');
        sessionStorage.setItem('kolicina',JSON.stringify(data));  
        span.innerText = data['kolicina'];
        window.location.reload(true);
    })
}


function izbrisi_korpu(){
    fetch('/ocisti-kosaricu',
    {method:'POST'}
    )
    .then(response => response.json())
    .then(data => {
        var span = document.getElementById('kolicina');
        sessionStorage.setItem('kolicina',JSON.stringify(data));  
        span.innerText = data['kolicina'];
        window.location.reload(true);
    })
}


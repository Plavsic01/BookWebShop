function dodaj_u_korpu(prod_id,btn_id){
    fetch('/dodaj-u-korpu/' + prod_id,
    {method:'POST'}
    )
    .then(response => response.json())
    .then(data => {
        var span = document.getElementById('kolicina');
        sessionStorage.setItem('kolicina',JSON.stringify(data));  
        span.innerText = data['kolicina'];
    })

    var dugme = document.getElementById('dugme-'+btn_id);
    
    dugme.classList.remove('btn-primary');
    dugme.classList.add('btn-success');
    dugme.innerHTML = "Dodano";
    dugme.disabled = true;

}




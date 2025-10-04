
const forms = document.getElementsByTagName('form');

Array.from(forms).forEach(form => {
    
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const loader = document.getElementById('loader');
        console.log(loader)
        loader.classList.remove('hidden');
        form.submit();
    });
});
$(document).ready(function(){

    $("#eelmised-tekstid").on("change",function(){
        var GetValue=$("#eelmised-tekstid").val();
        console.log(GetValue)
            fetch('/dropdown-text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ value: GetValue })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                $("#text").val(data);
            })
            .catch(error => {
                console.error(error);
            });
    });
});

            captcha_solution = ""
            function test() {
                let site = 'https://ammarsysdev.pythonanywhere.com/api/img'
                fetch(site)
                .then((response) => response.json())
                    .then((data) => {
                        captcha_solution = data['solution']
                        return data
                    })
                    .then((data) => {
                        var x = document.createElement("img");
                        x.src = data['url'];
                        x.alt = "Uh-oh, couldn't load the image :(";
                        document.body.appendChild(x);
                    });
            }
            function validateForm() {
                var x = document.forms["myForm"]["fname"].value;
                if (x == "") {
                    alert("Type somethin bruh");
                    return false;
                    }
                if (x != captcha_solution) {
                    alert('Wrong betch')
                    return false;
                    } else {
                    alert('Gj')
                    return true;
                    }
                }

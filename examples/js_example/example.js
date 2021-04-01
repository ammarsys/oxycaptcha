         // AN UNSAFE EXAMPLE, PLEASE REWRITE. WONDERING IF YOUR IMPLEMENTATION IS SAFE? ASK YOURSELF IF YOU HAVE TO HIDE THE CODE FROM SOMEONE, IF YES, ITS UNSAFE

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
                        var curCaptcha = document.getElementById("captcha")
                        if (curCaptcha != null) {
                            curCaptcha.remove();
                        }
                        var x = document.createElement("img");
                        document.getElementById("imgContainer").appendChild(x);
                        x.src = data['url'];
                        x.alt = "Uh-oh, couldn't load the image :(";
                        x.id = "captcha"
                    });
            }
            function validateForm() {
                var x = document.forms["myForm"]["fname"].value;
                if (x == "") {
                    alert("Please enter the code!");
                    return false;
                    }
                if (x != captcha_solution) {
                    alert('Incorrect code!')
                    return false;
                    } else {
                    alert('Correct code!')
                    return true;
                    }
                }
            test();
